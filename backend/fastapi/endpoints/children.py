from fastapi import APIRouter, Query, Depends
from typing import List, Optional
from children.models import Child,ChildVisit,HTSSample
from models.student import ChildResponse, ChildVisitResponse, ChildCreate, ChildUpdate
from fastapi_jwt_auth import AuthJWT
from fastapi import HTTPException, status
from datetime import date, timedelta
from django.db.models import OuterRef, Subquery
from django.utils import timezone
from django.db.models.functions import TruncMonth
from django.db.models.functions import TruncDay
from django.db.models import Count

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
    
@router.get('/dashboard/')
def dashboard(Authorize: AuthJWT = Depends() ):
    
    # Authorize.jwt_required()
    
    
    current_year = date.today().year
    start_year = current_year - 2

    total_children = Child.objects.filter(
        child_dob__year__range=(start_year, current_year)
    ).count()

    latest_visits = ChildVisit.objects.filter(
        child__child_dob__year__range=(start_year, current_year),
        child=OuterRef('pk')
    )

    children_with_latest_visits = Child.objects.annotate(
        latest_visit_date=Subquery(
            latest_visits.values('next_appointment_or_outcome_date')
            .order_by('-next_appointment_or_outcome_date')[:1]
        ),
        current_outcome=Subquery(
            latest_visits.values('follow_up_outcome')
            .order_by('-next_appointment_or_outcome_date')[:1]
        )
    )

    defaultedPepfarCount = defaultedMOHCount = missedCount = 0
    aliveCount = diedCount = toCount = disCount = artCount = noCount = 0

    for child in children_with_latest_visits:
        if child.current_outcome == 'Con':
            if child.latest_visit_date:
                days_since = (timezone.now().date() - child.latest_visit_date).days
                if days_since > 60:
                    defaultedMOHCount += 1
                elif days_since > 28:
                    defaultedPepfarCount += 1
                elif days_since > 7:
                    missedCount += 1
                else:
                    aliveCount += 1
        elif child.current_outcome == 'Died':
            diedCount += 1
        elif child.current_outcome == 'To':
            toCount += 1
        elif child.current_outcome == 'Dis':
            disCount += 1
        elif child.current_outcome == 'ART':
            artCount += 1
        else:
            noCount += 1

    outcomeData = [
        defaultedMOHCount + defaultedPepfarCount,
        missedCount,
        aliveCount,
        diedCount,
        toCount,
        disCount,
        artCount,
        noCount,
    ]

    today = timezone.now().date()

    total_visits = children_with_latest_visits.exclude(latest_visit_date=None).count()
    total_hts_samples = HTSSample.objects.count()
    upcoming_appointments = ChildVisit.objects.filter(
        next_appointment_or_outcome_date__gte=today,
        next_appointment_or_outcome_date__lte=today + timedelta(days=7)
    ).count()

    twelve_months_ago = today - timedelta(days=365)
    children_per_month = (
        Child.objects.filter(child_dob__gte=twelve_months_ago)
        .annotate(month=TruncMonth('child_dob'))
        .values('month')
        .annotate(count=Count('hcc_number'))
        .order_by('month')
    )
    children_per_month_labels = [c['month'].strftime('%b %Y') for c in children_per_month]
    children_per_month_data = [c['count'] for c in children_per_month]

    gender_distribution = (
        Child.objects.values('child_gender')
        .annotate(count=Count('hcc_number'))
        .order_by('child_gender')
    )
    gender_labels = [g['child_gender'] for g in gender_distribution]
    gender_data = [g['count'] for g in gender_distribution]

    visit_trends = (
        ChildVisit.objects.filter(visit_date__gte=today - timedelta(days=7))
        .annotate(day=TruncDay('visit_date'))
        .values('day')
        .annotate(
            total_visits=Count('id'),
            unique_children=Count('child', distinct=True)
        )
        .order_by('day')
    )

    visit_trends_labels = [v['day'].strftime('%a %d %b') for v in visit_trends]
    visit_trends_data = [v['total_visits'] for v in visit_trends]
    unique_children_trends_data = [v['unique_children'] for v in visit_trends]

    app_trends = (
        ChildVisit.objects.filter(
            next_appointment_or_outcome_date__gte=today,
            next_appointment_or_outcome_date__lte=today + timedelta(days=7)
        )
        .annotate(day=TruncDay('next_appointment_or_outcome_date'))
        .values('day')
        .annotate(total_apps=Count('id'))
        .order_by('day')
    )

    app_trends_labels = [v['day'].strftime('%a %d %b') for v in app_trends]
    app_trends_data = [v['total_apps'] for v in app_trends]

    # Build context for serializer
    context = {
        "current_year": current_year,
        "start_year": start_year,
        "total_children": total_children,
        "total_visits": total_visits,
        "total_hts_samples": total_hts_samples,
        "upcoming_appointments": upcoming_appointments,
        "unique_children_count": children_with_latest_visits.count(),
        "aliveCount": aliveCount,
        "tiPepfar": defaultedPepfarCount,
        "tiMOH": defaultedMOHCount,
        "outcomeData": outcomeData,
        "children_per_month_labels": children_per_month_labels,
        "children_per_month_data": children_per_month_data,
        "gender_labels": gender_labels,
        "gender_data": gender_data,
        "visit_trends_labels": visit_trends_labels,
        "visit_trends_data": visit_trends_data,
        "unique_children_trends_data": unique_children_trends_data,
        "outcome_labels": [],
        "outcome_data": [],
        "app_trends_labels": app_trends_labels,
        "app_trends_data": app_trends_data,
    }

    return context
    
@router.get("/children/", response_model=List[ChildResponse])
def list_children(    
    search: Optional[str] = Query(None, description="Value to search for"),
    search_by: Optional[str] = Query(None, description="Field to search by"),
    Authorize: AuthJWT = Depends()   # Inject AuthJWT dependency
):

    Authorize.jwt_required()

    children_qs = Child.objects.prefetch_related("visits", "hts_samples").all()

    if search and search_by:
        if search_by == 'hcc':
            filters = {f"hcc_number__icontains": search}
            children_qs = children_qs.filter(**filters)
        else:
            filters = {f"mother_art_number__icontains": search}
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