from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Operator, SourceOperator, Contact


async def allocate_operator(db: AsyncSession, source_id: int) -> int | None:
    rows = (await db.execute(
        select(SourceOperator).where(
            SourceOperator.source_id == source_id,
            SourceOperator.enabled == True
        )
    )).scalars().all()

    if not rows:
        return None

    candidates = []

    for row in rows:
        op = (await db.execute(
            select(Operator).where(
                Operator.id == row.operator_id,
                Operator.active == True
            )
        )).scalars().first()

        if not op:
            continue

        load = (await db.execute(
            select(func.count(Contact.id)).where(
                Contact.operator_id == op.id,
                Contact.status == "active"
            )
        )).scalar_one()

        if load >= op.max_leads:
            continue

        assigned = (await db.execute(
            select(func.count(Contact.id)).where(
                Contact.operator_id == op.id,
                Contact.source_id == source_id
            )
        )).scalar_one()

        # score = фактические/вес — чем меньше, тем лучше (можно поменять в случае чего)
        score = assigned / row.weight if row.weight > 0 else assigned

        candidates.append((op.id, score))

    if not candidates:
        return None

    candidates.sort(key=lambda x: x[1])
    operator_id, _ = candidates[0]

    return operator_id
