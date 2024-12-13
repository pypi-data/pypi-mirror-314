from typing import Optional

from pydantic import Field

from .base_model import BaseModel


class SqlFilterVerification(BaseModel):
    sql_filter_verification: "SqlFilterVerificationSqlFilterVerification" = Field(
        alias="sqlFilterVerification"
    )


class SqlFilterVerificationSqlFilterVerification(BaseModel):
    query_error: Optional[str] = Field(alias="queryError")


SqlFilterVerification.model_rebuild()
