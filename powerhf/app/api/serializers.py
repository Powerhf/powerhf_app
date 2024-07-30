from app.models import *
from rest_framework import serializers


class EnergyFuelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergyFuel
        fields = ['id','global_id','Tasks','DG_Serial_Number','DG_HMR_Status','DG_HMR_Reading','DG_PIU_Status','Current_DG_PIU_Reading',
            'Diesel_Filling_Done','Date_Of_Diesel_Filling','Diesel_Balance_Before_Filling','Fuel_Qty_Filled',
            'EB_Meter_Status','Current_EB_MTR_KWH','EB_PIU_Meter_Status','Current_EB_PIU_Reading', 'Total_DC_Load', 
            'Total_EB_KWH_Reading_from_all_Channels','Remarks','FT_ID','FT_name','FT_mobile_no','Receipt_No','Card_Number',
            'Vehicle_Plate','EB_Cumulative_KWH_Image','EB_Running_Hours_Cumulative_Image','DG_Running_Hours_Reading_Image',
            'DG_Running_Hours_as_per_piu_Reading_Image','Diesel_Bill_Number_Image','DG_Running_HRS','CPH_CPH_Comparison_With_Last_CPH',
            'CPH_as_par_HMR','CPH_as_par_PIU','EB_KWH']
        

class MonsoonChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = PMCL
        fields = ['id','Q1_Attach','Q1_Status','Q1_Material_Required','Q1_Remarks','Q2_Attach','Q2_Status','Q2_Material_Required',
                'Q2_Remarks','Q3_Attach','Q3_Status','Q3_Material_Required','Q3_Remarks','Q4_Attach','Q4_Status','Q4_Material_Required',
                'Q4_Remarks','Q5_Attach','Q5_Status','Q5_Material_Required','Q5_Remarks','Q6_Attach','Q6_Status','Q6_Material_Required',
                'Q6_Remarks','Q7_Attach','Q7_Status','Q7_Material_Required','Q7_Remarks','Q8_Attach','Q8_Status','Q8_Material_Required',
                'Q8_Remarks','Q9_Attach','Q9_Status','Q9_Material_Required','Q9_Remarks','Q10_Attach','Q10_Status','Q10_Material_Required',
                'Q10_Remarks']
