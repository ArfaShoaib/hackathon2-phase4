from sqlmodel import SQLModel, Field
from typing import Optional

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str

if __name__ == "__main__":
    print("Minimal Task model created successfully!")