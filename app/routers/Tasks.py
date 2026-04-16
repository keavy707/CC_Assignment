from fastapi import APIRouter, HTTPException , status
from app.models.Tasks import Tasks
from sqlmodel import Session, select

router = APIRouter(prefix="/Tasks", tags=["Tasks"])
from ..database import engine

@router.get("/", summary="Get all Tasks")
async def get_all():
    with Session(engine) as session:
        statement = select(Tasks)
        results = session.exec(statement).all()
        return results



@router.post("/", summary="Create a new Tasks", status_code=status.HTTP_201_CREATED)
async def create_item(_Tasks : Tasks):
    with Session(engine) as session:
        session.add(_Tasks)
        session.commit()
        session.refresh(_Tasks)
        return _Tasks


@router.get("/{item_id}", summary="Get Tasks by ID")
async def get_item(item_id: int):
    with Session(engine) as session:
        item = session.get(Tasks, item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tasks not found")
        return item



@router.put("/{item_id}", summary="Update Tasks")
async def update_item(_Tasks : Tasks , item_id: int):
    with Session(engine) as session:

        item = session.get(Tasks, item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tasks not found")

        for key, value in _Tasks.model_dump(exclude_unset=True).items():
            setattr(item, key, value)

        session.add(item)
        session.commit()
        session.refresh(item)
        return item


@router.delete("/{item_id}", summary="Delete Tasks" ,status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):

    with Session(engine) as session:
        item = session.get(Tasks, item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tasks not found")

        session.delete(item)
        session.commit()
        return None
