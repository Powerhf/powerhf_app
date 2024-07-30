from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.core.exceptions import ValidationError
from app.models import *

DEPARTMENTS = (
    ('Select department','Select department'),
    ('HR','HR'),
    ('IT','IT'),
    ('Accounts','Accounts'),
    ('CAD','CAD'),
    ('SCM','SCM'),
    ('Technical','Technical'),
)

# USERS_REGIONS = (
#     ('Select Region','Select Region'),('All','All'),('East','East'),('West','West'),('North','North'),('South','South'),
# )

# USERS_CIRCLES = (
#     ('Select Circle','Select Circle'),('All','All'),('JK','JK'),('UPE','UPE'),('UPW','UPW'),('HP','HP'),('HR','HR'),('PB','PB'),('DL','DL'),
#     ('MU','MU'),('MH','MH'),('GJ','GJ'),('RJ','RJ'),('RJ','RJ'),('CG','CG'),('AS','AS'),
#     ('NE','NE'),('WB','WB'),('KOL','KOL'),('OD','OD'),('JH','JH'),('BH','BH'),('AP','AP'),
#     ('TS','TS'),('TN','TN'),('KN','KN'),('KL','KL'),
# )

class RegistrationForm(UserCreationForm):
    username = forms.CharField(label='Username',widget=forms.TextInput(
        attrs={'class': 'input-form input-sign-form', 'placeholder': 'Enter your username', 'id':'autoSizingInputGroup'}
    ))
    first_name = forms.CharField(label='First Name',widget=forms.TextInput(
        attrs={'class': 'input-form input-sign-form', 'placeholder': 'Enter your first name', 'id':'autoSizingInputGroup'}
    ))
    last_name = forms.CharField(label='Last Name',widget=forms.TextInput(
        attrs={'class': 'input-form input-sign-form', 'placeholder': 'Enter your last name', 'id':'autoSizingInputGroup'}
    ))
    email = forms.CharField(label='Email Address',widget=forms.EmailInput(
        attrs={'class': 'input-form input-sign-form', 'placeholder': 'Enter your email address', 'id':'autoSizingInputGroup'}
    ))
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(
        attrs={'class': 'input-form input-sign-form', 'placeholder': 'Enter your password', 'id':'autoSizingInputGroup'}
    ))
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(
        attrs={'class': 'input-form input-sign-form', 'placeholder': 'Enter your confirm password', 'id':'autoSizingInputGroup'}
    ))

    class Meta:
        model = Users
        fields = ['username','first_name','last_name','email','department','role','region','circle']
        widgets = {
            'role': forms.Select(attrs={'class': 'input-form input-sign-form'}),
            'department': forms.Select(attrs={'class': 'input-form input-sign-form'}),
            'region': forms.Select(attrs={'class': 'input-form input-sign-form'}),
            'circle': forms.Select(attrs={'class': 'input-form input-sign-form'}),
        }

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        if Users.objects.filter(username=username).exists():
            raise ValidationError("Username already exists.")
        return username
    
    def clean_department(self):
        department = self.cleaned_data['department']
        if department == 'Select department':
            raise ValidationError("Select Department is mendatory.")
        return department

    # def clean_region(self):
    #     region = self.cleaned_data['region']
    #     if region == 'Select Region':
    #         raise ValidationError("Select Region is mendatory.")
    #     return region

    # def clean_circle(self):
    #     circle = self.cleaned_data['circle']
    #     if circle == 'Select Circle':
    #         raise ValidationError("Select Circle is mendatory.")
    #     return circle
        
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if Users.objects.filter(email=email).exists():
            raise ValidationError("Email already exists.")
        return email
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.pop('autofocus',None)


class UserAuthentication(AuthenticationForm):
    username = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'input-form', 'placeholder': 'Enter your email address', 'id':'autoSizingInputGroup'}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'input-form', 'placeholder': 'Enter your password', 'id':'autoSizingInputGroup'}
    ))




