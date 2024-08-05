from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import os

DEPARTMENTS = (
    ('None','None'),
    ('HR','HR'),
    ('IT','IT'),
    ('Accounts','Accounts'),
    ('CAD','CAD'),
    ('SCM','SCM'),
    ('Technical','Technical'),
    ('Sales','Sales'),
)

USERS_REGIONS = (
    ('None','None'),('All','All'),('East','East'),('West','West'),('North','North'),('South','South'),
)

USERS_CIRCLES = (
    ('None','None'),('All','All'),('JK','JK'),('UPE','UPE'),('UPW','UPW'),('HP','HP'),('HR','HR'),('PB','PB'),('DL','DL'),
    ('MU','MU'),('MH','MH'),('GJ','GJ'),('RJ','RJ'),('MP','MP'),('CG','CG'),('AS / NE','AS / NE'),
    ('WB / KOL','WB / KOL'),('OD','OD'),('JH','JH'),('BH','BH'),('AP','AP'),
    ('TS','TS'),('TN','TN'),('KN','KN'),('KL','KL'),
)

USER_ROLE = (
    ('None','None'),('ASM','ASM'),('RSM','RSM'),('Assistant Manager','Assistant Manager'),('Manager','Manager'),('General Manager','General Manager')
    ,('Deputy Manager','Deputy Manager'),('Deputy General Manager','Deputy General Manager'),('CEO','CEO'),('Senior Vice President','Senior Vice President'),('Service Head','Service Head'),('Engineer','Engineer')
    , ('Senior Engineer','Senior Engineer'),('IT Executive','IT Executive'),('CAD Executive','CAD Executive'),('Technician','Technician'),
    ('Sales','Sales'),('Vice President','Vice President'),('Associate Vice President','Associate Vice President'),('MIS Executive','MIS Executive')
)

class UserBaseManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError('Users must have a username')
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            password=password,
            )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Users(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=200, unique=True)
    department = models.CharField(max_length=50, choices=DEPARTMENTS)
    role = models.CharField(max_length=50, choices=USER_ROLE, null=True)
    region = models.CharField(max_length=30, null=True, choices=USERS_REGIONS)
    circle = models.CharField(max_length=10, null=True, choices=USERS_CIRCLES)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserBaseManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def has_perm(self, perms, obj=None):
        return self.is_admin
    
    def has_module_perms(self, abel_app):
        return True
    


class SiteFixed(models.Model):
    global_id = models.CharField(verbose_name='global ID', max_length=8, primary_key=True)
    site_name = models.CharField(verbose_name='Site Name', max_length=100)
    site_address = models.TextField(verbose_name='Site Address')
    cluster = models.CharField(verbose_name='Cluster', max_length=100)
    CE = models.CharField(verbose_name='SE', max_length=250)
    site_tenancy = models.CharField(verbose_name='Site Tenancy',max_length=250)
    DG_NON_DG = models.CharField(verbose_name='DG / Non DG', max_length=20)
    DG_capacity_kva = models.CharField(verbose_name='DG Capacity (Kva)', max_length=100)
    EB_status = models.CharField(verbose_name='EB Status', max_length=50)
    card_number = models.CharField(verbose_name='Card Number', max_length=100)
    last_month_approved_CPH = models.CharField(verbose_name='Last Month Approved CPH')

    def __str__(self):
        return str(self.global_id)
    


# Enery Models Start

IS_YES_OR_NO = (
    ('Yes','Yes'),
    ('No','No'),
)

# WORKING_NOTWORKING = (
#     ('Working','Working'),
#     ('Not-Working','Not-Working'),
#     ('Missing','Missing'),
# )

WORKING_NOTWORKING = (
    ('Available','Available'),
    ('Not-Available','Not-Available'),
)

TASKS = (
    ('Diesel Filling and Energy Reading','Diesel Filling and Energy Reading'),
    ('Energy Reading','Energy Reading'),
)

