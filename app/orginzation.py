from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session, joinedload
from app.database import get_session
from app.auth_bearer import JWTBearer
from app import models, schemas
from app.utils import get_user_from_token

orgRoute = APIRouter(prefix="/organization", tags=["Organization"])

@orgRoute.get("/", response_model=list[schemas.OrganizationResponse], dependencies=[Depends(JWTBearer())])
async def get_all_organizations(
    session: Session = Depends(get_session),
    token: str = Depends(JWTBearer())
):
    # Retrieve the current user
    current_user = get_user_from_token(session, token)

    # Query to fetch all organizations in the database
    organizations = session.query(models.Organization).all()

    # If no organizations found, raise a 404 error
    if not organizations:
        raise HTTPException(status_code=404, detail="No organizations found")

    return organizations

@orgRoute.post("/", response_model=schemas.OrganizationResponse, dependencies=[Depends(JWTBearer())])
async def create_organization(
    organization: schemas.OrganizationCreate,
    session: Session = Depends(get_session),
    token: str = Depends(JWTBearer())
):
    # Get the current user from token
    current_user = get_user_from_token(session, token)
    
    # Create a new organization instance
    new_org = models.Organization(
        name=organization.name,
        description=organization.description,
        owner_id=current_user.id  # Set the current user as the owner
    )
    session.add(new_org)  # Add the new organization to the session
    session.commit()  # Save the changes
    session.refresh(new_org)  # Refresh the instance to reflect changes in the database
    return new_org

@orgRoute.get("/{organization_id}", response_model=schemas.OrganizationResponse, dependencies=[Depends(JWTBearer())])
async def get_organization(
    organization_id: int,
    session: Session = Depends(get_session),
    token: str = Depends(JWTBearer())
):
    # Retrieve the current user
    current_user = get_user_from_token(session, token)

    # Query to retrieve the organization with owner and members loaded
    org = session.query(models.Organization) \
        .options(
            joinedload(models.Organization.owner),  # Load owner data
            joinedload(models.Organization.members)  # Load members data
        ) \
        .filter_by(id=organization_id) \
        .first()

    # Raise an error if the organization is not found
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    # Check if the user is the owner or a member of the organization
    if org.owner_id != current_user.id and current_user not in org.members:
        raise HTTPException(status_code=403, detail="Not authorized to view this organization")

    return org

@orgRoute.put("/{organization_id}", response_model=schemas.OrganizationResponse, dependencies=[Depends(JWTBearer())])
async def update_organization(
    organization_id: int,
    organization: schemas.OrganizationCreate,
    session: Session = Depends(get_session),
    token: str = Depends(JWTBearer())
):
    # Get the current user
    current_user = get_user_from_token(session, token)
    
    # Query to find the organization by ID and verify ownership
    org = session.query(models.Organization).filter_by(id=organization_id, owner_id=current_user.id).first()
    if not org:
        raise HTTPException(status_code=403, detail="Not authorized to update this organization")

    # Update organization fields
    org.name = organization.name
    org.description = organization.description
    session.commit()  # Commit the update
    session.refresh(org)  # Refresh instance to reflect changes in the database
    return org

@orgRoute.delete("/{organization_id}", dependencies=[Depends(JWTBearer())])
async def delete_organization(
    organization_id: int,
    session: Session = Depends(get_session),
    token: str = Depends(JWTBearer())
):
    # Get the current user
    current_user = get_user_from_token(session, token)
    
    # Query to find the organization by ID and verify ownership
    org = session.query(models.Organization).filter_by(id=organization_id, owner_id=current_user.id).first()
    if not org:
        raise HTTPException(status_code=403, detail="Not authorized to delete this organization")

    session.delete(org)  # Delete the organization
    session.commit()  # Commit the deletion
    return {"message": "Organization deleted successfully"}

@orgRoute.post("/{org_id}/invite", dependencies=[Depends(JWTBearer())])
async def invite_user_to_organization(
    org_id: int,
    email: str = Body(..., embed=True),  # Get the email of the user to invite
    session: Session = Depends(get_session),
    token: str = Depends(JWTBearer())
):
    # Get current user (organization owner)
    current_user = get_user_from_token(session, token)

    # Retrieve the organization by ID
    org = session.query(models.Organization).filter_by(id=org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    # Verify that the current user is the owner of the organization
    if org.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the organization owner can invite users")

    # Retrieve the target user by email
    target_user = session.query(models.User).filter_by(email=email).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the user is already a member of the organization
    if target_user in org.members:
        raise HTTPException(status_code=400, detail="User is already a member of the organization")

    # Create an invitation instance in the database
    invitation = models.OrganizationInvitation(
        organization_id=org_id,
        user_id=target_user.id,
        invited_by=current_user.id  # Set the current user as the inviter
    )
    session.add(invitation)  # Add the invitation to the session
    session.commit()  # Save the changes
    session.refresh(invitation)  # Refresh the instance

    return {"message": f"Invitation sent to {target_user.email}", "organization": org.name}