# class DieselFillingOrReadingForm(forms.ModelForm):
#     DG_Serial_Number = forms.CharField(required=False, widget=forms.TextInput(
#         attrs={'class':'inputformsfill'}
#     ))
#     DG_HMR_Reading = forms.CharField(required=False, widget=forms.NumberInput(
#         attrs={'class':'inputformsfill'}
#     ))
#     Current_DG_PIU_Reading = forms.CharField(required=False, widget=forms.NumberInput(
#         attrs={'class':'inputformsfill'}
#     ))
#     Total_DC_Load = forms.CharField(required=False, widget=forms.NumberInput(
#         attrs={'class':'inputformsfill'}
#     ))
#     Total_EB_KWH_Reading_from_all_Channels = forms.CharField(required=False, widget=forms.NumberInput(
#         attrs={'class':'inputformsfill'}
#     ))
#     Diesel_Balance_Before_Filling = forms.CharField(required=False, widget=forms.NumberInput(
#         attrs={'class':'inputformsfill amount', 'id':'DieselBefroe'}
#     ))
#     Fuel_Qty_Filled = forms.CharField(required=False, widget=forms.NumberInput(
#         attrs={'class':'inputformsfill amount', 'id':'FuelQFilled'}
#     ))
#     Current_Diesel_Balance = forms.CharField(disabled=True,required=False, widget=forms.NumberInput(
#         attrs={'class':'inputformsfill', 'id':'total_amount'}
#     ))
#     Current_EB_MTR_KWH = forms.CharField(required=False, widget=forms.NumberInput(
#         attrs={'class':'inputformsfill'}
#     ))
#     Current_EB_PIU_Reading = forms.CharField(required=False, widget=forms.NumberInput(
#         attrs={'class':'inputformsfill'}
#     ))
#     Remarks = forms.CharField(required=False, widget=forms.TextInput(
#         attrs={'class':'inputformsfill'}
#     ))
#     EB_Cumulative_KWH_Image = forms.ImageField(required=True, widget=forms.FileInput(
#         attrs={'class':'img-input'}
#     ))
#     EB_Running_Hours_Cumulative_Image = forms.ImageField(required=True, widget=forms.FileInput(
#         attrs={'class':'img-input'}
#     ))
#     DG_Running_Hours_Reading_Image = forms.ImageField(required=True, widget=forms.FileInput(
#         attrs={'class':'img-input'}
#     ))
#     DG_Running_Hours_as_per_piu_Reading_Image = forms.ImageField(required=True, widget=forms.FileInput(
#         attrs={'class':'img-input'}
#     ))
#     Diesel_Bill_Number_Image = forms.ImageField(required=True, widget=forms.FileInput(
#         attrs={'class':'img-input'}
#     ))