class EnergyFuel(models.Model):
    id = models.BigAutoField(primary_key=True)
    global_id = models.ForeignKey(SiteFixed, on_delete=models.CASCADE)
    Tasks = models.CharField(verbose_name='Tasks', max_length=200, choices=TASKS)
    DG_Serial_Number = models.TextField(verbose_name='DG Serial Number', null=True)
    DG_HMR_Status = models.CharField(verbose_name='DG HMR Status', max_length=30, choices=WORKING_NOTWORKING, null=True)
    DG_HMR_Reading = models.IntegerField(verbose_name='DG HMR Reading', null=True)
    DG_PIU_Status = models.CharField(verbose_name='DG PIU Status', max_length=30, choices=WORKING_NOTWORKING, null=True)
    Current_DG_PIU_Reading = models.IntegerField(verbose_name='Current DG PIU Reading', null=True)
    Diesel_Filling_Done = models.CharField(verbose_name='Diesel Filling Done', max_length=20, choices=IS_YES_OR_NO, null=True)
    Date_Of_Diesel_Filling = models.DateField(verbose_name='Date of Diesel Filling', null=True)
    Diesel_Balance_Before_Filling = models.IntegerField(verbose_name='Diesel Balance Before Filling', null=True)
    Fuel_Qty_Filled = models.IntegerField(verbose_name='Fuel Qty. Filled', null=True)
    Current_Diesel_Balance = models.IntegerField(verbose_name='Current Diesel Balance', null=True)
    EB_Meter_Status = models.CharField(verbose_name='EB Meter Status', max_length=30, choices=WORKING_NOTWORKING, null=True)
    Current_EB_MTR_KWH = models.IntegerField(verbose_name='Current EB MTR (KWH)', null=True)
    EB_PIU_Meter_Status = models.CharField(verbose_name='EB PIU Meter Status', max_length=30, choices=WORKING_NOTWORKING, null=True)
    Current_EB_PIU_Reading = models.IntegerField(verbose_name='Current EB PIU Reading', null=True)
    Total_DC_Load = models.IntegerField(verbose_name='Total DC Load', null=True)
    Total_EB_KWH_Reading_from_all_Channels = models.IntegerField(verbose_name='Total EB KWH Reading from all channels', null=True)
    Remarks = models.TextField(verbose_name='Remarks', null=True)
    FT_ID = models.CharField(verbose_name='FT ID', max_length=50, null=True)
    FT_name = models.CharField(verbose_name='FT Name', max_length=200, null=True)
    FT_mobile_no = models.CharField(verbose_name='FT Mobile No', max_length=10)
    Receipt_No = models.CharField(verbose_name='Receipt Number', null=True, max_length=200)
    Card_Number = models.CharField(verbose_name='Card Number', null=True, max_length=200)
    Vehicle_Plate = models.CharField(verbose_name='Vehicle Plate', null=True, max_length=200)
    EB_Cumulative_KWH_Image = models.ImageField(verbose_name='EB Cumulative KWH (As Per EB Meter) Image', null=True, upload_to='EB Cumulative KWH (As Per EB Meter)/%y')
    EB_Running_Hours_Cumulative_Image = models.ImageField(verbose_name='EB Cumulative KWH (As Per EB Meter) Image', null=True, upload_to='EB Cumulative KWH (As Per EB Meter)/%y')
    DG_Running_Hours_Reading_Image = models.ImageField(verbose_name='DG Running Hours Reading (As Per HMR Meter) Image', null=True, upload_to='DG Running Hours Reading (As Per HMR Meter)/%y')
    DG_Running_Hours_as_per_piu_Reading_Image = models.ImageField(verbose_name='DG Running Hours Reading (As Per PIU/12PMS/AMF) Image', null=True, upload_to='DG Running Hours Reading (As Per PIU/12PMS/AMF)/%y')
    Diesel_Bill_Number_Image = models.ImageField(verbose_name='Diesel Bill Number Image', null=True, upload_to='Diesel Bill Number/%y')
    DG_Running_HRS = models.TextField(verbose_name='DG Running Hrs', null=True)
    CPH_CPH_Comparison_With_Last_CPH = models.TextField(verbose_name='CPH and CPH Comparioson with Approved', null=True)
    CPH_as_par_HMR = models.TextField(verbose_name='CPH', null=True)	
    CPH_as_par_PIU = models.TextField(verbose_name='CPH', null=True)	
    EB_KWH = models.TextField(verbose_name='EB KWH', null=True)

    def __str__(self):
        return str(self.global_id.global_id)



