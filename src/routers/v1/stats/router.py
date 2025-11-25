from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
import sqlalchemy as sa

from src.database.database import get_session
from src.database.models import Contact, Operator, Source, Lead
from src.routers.v1.stats.schemas import DistributionStats, OperatorStats, SourceStats

router = APIRouter(prefix="/stats", tags=["Stats"])


@router.get(
    "/",
    summary="Get distribution statistics",
    status_code=status.HTTP_200_OK,
    response_model=DistributionStats
)
async def get_stats(
    db_session: Annotated[AsyncSession, Depends(get_session)],
):
    operators_stmt = sa.select(Operator)
    operators_result = await db_session.execute(operators_stmt)
    operators = operators_result.scalars().all()

    operator_stats = []
    for operator in operators:
        total_contacts = await db_session.execute(
            sa.select(sa.func.count(Contact.id)).where(Contact.operator_id == operator.id)
        )
        active_contacts = await db_session.execute(
            sa.select(sa.func.count(Contact.id)).where(
                Contact.operator_id == operator.id,
                Contact.status == "active"
            )
        )
        
        operator_stats.append(OperatorStats(
            operator_id=operator.id,
            operator_name=operator.name,
            total_contacts=total_contacts.scalar(),
            active_contacts=active_contacts.scalar(),
            max_leads=operator.max_leads
        ))

    sources_stmt = sa.select(Source)
    sources_result = await db_session.execute(sources_stmt)
    sources = sources_result.scalars().all()

    source_stats = []
    for source in sources:
        total_contacts = await db_session.execute(
            sa.select(sa.func.count(Contact.id)).where(Contact.source_id == source.id)
        )
        
        source_stats.append(SourceStats(
            source_id=source.id,
            source_name=source.name,
            total_contacts=total_contacts.scalar()
        ))

    total_leads = await db_session.execute(sa.select(sa.func.count(Lead.id)))
    total_contacts = await db_session.execute(sa.select(sa.func.count(Contact.id)))

    return DistributionStats(
        operator_stats=operator_stats,
        source_stats=source_stats,
        total_leads=total_leads.scalar(),
        total_contacts=total_contacts.scalar()
    )