#     class Meta:
#         model = EnergyFuel
#         widgets = {
#             'global_id': forms.Select(attrs={'class':'inputformsfill js-example-basic-single', 'name':'cars', 'id':'cars'}),
#             'Tasks': forms.Select(attrs={'class':'inputformsfill', 'id':'tasks_id'}),
#             'DG_HMR_Status': forms.Select(attrs={'class':'inputformsfill', 'id':'HMR_status'}),
#             'DG_PIU_Status': forms.Select(attrs={'class':'inputformsfill', 'id':'status_PUI'}),
#             'Diesel_Filling_Done': forms.Select(attrs={'class':'inputformsfill'}),
#             'EB_Meter_Status': forms.Select(attrs={'class':'inputformsfill', 'id':'EBMeter_status'}),
#             'EB_PIU_Meter_Status': forms.Select(attrs={'class':'inputformsfill', 'id':'EBPIU_Status'}),
#             'Date_Of_Diesel_Filling': forms.DateTimeInput(attrs={'class':'inputformsfill', 'type':'date'}),
#             'FT_ID': forms.TextInput(attrs={'class':'inputformsfill'}),
#             'FT_name': forms.TextInput(attrs={'class':'inputformsfill'}),
#             'FT_mobile_no': forms.TextInput(attrs={'class':'inputformsfill'}),
#             'Receipt_No': forms.TextInput(attrs={'class':'inputformsfill'}),
#             'Card_Number': forms.TextInput(attrs={'class':'inputformsfill'}),
#             'Vehicle_Plate': forms.TextInput(attrs={'class':'inputformsfill'}),
#         }
#         fields = ['global_id','Tasks','DG_Serial_Number','DG_HMR_Status','DG_HMR_Reading','DG_PIU_Status','Current_DG_PIU_Reading',
#                   'Diesel_Filling_Done','Date_Of_Diesel_Filling','Diesel_Balance_Before_Filling','Fuel_Qty_Filled',
#                   'EB_Meter_Status','Current_EB_MTR_KWH','EB_PIU_Meter_Status','Current_EB_PIU_Reading', 'Total_DC_Load', 
#                   'Total_EB_KWH_Reading_from_all_Channels','Remarks','FT_ID','FT_name','FT_mobile_no','Receipt_No','Card_Number',
#                   'Vehicle_Plate','EB_Cumulative_KWH_Image','EB_Running_Hours_Cumulative_Image','DG_Running_Hours_Reading_Image',
#                   'DG_Running_Hours_as_per_piu_Reading_Image','Diesel_Bill_Number_Image']



class DieselFillingOrReadingForm(forms.ModelForm):
    DG_HMR_Reading = forms.CharField(required=False, widget=forms.NumberInput(
        attrs={'class':'inputformsfill'}
    ))
    Current_DG_PIU_Reading = forms.CharField(required=False, widget=forms.NumberInput(
        attrs={'class':'inputformsfill'}
    ))
    Total_DC_Load = forms.CharField(required=False, widget=forms.NumberInput(
        attrs={'class':'inputformsfill'}
    ))
    Total_EB_KWH_Reading_from_all_Channels = forms.CharField(required=True, widget=forms.NumberInput(
        attrs={'class':'inputformsfill'}
    ))
    Diesel_Balance_Before_Filling = forms.CharField(required=True, widget=forms.NumberInput(
        attrs={'class':'inputformsfill amount', 'id':'DieselBefroe'}
    ))
    Fuel_Qty_Filled = forms.CharField(required=True, widget=forms.NumberInput(
        attrs={'class':'inputformsfill amount', 'id':'FuelQFilled'}
    ))
    Current_EB_MTR_KWH = forms.CharField(required=True, widget=forms.NumberInput(
        attrs={'class':'inputformsfill'}
    ))
    Current_EB_PIU_Reading = forms.CharField(required=True, widget=forms.NumberInput(
        attrs={'class':'inputformsfill'}
    ))
    EB_Cumulative_KWH_Image = forms.ImageField(required=True, widget=forms.FileInput(
        attrs={'class':'img-input'}
    ))
    EB_Running_Hours_Cumulative_Image = forms.ImageField(required=True, widget=forms.FileInput(
        attrs={'class':'img-input'}
    ))
    DG_Running_Hours_Reading_Image = forms.ImageField(required=True, widget=forms.FileInput(
        attrs={'class':'img-input'}
    ))
    DG_Running_Hours_as_per_piu_Reading_Image = forms.ImageField(required=True, widget=forms.FileInput(
        attrs={'class':'img-input'}
    ))
    Diesel_Bill_Number_Image = forms.ImageField(required=True, widget=forms.FileInput(
        attrs={'class':'img-input'}
    ))

    class Meta:
        model = EnergyFuel
        widgets = {
            'global_id': forms.Select(attrs={'class':'inputformsfill js-example-basic-single', 'name':'cars', 'id':'cars'}),
            'Tasks': forms.Select(attrs={'class':'inputformsfill', 'id':'tasks_id'}),
            'EB_Meter_Status': forms.Select(attrs={'class':'inputformsfill', 'id':'EBMeter_status'}),
            'Date_Of_Diesel_Filling': forms.DateTimeInput(attrs={'class':'inputformsfill', 'type':'date'}),
            'Receipt_No': forms.TextInput(attrs={'class':'inputformsfill'}),
        }
        fields = ['global_id','Tasks','DG_HMR_Reading','Current_DG_PIU_Reading','Date_Of_Diesel_Filling','Diesel_Balance_Before_Filling','Fuel_Qty_Filled',
                  'EB_Meter_Status','Current_EB_MTR_KWH','Current_EB_PIU_Reading', 'Total_DC_Load','Total_EB_KWH_Reading_from_all_Channels',
                  'Receipt_No','EB_Cumulative_KWH_Image','EB_Running_Hours_Cumulative_Image','DG_Running_Hours_Reading_Image',
                  'DG_Running_Hours_as_per_piu_Reading_Image','Diesel_Bill_Number_Image']