STATIC_SELECT = (
    ('Static','Static'),
    ('Mobile','Mobile'),
)

class EnergyDieelFilling(models.Model):
    file = models.FileField(verbose_name='File', upload_to='Diesel_Filling_PDF_Files/%y', null=True)
    File_id = models.CharField(verbose_name='File ID', max_length=50, unique=True, primary_key=True)
    Global_ID = models.CharField(verbose_name='Global ID', max_length=50)
    Circle = models.TextField(verbose_name='Circle', null=True)
    Site_Name = models.TextField(verbose_name='Site Name', null=True)
    Cluster = models.TextField(verbose_name='Cluster', null=True)
    Region = models.TextField(verbose_name='Region', null=True)
    User_Name = models.TextField(verbose_name='User Name', null=True)
    Assign_Date = models.DateField(verbose_name='Assign Date', null=True)
    Status = models.TextField(verbose_name='Status', null=True)
    Previous_Reading_Date_Time = models.DateTimeField(verbose_name='Previous Reading Date Time', null=True)
    Current_Reading_Date_Time = models.DateTimeField(verbose_name='Current Reading Date Time', null=True)
    Previous_EB_Cumulative_KWH_As_Per_EB_Meter = models.TextField(verbose_name='Previous EB Cumulative KWH As Per EB Meter', null=True)
    Current_EB_Cumulative_KWH_As_Per_EB_Meter = models.TextField(verbose_name='Current EB Cumulative KWH As Per EB Meter', null=True)
    Previous_EB_Running_Hours_Cumulative_Available_Not_Available = models.CharField(verbose_name='Previous EB Running Hours Cumulative Available Not Available', max_length=20, null=True, choices=WORKING_NOTWORKING)
    Current_EB_Running_Hours_Cumulative_Available_Not_Available = models.CharField(verbose_name='Current EB Running Hours Cumulative Available Not Available', max_length=20, null=True, choices=WORKING_NOTWORKING)
    Previous_EB_Running_Hours_Cumulative_As_per_PIU_I2PMS_AMF = models.TextField(verbose_name='Previous EB Running Hours Cumulative As per PIU I2PMS AMF', null=True)
    Current_EB_Running_Hours_Cumulative_As_per_PIU_I2PMS_AMF = models.TextField(verbose_name='Current EB Running Hours Cumulative As per PIU I2PMS AMF', null=True)
    Previous_Type_of_DG_Static_Mobile = models.CharField(verbose_name='Previous Type of DG Static Mobile', max_length=20, null=True, choices=STATIC_SELECT)
    Current_Type_of_DG_Static_Mobile = models.CharField(verbose_name='Current Type of DG Static Mobile', max_length=20, null=True, choices=STATIC_SELECT)
    Previous_DG_Running_Hours_Reading_As_Per_HMR = models.TextField(verbose_name='Previous DG Running Hours Reading (As Per HMR)', null=True)
    Current_DG_Running_Hours_Reading_As_Per_HMR = models.TextField(verbose_name='Current DG Running Hours Reading (As Per HMR)', null=True)
    Previous_DG_Running_Hours_Reading_As_Per_PIU_I2PMS_AMF = models.TextField(verbose_name='Previous DG Running Hours Reading(As Per PIU/I2PMS/AMF)', null=True)
    Current_DG_Running_Hours_Reading_As_Per_PIU_I2PMS_AMF = models.TextField(verbose_name='Current DG Running Hours Reading(As Per PIU/I2PMS/AMF)', null=True)
    Previous_Opening_Diesel_stock_Before_Filling = models.TextField(verbose_name='Previous Opening Diesel stock Before Filling', null=True)
    Current_Opening_Diesel_stock_Before_Filling = models.TextField(verbose_name='Current Opening Diesel stock Before Filling', null=True)
    Previous_Filled_Ltrs = models.TextField(verbose_name='Previous Filled Ltrs', null=True)
    Current_Filled_Ltrs = models.TextField(verbose_name='Current Filled Ltrs', null=True)
    Previous_Diesel_Bill_Number = models.TextField(verbose_name='Previous Diesel Bill Number', null=True)
    Current_Diesel_Bill_Number = models.TextField(verbose_name='Current Diesel Bill Number', null=True)
    Previous_Remarks_If_any = models.TextField(verbose_name='Previous Remarks If any', null=True)
    Current_Remarks_If_any = models.TextField(verbose_name='Current Remarks If any', null=True)
    No_of_days_since_previous_filling  = models.TextField(verbose_name='No of days since previous filling', null=True)
    Calculated_CPH_HMR  = models.TextField(verbose_name='Calculated CPH (HMR)', null=True)
    Calculated_CPH_As_per_PIU_I2PMS_AMF = models.TextField(verbose_name='Calculated CPH (As per PIU/I2PMS/AMF)', null=True)
    Calculated_DG_HR_HMR = models.TextField(verbose_name='Calculated DG HR (HMR)', null=True)
    Calculated_DG_HR_As_per_PIU_I2PMS_AMF = models.TextField(verbose_name='Calculated DG HR (As per PIU/I2PMS/AMF)', null=True)
    Calculated_EB_KWH_As_per_Meter = models.TextField(verbose_name='Calculated EB KWH (As per Meter)', null=True)
    Calculated_EB_HR_As_per_PIU_I2PMS_AMF = models.TextField(verbose_name='Calculated EB HR (As per PIU/I2PMS/AMF)', null=True)
    Deviation = models.TextField(verbose_name='Deviation', null=True)

    def __str__(self):
        return str(self.File_id)
    


