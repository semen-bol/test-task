from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
import sqlalchemy as sa

from src.database.database import get_session
from src.database.models import Lead, Contact, Source
from src.utils.operators_autoallocate import allocate_operator
from src.routers.v1.contacts.schemas import ContactCreateRequest, ContactResponse

router = APIRouter(prefix="/contacts", tags=["Contacts"])


@router.post(
    "/",
    summary="Register new contact",
    status_code=status.HTTP_201_CREATED,
    response_model=ContactResponse
)
async def create_contact(
    request: ContactCreateRequest,
    db_session: Annotated[AsyncSession, Depends(get_session)],
):
    source_stmt = sa.select(Source).where(Source.id == request.source_id)
    source_result = await db_session.execute(source_stmt)
    source = source_result.scalar_one_or_none()
    
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Source not found"
        )

    lead_stmt = sa.select(Lead).where(Lead.external_id == request.external_id)
    lead_result = await db_session.execute(lead_stmt)
    lead = lead_result.scalar_one_or_none()
    
    if not lead:
        lead = Lead(external_id=request.external_id, )
        db_session.add(lead)
        await db_session.flush()

    operator_id = await allocate_operator(db_session, request.source_id)

    contact = Contact(
        lead_id=lead.id,
        source_id=request.source_id,
        operator_id=operator_id,
        payload=request.payload,
        status="active"
    )
    
    db_session.add(contact)
    await db_session.flush()

    result = ContactResponse(
        id=contact.id,
        lead_id=lead.id,
        source_id=contact.source_id,
        operator_id=contact.operator_id,
        status=contact.status,
        payload=contact.payload,
        created_at=contact.created_at
    )
    
    await db_session.commit()
    return result