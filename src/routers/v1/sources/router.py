from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
import sqlalchemy as sa

from src.database.database import get_session
from src.database.models import Source, SourceOperator, Operator
from src.routers.v1.sources.schemas import SourceCreated, OperatorLinkedResponse

router = APIRouter(prefix="/sources", tags=["Sources"])

@router.post(
    "/",
    summary="Create source",
    status_code=status.HTTP_201_CREATED,
    response_model=SourceCreated
)
async def create_source(
    name: str,
    db_session: Annotated[AsyncSession, Depends(get_session)],
):
    new_source = Source(name=name)
    db_session.add(new_source)

    await db_session.flush()
    source = SourceCreated(id=new_source.id, name=name)
    await db_session.commit()
    
    return source

@router.post(
    "/{source_id}/operators",
    summary="Link operator to source with weight",
    status_code=status.HTTP_200_OK,
    response_model=OperatorLinkedResponse
)
async def link_operator_to_source(
    db_session: Annotated[AsyncSession, Depends(get_session)],
    source_id: int,
    operator_id: int,
    weight: int = 1,
):
    source_stmt = sa.select(Source).where(Source.id == source_id)
    source_result = await db_session.execute(source_stmt)
    source = source_result.scalar_one_or_none()
    
    operator_stmt = sa.select(Operator).where(Operator.id == operator_id)
    operator_result = await db_session.execute(operator_stmt)
    operator = operator_result.scalar_one_or_none()
    
    if not source or not operator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )
    
    existing_stmt = sa.select(SourceOperator).where(
        SourceOperator.source_id == source_id,
        SourceOperator.operator_id == operator_id
    )
    existing_result = await db_session.execute(existing_stmt)
    existing_link = existing_result.scalar_one_or_none()
    
    if existing_link:
        stmt = sa.update(SourceOperator).where(
            SourceOperator.source_id == source_id,
            SourceOperator.operator_id == operator_id
        ).values(weight=weight)
    else:
        new_link = SourceOperator(
            source_id=source_id,
            operator_id=operator_id,
            weight=weight
        )
        db_session.add(new_link)
    
    await db_session.commit()
    return OperatorLinkedResponse(source_id=source_id, operator_id=operator_id, weight=weight)