CLUSTERS = (
    ('Balasore','Balasore'),
    ('Baripada','Baripada'),
    ('Berhampur','Berhampur'),
    ('Bhadrak','Bhadrak'),
    ('Bhubaneswar','Bhubaneswar'),
    ('Cuttack','Cuttack'),
    ('Paradeep','Paradeep'),
    ('Puri','Puri'),
    ('Rouekela','Rouekela'),
    ('Sambalpur','Sambalpur'),
)

CUSTOMERS = (
    ('ATC','ATC'),
    ('JIO','JIO'),
)

class FuelDrawn(models.Model):
    FT_ID = models.CharField(verbose_name='FT ID', max_length=50)
    FT_name = models.CharField(verbose_name='FT Name', max_length=200)
    FT_mobile_no = models.CharField(verbose_name='FT Mobile No', max_length=10)
    Cluster_Name = models.CharField(verbose_name='Cluster Name', max_length=50, choices=CLUSTERS)
    Fuel_Drawn_Date = models.DateField(verbose_name='Fuel Drawn Date')
    Card_No = models.TextField(verbose_name='Booklet No. / Card No.')
    City_Township_Fuel_Station = models.TextField(verbose_name='City /Township (Fuel Station)')
    Customer = models.CharField(verbose_name='Customer', max_length=20, choices=CUSTOMERS)
    Fuel_Station_Name = models.TextField(verbose_name='Fuel Station Name')
    Diesel_Purchased_Qty = models.IntegerField(verbose_name='Diesel Purchased Qty. (Liters)')
    Diesel_Per_Ltr_Cost_Rs = models.IntegerField(verbose_name='Diesel Per Ltr. Cost. Rs.')
    Total_Diesel_Cost_Rs = models.IntegerField(verbose_name='Total Diesel Cost Rs.')
    Receipt_No = models.TextField(verbose_name='Receipt No')
    Receipt_Image_Upload = models.ImageField(verbose_name='Receipt Image Upload', upload_to='Receipt Image Upload/%y')
    Vehicle_Plate = models.TextField(verbose_name='Vehicle Plate')
    Remarks = models.TextField(verbose_name='Remarks')


    def __str__(self):
        return str(self.FT_ID)



