from fastapi import APIRouter
from typing import List
from children.models import Child
from models.student import ChildResponse, ChildVisitResponse

router = APIRouter()

@router.get("/children", response_model=List[ChildResponse])
def list_children():
    children_qs = Child.objects.prefetch_related('visits', 'hts_samples').all()

    result = []
    for child in children_qs:
        result.append(
            ChildResponse(
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
                visits=list(child.visits.all()),          # RelatedManager -> list
                hts_samples=list(child.hts_samples.all()) # RelatedManager -> list
            )

        )
    return result