class FuelDrawnFTForm(forms.ModelForm):
    Remarks = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class':'inputformsfill', 'id':'input_id_frm'}
    ))
    Total_Diesel_Cost_Rs = forms.CharField(disabled=True,required=False, widget=forms.TextInput(
        attrs={'class':'inputformsfill', 'id':'amount3', 'value':'0'}
    ))
    class Meta:
        model = FuelDrawn
        widgets = {
            'FT_ID': forms.TextInput(attrs={'class':'inputformsfill', 'id':'input_id_frm'}),
            'FT_name': forms.TextInput(attrs={'class':'inputformsfill', 'id':'input_id_frm'}),
            'FT_mobile_no': forms.TextInput(attrs={'class':'inputformsfill', 'id':'input_id_frm'}),
            'Cluster_Name': forms.Select(attrs={'class':'inputformsfill', 'id':'input_id_frm'}),
            'Fuel_Drawn_Date': forms.DateInput(attrs={'class':'inputformsfill', 'id':'input_id_frm', 'type':'date'}),
            'Card_No': forms.TextInput(attrs={'class':'inputformsfill', 'id':'input_id_frm'}),
            'City_Township_Fuel_Station': forms.TextInput(attrs={'class':'inputformsfill', 'id':'input_id_frm'}),                 
            'Customer': forms.Select(attrs={'class':'inputformsfill', 'id':'input_id_frm'}),
            'Fuel_Station_Name': forms.TextInput(attrs={'class':'inputformsfill', 'id':'input_id_frm'}),
            'Diesel_Purchased_Qty': forms.NumberInput(attrs={'class':'inputformsfill', 'id':'amount1'}),
            'Diesel_Per_Ltr_Cost_Rs': forms.NumberInput(attrs={'class':'inputformsfill', 'id':'amount2'}),                
            'Receipt_No': forms.TextInput(attrs={'class':'inputformsfill', 'id':'input_id_frm'}),                
            'Receipt_Image_Upload': forms.FileInput(attrs={'class':'img-input', 'id':'input_id_frm'}),
            'Vehicle_Plate':forms.TextInput(attrs={'class':'inputformsfill', 'id':'input_id_frm'}),
        }
        fields = ['FT_ID','FT_name','FT_mobile_no','Cluster_Name','Fuel_Drawn_Date','Card_No','City_Township_Fuel_Station',
                  'Customer','Fuel_Station_Name','Diesel_Purchased_Qty','Diesel_Per_Ltr_Cost_Rs','Total_Diesel_Cost_Rs',
                  'Receipt_No','Receipt_Image_Upload','Vehicle_Plate','Remarks']        
        



class EnergyPDFFIleUpload(forms.ModelForm):
    file = forms.FileField(required=True, widget=forms.FileInput(
        attrs={'class':'img-input', 'accept':'application/pdf'}
    ))
    class Meta:
        model = EnergyDieelFilling
        fields = ['file']



