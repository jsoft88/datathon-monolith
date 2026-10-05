import os
from contextlib import contextmanager
from decimal import Decimal, InvalidOperation
from typing import Any, Iterator

_ALLOWED_ID_COLUMNS = {"_transaction_id", "transaction_id"}
_ALLOWED_CUSTOMER_COLUMNS = {"_customer_id", "customer_id"}

_pool = None


def _require_ident(value: str, allowed: set[str], label: str) -> str:
    if value not in allowed:
        raise ValueError(f"Unsupported {label}: {value}")
    return value


def schema_name() -> str:
    return os.getenv("POSTGRES_DATA_SCHEMA", os.getenv("POSTGRES_SCHEMA", "datathon_factored"))


def transaction_id_column() -> str:
    return _require_ident(
        os.getenv("POSTGRES_TRANSACTION_ID_COLUMN", "transaction_id"),
        _ALLOWED_ID_COLUMNS,
        "transaction id column",
    )


def customer_id_column() -> str:
    return _require_ident(
        os.getenv("POSTGRES_CUSTOMER_ID_COLUMN", "customer_id"),
        _ALLOWED_CUSTOMER_COLUMNS,
        "customer id column",
    )


def configured() -> bool:
    return bool(os.getenv("POSTGRES_HOST") and os.getenv("POSTGRES_DBNAME"))


def _dsn() -> str:
    host = os.environ["POSTGRES_HOST"]
    port = os.getenv("POSTGRES_PORT", "5432")
    user = os.environ["POSTGRES_USER"]
    password = os.environ["POSTGRES_PASSWORD"]
    dbname = os.environ["POSTGRES_DBNAME"]
    return f"host={host} port={port} user={user} password={password} dbname={dbname}"


def get_pool():
    global _pool
    if _pool is None:
        from psycopg_pool import ConnectionPool

        _pool = ConnectionPool(_dsn(), min_size=1, max_size=8, open=True, kwargs={"autocommit": True})
    return _pool


@contextmanager
def connect() -> Iterator[Any]:
    with get_pool().connection() as connection:
        yield connection


def customer_exists(customer_id: str) -> bool:
    sql = f"""
        SELECT 1
        FROM {schema_name()}.stg_customers
        WHERE {customer_id_column()} = %s
        LIMIT 1
    """
    print(f"customer_exists sql: {customer_id}")
    with connect() as connection:
        cursor = connection.execute(sql, (customer_id,))
        row = cursor.fetchone()
    return row is not None


