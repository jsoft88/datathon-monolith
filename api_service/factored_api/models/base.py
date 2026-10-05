from typing import Literal

from pydantic import BaseModel, ConfigDict


class ContractModel(BaseModel):
    """Base model whose JSON Schema is intended for data-contract snapshots."""

    model_config = ConfigDict(extra="forbid")


def contract_config(
    table: str,
    *,
    kind: Literal["dimension", "fact", "reference"],
    source: str,
    partition: str,
    primary_key: list[str],
    unique: list[str] | None = None,
    foreign_keys: dict[str, str] | None = None,
) -> ConfigDict:
    extra: dict = {
        "x-table": table,
        "x-table-kind": kind,
        "x-source": source,
        "x-partition": partition,
        "x-primary-key": primary_key,
    }
    if unique:
        extra["x-unique"] = unique
    if foreign_keys:
        extra["x-foreign-keys"] = foreign_keys
    return ConfigDict(json_schema_extra=extra)
