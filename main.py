from fastapi import FastAPI, Depends, HTTPException, status, Path
from db.models import Todos
from db.database import engine, Base, db_dependency
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel
from schemas.todo_schema import TodoResponse


app = FastAPI(title="Todo App")


Base.metadata.create_all(bind=engine)


@app.get("/", tags=["Read Item"], status_code=status.HTTP_200_OK)
async def read_all_list(db:db_dependency):
    return db.query(Todos).all()

@app.get("/{id}" ,tags=["Read Item"], status_code=status.HTTP_200_OK)
async def read_specific_task(db:db_dependency, id : int = Path(gt=0) ):
    task = db.query(Todos).filter(Todos.id == id).first()
    if task:
        return task
    raise HTTPException(
        status_code=404,
        detail=f"No task with id={id} was found."
    )

@app.post('/todo',tags=["Write Item"], status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request : TodoResponse):
    todo_model = Todos(**todo_request.model_dump())
    db.add(todo_model)
    db.commit()

@app.put("/todo/{todo_id}",
         tags=["Alter Item"], 
         status_code=status.HTTP_204_NO_CONTENT)
async def edit_todo(db:db_dependency, 
                    todorequest : TodoResponse,
                    todo_id : int = Path(gt=0)
                    ):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"No task with id={todo_id} was found."
        )
    else:
        todo_model.title = todorequest.title
        todo_model.description = todorequest.description
        todo_model.priority = todorequest.priority
        todo_model.completion_status = todorequest.completion_status
        db.add(todo_model)
        db.commit()