from app.models import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from app.api.serializers import *


class EnergyFuelViewsets(viewsets.ViewSet):
    def list(self, request):
        fuel_report = EnergyFuel.objects.filter(Tasks='Diesel Filling and Energy Reading').order_by('-Date_Of_Diesel_Filling')
        energy_data = fuel_report.values(
            'global_id__global_id','global_id__site_name','global_id__site_address','global_id__cluster','global_id__CE','global_id__site_tenancy',
            'global_id__DG_NON_DG','global_id__DG_capacity_kva','global_id__EB_status','global_id__card_number','global_id__last_month_approved_CPH',
            'Tasks','DG_Serial_Number','DG_HMR_Status','DG_HMR_Reading','DG_PIU_Status','Current_DG_PIU_Reading',
            'Diesel_Filling_Done','Date_Of_Diesel_Filling','Diesel_Balance_Before_Filling','Fuel_Qty_Filled','Current_Diesel_Balance',
            'EB_Meter_Status','Current_EB_MTR_KWH','EB_PIU_Meter_Status','Current_EB_PIU_Reading','Total_DC_Load',
            'Total_EB_KWH_Reading_from_all_Channels','Remarks','FT_ID','FT_name','FT_mobile_no','Receipt_No','Card_Number','Vehicle_Plate',
            'EB_Cumulative_KWH_Image','EB_Running_Hours_Cumulative_Image','DG_Running_Hours_Reading_Image',
            'DG_Running_Hours_as_per_piu_Reading_Image','Diesel_Bill_Number_Image','DG_Running_HRS','CPH_CPH_Comparison_With_Last_CPH',
            'CPH_as_par_HMR','CPH_as_par_PIU','EB_KWH'
        )
        data_energy = list(energy_data)
        fuel_report2_ = EnergyFuel.objects.filter(Tasks='Energy Reading').order_by('-Date_Of_Diesel_Filling')
        energy_data2_ = fuel_report2_.values(
            'global_id__global_id','global_id__site_name','global_id__site_address','global_id__cluster','global_id__CE','global_id__site_tenancy',
            'global_id__DG_NON_DG','global_id__DG_capacity_kva','global_id__EB_status','global_id__card_number','global_id__last_month_approved_CPH',
            'Tasks','DG_Serial_Number','DG_HMR_Status','DG_HMR_Reading','DG_PIU_Status','Current_DG_PIU_Reading',
            'Diesel_Filling_Done','Date_Of_Diesel_Filling','Diesel_Balance_Before_Filling','Fuel_Qty_Filled','Current_Diesel_Balance',
            'EB_Meter_Status','Current_EB_MTR_KWH','EB_PIU_Meter_Status','Current_EB_PIU_Reading','Total_DC_Load',
            'Total_EB_KWH_Reading_from_all_Channels','Remarks','FT_ID','FT_name','FT_mobile_no','Receipt_No','Card_Number','Vehicle_Plate',
            'EB_Cumulative_KWH_Image','EB_Running_Hours_Cumulative_Image','DG_Running_Hours_Reading_Image',
            'DG_Running_Hours_as_per_piu_Reading_Image','Diesel_Bill_Number_Image','DG_Running_HRS','CPH_CPH_Comparison_With_Last_CPH',
            'CPH_as_par_HMR','CPH_as_par_PIU','EB_KWH'
        )
        energy_reading = list(energy_data2_)
        return Response({'energy_data':data_energy, 'energy_reading':energy_reading})
    
    

class MonsoonChecklistViewset(viewsets.ViewSet):
    def list(self, request):
        monsoon_checklist = PMCL.objects.all().order_by('-date')
        checklist_data = monsoon_checklist.values(
            'user__first_name', 'global_id', 'user__last_name','Q1_Status','Q1_Material_Required','Q1_Remarks','Q2_Status',
            'Q2_Material_Required','Q2_Remarks','Q3_Status','Q3_Material_Required','Q3_Remarks','Q4_Status',
            'Q4_Material_Required','Q4_Remarks','Q5_Status','Q5_Material_Required','Q5_Remarks','Q6_Status',
            'Q6_Material_Required','Q6_Remarks','Q7_Status','Q7_Material_Required','Q7_Remarks','Q8_Status',
            'Q8_Material_Required','Q8_Remarks','Q9_Status','Q9_Material_Required','Q9_Remarks','Q10_Status',
            'Q10_Material_Required','Q10_Remarks','date','time'
        )
        data_checklist = list(checklist_data)
        return Response({'checklist':data_checklist})
    
    def retrieve(self, request, pk=None):
        id = pk        
        if id is not None:
            monsoon_checklist = PMCL.objects.filter(id=id)
            checklist_data = monsoon_checklist.values(
                'user__first_name', 'user__last_name','Q1_Status','Q1_Material_Required','Q1_Remarks','Q2_Status',
                'Q2_Material_Required','Q2_Remarks','Q3_Status','Q3_Material_Required','Q3_Remarks','Q4_Status',
                'Q4_Material_Required','Q4_Remarks','Q5_Status','Q5_Material_Required','Q5_Remarks','Q6_Status',
                'Q6_Material_Required','Q6_Remarks','Q7_Status','Q7_Material_Required','Q7_Remarks','Q8_Status',
                'Q8_Material_Required','Q8_Remarks','Q9_Status','Q9_Material_Required','Q9_Remarks','Q10_Status',
                'Q10_Material_Required','Q10_Remarks','date','time'
            )
            return Response({'status':'true','checklist':checklist_data})
        else:
            return Response({'status':'false'})
        