# Pre Monsoon Model:



class PreMonsoonImages(models.Model):
    images = models.ImageField(verbose_name='Images', upload_to='att_pmcl/%y', null=True)

    def __str__(self):
        return str(self.images)

STATUS = (
    ('Ok','Ok'),
    ('Not Ok','Not Ok')
)
class PMCL(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    global_id = models.ForeignKey(SiteFixed, on_delete=models.CASCADE, null=True)
    Q1_Attach=models.ManyToManyField(PreMonsoonImages, related_name='Q1_Attach')
    Q1_Status=models.CharField(verbose_name='Status', max_length=10, choices=STATUS)
    Q1_Material_Required = models.TextField(verbose_name='Material_Required', null=True)
    Q1_Remarks = models.TextField(verbose_name='Remarks', null=True)
    Q2_Attach=models.ManyToManyField(PreMonsoonImages, related_name='Q2_Attach')
    Q2_Status=models.CharField(verbose_name='Status', max_length=10, choices=STATUS)
    Q2_Material_Required = models.TextField(verbose_name='Material_Required', null=True)
    Q2_Remarks = models.TextField(verbose_name='Remarks', null=True)
    Q3_Attach=models.ManyToManyField(PreMonsoonImages, related_name='Q3_Attach')
    Q3_Status=models.CharField(verbose_name='Status', max_length=10, choices=STATUS)
    Q3_Material_Required = models.TextField(verbose_name='Material_Required', null=True)
    Q3_Remarks = models.TextField(verbose_name='Remarks', null=True)
    Q4_Attach=models.ManyToManyField(PreMonsoonImages, related_name='Q4_Attach')
    Q4_Status=models.CharField(verbose_name='Status', max_length=10, choices=STATUS)
    Q4_Material_Required = models.TextField(verbose_name='Material_Required', null=True)
    Q4_Remarks = models.TextField(verbose_name='Remarks', null=True)
    Q5_Attach=models.ManyToManyField(PreMonsoonImages, related_name='Q5_Attach')
    Q5_Status=models.CharField(verbose_name='Status', max_length=10, choices=STATUS)
    Q5_Material_Required = models.TextField(verbose_name='Material_Required', null=True)
    Q5_Remarks = models.TextField(verbose_name='Remarks', null=True)
    Q6_Attach=models.ManyToManyField(PreMonsoonImages, related_name='Q6_Attach')
    Q6_Status=models.CharField(verbose_name='Status', max_length=10, choices=STATUS)
    Q6_Material_Required = models.TextField(verbose_name='Material_Required', null=True)
    Q6_Remarks = models.TextField(verbose_name='Remarks', null=True)
    Q7_Attach=models.ManyToManyField(PreMonsoonImages, related_name='Q7_Attach')
    Q7_Status=models.CharField(verbose_name='Status', max_length=10, choices=STATUS)
    Q7_Material_Required = models.TextField(verbose_name='Material_Required', null=True)
    Q7_Remarks = models.TextField(verbose_name='Remarks', null=True)
    Q8_Attach=models.ManyToManyField(PreMonsoonImages, related_name='Q8_Attach')
    Q8_Status=models.CharField(verbose_name='Status', max_length=10, choices=STATUS)
    Q8_Material_Required = models.TextField(verbose_name='Material_Required', null=True)
    Q8_Remarks = models.TextField(verbose_name='Remarks', null=True)
    Q9_Attach=models.ManyToManyField(PreMonsoonImages, related_name='Q9_Attach')
    Q9_Status=models.CharField(verbose_name='Status', max_length=10, choices=STATUS)
    Q9_Material_Required = models.TextField(verbose_name='Material_Required', null=True)
    Q9_Remarks = models.TextField(verbose_name='Remarks', null=True)
    Q10_Attach=models.ManyToManyField(PreMonsoonImages, related_name='Q10_Attach')
    Q10_Status=models.CharField(verbose_name='Status', max_length=10, choices=STATUS)
    Q10_Material_Required = models.TextField(verbose_name='Material_Required', null=True)
    Q10_Remarks = models.TextField(verbose_name='Remarks', null=True)
    date = models.DateField(verbose_name='Date', auto_now_add=True)
    time = models.TimeField(verbose_name='Time', auto_now_add=True)

# Pre Monsoon Model End:    


# Documents Reporsitory:

PEOJECT_TYPES = (
    ('Fuel Pump Automation Work','Feul Pump Automation Work'),('DG R&R, For ATC, Ascend, TVI','DG R&R, For ATC, Ascend, TVI'),
    ('EV Charger I&C, PM & BDN Calls','EV Charger I&C, PM & BDN Calls'),('Retail DG Repair','Retail DG Repair'),
    ('5G Upgradation For ATC','5G Upgradation For ATC'),('FTTH For Microscan','FTTH For Microscan'),
)

REGIONS = (
    ('East','East'),('West','West'),('North','North'),('South','South'),
)

CIRCLES = (
    ('JK','JK'),('UPE','UPE'),('UPW','UPW'),('HP','HP'),('HR','HR'),('PB','PB'),('DL','DL'),
    ('MU','MU'),('MH','MH'),('GJ','GJ'),('RJ','RJ'),('MP','MP'),('CG','CG'),('AS / NE','AS / NE'),
    ('WB / KOL','WB / KOL'),('OD','OD'),('JH','JH'),('BH','BH'),('AP','AP'),
    ('TS','TS'),('TN','TN'),('KN','KN'),('KL','KL'),
)

FILE_CATEGORY = (
    ('FSR','FSR'),('Civil Image','Civil Image'),('Civil Work','Civil Work'),('Electrical Work','Electrical Work')
    ,('Site Image','Site Image'),('PM Image','PM Image'), ('Survey Report','Survey Report'), ('I&C Report ','I&C Report ')
)

class  DocumentsOfRepository(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    files = models.FileField(verbose_name='Files', upload_to='Documents_repository/%y', null=True)
    file_name = models.TextField(verbose_name='File Name', null=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True) 

    def __str__(self):
        return self.files
    

class DocumentRepository(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    document_id = models.TextField(verbose_name='Document ID', null=True, unique=True)
    project_type = models.CharField(verbose_name='Project Types', max_length=100, choices=PEOJECT_TYPES, null=True)
    region = models.CharField(verbose_name='Regions', max_length=100, choices=REGIONS, null=True)
    site_docs_id = models.CharField(verbose_name='SiteID & DocumentID', max_length=100, null=True)
    circles = models.CharField(verbose_name='Circles', max_length=50, choices=CIRCLES)
    documents = models.ManyToManyField(DocumentsOfRepository, related_name='Documents')
    file_category = models.CharField(verbose_name='File Category', choices=FILE_CATEGORY, null=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.circles)

# Documents Reporsitory END


# Target Project 

class ProjectTypeModel(models.Model):
    project_type = models.CharField(max_length=250, null=True)

    def __str__(self):
        return str(self.project_type) 

class CustomerDataModel(models.Model):
    customers = models.CharField(max_length=250, null=True)

    def __str__(self):
        return str(self.customers) 
    


class ProjectsMasterModel(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    site_id = models.CharField(max_length=250, null=True)
    site_name = models.CharField(max_length=250, null=True)
    customer = models.CharField(max_length=250, null=True)
    project_type = models.CharField(max_length=250, null=True)
    customer_expected_target_date = models.DateField(null=True)
    assigned_to_asm = models.CharField(max_length=250, null=True)
    sales_remark = models.TextField(null=True)
    project_description = models.TextField(null=True)
    assigned_to_technician = models.CharField(max_length=250, null=True)
    technician_target_date = models.DateField(null=True)
    asm_remarks = models.TextField(null=True)
    project_status = models.CharField(max_length=250, null=True)
    completed_date = models.DateField(null=True)
    technician_remarks = models.TextField(null=True)
    pendings = models.CharField(max_length=50, null=True)
    completed = models.CharField(max_length=50, null=True)


# Target Project END 