from django.db import models, transaction
from django.core.validators import MinValueValidator
from datetime import datetime, date
import csv
from io import StringIO
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay
from django.db.models import ExpressionWrapper, F, IntegerField, Value, When,Case

class PatientManager(models.Manager):
    def under_age(self, age_limit, **filters):
        today = date.today()

        return self.annotate(
            birth_year=ExtractYear('birthdate'),
            birth_month=ExtractMonth('birthdate'),
            birth_day=ExtractDay('birthdate'),
        ).annotate(
            age=Value(today.year) - F('birth_year') -
            Case(
                When(
                    birth_month__gt=today.month,
                    then=Value(1)
                ),
                When(
                    birth_month=today.month,
                    birth_day__gt=today.day,
                    then=Value(1)
                ),
                default=Value(0),
                output_field=IntegerField()
            )
        ).filter(age__lt=age_limit, **filters)
    
class Patient(models.Model):
    OUTCOME_CHOICES = [
        ('On antiretrovirals', 'On antiretrovirals'),
        ('Patient transferred out', 'Patient transferred out'),
        ('Defaulted', 'Defaulted'),
        ('Patient died', 'Patient died'),
        ('Treatment stopped', 'Treatment stopped'),

    ]
    
    GENDER_CHOICES = [
        ('Female', 'Female'),
        ('Male', 'Male'),
    ]
    
    arv_number = models.IntegerField(primary_key=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    birthdate = models.DateField()
    outcome = models.CharField(max_length=50, choices=OUTCOME_CHOICES)
    art_start_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PatientManager()

    def age(self):
        today = date.today()
        return today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))

    @classmethod
    def parse_date(cls, date_str):
        """Fast date parsing for DD-MMM-YY format"""
        month_map = {
            'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
            'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
        }
        today = date.today()
        two_digit_year = today.strftime("%y")

        day, month, year = date_str.split('-')
        print(two_digit_year)

        year = int(year) + (2000 if int(year) <= int(two_digit_year) else 1900)
        return datetime(year, month_map[month], int(day)).date()

    @classmethod
    def import_from_csv(cls, csv_file):
        from io import TextIOWrapper
        results = {'created': 0, 'updated': 0, 'unchanged': 0, 'errors': []}
        
        try:
            # Read entire file into memory for faster processing
            content = TextIOWrapper(csv_file.file, encoding='utf-8').read()
            reader = csv.DictReader(StringIO(content))
            
            # Preload all existing ARV numbers for single query
            existing_patients = {
                p.arv_number: p 
                for p in cls.objects.filter(
                    arv_number__in=[int(row['ARV Number']) for row in reader]
                )
            }
            
            # Reset reader for actual processing
            reader = csv.DictReader(StringIO(content))
            
            to_create = []
            to_update = []
            
            for row in reader:
                try:
                    arv_number = int(row['ARV Number'])
                    patient_data = {
                        'gender': row['Gender'],
                        'birthdate': cls.parse_date(row['Birthdate']),
                        'outcome': row['Outcome'],
                        'art_start_date': cls.parse_date(row['Art start date'])
                    }
                    
                    if arv_number in existing_patients:
                        existing = existing_patients[arv_number]
                        if existing.outcome != patient_data['outcome']:
                            for field, value in patient_data.items():
                                setattr(existing, field, value)
                            to_update.append(existing)
                            results['updated'] += 1
                        else:
                            results['unchanged'] += 1
                    else:
                        to_create.append(cls(arv_number=arv_number, **patient_data))
                        results['created'] += 1
                        
                except Exception as e:
                    results['errors'].append({
                        'row': row,
                        'error': str(e)
                    })
                    continue
            
            # Bulk operations
            with transaction.atomic():
                if to_create:
                    cls.objects.bulk_create(to_create)
                if to_update:
                    cls.objects.bulk_update(to_update, ['gender', 'birthdate', 'outcome', 'art_start_date'])
            
            return results
            
        except Exception as e:
            results['errors'].append({
                'error': f"File processing error: {str(e)}"
            })
            return results
    
