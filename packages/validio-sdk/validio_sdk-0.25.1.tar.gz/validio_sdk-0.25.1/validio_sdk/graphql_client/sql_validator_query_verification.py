from typing import Any, List, Optional

from pydantic import Field

from .base_model import BaseModel


class SqlValidatorQueryVerification(BaseModel):
    sql_validator_query_verification: (
        "SqlValidatorQueryVerificationSqlValidatorQueryVerification"
    ) = Field(alias="sqlValidatorQueryVerification")


class SqlValidatorQueryVerificationSqlValidatorQueryVerification(BaseModel):
    query: Optional[str]
    records: Optional[
        "SqlValidatorQueryVerificationSqlValidatorQueryVerificationRecords"
    ]
    query_error: Optional[str] = Field(alias="queryError")


class SqlValidatorQueryVerificationSqlValidatorQueryVerificationRecords(BaseModel):
    columns: List[str]
    rows: List[Any]


SqlValidatorQueryVerification.model_rebuild()
SqlValidatorQueryVerificationSqlValidatorQueryVerification.model_rebuild()
