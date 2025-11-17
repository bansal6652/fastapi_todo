from pydantic import BaseModel, Field


class TodoResponse(BaseModel):
    title : str = Field(min_length=3)
    description : str = Field(min_length=3, max_length=100)
    priority : int = Field(gt=0,lt=6)
    completion_status : bool = False