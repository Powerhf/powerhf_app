from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from app.models import *

class UserAccountsAdmin(UserAdmin):
    list_display = ['id','username' ,'first_name' ,'last_name' ,'email' ,'department', 'role', 'region', 'circle',
    'date_joined', 'last_login','is_staff','is_admin','is_active','is_superuser']
    search_fields = ['id','username','first_name','last_name' ,'email' ,'department', 'role']
    readonly_fields = ['date_joined','last_login']

    filter_horizontal = []
    list_filter = []
    fieldsets = []
admin.site.register(Users, UserAccountsAdmin)


class EnergyFuelAdmin(admin.ModelAdmin):
    list_display = ['id','global_id','Tasks','DG_Serial_Number','DG_HMR_Status','DG_HMR_Reading','DG_PIU_Status','Current_DG_PIU_Reading',
    'Diesel_Filling_Done','Date_Of_Diesel_Filling','Diesel_Balance_Before_Filling','Fuel_Qty_Filled',
    'EB_Meter_Status','Current_EB_MTR_KWH','EB_PIU_Meter_Status','Current_EB_PIU_Reading', 'Total_DC_Load', 
    'Total_EB_KWH_Reading_from_all_Channels','Remarks','FT_ID','FT_name','FT_mobile_no','Receipt_No','Card_Number',
    'Vehicle_Plate','EB_Cumulative_KWH_Image','EB_Running_Hours_Cumulative_Image','DG_Running_Hours_Reading_Image',
    'DG_Running_Hours_as_per_piu_Reading_Image','Diesel_Bill_Number_Image','DG_Running_HRS','CPH_CPH_Comparison_With_Last_CPH',
    'CPH_as_par_HMR','CPH_as_par_PIU','EB_KWH']
    search_fields = ['id','global_id','Date_Of_Diesel_Filling']

    filter_horizontal = []
    list_filter = []
    fieldsets = []
admin.site.register(EnergyFuel, EnergyFuelAdmin)


class EnergyDieselFillingAdmin(admin.ModelAdmin):
    list_display = [
        'file','File_id','Global_ID','Circle','Site_Name','Cluster','Region','User_Name','Assign_Date','Status','Previous_Reading_Date_Time',
        'Current_Reading_Date_Time','Previous_EB_Cumulative_KWH_As_Per_EB_Meter','Current_EB_Cumulative_KWH_As_Per_EB_Meter',
        'Previous_EB_Running_Hours_Cumulative_Available_Not_Available','Current_EB_Running_Hours_Cumulative_Available_Not_Available',
        'Previous_EB_Running_Hours_Cumulative_As_per_PIU_I2PMS_AMF','Current_EB_Running_Hours_Cumulative_As_per_PIU_I2PMS_AMF',
        'Previous_Type_of_DG_Static_Mobile','Current_Type_of_DG_Static_Mobile','Previous_DG_Running_Hours_Reading_As_Per_HMR','Current_DG_Running_Hours_Reading_As_Per_HMR',
        'Previous_DG_Running_Hours_Reading_As_Per_PIU_I2PMS_AMF','Current_DG_Running_Hours_Reading_As_Per_PIU_I2PMS_AMF',
        'Previous_Opening_Diesel_stock_Before_Filling','Current_Opening_Diesel_stock_Before_Filling','Previous_Filled_Ltrs',
        'Current_Filled_Ltrs','Previous_Diesel_Bill_Number','Current_Diesel_Bill_Number','Previous_Remarks_If_any','Current_Remarks_If_any',
        'No_of_days_since_previous_filling','Calculated_CPH_HMR','Calculated_CPH_As_per_PIU_I2PMS_AMF','Calculated_DG_HR_HMR',
        'Calculated_DG_HR_As_per_PIU_I2PMS_AMF','Calculated_EB_KWH_As_per_Meter','Calculated_EB_HR_As_per_PIU_I2PMS_AMF','Deviation'
    ]
    search_fields = ['File_id','Global_ID']

    filter_horizontal = []
    list_filter = []
    fieldsets = []
admin.site.register(EnergyDieelFilling, EnergyDieselFillingAdmin)


class FuelDrawnAdmin(admin.ModelAdmin):
    list_display = [
        'id','FT_ID','FT_name','FT_mobile_no','Cluster_Name','Fuel_Drawn_Date','Card_No','City_Township_Fuel_Station',
        'Customer','Fuel_Station_Name','Diesel_Purchased_Qty','Diesel_Per_Ltr_Cost_Rs','Total_Diesel_Cost_Rs',
        'Receipt_No','Receipt_Image_Upload','Vehicle_Plate','Remarks'
    ]
    search_fields = ['id','FT_ID','FT_name','FT_mobile_no','Cluster_Name','Fuel_Drawn_Date','Card_No','Vehicle_Plate']

    filter_horizontal = []
    list_filter = []
    fieldsets = []
