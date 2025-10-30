from typing import Optional,List
from datetime import date
from pydantic import BaseModel

class ChildVisitResponse(BaseModel):
    child_id: int  # foreign key reference
    visit_date: Optional[date] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    muac: Optional[float] = None

    wasting: Optional[str] = "No"
    breastfeeding: Optional[str] = "Exc"
    mother_art_status: Optional[str] = "On ART"
    clinical_monitoring: Optional[str] = "NAD"
    hiv_testing: Optional[str] = "No"
    infection_status: Optional[str] = "C"
    drug_given: Optional[str] = "CPT"
    cpt_given: Optional[int] = None
    follow_up_outcome: Optional[str] = "Con"
    art_number: Optional[int] = None
    next_appointment_or_outcome_date: Optional[date] = None

    class Config:
        orm_mode = True

class HTSSampleResponse(BaseModel):
    sample_date: date
    test_type: str
    reason: Optional[str]
    sample_id: str
    result: Optional[str]
    date_received: Optional[date]

    class Config:
        orm_mode = True


class ChildResponse(BaseModel):
    hcc_number: int
    child_name: str
    child_dob: Optional[date]
    child_gender: Optional[str] = None
    child_birth_weight: Optional[float] = None
    guardian_name: Optional[str] = None
    relationship: Optional[str] = None
    guardian_phone: Optional[str] = None
    physical_address: Optional[str] = None
    agrees_to_fup: Optional[str] = None
    mother_status: Optional[str] = None
    mother_art_number: Optional[str] = None
    mother_art_start_date: Optional[date] = None

    class Config:
        orm_mode = True

