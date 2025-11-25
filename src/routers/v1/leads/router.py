from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
import sqlalchemy as sa

from src.database.database import get_session
from src.database.models import Lead, Contact
from src.routers.v1.leads.schemas import LeadResponse, LeadWithContactsResponse, ContactResponse

router = APIRouter(prefix="/leads", tags=["Leads"])


@router.get(
    "/",
    summary="Get all leads",
    status_code=status.HTTP_200_OK,
    response_model=List[LeadResponse]
)
async def get_leads(
    db_session: Annotated[AsyncSession, Depends(get_session)],
):
    stmt = sa.select(Lead)
    result = await db_session.execute(stmt)

    leads = result.scalars().all()
    return leads

@router.get(
    "/{lead_id}/contacts",
    summary="Get lead contacts by lead id",
    status_code=status.HTTP_200_OK,
    response_model=LeadWithContactsResponse
)
async def get_lead_contacts(
    lead_id: int,
    db_session: Annotated[AsyncSession, Depends(get_session)],
):
    lead_stmt = sa.select(Lead).where(Lead.id == lead_id)
    lead_result = await db_session.execute(lead_stmt)
    lead = lead_result.scalar_one_or_none()
    
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )

    contacts_stmt = sa.select(Contact).where(Contact.lead_id == lead_id)
    contacts_result = await db_session.execute(contacts_stmt)
    contacts = contacts_result.scalars().all()

    return LeadWithContactsResponse(
        lead=LeadResponse(
            id=lead.id,
            external_id=lead.external_id,
            payload=lead.payload,
            created_at=lead.created_at
        ),
        contacts=[
            ContactResponse(
                id=contact.id,
                source_id=contact.source_id,
                operator_id=contact.operator_id,
                status=contact.status,
                payload=contact.payload,
                created_at=contact.created_at
            )
            for contact in contacts
        ]
    )