def fetch_customer(customer_id: str) -> dict[str, Any] | None:
    sql = f"""
        SELECT
            {customer_id_column()} AS customer_id,
            first_name,
            last_name,
            document_number
        FROM {schema_name()}.stg_customers
        WHERE {customer_id_column()} = %s
        LIMIT 1
    """
    with connect() as connection:
        cursor = connection.execute(sql, (customer_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        columns = [desc.name for desc in cursor.description]
    return _row_to_dict(columns, row)


def fetch_customer_by_document_number(document_number: str) -> dict[str, Any] | None:
    sql = f"""
        SELECT
            {customer_id_column()} AS customer_id,
            first_name,
            last_name,
            document_number
        FROM {schema_name()}.stg_customers
        WHERE document_number = %s
        LIMIT 1
    """
    print(f"fetch_customer_by_document_number: {document_number}")
    with connect() as connection:
        cursor = connection.execute(sql, (document_number,))
        row = cursor.fetchone()
        if row is None:
            return None
        columns = [desc.name for desc in cursor.description]
    return _row_to_dict(columns, row)


def fetch_recent_transactions(customer_id: str, limit: int = 3) -> list[dict[str, Any]]:
    sql = f"""
        SELECT
            t.{transaction_id_column()} AS transaction_id,
            t.customer_id,
            t.transaction_date,
            t.amount,
            t.amount_usd,
            t.currency,
            t.merchant_name,
            t.transaction_type,
            t.transaction_status,
            t.channel,
            t.is_fraud
        FROM {schema_name()}.stg_transactions AS t
        WHERE t.customer_id = %s
        ORDER BY t.transaction_date DESC
        LIMIT %s
    """
    with connect() as connection:
        cursor = connection.execute(sql, (customer_id, limit))
        rows = cursor.fetchall()
        columns = [desc.name for desc in cursor.description]
    return [_row_to_dict(columns, row) for row in rows]


def compile_dispute_search_sql(
    *,
    month: int | None = None,
    day: int | None = None,
    iso_date: str | None = None,
    amount: float | Decimal | str | None = None,
    tolerance: float | Decimal | str | None = None,
) -> tuple[str, list[Any]]:
    """Build a SELECT-only, parameterized search scoped to a bound customer_id."""
    conditions = ["t.customer_id = %s"]
    params: list[Any] = []

    if iso_date:
        conditions.append("t.transaction_date::date = %s")
        params.append(iso_date)
    elif month and day:
        conditions.append("EXTRACT(MONTH FROM t.transaction_date::date) = %s")
        conditions.append("EXTRACT(DAY FROM t.transaction_date::date) = %s")
        params.extend([month, day])

    if amount is not None:
        target = _as_decimal(amount)
        delta = _as_decimal(tolerance) if tolerance is not None else max(Decimal("5.00"), target * Decimal("0.15"))
        amount_usd = _numeric_sql("t.amount_usd")
        local_amount = _numeric_sql("t.amount")
        conditions.append(
            f"""(
                ({amount_usd} IS NOT NULL AND ABS({amount_usd} - %s::numeric) <= %s::numeric)
                OR ({local_amount} IS NOT NULL AND ABS({local_amount} - %s::numeric) <= %s::numeric)
            )"""
        )
        params.extend([float(target), float(delta), float(target), float(delta)])

    sql = f"""
        SELECT
            t.{transaction_id_column()} AS transaction_id,
            t.customer_id,
            t.transaction_date,
            t.amount,
            t.amount_usd,
            t.currency,
            t.merchant_name,
            t.transaction_type,
            t.transaction_status,
            t.channel,
            t.is_fraud
        FROM {schema_name()}.stg_transactions AS t
        WHERE {' AND '.join(conditions)}
        ORDER BY t.transaction_date DESC
        LIMIT 20
    """
    return sql, params


def search_customer_transactions(customer_id: str, sql: str, params: list[Any]) -> list[dict[str, Any]]:
    _assert_safe_select(sql)
    bound = [customer_id, *params]
    with connect() as connection:
        cursor = connection.execute(sql, bound)
        rows = cursor.fetchall()
        columns = [desc.name for desc in cursor.description]
    return [_row_to_dict(columns, row) for row in rows]


def _assert_safe_select(sql: str) -> None:
    compact = " ".join(sql.lower().split())
    if not compact.lstrip().startswith("select"):
        raise ValueError("Only SELECT statements are allowed")
    forbidden = (" delete ", " drop ", " truncate ", " alter ", " update ", " insert ", " grant ", " revoke ")
    padded = f" {compact} "
    if any(token in padded for token in forbidden):
        raise ValueError("Refusing to execute a mutating SQL statement")
    if ";" in compact.rstrip(";"):
        raise ValueError("Refusing to execute multiple SQL statements")


def _numeric_sql(column: str) -> str:
    """Cast a text/float amount column to numeric, treating blanks as NULL."""
    return f"NULLIF(BTRIM({column}::text), '')::numeric"


def _as_decimal(value: float | Decimal | str) -> Decimal:
    try:
        return value if isinstance(value, Decimal) else Decimal(str(value).strip().replace(",", ""))
    except (InvalidOperation, AttributeError, ValueError) as exc:
        raise ValueError(f"Invalid amount: {value!r}") from exc


def _row_to_dict(columns: list[str], row: tuple) -> dict[str, Any]:
    payload = dict(zip(columns, row, strict=True))
    for key, value in payload.items():
        if hasattr(value, "isoformat"):
            payload[key] = value.isoformat()
        elif isinstance(value, (Decimal, float)):
            payload[key] = str(value)
    return payload
