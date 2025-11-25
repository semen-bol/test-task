from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
import sqlalchemy as sa

from src.database.database import get_session
from src.database.models import Operator
from src.routers.v1.operators.schemas import ResultOperator, CreatedOperator

router = APIRouter(prefix="/operators", tags=["Operators"])

@router.get(
    "/",
    summary="Operators",
    status_code=status.HTTP_200_OK,
    response_model=List[ResultOperator]
)
async def operators(
    db_session: Annotated[AsyncSession, Depends(get_session)],
):
    stmt = sa.select(Operator)

    result = await db_session.execute(stmt)
    operators = result.scalars().all()

    return operators

@router.post(
    "/",
    summary="Create operator",
    status_code=status.HTTP_201_CREATED,
    response_model=CreatedOperator
)
async def create_operator(
    name: str,
    active: bool,
    max_leads: int,
    db_session: Annotated[AsyncSession, Depends(get_session)],
):
    new_operator = Operator(name=name, active=active, max_leads=max_leads)

    db_session.add(new_operator)
    await db_session.flush()

    result = CreatedOperator(id=new_operator.id, name=name, active=active, max_leads=max_leads, created_at=new_operator.created_at)
    await db_session.commit()

    return result

@router.patch(
    "/{id}",
    summary="Edit operator fields (active / max_leads)",
    status_code=status.HTTP_204_NO_CONTENT
)
async def edit_operator(
    id: int,
    db_session: Annotated[AsyncSession, Depends(get_session)],
    active: bool | None = None,
    max_leads: int | None = None,
):
    if active is None and max_leads is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field (active or max_leads) must be provided"
        )

    stmt = sa.update(Operator).where(Operator.id == id)

    values = {}
    if active is not None:
        values['active'] = active
    if max_leads is not None:
        values['max_leads'] = max_leads

    stmt = stmt.values(**values)

    await db_session.execute(stmt)
    await db_session.commit()

    return None