class LabResult(models.Model):
    MODE_CHOICES = [
        ('Email', 'Email'),
        ('Portal', 'Portal'),
        ('Courier', 'Courier'),
        ('In-person', 'In-person'),
    ]
    
    TEST_REASON_CHOICES = [
        ('Medical examination, routine', 'Routine Examination'),
        ('Diagnostic test', 'Diagnostic Test'),
        ('Follow-up', 'Follow-up'),
    ]
    
    arv_number = models.ForeignKey(
        'Patient',
        to_field='arv_number',
        on_delete=models.CASCADE,
        db_column='arv_number'
    )
    accession_number = models.CharField(max_length=20)
    status = models.CharField(max_length=50, blank=True, null=True)
    order_date = models.DateField()
    result = models.CharField(max_length=255, blank=True, null=True)
    date_received = models.DateField(blank=True, null=True)
    mode_of_delivery = models.CharField(max_length=20, choices=MODE_CHOICES, blank=True, null=True)
    test_reason = models.CharField(max_length=100, choices=TEST_REASON_CHOICES, blank=True, null=True)
    tat_days = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'lab_results'

    @classmethod
    def parse_arv_number(cls, arv_string):
        """
        Extracts numeric ARV number from formats like:
        - LGWN-ARV-2563 → 2563
        - ARV-2563 → 2563
        - 2563 → 2563
        """
        if not arv_string or str(arv_string).strip().upper() == 'N/A':
            return None
            
        # Convert to string and clean
        clean_num = str(arv_string).strip()
        
        # Remove prefixes if they exist
        prefixes = ['LGWN-ARV-', 'ARV-']
        for prefix in prefixes:
            if clean_num.startswith(prefix):
                clean_num = clean_num[len(prefix):]
                break
                
        try:
            return int(clean_num)
        
        except ValueError:
            return None

    @classmethod
    def parse_date(cls, date_str):
        """
        Parse dates in multiple formats:
        - 28-Apr-2025 (hyphen separator, 4-digit year)
        - 28-Apr-25 (hyphen separator, 2-digit year) 
        - 28/Apr/2025 (slash separator, 4-digit year)
        - 28/Apr/25 (slash separator, 2-digit year)
        """
        if not date_str or str(date_str).strip().upper() == 'N/A':
            return None
            
        month_map = {
            'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
            'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
        }
        
        try:
            # Normalize the string and try both separators
            date_str = str(date_str).strip()
            
            # Try hyphen first, then slash if that fails
            for separator in ['-', '/']:
                parts = date_str.split(separator)
                if len(parts) == 3:
                    day, month, year = parts
                    
                    # Handle month (case insensitive)
                    month = month.capitalize()
                    if month not in month_map:
                        continue  # Try next separator
                    
                    today = date.today()
                    two_digit_year = today.strftime("%y")
                    # Handle year (2 or 4 digits)
                    year_int = int(year)
                    if len(year) == 2:  # 2-digit year
                        year_int += 2000 if year_int <= int(two_digit_year) else 1900
                    
                    # Validate day
                    day_int = int(day)
                    if day_int < 1 or day_int > 31:
                        raise ValueError(f"Invalid day: {day}")
                    
                    return datetime(year_int, month_map[month], day_int).date()
            
            # If we get here, no valid format was found
            raise ValueError("Date format not recognized. Expected DD-MMM-YY or DD/MMM/YY")
            
        except Exception as e:
            raise ValueError(f"Invalid date format: {date_str}. Error: {str(e)}")

    @classmethod
    def clean_accession_number(cls, accession_num):
        """Clean accession numbers including N/A cases"""
        if not accession_num or str(accession_num).strip().upper() in ['N/A', "'N/A'"]:
            return None
        
        return str(accession_num).strip().strip("'")

    @classmethod
    def clean_result_value(cls, result):
        """Handle special result values like #NAME?"""
        if not result or str(result).strip().upper() == '#NAME?':
            return None
        return str(result).strip()

    @classmethod
    def import_large_csv(cls, csv_file, chunk_size=5000):
        """
        Completely replaces all LabResult data with the contents of the CSV file
        - Deletes all existing records first
        - Creates new records from CSV
        - No update checks or comparisons
        """
        results = {
            'deleted': 0,
            'created': 0,
            'errors': []
        }

        try:
            # First delete ALL existing records
            with transaction.atomic():
                deleted_count, _ = cls.objects.all().delete()
                results['deleted'] = deleted_count

            # Then import all new records from CSV
            file_content = csv_file.read().decode('utf-8')
            reader = csv.DictReader(StringIO(file_content))
            
            to_create = []
            
            for row in reader:
                try:
                    arv_num = cls.parse_arv_number(row.get('ARV#', ''))
                    if not arv_num:
                        results['errors'].append({
                            'row': row,
                            'error': "Invalid ARV number"
                        })
                        continue

                    # Check patient exists (if needed)
                    if not Patient.objects.filter(arv_number=arv_num).exists():
                        results['errors'].append({
                            'row': row,
                            'error': f"Patient ARV#{arv_num} not found"
                        })
                        continue

                    # Create new record
                    lab_result = cls(
                        arv_number_id=arv_num,
                        accession_number=cls.clean_accession_number(row.get('Accession #', '')),
                        status=cls.clean_result_value(row.get('Status', '')),
                        order_date=cls.parse_date(row.get('Order Date', '')),
                        result=cls.clean_result_value(row.get('Result', '')),
                        date_received=cls.parse_date(row.get('Date received', '')),
                        mode_of_delivery=cls.clean_result_value(row.get('Mode of Delivery', '')),
                        test_reason=cls.clean_result_value(row.get('Test reason', '')),
                        tat_days=int(row['TAT(Days)']) if row.get('TAT(Days)') and row['TAT(Days)'].isdigit() else None
                    )
                    to_create.append(lab_result)
                    
                except Exception as e:
                    results['errors'].append({
                        'row': row,
                        'error': str(e)
                    })
                    continue

            # Bulk create all valid records
            with transaction.atomic():
                cls.objects.bulk_create(to_create)
                results['created'] = len(to_create)

            return results

        except Exception as e:
            results['errors'].append({
                'error': f"File processing error: {str(e)}"
            })
            return results
        
