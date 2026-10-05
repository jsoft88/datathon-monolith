import factored_api.models as models
from pathlib import Path
import pydantic
import requests
import os

DATAHUB_API_URL = os.environ["DATAHUB_API_URL"]
DATAHUB_API_KEY = os.environ["DATAHUB_API_KEY"]

DATAHUB_URN = "urn:li:dataset:(urn:li:dataPlatform:postgres,postgres.datathon_factored.{},PROD)"

def _datahub_types_checker(model_type: str, datahub_type: str) -> bool:
    if model_type == "string":
        return datahub_type == "string"
    if model_type in ("int", "float"):
        return datahub_type == "number"
    if model_type == "boolean":
        return datahub_type == "boolean"
    if model_type in ("datetime", "date"):
        return datahub_type == "time"
    return True # default to true when model_type is not in the list

def _is_breaking_change(model_type: str, datahub_type: str) -> bool:
    if datahub_type == "number" and model_type in ("string", "bool"):
        return True
    if datahub_type == "string" and model_type in ("bool", "float", "int"):
        return True
    if datahub_type == "time" and model_type in ("number", "float", "int", "date"):
        return True

    return False

def _fetch_datahub_schema(model_name: str) -> dict:
    dataset_urn = DATAHUB_URN.format(model_name)
    print("Fetching datahub schema for ", dataset_urn)
    response = requests.post(f"{DATAHUB_API_URL}/api/graphql", json={
        "query": f"""
        query GetEntityDetails{{
            entity(urn: "{dataset_urn}"){{
                urn
                type
                ... on Dataset {{
                    name
                    origin
                    platform {{
                        urn
                        name
                    }}
                    properties {{
                        name
                        description
                        qualifiedName
                    }}
                    schemaMetadata {{
                        fields {{
                        fieldPath
                        type
                        description
                        }}
                    }}
                }}
            }}
        }}
            """,
    }, headers={
        "Authorization": f"Bearer {DATAHUB_API_KEY}"
    })
    # print("Response: ", response.json().get("data", {}))
    resp = response.json()
    if resp.get("data", {}).get("entity", {}).get("schemaMetadata"):
        return {
            item["fieldPath"]: item for item in resp.get("data", {}).get("entity", {}).get("schemaMetadata").get("fields") if "_airbyte" not in item["fieldPath"] and "_ab_source" not in item["fieldPath"]
        }
    return None

def _check_fields_count(pydantic_schema: dict, datahub_schema: list) -> int:
    """
    Checks the number of fields in the pydantic schema and the datahub schema
    returns:
        int < 0 if the number of fields is less than the datahub schema
        int = 0 if the number of fields is equal to the datahub schema
        int > 0 if the number of fields is greater than the datahub schema
    """
    print("Pydantic schema fields: ", len(pydantic_schema["properties"].keys()))
    print("Datahub schema fields: ", len(datahub_schema))
    if len(pydantic_schema["properties"].keys()) < len(datahub_schema):
        return len(pydantic_schema["properties"].keys()) - len(datahub_schema)
    if len(pydantic_schema["properties"].keys()) > len(datahub_schema):
        return len(pydantic_schema["properties"].keys()) - len(datahub_schema)
    return 0

def _generate_datahub_lookup_fields(field_name: str, foreign_keys: list[str]) -> str:
    """
    Handle special column naming that Datahub uses when creating metadata
    """
    return "_" + field_name if ("_id" in field_name and field_name not in foreign_keys and field_name not in {'session_id', 'element_id'}) or field_name == 'date' else field_name

def verify_schema(location: str):
    for clazz in map(models.__dict__.get, models.__all__):
        if type(clazz) == pydantic._internal._model_construction.ModelMetaclass:
            print("Model config: ", clazz.model_config)
            foreign_keys = clazz.model_config.get("json_schema_extra", {}).get("x-foreign-keys", {}).keys()
            print("foreign_keys: ", foreign_keys)
            pydantic_schema = clazz.model_json_schema()
            print("Verifying schema for ", pydantic_schema.get("x-table"))
            datahub_schema = _fetch_datahub_schema(pydantic_schema.get("x-table"))
            if datahub_schema is None:
                print(f"No datahub schema found for {pydantic_schema.get('x-table')}")
                continue
            if _check_fields_count(pydantic_schema, datahub_schema) < 0:
                raise ValueError(f"The number of fields in the pydantic schema is less than the number of fields in the datahub schema for {pydantic_schema.get('x-table')}")
            for field_name, props in pydantic_schema["properties"].items():
                if "$ref" in props:
                    continue
                lookup_field_name = _generate_datahub_lookup_fields(field_name, foreign_keys)
                print(lookup_field_name, datahub_schema[lookup_field_name]["type"], "->", props)
                if "anyOf" in props:
                    for types in props["anyOf"]:
                        if "$ref" in types or types["type"].strip().lower() == 'null':
                            continue
                        if _is_breaking_change(types["type"].strip().lower(), datahub_schema[lookup_field_name]["type"].strip().lower()):
                            raise ValueError(f"The type of the field {field_name} is a breaking change from {datahub_schema[lookup_field_name]['type']} to {types['type']}")
                elif _is_breaking_change(props["type"].strip().lower(), datahub_schema[lookup_field_name]["type"].strip().lower()):
                    raise ValueError(f"The type of the field {field_name} is a breaking change from {datahub_schema[lookup_field_name]['type']} to {props['type']}")

    print("Schema verification completed successfully")


if __name__ == "__main__":
    verify_schema("")