class PMCL_Forms(forms.ModelForm):
    Q1_Attach = forms.FileField(required=False, widget=forms.TextInput(
        attrs={'class':'mon-box-img-input', 'multiple':True, 'type': 'file', 'id':'Q1_Attach', 'accept':'image/*'}
    ))
    Q2_Attach = forms.FileField(required=False, widget=forms.TextInput(
        attrs={'class':'mon-box-img-input', 'multiple':True, 'type': 'file', 'id':'Q2_Attach', 'accept':'image/*'}
    ))
    Q3_Attach = forms.FileField(required=False, widget=forms.TextInput(
        attrs={'class':'mon-box-img-input', 'multiple':True, 'type': 'file', 'id':'Q3_Attach', 'accept':'image/*'}
    ))
    Q4_Attach = forms.FileField(required=False, widget=forms.TextInput(
        attrs={'class':'mon-box-img-input', 'multiple':True, 'type': 'file', 'id':'Q4_Attach', 'accept':'image/*'}
    ))
    Q5_Attach = forms.FileField(required=False, widget=forms.TextInput(
        attrs={'class':'mon-box-img-input', 'multiple':True, 'type': 'file', 'id':'Q5_Attach', 'accept':'image/*'}
    ))
    Q6_Attach = forms.FileField(required=False, widget=forms.TextInput(
        attrs={'class':'mon-box-img-input', 'multiple':True, 'type': 'file', 'id':'Q6_Attach', 'accept':'image/*'}
    ))
    Q7_Attach = forms.FileField(required=False, widget=forms.TextInput(
        attrs={'class':'mon-box-img-input', 'multiple':True, 'type': 'file', 'id':'Q7_Attach', 'accept':'image/*'}
    ))
    Q8_Attach = forms.FileField(required=False, widget=forms.TextInput(
        attrs={'class':'mon-box-img-input', 'multiple':True, 'type': 'file', 'id':'Q8_Attach', 'accept':'image/*'}
    ))
    Q9_Attach = forms.FileField(required=False, widget=forms.TextInput(
        attrs={'class':'mon-box-img-input', 'multiple':True, 'type': 'file', 'id':'Q9_Attach', 'accept':'image/*'}
    ))
    Q10_Attach = forms.FileField(required=False, widget=forms.TextInput(
        attrs={'class':'mon-box-img-input', 'multiple':True, 'type': 'file', 'id':'Q10_Attach', 'accept':'image/*'}
    ))
    Q1_Material_Required = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'class':'text-box', 'id':'Q1_Material_Required'}
    ))
    Q2_Material_Required = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'class':'text-box', 'id':'Q2_Material_Required'}
    ))
    Q3_Material_Required = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'class':'text-box', 'id':'Q3_Material_Required'}
    ))
    Q4_Material_Required = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'class':'text-box', 'id':'Q4_Material_Required'}
    ))
    Q5_Material_Required = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'class':'text-box', 'id':'Q5_Material_Required'}
    ))
    Q6_Material_Required = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'class':'text-box', 'id':'Q6_Material_Required'}
    ))
    Q7_Material_Required = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'class':'text-box', 'id':'Q7_Material_Required'}
    ))
    Q8_Material_Required = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'class':'text-box', 'id':'Q8_Material_Required'}
    ))
    Q9_Material_Required = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'class':'text-box', 'id':'Q9_Material_Required'}
    ))
    Q10_Material_Required = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'class':'text-box', 'id':'Q10_Material_Required'}
    ))
    Q1_Remarks = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'class':'text-box', 'id':'Q1_Remarks'}
    ))
    Q2_Remarks = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'class':'text-box', 'id':'Q2_Remarks'}
    ))
    Q3_Remarks = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'class':'text-box', 'id':'Q3_Remarks'}
    ))
    Q4_Remarks = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'class':'text-box', 'id':'Q4_Remarks'}
    ))
    Q5_Remarks = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'class':'text-box', 'id':'Q5_Remarks'}
    ))
    Q6_Remarks = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'class':'text-box', 'id':'Q6_Remarks'}
    ))
    Q7_Remarks = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'class':'text-box', 'id':'Q7_Remarks'}
    ))
    Q8_Remarks = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'class':'text-box', 'id':'Q8_Remarks'}
    ))
    Q9_Remarks = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'class':'text-box', 'id':'Q9_Remarks'}
    ))
    Q10_Remarks = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'class':'text-box', 'id':'Q10_Remarks'}
    ))
    class Meta:
        model = PMCL
        fields = ['global_id','Q1_Attach','Q1_Status','Q1_Material_Required','Q1_Remarks','Q2_Attach','Q2_Status','Q2_Material_Required','Q2_Remarks',
            'Q3_Attach','Q3_Status','Q3_Material_Required','Q3_Remarks','Q4_Attach','Q4_Status','Q4_Material_Required','Q4_Remarks',
            'Q5_Attach','Q5_Status','Q5_Material_Required','Q5_Remarks','Q6_Attach','Q6_Status','Q6_Material_Required','Q6_Remarks',
            'Q7_Attach','Q7_Status','Q7_Material_Required','Q7_Remarks','Q8_Attach','Q8_Status','Q8_Material_Required','Q8_Remarks',
            'Q9_Attach','Q9_Status','Q9_Material_Required','Q9_Remarks','Q10_Attach','Q10_Status','Q10_Material_Required','Q10_Remarks']
        widgets = {
            'global_id':forms.Select(attrs={'class':'inputformsfill js-example-basic-single', 'name':'cars', 'id':'cars'}),
            'Q1_Status':forms.Select(attrs={'class':'text-monsson-box', 'id':'Q1_Status'}),
            'Q2_Status':forms.Select(attrs={'class':'text-monsson-box', 'id':'Q2_Status'}),
            'Q3_Status':forms.Select(attrs={'class':'text-monsson-box', 'id':'Q3_Status'}),
            'Q4_Status':forms.Select(attrs={'class':'text-monsson-box', 'id':'Q4_Status'}),
            'Q5_Status':forms.Select(attrs={'class':'text-monsson-box', 'id':'Q5_Status'}),
            'Q6_Status':forms.Select(attrs={'class':'text-monsson-box', 'id':'Q6_Status'}),
            'Q7_Status':forms.Select(attrs={'class':'text-monsson-box', 'id':'Q7_Status'}),
            'Q8_Status':forms.Select(attrs={'class':'text-monsson-box', 'id':'Q8_Status'}),
            'Q9_Status':forms.Select(attrs={'class':'text-monsson-box', 'id':'Q9_Status'}),
            'Q10_Status':forms.Select(attrs={'class':'text-monsson-box', 'id':'Q10_Status'}),
        }



# Documents Repository:

class DocumentsRepositoryForm(forms.ModelForm):
    site_docs_id = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class':'inputformsfill', 'name':'site_docs_id_dt'}
    ))
    documents = forms.FileField(required=True, widget=forms.TextInput(
        attrs={'class':'mon-box-img-input', 'multiple':True, 'id':'documents', 'type': 'file', 'accept':'*/*'}
    ))
    class Meta:
        model = DocumentRepository
        fields = ['project_type','region','site_docs_id','documents','circles','file_category']
        widgets = {
            'project_type': forms.Select(attrs={'class':'inputformsfill', 'name':'project_dt_types'}),
            'region': forms.Select(attrs={'class':'inputformsfill', 'name':'regions_dt'}),
            'circles': forms.Select(attrs={'class':'inputformsfill', 'name':'circles_dt'}),
            'file_category': forms.Select(attrs={'class':'inputformsfill', 'name':'file_category_dt'}),
        }


# Documents Repository END