class Regimen(models.Model):
    
    arv_number = models.ForeignKey(
        'Patient',
        to_field='arv_number',
        on_delete=models.CASCADE,
        db_column='arv_number'
    )
    gender = models.CharField(max_length=20)
    weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    regimen = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        db_table = 'regimen'

    @classmethod
    def parse_arv_number(cls, arv_string):
        """
        Extracts numeric ARV number from formats like:
        - LGWN-ARV-2563 → 2563
        - ARV-2563 → 2563
        - 2563 → 2563
        """
        if not arv_string or str(arv_string).strip().upper() == 'N/A':
            return None
            
        # Convert to string and clean
        clean_num = str(arv_string).strip()
        
        # Remove prefixes if they exist
        prefixes = ['LGWN-ARV-', 'ARV-']
        for prefix in prefixes:
            if clean_num.startswith(prefix):
                clean_num = clean_num[len(prefix):]
                break
                
        try:
            return int(clean_num)
        
        except ValueError:
            return None


    @classmethod
    def import_regimen_data(cls, csv_file, chunk_size=5000):
        results = {
            'deleted': 0,
            'created': 0,
            'errors': []
        }

        try:
            # First delete ALL existing records
            with transaction.atomic():
                deleted_count, _ = cls.objects.all().delete()
                results['deleted'] = deleted_count

            file_content = csv_file.read().decode('utf-8')
            reader = csv.DictReader(StringIO(file_content))
            
            to_create = []
            
            for row in reader:
                try:
                    arv_num = cls.parse_arv_number(row.get('ARV#', ''))

                    if not arv_num:
                        results['errors'].append({
                            'row': row,
                            'error': "Invalid ARV number"
                        })
                        continue

                    # Check patient exists (if needed)
                    if not Patient.objects.filter(arv_number=arv_num).exists():
                        results['errors'].append({
                            'row': row,
                            'error': f"Patient ARV#{arv_num} not found"
                        })
                        continue

                    # Create new record
                    lab_result = cls(
                        arv_number_id=arv_num,
                        gender=row.get('Gender', ''),
                        weight=row.get('Weight(Kg)', ''),
                        regimen=row.get('Curr.Reg', ''),
                    )
                    to_create.append(lab_result)
                    
                except Exception as e:
                    results['errors'].append({
                        'row': row,
                        'error': str(e)
                    })
                    continue

            # Bulk create all valid records
            with transaction.atomic():
                cls.objects.bulk_create(to_create)
                results['created'] = len(to_create)

            return results

        except Exception as e:
            results['errors'].append({
                'error': f"File processing error: {str(e)}"
            })
            return results