admin.site.register(FuelDrawn, FuelDrawnAdmin)


class SiteFixedAdmin(admin.ModelAdmin):
    list_display = [
        'global_id','site_name','site_address','cluster','CE','site_tenancy','DG_NON_DG','DG_capacity_kva',
        'EB_status','card_number','last_month_approved_CPH'
    ]
    search_fields = ['global_id','site_name','site_address','cluster','CE','site_tenancy','DG_NON_DG','DG_capacity_kva',
        'EB_status','card_number','last_month_approved_CPH']

    filter_horizontal = []
    list_filter = []
    fieldsets = []
admin.site.register(SiteFixed, SiteFixedAdmin)


class PMCLAdmin(admin.ModelAdmin):
    list_display = ['user','global_id','Q1_Status','Q1_Material_Required','Q1_Remarks','Q2_Status',
                    'Q2_Material_Required','Q2_Remarks','Q3_Status','Q3_Material_Required','Q3_Remarks',
                    'Q4_Status','Q4_Material_Required','Q4_Remarks','Q5_Status','Q5_Material_Required','Q5_Remarks',
                    'Q6_Status','Q6_Material_Required','Q6_Remarks','Q7_Status','Q7_Material_Required',
                    'Q7_Remarks','Q8_Status','Q8_Material_Required','Q8_Remarks','Q9_Status',
                    'Q9_Material_Required','Q9_Remarks','Q10_Status','Q10_Material_Required','Q10_Remarks','date','time']
    
    search_fields = ['user','global_id','Q1_Status','Q1_Material_Required','Q1_Remarks','Q2_Status', 'Q2_Material_Required',
                    'Q2_Remarks','Q3_Status','Q3_Material_Required','Q3_Remarks', 'Q4_Status','Q4_Material_Required','Q4_Remarks',
                    'Q5_Status','Q5_Material_Required','Q5_Remarks', 'Q6_Status','Q6_Material_Required','Q6_Remarks','Q7_Status',
                    'Q7_Material_Required','Q7_Remarks','Q8_Status','Q8_Material_Required','Q8_Remarks','Q9_Status',
                    'Q9_Material_Required','Q9_Remarks','Q10_Status','Q10_Material_Required','Q10_Remarks','date','time']

    filter_horizontal = []
    list_filter = []
    fieldsets = []
admin.site.register(PMCL, PMCLAdmin)


class PMCLImageAdmin(admin.ModelAdmin):
    list_display = ['id','images']

    filter_horizontal = []
    list_filter = []
    fieldsets = []
admin.site.register(PreMonsoonImages, PMCLImageAdmin)


class DocumentRepositoryAdmin(admin.ModelAdmin):
    list_display = ['user','document_id','project_type','region','site_docs_id','circles','file_category','date','time']

    search_fields = ['user','document_id','project_type','region','site_docs_id','circles','file_category','date','time']

    filter_horizontal = []
    list_filter = []
    fieldsets = []
admin.site.register(DocumentRepository, DocumentRepositoryAdmin)


class DocumentsOfRepositoryAdmin(admin.ModelAdmin):
    list_display = ['files','file_name','date','time']

    search_fields = ['file_name','date','time']

    filter_horizontal = []
    list_filter = []
    fieldsets = []
admin.site.register(DocumentsOfRepository, DocumentsOfRepositoryAdmin)


class ProjectTypeAdmin(admin.ModelAdmin):
    list_display = ['project_type']

    filter_horizontal = []
    list_filter = []
    fieldsets = []
admin.site.register(ProjectTypeModel, ProjectTypeAdmin)


class CustomerDataAdmin(admin.ModelAdmin):
    list_display = ['customers']

    filter_horizontal = []
    list_filter = []
    fieldsets = []
admin.site.register(CustomerDataModel, CustomerDataAdmin)


class ProjectsMasterModelAdmin(admin.ModelAdmin):
    list_display = ['user','site_id','site_name','customer','project_type','customer_expected_target_date','assigned_to_asm',
                    'sales_remark','project_description','assigned_to_technician','technician_target_date','asm_remarks',
                    'project_status','completed_date','technician_remarks','pendings','completed']

    filter_horizontal = []
    list_filter = []
    fieldsets = []
admin.site.register(ProjectsMasterModel, ProjectsMasterModelAdmin)




