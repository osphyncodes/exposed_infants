from fastapi import APIRouter, Query, Depends
from typing import List, Optional
from children.models import Child,ChildVisit,HTSSample
from models.student import ChildResponse, ChildVisitResponse, ChildCreate, ChildUpdate
from fastapi_jwt_auth import AuthJWT
from fastapi import HTTPException, status

router = APIRouter(prefix="", tags=["exposed"])

def serialize_child(child: Child):
    return ChildResponse(
        hcc_number=child.hcc_number,
        child_name=child.child_name,
        child_dob=child.child_dob,
        child_gender=child.child_gender,
        child_birth_weight=child.child_birth_weight,
        guardian_name=child.guardian_name,
        relationship=child.relationship,
        guardian_phone=child.guardian_phone,
        physical_address=child.physical_address,
        agrees_to_fup=child.agrees_to_fup,
        mother_status=child.mother_status,
        mother_art_number=child.mother_art_number,
        mother_art_start_date=child.mother_art_start_date,
        visits=list(ChildVisit.objects.filter(child=child).all().values()),
        hts_samples=list(HTSSample.objects.filter(child=child).all().values()),
    )
    
    
@router.get("/children/", response_model=List[ChildResponse])
def list_children(    
    search: Optional[str] = Query(None, description="Value to search for"),
    search_by: Optional[str] = Query(None, description="Field to search by"),
    Authorize: AuthJWT = Depends()   # Inject AuthJWT dependency
):

    Authorize.jwt_required()

    children_qs = Child.objects.prefetch_related("visits", "hts_samples").all()

    if search and search_by:
        filters = {f"hcc_number__icontains": search}
        children_qs = children_qs.filter(**filters)

    return [serialize_child(child) for child in children_qs.order_by('-child_dob')[:10]]



@router.get("/children/{child_id}", response_model=ChildResponse)
def get_child(child_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    try:
        child = Child.objects.prefetch_related("visits", "hts_samples").get(pk=child_id)
    except Child.DoesNotExist:
        raise HTTPException(status_code=404, detail="Child not found")

    return serialize_child(child)

@router.post("/children/create/", response_model=ChildResponse, status_code=status.HTTP_201_CREATED)
def create_child(data: ChildCreate, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    
    try:
        # Create child using Django ORM
        child = Child.objects.create(**data.dict())
        return serialize_child(child)
    
    except Exception as e:
        # Log the error if you want
        print(f"Error creating child: {e}")
        # Return a friendly HTTP error response
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create child: {str(e)}"
        )

# ✅ UPDATE
@router.put("/children/{hcc_number}", response_model=ChildResponse)
def update_child(hcc_number: int, data: ChildUpdate, Authorize: AuthJWT = Depends()):
    print(hcc_number, data)
    Authorize.jwt_required()

    try:
        child = Child.objects.filter(hcc_number=hcc_number).first()
    except Child.DoesNotExist:
        raise HTTPException(status_code=404, detail="Child not found")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(child, field, value)
    child.save()

    return serialize_child(child)

# ✅ DELETE
@router.delete("/children/{child_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_child(child_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    deleted, _ = Child.objects.filter(id=child_id).delete()
    if not deleted:
        raise HTTPException(status_code=404, detail="Child not found")

    return {"detail": "Child deleted successfully"}

def children(child_object, hcc_number=None):
    pass