class Genotype(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name= 'genotypes') 
    application_date = models.DateField()
    REASON_CHOICES = [
        ('Treatment failure', 'Treatment failur'),
        ('Targeted', 'Targeted')
    ]   
    reason = models.CharField(max_length=50, choices=REASON_CHOICES)
    RESULT_CHOICES = [
        ('Resistance Detected', 'Resistance Detected'),
        ('Resistance Not Detected', 'Resistance Not Detected')
    ] 
    result = models.CharField(max_length=50, choices=RESULT_CHOICES, null=True, blank=True)
    result_date = models.DateField(null=True, blank=True)

class Staff(models.Model):
    name = models.CharField(max_length=255)
    CADRE_CHOICES = [
        ('Coordinator', 'Coordinator'),
        ('Supervisor', 'Supervisor'),
        ('Statistcal Clerk', 'Statistical Clerk'),
        ('HDA/Treatment Supporter', 'HDA/Treatment Supporter'),
        ('Treatment Supporter', 'Treatment Supporter')
    ]
    cadre = models.CharField(max_length=255, choices=CADRE_CHOICES)

    def __str__(self):
        return f"{self.name}, Position: {self.cadre}"

class Survey(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name= 'surveys')
    survey_date = models.DateField()
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, related_name='surveys')
    guardian_presence = models.BooleanField()
    adherence_challenges = models.TextField()
    psychosocial_issues = models.TextField(null=True, blank=True)
    home_environment = models.TextField(null=True, blank=True)
    school_issues = models.TextField(null=True, blank=True)
    proposed_solutions = models.TextField(null=True, blank=True)
    action_plan = models.TextField(null=True, blank=True)
    follow_up_date = models.DateField(null=True, blank= True)

    def __str__(self):
        return f"{self.survey_date}"

class Presentation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name= 'presentations')
    presentation_date = models.DateField()
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, related_name='presentations')
    experts_present = models.TextField()
    feedback = models.TextField()
    follow_up_actions = models.TextField()
    follow_up_date = models.DateField()

    def __str__(self):
        return f"{self.presentation_date} Experts Present: {self.experts_present}"

class Relationship(models.TextChoices):
    # Family - by blood
    MOTHER = 'mother', 'Mother'
    FATHER = 'father', 'Father'
    SON = 'son', 'Son'
    DAUGHTER = 'daughter', 'Daughter'
    BROTHER = 'brother', 'Brother'
    SISTER = 'sister', 'Sister'
    GRANDFATHER = 'grandfather', 'Grandfather'
    GRANDMOTHER = 'grandmother', 'Grandmother'
    GRANDSON = 'grandson', 'Grandson'
    GRANDDAUGHTER = 'granddaughter', 'Granddaughter'
    UNCLE = 'uncle', 'Uncle'
    AUNT = 'aunt', 'Aunt'
    NEPHEW = 'nephew', 'Nephew'
    NIECE = 'niece', 'Niece'
    COUSIN = 'cousin', 'Cousin'

    # Family - by marriage
    HUSBAND = 'husband', 'Husband'
    WIFE = 'wife', 'Wife'
    STEPFATHER = 'stepfather', 'Stepfather'
    STEPMOTHER = 'stepmother', 'Stepmother'
    STEPSON = 'stepson', 'Stepson'
    STEPDAUGHTER = 'stepdaughter', 'Stepdaughter'
    STEPBROTHER = 'stepbrother', 'Stepbrother'
    STEPSISTER = 'stepsister', 'Stepsister'
    FATHER_IN_LAW = 'father_in_law', 'Father-in-law'
    MOTHER_IN_LAW = 'mother_in_law', 'Mother-in-law'
    BROTHER_IN_LAW = 'brother_in_law', 'Brother-in-law'
    SISTER_IN_LAW = 'sister_in_law', 'Sister-in-law'
    SON_IN_LAW = 'son_in_law', 'Son-in-law'
    DAUGHTER_IN_LAW = 'daughter_in_law', 'Daughter-in-law'
    EX_HUSBAND = 'ex_husband', 'Ex-husband'
    EX_WIFE = 'ex_wife', 'Ex-wife'

    # Romantic
    BOYFRIEND = 'boyfriend', 'Boyfriend'
    GIRLFRIEND = 'girlfriend', 'Girlfriend'
    FIANCE = 'fiance', 'Fiancé/Fiancée'
    PARTNER = 'partner', 'Partner'
    SIGNIFICANT_OTHER = 'significant_other', 'Significant Other'
    EX_PARTNER = 'ex_partner', 'Ex-Partner'

    # Social
    FRIEND = 'friend', 'Friend'
    BEST_FRIEND = 'best_friend', 'Best Friend'
    NEIGHBOR = 'neighbor', 'Neighbor'
    ROOMMATE = 'roommate', 'Roommate'
    CLASSMATE = 'classmate', 'Classmate'
    TEAMMATE = 'teammate', 'Teammate'
    COMPANION = 'companion', 'Companion'
    MENTOR = 'mentor', 'Mentor'
    MENTEE = 'mentee', 'Mentee'

    # Professional
    BOSS = 'boss', 'Boss'
    COLLEAGUE = 'colleague', 'Colleague'
    EMPLOYEE = 'employee', 'Employee'
    CLIENT = 'client', 'Client'
    SUPERVISOR = 'supervisor', 'Supervisor'
    INTERN = 'intern', 'Intern'
    CONTRACTOR = 'contractor', 'Contractor'
    BUSINESS_PARTNER = 'business_partner', 'Business Partner'

    # Education
    TEACHER = 'teacher', 'Teacher'
    STUDENT = 'student', 'Student'
    PRINCIPAL = 'principal', 'Principal'
    TUTOR = 'tutor', 'Tutor'
    ADVISOR = 'advisor', 'Advisor'

    # Healthcare
    PRIMARY_CAREGIVER = 'primary_caregiver', 'Primary Caregiver'
    LEGAL_GUARDIAN = 'legal_guardian', 'Legal Guardian'
    EMERGENCY_CONTACT = 'emergency_contact', 'Emergency Contact'
    HEALTHCARE_PROXY = 'healthcare_proxy', 'Healthcare Proxy'
    SOCIAL_WORKER = 'social_worker', 'Social Worker'
    DOCTOR = 'doctor', 'Doctor'
    NURSE = 'nurse', 'Nurse'

    # Legal
    POWER_OF_ATTORNEY = 'power_of_attorney', 'Power of Attorney'
    TRUSTEE = 'trustee', 'Trustee'
    EXECUTOR = 'executor', 'Executor'

