from pydantic import Field

from .. import _Base


class ReplicaItem(_Base):
    body: str = Field(alias="Body", examples=["Привет"])
    role: bool = Field(alias="Role", description="True = ai, False = client", examples=[False])
    date_time: str = Field(alias="DateTime", examples=["2024-12-10-18-03-46"])
    previous_score: float | None = Field(None, alias="PreviousScore")
