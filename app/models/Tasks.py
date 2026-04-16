from sqlmodel import Field, SQLModel


class Tasks(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