class Guardian(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='guardians')
    GUARDIAN_TYPE_CHOICES = [
        ('Primary', 'Primary'),
        ('Secondary', 'Secondary')
    ]
    type = models.CharField(max_length=9, choices=GUARDIAN_TYPE_CHOICES)
    name = models.CharField(max_length=255)
    birthdate = models.DateField()
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    relationship = models.CharField(max_length=255, choices=Relationship.choices)
    on_art = models.BooleanField()
    facility = models.CharField(max_length=255)
    art_number = models.IntegerField()

    VL_STATUS_CHOICES = [
        ('Suppressed', 'Suppressed'),
        ('High', 'High'),
        ('Unknown', 'Unknown')
    ]

    def __str__(self):
        return f"{self.name}, Type: {self.type}"
    
class BoardingType(models.TextChoices):
    SELF_BOARDING = 'self_boarding', 'Self-Boarding'
    FULL_BOARDING = 'full_boarding', 'Full Boarding'
    DAY_SCHOLAR = 'day_scholar', 'Day Scholar'
    WEEKLY_BOARDING = 'weekly_boarding', 'Weekly Boarding'
    PARTIAL_BOARDING = 'partial_boarding', 'Partial Boarding'

class schoolLevel(models.TextChoices):
    STD_1 = 'STD 1', 'Standard 1'
    STD_2 = 'STD 2', 'Standard 2'
    STD_3 = 'STD 3', 'Standard 3'
    STD_4 = 'STD 4', 'Standard 4'
    STD_5 = 'STD 5', 'Standard 5'
    STD_6 = 'STD 6', 'Standard 6'
    STD_7 = 'STD 7', 'Standard 7'
    STD_8 = 'STD 8', 'Standard 8'

    # Secondary School
    FORM_1 = 'FORM 1', 'Form 1'
    FORM_2 = 'FORM 2', 'Form 2'
    FORM_3 = 'FORM 3', 'Form 3'
    FORM_4 = 'FORM 4', 'Form 4'

    College = 'College'

class School(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='school')
    school = models.CharField(max_length=255, null=True, blank=True)
    level = models.CharField(max_length=11, choices=schoolLevel.choices)
    boarding_type = models.CharField(max_length=255, choices=BoardingType.choices)

    def __str__(self):
        return f"{self.school}, Level: {self.level}, Boarding Type: {self.boarding_type}"

class village(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='village')
    name = models.CharField(max_length=255),
    chw = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}: Assigned CHW: {self.chw}"
