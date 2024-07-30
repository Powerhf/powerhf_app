from django.shortcuts import render, redirect, get_object_or_404
from app.forms import *
from app.models import *
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from pdfquery import PDFQuery
from datetime import datetime, date
import pandas as pd
import os
import random


#################### User Registration ####################
def Userregistation(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                messages.success(request, 'User data has been created successfully.')
                form.save()
                return redirect('register')
        else:
            form = RegistrationForm()
        return render(request, 'signup.html', {'forms':form})
    else:
        return redirect('index')
    

#################### User Login ####################
def UserLogin(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UserAuthentication(request=request,data=request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('index')
                else:
                    return HttpResponse("<h5>!Something done wrong, please try again.</h5>")
        else:
            form = UserAuthentication()                
        return render(request, 'login.html', {'forms':form})
    else:
        return redirect('index')


#################### Home Page ####################
def Index(request):
    if request.user.is_authenticated:
        energy_data = EnergyFuel.objects.filter(Tasks='Diesel Filling and Energy Reading').values()
        # drf = pd.DataFrame(energy_data)
        # print(drf[['global_id_id','CPH_as_par_HMR']])
        # gb_id = energy_data.global_id_id
        # cph_hmr = energy_data.CPH_as_par_HMR
        return render(request, 'app/index.html', {'energy_data':energy_data})
    else:
        return redirect('auth')
    
#################### HOTO Report ####################
def Reports_Hoto(request):
    if request.user.is_authenticated:
        return render(request, 'app/reports/hoto_report.html')
    else:
        return redirect('auth')

#################### DRF Report ####################
class DRFReport(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            pagination_fuel_report = EnergyFuel.objects.filter(Tasks='Diesel Filling and Energy Reading').order_by('-Date_Of_Diesel_Filling')
            paginator = Paginator(pagination_fuel_report, 50, orphans=1)
            page_number = request.GET.get('page')
            data_obj = paginator.get_page(page_number)
            context = {'fuel_report':data_obj, 'all_dfr_data':pagination_fuel_report}
            return render(request, 'app/reports/energy_report_drf.html', context)
        else:
            return redirect('auth')

#################### Fuel Draw Report ####################
class FuelDrawnReport(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            Pagination_fuel_drawn = FuelDrawn.objects.filter().order_by('-Fuel_Drawn_Date')
            paginator = Paginator(Pagination_fuel_drawn, 50, orphans=1)
            page_number = request.GET.get('page')
            data_obj = paginator.get_page(page_number)
            context = {'fuel_drawn':data_obj, 'all_fuel_drawn_data':Pagination_fuel_drawn}
            return render(request, 'app/reports/energy_report_fuel_drawn.html', context)
        else:
            return redirect('auth')
            
#################### Energy Reading Report ####################
class EnergyReadingReport(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            pagination_fuel_report = EnergyFuel.objects.filter(Tasks='Energy Reading').order_by('-Date_Of_Diesel_Filling')
            paginator = Paginator(pagination_fuel_report, 50, orphans=1)
            page_number = request.GET.get('page')
            data_obj = paginator.get_page(page_number)
            context = {'fuel_report':data_obj, 'all_reading_data':pagination_fuel_report}
            return render(request, 'app/reports/energy_report_diesel_reading.html', context)
        else:
            return redirect('auth')
        

#################### DRF Filter Report ####################
class EnergyDFRFilters(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            if request.GET.get('start_date') and request.GET.get('end_date'):
                start_date = request.GET.get('start_date')
                end_date = request.GET.get('end_date')
                fuel_report = EnergyFuel.objects.filter(Tasks='Diesel Filling and Energy Reading', Date_Of_Diesel_Filling__range=(start_date, end_date)).order_by('Date_Of_Diesel_Filling')
                return render(request, 'app/reports/energy_filters.html', {'fuel_report':fuel_report})
            elif request.GET.get('start_date'):
                start_date = request.GET.get('start_date')
                fuel_report = EnergyFuel.objects.filter(Tasks='Diesel Filling and Energy Reading', Date_Of_Diesel_Filling=start_date).order_by('Date_Of_Diesel_Filling')
                return render(request, 'app/reports/energy_filters.html', {'fuel_report':fuel_report})
            elif request.GET.get('end_date'):
                end_date = request.GET.get('end_date')
                fuel_report = EnergyFuel.objects.filter(Tasks='Diesel Filling and Energy Reading', Date_Of_Diesel_Filling=end_date).order_by('Date_Of_Diesel_Filling')
                return render(request, 'app/reports/energy_filters.html', {'fuel_report':fuel_report})
            else:
                return HttpResponse('<h5>Getting some error, Please write again. Back to <a href="/reports/energy/drf/">reports</a></h5>')
        else:
            return redirect('auth')
        

#################### Energy Reading Filter Report ####################
class EnergyReadingFilters(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            if request.GET.get('start_date') and request.GET.get('end_date'):
                start_date = request.GET.get('start_date')
                end_date = request.GET.get('end_date')
                fuel_report = EnergyFuel.objects.filter(Tasks='Energy Reading', Date_Of_Diesel_Filling__range=(start_date, end_date)).order_by('Date_Of_Diesel_Filling')
                return render(request, 'app/reports/energy_filters.html', {'fuel_report':fuel_report})
            elif request.GET.get('start_date'):
                start_date = request.GET.get('start_date')
                fuel_report = EnergyFuel.objects.filter(Tasks='Energy Reading', Date_Of_Diesel_Filling=start_date).order_by('Date_Of_Diesel_Filling')
                return render(request, 'app/reports/energy_filters.html', {'fuel_report':fuel_report})
            elif request.GET.get('end_date'):
                end_date = request.GET.get('end_date')
                fuel_report = EnergyFuel.objects.filter(Tasks='Energy Reading', Date_Of_Diesel_Filling=end_date).order_by('Date_Of_Diesel_Filling')
                return render(request, 'app/reports/energy_filters.html', {'fuel_report':fuel_report})
            else:
                return HttpResponse('<h5>Getting some error, Please write again. Back to <a href="/reports/energy/energy-reading/">reports</a></h5>')
        else:
            return redirect('auth')
        

#################### Fuel Draw Filter Report Page ####################
class FuelDrawnFilters(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            if request.GET.get('start_date') and request.GET.get('end_date'):
                start_date = request.GET.get('start_date')
                end_date = request.GET.get('end_date')
                fuel_report = FuelDrawn.objects.filter(Fuel_Drawn_Date__range=(start_date, end_date)).order_by('Fuel_Drawn_Date')
                return render(request, 'app/reports/fuel_drawn_filter.html', {'fuel_drawn':fuel_report})
            elif request.GET.get('start_date'):
                start_date = request.GET.get('start_date')
                fuel_report = FuelDrawn.objects.filter(Fuel_Drawn_Date=start_date).order_by('Fuel_Drawn_Date')
                return render(request, 'app/reports/fuel_drawn_filter.html', {'fuel_drawn':fuel_report})
            elif request.GET.get('end_date'):
                end_date = request.GET.get('end_date')
                fuel_report = FuelDrawn.objects.filter(Fuel_Drawn_Date=end_date).order_by('Fuel_Drawn_Date')
                return render(request, 'app/reports/fuel_drawn_filter.html', {'fuel_drawn':fuel_report})
            else:
                return HttpResponse('<h5>Getting some error, Please write again. Back to <a href="/reports/energy/fuel-drawn/">reports</a></h5>')
        else:
            return redirect('auth')

#################### PM Report Page ####################
class PM_Reports(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'app/reports/pm_repo.html')
        else:
            return redirect('auth')

#################### CM Report Page ####################
class CM_Reports(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'app/reports/cm_repo.html')
        else:
            return redirect('auth')

#################### Diesel FSR Report Page ####################
class Diese_Filling_FSR_Reports(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            pagination_fuel_report = EnergyDieelFilling.objects.all().order_by('-Current_Reading_Date_Time')
            paginator = Paginator(pagination_fuel_report, 50, orphans=1)
            page_number = request.GET.get('page')
            data_obj = paginator.get_page(page_number)
            context = {'fuel_report':data_obj, 'all_fsr_data':pagination_fuel_report}
            return render(request, 'app/reports/diesel_filling_fsr_report.html', context)
        else:
            return redirect('auth')
        
#################### PM Form Page ####################        
class PM_Transactions(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'app/forms/pm_trans.html')
        else:
            return redirect('auth')

#################### CM Form Page ####################
class CM_Transactions(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'app/forms/cm_trans.html')
        else:
            return redirect('auth')
        

#################### Extract Data from PDF (Will only work with 1 ATC format PDF) #################### 
class Diesel_Filling_FSR_Transactions(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:          
            forms = EnergyPDFFIleUpload()
            context = {'forms':forms}  
            return render(request, 'app/forms/diesel_filling_fsr_transactions.html', context)
        else:
            return redirect('auth')
    
    def post(self, request):
        if request.user.is_authenticated:
            form = EnergyPDFFIleUpload(data=request.POST, files=request.FILES)
            if form.is_valid():
                pdf_file = form.cleaned_data['file'] 
                pdf = PDFQuery(pdf_file)
                pdf.load()                       

                if pdf.pq('LTTextLineHorizontal:in_bbox("492.79, 757.93, 526.15, 767.93")').text():
                    SIteGlobalID = pdf.pq('LTTextLineHorizontal:in_bbox("492.79, 757.93, 526.15, 767.93")').text()
                else:
                    messages.error(request, "Please upload correct PDF format of diesel filling.")
                    return redirect('diese_filling_fsr_transactions')  

                if pdf.pq('LTTextLineHorizontal:in_bbox("201.82, 715.93, 251.86, 725.93")').text() != '':
                    AssingDate = pdf.pq('LTTextLineHorizontal:in_bbox("201.82, 715.93, 251.86, 725.93")').text()
                    AssingDate2 = datetime.strptime(AssingDate, '%d/%m/%Y')
                    assign_date = datetime.strftime(AssingDate2, '%Y-%m-%d')
                else:
                    assign_date = ''             
                
                # Static_ATC_data = SiteFixed.objects.get(global_id=SIteGlobalID)

                file_id = f'{SIteGlobalID}-{assign_date}'

                if not EnergyDieelFilling.objects.filter(File_id=file_id):

                    if pdf.pq('LTTextLineHorizontal:in_bbox("492.79, 757.93, 526.15, 767.93")').text() == SIteGlobalID:

                        if pdf.pq('LTTextLineHorizontal:in_bbox("260.49, 689.516, 334.518, 701.516")').text() == 'Diesel Filling':

                            if pdf.pq('LTTextLineHorizontal:in_bbox("207.95, 757.93, 245.74, 767.93")').text() != '':
                                circle = pdf.pq('LTTextLineHorizontal:in_bbox("207.95, 757.93, 245.74, 767.93")').text()
                            else:
                                circle = ''

                            if pdf.pq('LTTextLineHorizontal:in_bbox("188.49, 743.93, 265.2, 753.93")').text() != '':
                                site_name = pdf.pq('LTTextLineHorizontal:in_bbox("188.49, 743.93, 265.2, 753.93")').text()
                            elif pdf.pq('LTTextLineHorizontal:in_bbox("175.71, 743.93, 277.97, 753.93")').text() != '':
                                site_name = pdf.pq('LTTextLineHorizontal:in_bbox("175.71, 743.93, 277.97, 753.93")').text()
                            elif pdf.pq('LTTextLineHorizontal:in_bbox("209.06, 743.93, 244.62, 753.93")').text() != '':
                                site_name = pdf.pq('LTTextLineHorizontal:in_bbox("209.06, 743.93, 244.62, 753.93")').text()
                            else:
                                site_name = ''

                            if pdf.pq('LTTextLineHorizontal:in_bbox("478.9, 743.93, 540.04, 753.93")').text() != '':
                                cluster = pdf.pq('LTTextLineHorizontal:in_bbox("478.9, 743.93, 540.04, 753.93")').text()
                            else:
                                cluster = ''

                            if pdf.pq('LTTextLineHorizontal:in_bbox("477.23, 729.93, 541.71, 739.93")').text() != '':
                                user_name = pdf.pq('LTTextLineHorizontal:in_bbox("477.23, 729.93, 541.71, 739.93")').text()
                            elif pdf.pq('LTTextLineHorizontal:in_bbox("467.78, 729.93, 551.16, 739.93")').text() != '':
                                user_name = pdf.pq('LTTextLineHorizontal:in_bbox("467.78, 729.93, 551.16, 739.93")').text()
                            else:
                                user_name = ''

                            if pdf.pq('LTTextLineHorizontal:in_bbox("461.12, 715.93, 557.82, 725.93")').text() != '':
                                status = pdf.pq('LTTextLineHorizontal:in_bbox("461.12, 715.93, 557.82, 725.93")').text()
                                if status == 'Rejected by CE/CI Close':
                                    messages.error(request, "This PDF file is rejected, Please upload approved file.")
                                    return redirect('diese_filling_fsr_transactions')
                            elif pdf.pq('LTTextLineHorizontal:in_bbox("454.17, 715.93, 564.76, 725.93")').text() != '':
                                status = pdf.pq('LTTextLineHorizontal:in_bbox("454.17, 715.93, 564.76, 725.93")').text()
                                if status == 'Rejected by CE/CI Close':
                                    messages.error(request, "This PDF file is rejected, Please upload approved file.")
                                    return redirect('diese_filling_fsr_transactions')
                            else:
                                status = ''

                            if pdf.pq('LTTextLineHorizontal:in_bbox("213.78, 729.93, 239.9, 739.93")').text() != '':
                                region = pdf.pq('LTTextLineHorizontal:in_bbox("213.78, 729.93, 239.9, 739.93")').text()
                            else:
                                region = ''
                            
                            # Date Time
                            if pdf.pq('LTTextLineHorizontal:in_bbox("322.29, 661.93, 414.03, 671.93")').text() != '':
                                Previous_Reading_Date_Time = pdf.pq('LTTextLineHorizontal:in_bbox("322.29, 661.93, 414.03, 671.93")').text()
                                naive_datetime1 = datetime.strptime(Previous_Reading_Date_Time, '%d/%m/%Y %H:%M:%S')  
                                New_dt1 = datetime.strftime(naive_datetime1, '%Y-%m-%d')      
                                New_time1 = datetime.strftime(naive_datetime1, '%H:%M:%S')
                                previous_date_time = f'{New_dt1} {New_time1}'  
                            else:
                                previous_date_time = ''
                            
                            if pdf.pq('LTTextLineHorizontal:in_bbox("463.6, 661.93, 555.34, 671.93")').text() != '':
                                CUrrent_Reading_Date_Time = pdf.pq('LTTextLineHorizontal:in_bbox("463.6, 661.93, 555.34, 671.93")').text()
                                naive_datetime2 = datetime.strptime(CUrrent_Reading_Date_Time, '%d/%m/%Y %H:%M:%S')  
                                New_dt2 = datetime.strftime(naive_datetime2, '%Y-%m-%d')      
                                New_time2 = datetime.strftime(naive_datetime2, '%H:%M:%S')
                                current_date_time = f'{New_dt2} {New_time2}'  
                            else:
                                current_date_time = ''

                            # DG HMR
                            if pdf.pq('LTTextLineHorizontal:in_bbox("357.04, 571.93, 379.28, 581.93")').text() != '': 
                                previous_DG_running_reading = pdf.pq('LTTextLineHorizontal:in_bbox("357.04, 571.93, 379.28, 581.93")').text()
                            elif pdf.pq('LTTextLineHorizontal:in_bbox("354.26, 571.93, 382.06, 581.93")').text() != '': 
                                previous_DG_running_reading = pdf.pq('LTTextLineHorizontal:in_bbox("354.26, 571.93, 382.06, 581.93")').text()
                            else:
                                previous_DG_running_reading = ''

                            if pdf.pq('LTTextLineHorizontal:in_bbox("498.35, 571.93, 520.59, 581.93")').text() != '': 
                                current_DG_running_reading = pdf.pq('LTTextLineHorizontal:in_bbox("498.35, 571.93, 520.59, 581.93")').text()
                            elif pdf.pq('LTTextLineHorizontal:in_bbox("495.57, 571.93, 523.37, 581.93")').text() != '': 
                                current_DG_running_reading = pdf.pq('LTTextLineHorizontal:in_bbox("495.57, 571.93, 523.37, 581.93")').text()
                            else:
                                current_DG_running_reading = ''

                            # DG PIU
                            if pdf.pq('LTTextLineHorizontal:in_bbox("358.43, 552.93, 377.89, 562.93")').text() != '':
                                previous_DG_running_piu_reading = pdf.pq('LTTextLineHorizontal:in_bbox("358.43, 552.93, 377.89, 562.93")').text()
                            elif pdf.pq('LTTextLineHorizontal:in_bbox("357.04, 552.93, 379.28, 562.93")').text() != '':
                                previous_DG_running_piu_reading = pdf.pq('LTTextLineHorizontal:in_bbox("357.04, 552.93, 379.28, 562.93")').text()
                            else:
                                previous_DG_running_piu_reading = ''

                            if pdf.pq('LTTextLineHorizontal:in_bbox("499.74, 552.93, 519.2, 562.93")').text() != '':
                                current_DG_running_piu_reading = pdf.pq('LTTextLineHorizontal:in_bbox("499.74, 552.93, 519.2, 562.93")').text()
                            elif pdf.pq('LTTextLineHorizontal:in_bbox("498.35, 552.93, 520.59, 562.93")').text() != '':
                                current_DG_running_piu_reading = pdf.pq('LTTextLineHorizontal:in_bbox("498.35, 552.93, 520.59, 562.93")').text()
                            else:
                                current_DG_running_piu_reading = ''


                            # EB
                            if pdf.pq('LTTextLineHorizontal:in_bbox("418.53, 628.93, 459.1, 638.93")').text() == 'Available':
                                EB_Running_Hours_Cumulative_Available_Not_Available = pdf.pq('LTTextLineHorizontal:in_bbox("418.53, 628.93, 459.1, 638.93")').text()
                            else:
                                EB_Running_Hours_Cumulative_Available_Not_Available = 'Not-Available'

                            
                            if pdf.pq('LTTextLineHorizontal:in_bbox("351.48, 647.93, 384.84, 657.93")').text() != '':
                                previou_EB_meter_reading = pdf.pq('LTTextLineHorizontal:in_bbox("351.48, 647.93, 384.84, 657.93")').text()
                            else:
                                previou_EB_meter_reading = ''
                            
                            if pdf.pq('LTTextLineHorizontal:in_bbox("492.79, 647.93, 526.15, 657.93")').text() != '':
                                current_EB_meters_reading = pdf.pq('LTTextLineHorizontal:in_bbox("492.79, 647.93, 526.15, 657.93")').text()
                            else:
                                current_EB_meters_reading = ''

                            # EB PIU
                            if pdf.pq('LTTextLineHorizontal:in_bbox("352.87, 604.93, 383.45, 614.93")').text() != '':
                                previou_EB_meters_PIU_reading = pdf.pq('LTTextLineHorizontal:in_bbox("352.87, 604.93, 383.45, 614.93")').text()
                            else:
                                previou_EB_meters_PIU_reading = ''
                            
                            if pdf.pq('LTTextLineHorizontal:in_bbox("494.18, 604.93, 524.76, 614.93")').text() != '':
                                current_EB_meters_PIU_reading = pdf.pq('LTTextLineHorizontal:in_bbox("494.18, 604.93, 524.76, 614.93")').text()
                            else:
                                current_EB_meters_PIU_reading = ''
                            
                            
                            # Static
                            if pdf.pq('LTTextLineHorizontal:in_bbox("355.65, 585.93, 380.66, 595.93")').text() != '':
                                Previous_Type_of_DG_Static_Mobile = pdf.pq('LTTextLineHorizontal:in_bbox("355.65, 585.93, 380.66, 595.93")').text()
                            else:
                                Previous_Type_of_DG_Static_Mobile = ''

                            if pdf.pq('LTTextLineHorizontal:in_bbox("496.96, 585.93, 521.97, 595.93")').text() != '':
                                Current_Type_of_DG_Static_Mobile = pdf.pq('LTTextLineHorizontal:in_bbox("496.96, 585.93, 521.97, 595.93")').text()
                            else:
                                Current_Type_of_DG_Static_Mobile = ''
                            
                            # Before Filling
                            if pdf.pq('LTTextLineHorizontal:in_bbox("365.38, 533.93, 370.94, 543.93")').text() != '':
                                Previous_Opening_Diesel_stock_Before_Filling = pdf.pq('LTTextLineHorizontal:in_bbox("365.38, 533.93, 370.94, 543.93")').text()
                            elif pdf.pq('LTTextLineHorizontal:in_bbox("362.6, 533.93, 373.72, 543.93")').text() != '':
                                Previous_Opening_Diesel_stock_Before_Filling = pdf.pq('LTTextLineHorizontal:in_bbox("362.6, 533.93, 373.72, 543.93")').text()
                            else:
                                Previous_Opening_Diesel_stock_Before_Filling = ''
                            
                            if pdf.pq('LTTextLineHorizontal:in_bbox("503.91, 533.93, 515.03, 543.93")').text() != '':
                                Current_Opening_Diesel_stock_Before_Filling = pdf.pq('LTTextLineHorizontal:in_bbox("503.91, 533.93, 515.03, 543.93")').text()
                            else:
                                Current_Opening_Diesel_stock_Before_Filling = ''

                            # Filled Ltr
                            if pdf.pq('LTTextLineHorizontal:in_bbox("362.6, 519.93, 373.72, 529.93")').text() != '':
                                Previous_Filled_Ltrs = pdf.pq('LTTextLineHorizontal:in_bbox("362.6, 519.93, 373.72, 529.93")').text()
                            else:
                                Previous_Filled_Ltrs = ''
                            
                            if pdf.pq('LTTextLineHorizontal:in_bbox("503.91, 519.93, 515.03, 529.93")').text() != '':
                                Current_Filled_Ltrs = pdf.pq('LTTextLineHorizontal:in_bbox("503.91, 519.93, 515.03, 529.93")').text()
                            else:
                                Current_Filled_Ltrs = ''

                            # Diesel_Bill_Number
                            if pdf.pq('LTTextLineHorizontal:in_bbox("354.26, 505.93, 382.06, 515.93")').text() != '':
                                Previous_Diesel_Bill_Number = pdf.pq('LTTextLineHorizontal:in_bbox("354.26, 505.93, 382.06, 515.93")').text()
                            if pdf.pq('LTTextLineHorizontal:in_bbox("351.48, 505.93, 384.84, 515.93")').text() != '':
                                Previous_Diesel_Bill_Number = pdf.pq('LTTextLineHorizontal:in_bbox("351.48, 505.93, 384.84, 515.93")').text()
                            else:
                                Previous_Diesel_Bill_Number = ''
                            
                            if pdf.pq('LTTextLineHorizontal:in_bbox("495.57, 505.93, 523.37, 515.93")').text() != '':
                                Current_Diesel_Bill_Number = pdf.pq('LTTextLineHorizontal:in_bbox("495.57, 505.93, 523.37, 515.93")').text()
                            if pdf.pq('LTTextLineHorizontal:in_bbox("492.79, 505.93, 526.15, 515.93")').text() != '':
                                Current_Diesel_Bill_Number = pdf.pq('LTTextLineHorizontal:in_bbox("492.79, 505.93, 526.15, 515.93")').text()
                            else:
                                Current_Diesel_Bill_Number = ''


                            # Remarks
                            if pdf.pq('LTTextLineHorizontal:in_bbox("332.86, 491.93, 403.45, 501.93")').text() != '':
                                Previous_Remarks  = pdf.pq('LTTextLineHorizontal:in_bbox("332.86, 491.93, 403.45, 501.93")').text()
                            else:
                                Previous_Remarks = ''
                            
                            if pdf.pq('LTTextLineHorizontal:in_bbox("444.16, 491.93, 574.77, 501.93")').text() != '':
                                Remarks1  = pdf.pq('LTTextLineHorizontal:in_bbox("444.16, 491.93, 574.77, 501.93")').text()
                            else:
                                Remarks1 = ''
                            
                            if pdf.pq('LTTextLineHorizontal:in_bbox("479.73, 481.93, 539.2, 491.93")').text() != '':
                                Remarks2  = pdf.pq('LTTextLineHorizontal:in_bbox("479.73, 481.93, 539.2, 491.93")').text()
                            else:
                                Remarks2 = ''

                            # Calculated Field:
                            if pdf.pq('LTTextLineHorizontal:in_bbox("454.57, 429.93, 479.59, 439.93")').text() != '':
                                No_of_days_since_previous_filling = pdf.pq('LTTextLineHorizontal:in_bbox("454.57, 429.93, 479.59, 439.93")').text()
                            elif pdf.pq('LTTextLineHorizontal:in_bbox("454.57, 439.93, 479.59, 449.93")').text() != '':
                                No_of_days_since_previous_filling = pdf.pq('LTTextLineHorizontal:in_bbox("454.57, 439.93, 479.59, 449.93")').text()
                            else:
                                No_of_days_since_previous_filling = ''
                            
                            if pdf.pq('LTTextLineHorizontal:in_bbox("457.35, 425.93, 476.81, 435.93")').text() != '':
                                cph_hmr  = pdf.pq('LTTextLineHorizontal:in_bbox("457.35, 425.93, 476.81, 435.93")').text()
                            elif pdf.pq('LTTextLineHorizontal:in_bbox("454.57, 425.93, 479.59, 435.93")').text() != '':
                                cph_hmr  = pdf.pq('LTTextLineHorizontal:in_bbox("454.57, 425.93, 479.59, 435.93")').text()
                            else:
                                cph_hmr = ''

                            if pdf.pq('LTTextLineHorizontal:in_bbox("457.35, 411.93, 476.81, 421.93")').text() != '':
                                cph_piu  = pdf.pq('LTTextLineHorizontal:in_bbox("457.35, 411.93, 476.81, 421.93")').text()
                            elif pdf.pq('LTTextLineHorizontal:in_bbox("454.57, 411.93, 479.59, 421.93")').text() != '':
                                cph_piu  = pdf.pq('LTTextLineHorizontal:in_bbox("454.57, 411.93, 479.59, 421.93")').text()
                            else:
                                cph_piu = ''

                            if pdf.pq('LTTextLineHorizontal:in_bbox("454.57, 397.93, 479.59, 407.93")').text() != '':
                                hmr  = pdf.pq('LTTextLineHorizontal:in_bbox("454.57, 397.93, 479.59, 407.93")').text()
                            elif pdf.pq('LTTextLineHorizontal:in_bbox("454.57, 387.93, 479.59, 397.93")').text() != '':
                                hmr  = pdf.pq('LTTextLineHorizontal:in_bbox("454.57, 387.93, 479.59, 397.93")').text()
                            elif pdf.pq('LTTextLineHorizontal:in_bbox("457.35, 397.93, 476.81, 407.93")').text() != '':
                                hmr  = pdf.pq('LTTextLineHorizontal:in_bbox("457.35, 397.93, 476.81, 407.93")').text()
                            else:
                                hmr = ''

                            if pdf.pq('LTTextLineHorizontal:in_bbox("441.78, 369.93, 492.37, 379.93")').text() != '':
                                kwh  = pdf.pq('LTTextLineHorizontal:in_bbox("441.78, 369.93, 492.37, 379.93")').text()
                            elif pdf.pq('LTTextLineHorizontal:in_bbox("446.23, 369.93, 487.93, 379.93")').text() != '':
                                kwh  = pdf.pq('LTTextLineHorizontal:in_bbox("446.23, 369.93, 487.93, 379.93")').text()
                            elif pdf.pq('LTTextLineHorizontal:in_bbox("449.01, 359.93, 485.15, 369.93")').text() != '':
                                kwh  = pdf.pq('LTTextLineHorizontal:in_bbox("449.01, 359.93, 485.15, 369.93")').text()
                            else:
                                kwh = ''
                            
                            if pdf.pq('LTTextLineHorizontal:in_bbox("457.35, 373.93, 476.81, 383.93")').text() != '':
                                hmr_piu = pdf.pq('LTTextLineHorizontal:in_bbox("457.35, 373.93, 476.81, 383.93")').text() 
                            elif pdf.pq('LTTextLineHorizontal:in_bbox("457.35, 383.93, 476.81, 393.93")').text() != '':
                                hmr_piu = pdf.pq('LTTextLineHorizontal:in_bbox("457.35, 383.93, 476.81, 393.93")').text() 
                            else:
                                hmr_piu = ''
                            
                            if pdf.pq('LTTextLineHorizontal:in_bbox("457.35, 345.93, 476.81, 355.93")').text() != '':
                                kwh_piu = pdf.pq('LTTextLineHorizontal:in_bbox("457.35, 345.93, 476.81, 355.93")').text()
                            elif pdf.pq('LTTextLineHorizontal:in_bbox("451.79, 355.93, 482.37, 365.93")').text() != '':
                                kwh_piu = pdf.pq('LTTextLineHorizontal:in_bbox("451.79, 355.93, 482.37, 365.93")').text()
                            else:
                                kwh_piu = ''
                            
                            if pdf.pq('LTTextLineHorizontal:in_bbox("425.39, 331.93, 508.77, 341.93")').text() != '':
                                Deviation  = pdf.pq('LTTextLineHorizontal:in_bbox("425.39, 331.93, 508.77, 341.93")').text() 
                            elif pdf.pq('LTTextLineHorizontal:in_bbox("428.31, 341.93, 505.84, 351.93")').text() != '':
                                Deviation  = pdf.pq('LTTextLineHorizontal:in_bbox("428.31, 341.93, 505.84, 351.93")').text() 
                            elif pdf.pq('LTTextLineHorizontal:in_bbox("425.39, 341.93, 508.77, 351.93")').text() != '':
                                Deviation  = pdf.pq('LTTextLineHorizontal:in_bbox("425.39, 341.93, 508.77, 351.93")').text() 
                            else:
                                Deviation = ''                            
                                            

                            pdf_data_reg = EnergyDieelFilling(
                                file=pdf_file, File_id=file_id, Global_ID=SIteGlobalID, Circle=circle, Site_Name=site_name, Cluster=cluster,Region=region,User_Name=user_name
                                ,Assign_Date=assign_date, Status=status, Previous_Reading_Date_Time=previous_date_time, Current_Reading_Date_Time=current_date_time, Previous_EB_Cumulative_KWH_As_Per_EB_Meter=previou_EB_meter_reading
                                ,Current_EB_Cumulative_KWH_As_Per_EB_Meter=current_EB_meters_reading,Previous_EB_Running_Hours_Cumulative_Available_Not_Available=EB_Running_Hours_Cumulative_Available_Not_Available, Current_EB_Running_Hours_Cumulative_Available_Not_Available=EB_Running_Hours_Cumulative_Available_Not_Available
                                ,Previous_EB_Running_Hours_Cumulative_As_per_PIU_I2PMS_AMF=previou_EB_meters_PIU_reading, Current_EB_Running_Hours_Cumulative_As_per_PIU_I2PMS_AMF=current_EB_meters_PIU_reading
                                ,Previous_Type_of_DG_Static_Mobile=Previous_Type_of_DG_Static_Mobile, Current_Type_of_DG_Static_Mobile=Current_Type_of_DG_Static_Mobile, Previous_DG_Running_Hours_Reading_As_Per_HMR=previous_DG_running_reading, Current_DG_Running_Hours_Reading_As_Per_HMR=current_DG_running_reading
                                ,Previous_DG_Running_Hours_Reading_As_Per_PIU_I2PMS_AMF=previous_DG_running_piu_reading, Current_DG_Running_Hours_Reading_As_Per_PIU_I2PMS_AMF=current_DG_running_piu_reading
                                ,Previous_Opening_Diesel_stock_Before_Filling=Previous_Opening_Diesel_stock_Before_Filling, Current_Opening_Diesel_stock_Before_Filling=Current_Opening_Diesel_stock_Before_Filling
                                ,Previous_Filled_Ltrs=Previous_Filled_Ltrs, Current_Filled_Ltrs=Current_Filled_Ltrs, Previous_Diesel_Bill_Number=Previous_Diesel_Bill_Number, Current_Diesel_Bill_Number=Current_Diesel_Bill_Number
                                ,Previous_Remarks_If_any=Previous_Remarks, Current_Remarks_If_any=f'{Remarks1} {Remarks2}', No_of_days_since_previous_filling=No_of_days_since_previous_filling, Calculated_CPH_HMR=cph_hmr
                                ,Calculated_CPH_As_per_PIU_I2PMS_AMF=cph_piu, Calculated_DG_HR_HMR=hmr, Calculated_DG_HR_As_per_PIU_I2PMS_AMF=hmr_piu, Calculated_EB_KWH_As_per_Meter=kwh, Calculated_EB_HR_As_per_PIU_I2PMS_AMF=kwh_piu, Deviation=Deviation
                            )

                            messages.success(request, 'Your PDF file has been uploaded successfully.')

                            pdf_data_reg.save()

                            return redirect('diese_filling_fsr_transactions')                    
                    else:
                        messages.error(request, 'This Global ID / Site ID is not register in Site Static Data, Please register first & then upload file.')

                        return redirect('diese_filling_fsr_transactions')
                else:
                    messages.error(request, 'This PDF data is already registered.')

                    return redirect('diese_filling_fsr_transactions')
            else:
                    messages.error(request, 'Somethings went wrong, Please check the uploded file.')

                    return redirect('diese_filling_fsr_transactions')
        else:
            return redirect('auth')

        

#################### Previous Diesel Filling and Diesel Reading Data Upload form ####################
# class DieselFillingOrReadingViews(TemplateView):
#     def get(self, request):
#         if request.user.is_authenticated:
#             form = DieselFillingOrReadingForm()     
#             context = {'forms':form}
#             return render(request, 'app/forms/atcfillingform.html', context)
#         else:
#             return redirect('auth')
        
#     def post(self, request):
#         if request.user.is_authenticated:
#             form = DieselFillingOrReadingForm(data=request.POST, files=request.FILES)
#             if form.is_valid():
#                 global_id = form.cleaned_data['global_id']                
#                 tasks = form.cleaned_data['Tasks']                
#                 DG_Serial_Number = form.cleaned_data['DG_Serial_Number']

#                 glb_id = str(global_id)
#                 last_data_1 = EnergyFuel.objects.filter(global_id=glb_id).order_by('-id').first()

#                 DG_HMR_Status = form.cleaned_data['DG_HMR_Status']
#                 if DG_HMR_Status == 'Working':
#                     DG_HMR_Reading = form.cleaned_data['DG_HMR_Reading']                                                                                                                                                                                                                                                                                                                                                                                                
#                 else:
#                     DG_HMR_Reading = 0

#                 DG_PIU_Status = form.cleaned_data['DG_PIU_Status']
#                 if DG_PIU_Status == 'Working':
#                     Current_DG_PIU_Reading = form.cleaned_data['Current_DG_PIU_Reading']
#                 else:
#                     Current_DG_PIU_Reading = 0

#                 Diesel_Filling_Done = form.cleaned_data['Diesel_Filling_Done']
#                 Date_Of_Diesel_Filling = form.cleaned_data['Date_Of_Diesel_Filling']

#                 if form.cleaned_data['Diesel_Balance_Before_Filling'] == '':                
#                     Diesel_Balance_Before_Filling = 0
#                 else:
#                     Diesel_Balance_Before_Filling = form.cleaned_data['Diesel_Balance_Before_Filling']

#                 if form.cleaned_data['Fuel_Qty_Filled'] == '':
#                     Fuel_Qty_Filled = 0
#                 else:
#                     Fuel_Qty_Filled = form.cleaned_data['Fuel_Qty_Filled']     

#                 Current_Diesel_Balance = 0
#                 dbbf = 0
#                 fqf = 0
#                 dbbf = int(Diesel_Balance_Before_Filling)
#                 fqf = int(Fuel_Qty_Filled)
#                 Current_Diesel_Balance = dbbf + fqf
                
#                 EB_Meter_Status = form.cleaned_data['EB_Meter_Status']
#                 if EB_Meter_Status == 'Working':
#                     Current_EB_MTR_KWH = form.cleaned_data['Current_EB_MTR_KWH']
#                 else:
#                     Current_EB_MTR_KWH = 0

#                 EB_PIU_Meter_Status = form.cleaned_data['EB_PIU_Meter_Status']
#                 if EB_PIU_Meter_Status == 'Working':
#                     Current_EB_PIU_Reading = form.cleaned_data['Current_EB_PIU_Reading']
#                 else:
#                     Current_EB_PIU_Reading = 0
                
#                 if form.cleaned_data['Total_DC_Load'] == '':
#                     Total_DC_Load = 0
#                 else:
#                     Total_DC_Load = form.cleaned_data['Total_DC_Load']

#                 if form.cleaned_data['Total_EB_KWH_Reading_from_all_Channels'] == '':
#                     Total_EB_KWH_Reading_from_all_Channels = 0
#                 else:
#                     Total_EB_KWH_Reading_from_all_Channels = form.cleaned_data['Total_EB_KWH_Reading_from_all_Channels']
#                 Remarks = form.cleaned_data['Remarks']
#                 FT_ID = form.cleaned_data['FT_ID']
#                 FT_name = form.cleaned_data['FT_name']
#                 FT_mobile_no = form.cleaned_data['FT_mobile_no']
#                 Receipt_No = form.cleaned_data['Receipt_No']
#                 Card_Number = form.cleaned_data['Card_Number']
#                 Vehicle_Plate = form.cleaned_data['Vehicle_Plate']
#                 EB_Cumulative_KWH_Image = form.cleaned_data['EB_Cumulative_KWH_Image']
#                 EB_Running_Hours_Cumulative_Image = form.cleaned_data['EB_Running_Hours_Cumulative_Image']
#                 DG_Running_Hours_Reading_Image = form.cleaned_data['DG_Running_Hours_Reading_Image']
#                 DG_Running_Hours_as_per_piu_Reading_Image = form.cleaned_data['DG_Running_Hours_as_per_piu_Reading_Image']
#                 Diesel_Bill_Number_Image = form.cleaned_data['Diesel_Bill_Number_Image']
                
#                 if last_data_1 == None:
#                     # This is DG_Running_HRS:
#                     hr_dg_sum = 0
#                     # This is CPH as par hmr:
#                     cph_hmr_div = 0
#                     # This is CPH as par piu:
#                     cph_piu_div = 0
#                     # This is KWH:
#                     KWH_mtr = 0
#                     # This is CPH approved:
#                     approved_cph_data = 0
                    
#                 else:
#                     last_data = EnergyFuel.objects.filter(global_id=glb_id).order_by('-id').first()
#                     # This is DG_Running_HRS:
#                     HMR_read = int(last_data_1.DG_HMR_Reading)
#                     hmrread = int(DG_HMR_Reading)
#                     if hmrread < HMR_read:
#                         if DG_HMR_Status == 'Working':
#                             DG_HMR_Reading = form.cleaned_data['DG_HMR_Reading']
#                         else:
#                             DG_HMR_Reading = 0
#                     # This is DG hmr:
#                     DG_hr = int(DG_HMR_Reading)               
#                     dghr_int = int(last_data.DG_HMR_Reading)
#                     dg_hr = (DG_hr - dghr_int)
#                     dghr = str(dg_hr)
#                     hr_dg_sum = 0
#                     if dghr[:1] == '-':
#                         hr_dg_sum = dghr[1:]
#                     else:
#                         hr_dg_sum = dghr

#                     # This is CPH as par hmr:
#                     minus = 0
#                     lst_d_b = int(last_data.Fuel_Qty_Filled)
#                     current_d_b = int(last_data.Current_Diesel_Balance)
#                     minus = (current_d_b - lst_d_b)
#                     hmr = int(hr_dg_sum)
#                     diesel = int(minus)
#                     diesel_hmr_div = 0
#                     if hmr == 0 or diesel == 0:
#                         diesel_hmr_div = 0
#                     else:
#                         diesel_hmr_div = (diesel / hmr)   
#                     dieselhmrdiv = str(round(diesel_hmr_div, 1))  
#                     if dieselhmrdiv[:1] == '-':
#                         cph_hmr_div = dieselhmrdiv[1:]
#                     else:
#                         cph_hmr_div = dieselhmrdiv 
                    
#                     # This is CPH as par piu:
#                     DG_piu = int(Current_DG_PIU_Reading)               
#                     dgpiu_int = int(last_data.Current_DG_PIU_Reading)
#                     dg_piu = (DG_piu - dgpiu_int)
#                     dgpiu = str(dg_piu)
#                     hr_piu_sum = 0
#                     if dgpiu[:1] == '-':
#                         hr_piu_sum = dgpiu[1:]
#                     else:
#                         hr_piu_sum = dgpiu
#                     piu_minus = 0
#                     lst_d_b_piu = int(last_data.Fuel_Qty_Filled)
#                     current_d_b_piu = int(last_data.Current_Diesel_Balance)
#                     piu_minus = (current_d_b_piu - lst_d_b_piu)
#                     piu = int(hr_piu_sum)
#                     diesel_piu = int(piu_minus)
#                     diesel_piu_div = 0
#                     if piu == 0 or diesel_piu == 0:
#                         diesel_piu_div = 0
#                     else:
#                         diesel_piu_div = (diesel_piu / piu)   
#                     dieselpiudiv = str(round(diesel_piu_div, 1))  
#                     if dieselpiudiv[:1] == '-':
#                         cph_piu_div = dieselpiudiv[1:]
#                     else:
#                         cph_piu_div = dieselpiudiv 

#                     # This is KWH:
#                     min_KWH_mtr = 0
#                     lst_kwh_mtr = int(last_data.Current_EB_MTR_KWH)
#                     present_mtr = int(Current_EB_MTR_KWH)
#                     min_KWH_mtr = (present_mtr - lst_kwh_mtr)
#                     minKWHmtr = str(min_KWH_mtr)
#                     if minKWHmtr[:1] == '-':
#                         KWH_mtr = minKWHmtr[1:]
#                     else:
#                         KWH_mtr = minKWHmtr

#                     # This is CPH approve by CPH:
#                     last_cph_div = 0
#                     lastcph_data = SiteFixed.objects.filter(global_id=glb_id).order_by('-global_id').first()
#                     last_approve_cph = float(lastcph_data.last_month_approved_CPH)
#                     last_cph_div = (diesel_hmr_div - last_approve_cph)
#                     div_with_last_cph = 0
#                     if last_approve_cph == 0 or last_cph_div == 0:
#                         div_with_last_cph = 0
#                     else:
#                         div_with_last_cph = (last_cph_div / last_approve_cph)
#                     div_last_cph = str(round(div_with_last_cph, 1))
#                     if div_last_cph[:1] == '-':
#                         approved_cph_data = div_last_cph[1:]
#                     else:
#                         approved_cph_data = div_last_cph
            
#                 reg = EnergyFuel(global_id=global_id,DG_Serial_Number=DG_Serial_Number,DG_HMR_Status=DG_HMR_Status,
#                 DG_HMR_Reading=DG_HMR_Reading,DG_PIU_Status=DG_PIU_Status,Current_DG_PIU_Reading=Current_DG_PIU_Reading,Diesel_Filling_Done=Diesel_Filling_Done,
#                 Date_Of_Diesel_Filling=Date_Of_Diesel_Filling,Diesel_Balance_Before_Filling=Diesel_Balance_Before_Filling,
#                 Fuel_Qty_Filled=Fuel_Qty_Filled,Current_Diesel_Balance=Current_Diesel_Balance,EB_Meter_Status=EB_Meter_Status,
#                 Current_EB_MTR_KWH=Current_EB_MTR_KWH,EB_PIU_Meter_Status=EB_PIU_Meter_Status,Current_EB_PIU_Reading=Current_EB_PIU_Reading,
#                 Tasks=tasks,Total_DC_Load=Total_DC_Load,Total_EB_KWH_Reading_from_all_Channels=Total_EB_KWH_Reading_from_all_Channels,
#                 Remarks=Remarks,FT_ID=FT_ID,FT_name=FT_name,FT_mobile_no=FT_mobile_no,Receipt_No=Receipt_No,Card_Number=Card_Number,
#                 Vehicle_Plate=Vehicle_Plate,EB_Cumulative_KWH_Image=EB_Cumulative_KWH_Image,EB_Running_Hours_Cumulative_Image=EB_Running_Hours_Cumulative_Image,
#                 DG_Running_Hours_Reading_Image=DG_Running_Hours_Reading_Image,DG_Running_Hours_as_per_piu_Reading_Image=DG_Running_Hours_as_per_piu_Reading_Image,
#                 Diesel_Bill_Number_Image=Diesel_Bill_Number_Image, DG_Running_HRS=hr_dg_sum, CPH_CPH_Comparison_With_Last_CPH=approved_cph_data, 
#                 CPH_as_par_HMR=cph_hmr_div, CPH_as_par_PIU=cph_piu_div, EB_KWH=KWH_mtr)

#                 messages.success(request, 'Your data has been submitted successfully.')

#                 reg.save()

#                 return redirect('atcform')
#             else:
#                 messages.error(request, 'Somethings went wrong, Please enter correct details.')
                
#                 return redirect('atcform')
#         else:
#             return redirect('auth')


        
#################### New Diesel Filling and Diesel Reading Data Upload form ####################
class Energy_Transactions(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            form = DieselFillingOrReadingForm()     
            context = {'forms':form}
            return render(request, 'app/forms/diesel_filling_and_reading.html', context)
        else:
            return redirect('auth')
        
    def post(self, request):
        if request.user.is_authenticated:
            form = DieselFillingOrReadingForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                global_id = form.cleaned_data['global_id']                
                tasks = form.cleaned_data['Tasks']                

                glb_id = str(global_id)
                last_data_1 = EnergyFuel.objects.filter(global_id=glb_id).order_by('-id').first()

                DG_HMR_Reading = form.cleaned_data['DG_HMR_Reading'] 

                Current_DG_PIU_Reading = form.cleaned_data['Current_DG_PIU_Reading']

                Date_Of_Diesel_Filling = form.cleaned_data['Date_Of_Diesel_Filling']

                if form.cleaned_data['Diesel_Balance_Before_Filling'] == '':                
                    Diesel_Balance_Before_Filling = 0
                else:
                    Diesel_Balance_Before_Filling = form.cleaned_data['Diesel_Balance_Before_Filling']

                if form.cleaned_data['Fuel_Qty_Filled'] == '':
                    Fuel_Qty_Filled = 0
                else:
                    Fuel_Qty_Filled = form.cleaned_data['Fuel_Qty_Filled']     

                Current_Diesel_Balance = 0
                dbbf = 0
                fqf = 0
                dbbf = int(Diesel_Balance_Before_Filling)
                fqf = int(Fuel_Qty_Filled)
                Current_Diesel_Balance = dbbf + fqf
                
                EB_Meter_Status = form.cleaned_data['EB_Meter_Status']
                if EB_Meter_Status == 'Available':
                    Current_EB_MTR_KWH = form.cleaned_data['Current_EB_MTR_KWH']
                else:
                    Current_EB_MTR_KWH = 0

                Current_EB_PIU_Reading = form.cleaned_data['Current_EB_PIU_Reading']
                
                if form.cleaned_data['Total_DC_Load'] == '':
                    Total_DC_Load = 0
                else:
                    Total_DC_Load = form.cleaned_data['Total_DC_Load']

                if form.cleaned_data['Total_EB_KWH_Reading_from_all_Channels'] == '':
                    Total_EB_KWH_Reading_from_all_Channels = 0
                else:
                    Total_EB_KWH_Reading_from_all_Channels = form.cleaned_data['Total_EB_KWH_Reading_from_all_Channels']

                Receipt_No = form.cleaned_data['Receipt_No']
                EB_Cumulative_KWH_Image = form.cleaned_data['EB_Cumulative_KWH_Image']
                EB_Running_Hours_Cumulative_Image = form.cleaned_data['EB_Running_Hours_Cumulative_Image']
                DG_Running_Hours_Reading_Image = form.cleaned_data['DG_Running_Hours_Reading_Image']
                DG_Running_Hours_as_per_piu_Reading_Image = form.cleaned_data['DG_Running_Hours_as_per_piu_Reading_Image']
                Diesel_Bill_Number_Image = form.cleaned_data['Diesel_Bill_Number_Image']
                
                if last_data_1 == None:
                    # This is DG_Running_HRS:
                    hr_dg_sum = 0
                    # This is CPH as par hmr:
                    cph_hmr_div = 0
                    # This is CPH as par piu:
                    cph_piu_div = 0
                    # This is KWH:
                    KWH_mtr = 0
                    # This is CPH approved:
                    approved_cph_data = 0
                    
                else:
                    last_data = EnergyFuel.objects.filter(global_id=glb_id).order_by('-id').first()
                    # This is DG hmr:
                    DG_hr = int(DG_HMR_Reading)               
                    dghr_int = int(last_data.DG_HMR_Reading)
                    if DG_hr > dghr_int:
                        dg_hr = (DG_hr - dghr_int)
                        dghr = str(dg_hr)
                        hr_dg_sum = 0
                        if dghr[:1] == '-':
                            hr_dg_sum = dghr[1:]
                        else:
                            hr_dg_sum = dghr
                    else:
                        hr_dg_sum = 0

                    # This is CPH as par hmr:
                    minus = 0
                    lst_d_b = int(last_data.Fuel_Qty_Filled)
                    current_d_b = int(last_data.Current_Diesel_Balance)
                    minus = (current_d_b - lst_d_b)
                    hmr = int(hr_dg_sum)
                    diesel = int(minus)
                    diesel_hmr_div = 0
                    if hmr == 0 or diesel == 0:
                        diesel_hmr_div = 0
                    else:
                        diesel_hmr_div = (diesel / hmr)   
                    dieselhmrdiv = str(round(diesel_hmr_div, 1))  
                    if dieselhmrdiv[:1] == '-':
                        cph_hmr_div = dieselhmrdiv[1:]
                    else:
                        cph_hmr_div = dieselhmrdiv 
                    
                    # This is CPH as par piu:
                    DG_piu = int(Current_DG_PIU_Reading)               
                    dgpiu_int = int(last_data.Current_DG_PIU_Reading)
                    if DG_piu > dgpiu_int:
                        dg_piu = (DG_piu - dgpiu_int)
                        dgpiu = str(dg_piu)
                        hr_piu_sum = 0
                        if dgpiu[:1] == '-':
                            hr_piu_sum = dgpiu[1:]
                        else:
                            hr_piu_sum = dgpiu
                    else:
                        hr_piu_sum = 0
                    piu_minus = 0
                    lst_d_b_piu = int(last_data.Fuel_Qty_Filled)
                    current_d_b_piu = int(last_data.Current_Diesel_Balance)
                    piu_minus = (current_d_b_piu - lst_d_b_piu)
                    piu = int(hr_piu_sum)
                    diesel_piu = int(piu_minus)
                    diesel_piu_div = 0
                    if piu == 0 or diesel_piu == 0:
                        diesel_piu_div = 0
                    else:
                        diesel_piu_div = (diesel_piu / piu)   
                    dieselpiudiv = str(round(diesel_piu_div, 1))  
                    if dieselpiudiv[:1] == '-':
                        cph_piu_div = dieselpiudiv[1:]
                    else:
                        cph_piu_div = dieselpiudiv 

                    # This is KWH:
                    min_KWH_mtr = 0
                    lst_kwh_mtr = int(last_data.Current_EB_MTR_KWH)
                    present_mtr = int(Current_EB_MTR_KWH)
                    if present_mtr > lst_kwh_mtr:
                        min_KWH_mtr = (present_mtr - lst_kwh_mtr)
                        minKWHmtr = str(min_KWH_mtr)
                        if minKWHmtr[:1] == '-':
                            KWH_mtr = minKWHmtr[1:]
                        else:
                            KWH_mtr = minKWHmtr
                    else:
                        KWH_mtr = 0

                    # This is CPH approve by CPH:
                    last_cph_div = 0
                    lastcph_data = SiteFixed.objects.filter(global_id=glb_id).order_by('-global_id').first()
                    last_approve_cph = float(lastcph_data.last_month_approved_CPH)
                    last_cph_div = (diesel_hmr_div - last_approve_cph)
                    div_with_last_cph = 0
                    if last_approve_cph == 0 or last_cph_div == 0:
                        div_with_last_cph = 0
                    else:
                        div_with_last_cph = (last_cph_div / last_approve_cph)
                    div_last_cph = str(round(div_with_last_cph, 1))
                    if div_last_cph[:1] == '-':
                        approved_cph_data = div_last_cph[1:]
                    else:
                        approved_cph_data = div_last_cph
            
                reg = EnergyFuel(global_id=global_id,DG_HMR_Reading=DG_HMR_Reading,Current_DG_PIU_Reading=Current_DG_PIU_Reading,
                Date_Of_Diesel_Filling=Date_Of_Diesel_Filling,Diesel_Balance_Before_Filling=Diesel_Balance_Before_Filling,
                Fuel_Qty_Filled=Fuel_Qty_Filled,Current_Diesel_Balance=Current_Diesel_Balance,EB_Meter_Status=EB_Meter_Status,
                Current_EB_MTR_KWH=Current_EB_MTR_KWH,Current_EB_PIU_Reading=Current_EB_PIU_Reading,Tasks=tasks,Total_DC_Load=Total_DC_Load,
                Total_EB_KWH_Reading_from_all_Channels=Total_EB_KWH_Reading_from_all_Channels,Receipt_No=Receipt_No,EB_Cumulative_KWH_Image=EB_Cumulative_KWH_Image,
                EB_Running_Hours_Cumulative_Image=EB_Running_Hours_Cumulative_Image, DG_Running_Hours_Reading_Image=DG_Running_Hours_Reading_Image,
                DG_Running_Hours_as_per_piu_Reading_Image=DG_Running_Hours_as_per_piu_Reading_Image, Diesel_Bill_Number_Image=Diesel_Bill_Number_Image,
                DG_Running_HRS=hr_dg_sum, CPH_CPH_Comparison_With_Last_CPH=approved_cph_data, CPH_as_par_HMR=cph_hmr_div, CPH_as_par_PIU=cph_piu_div, EB_KWH=KWH_mtr)

                messages.success(request, 'Your data has been submitted successfully.')

                reg.save()

                return redirect('atcform')
            else:
                messages.error(request, 'Somethings went wrong, Please enter correct details.')
                
                return redirect('atcform')
        else:
            return redirect('auth')


#################### Fuel Draw Data Upload form ####################
class FuelDrawnViews(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            form = FuelDrawnFTForm()
            fuel_drawn = FuelDrawn.objects.all() 
            context = {'forms':form, 'fuel_drawn':fuel_drawn}
            return render(request, 'app/forms/atc_fuel_drawn.html', context)
        else:
            return redirect('auth')
        
    def post(self, request):
        if request.user.is_authenticated:
            form = FuelDrawnFTForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                FT_ID = form.cleaned_data['FT_ID']
                FT_name = form.cleaned_data['FT_name']
                FT_mobile_no = form.cleaned_data['FT_mobile_no']
                Cluster_Name = form.cleaned_data['Cluster_Name']
                Fuel_Drawn_Date = form.cleaned_data['Fuel_Drawn_Date']
                Card_No = form.cleaned_data['Card_No']
                City_Township_Fuel_Station = form.cleaned_data['City_Township_Fuel_Station']
                Customer = form.cleaned_data['Customer']
                Fuel_Station_Name = form.cleaned_data['Fuel_Station_Name']
                Diesel_Purchased_Qty = form.cleaned_data['Diesel_Purchased_Qty']
                Diesel_Per_Ltr_Cost_Rs = form.cleaned_data['Diesel_Per_Ltr_Cost_Rs']
                Total_Diesel_Cost_Rs = int(Diesel_Purchased_Qty) * int(Diesel_Per_Ltr_Cost_Rs)
                Receipt_No = form.cleaned_data['Receipt_No']
                Receipt_Image_Upload = form.cleaned_data['Receipt_Image_Upload']
                Vehicle_Plate = form.cleaned_data['Vehicle_Plate']
                Remarks = form.cleaned_data['Remarks']

                reg = FuelDrawn(FT_ID=FT_ID,FT_name=FT_name,FT_mobile_no=FT_mobile_no,Cluster_Name=Cluster_Name,
                Fuel_Drawn_Date=Fuel_Drawn_Date,Card_No=Card_No,City_Township_Fuel_Station=City_Township_Fuel_Station,Customer=Customer,
                Fuel_Station_Name=Fuel_Station_Name,Diesel_Purchased_Qty=Diesel_Purchased_Qty,Diesel_Per_Ltr_Cost_Rs=Diesel_Per_Ltr_Cost_Rs,
                Total_Diesel_Cost_Rs=Total_Diesel_Cost_Rs,Receipt_No=Receipt_No,Receipt_Image_Upload=Receipt_Image_Upload,
                Vehicle_Plate=Vehicle_Plate,Remarks=Remarks)

                messages.success(request, 'Your data has been submitted successfully.')

                reg.save()

                return redirect('fueldrawnform')
            else:
                messages.error(request, 'Somethings went wrong, Please enter correct details.')

                return redirect('fueldrawnform')
        else: 
            return redirect('auth')


#################### Pre Monsoon Check List Data Upload Form ####################
class PreMonsoonChecklist(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            forms = PMCL_Forms()
            context = {'forms':forms}
            return render(request, 'app/forms/pre_monsoon_checklist.html', context)
        else:
            return redirect('auth')
    
    def post(self, request):
        if request.user.is_authenticated:
            forms = PMCL_Forms(data=request.POST, files=request.FILES)
            if forms.is_valid():
                global_id = forms.cleaned_data['global_id']                
                Q1_Attach = request.FILES.getlist('Q1_Attach')                
                Q1_Status = forms.cleaned_data['Q1_Status']
                Q1_Material_Required = forms.cleaned_data['Q1_Material_Required']
                Q1_Remarks = forms.cleaned_data['Q1_Remarks']
                Q2_Attach = request.FILES.getlist('Q2_Attach')
                Q2_Status = forms.cleaned_data['Q2_Status']
                Q2_Material_Required = forms.cleaned_data['Q2_Material_Required']
                Q2_Remarks = forms.cleaned_data['Q2_Remarks']
                Q3_Attach = request.FILES.getlist('Q3_Attach')
                Q3_Status = forms.cleaned_data['Q3_Status']
                Q3_Material_Required = forms.cleaned_data['Q3_Material_Required']
                Q3_Remarks = forms.cleaned_data['Q3_Remarks']
                Q4_Attach = request.FILES.getlist('Q4_Attach')
                Q4_Status = forms.cleaned_data['Q4_Status']
                Q4_Material_Required = forms.cleaned_data['Q4_Material_Required']
                Q4_Remarks = forms.cleaned_data['Q4_Remarks']
                Q5_Attach = request.FILES.getlist('Q5_Attach')
                Q5_Status = forms.cleaned_data['Q5_Status']
                Q5_Material_Required = forms.cleaned_data['Q5_Material_Required']
                Q5_Remarks = forms.cleaned_data['Q5_Remarks']
                Q6_Attach = request.FILES.getlist('Q6_Attach')
                Q6_Status = forms.cleaned_data['Q6_Status']
                Q6_Material_Required = forms.cleaned_data['Q6_Material_Required']
                Q6_Remarks = forms.cleaned_data['Q6_Remarks']
                Q7_Attach = request.FILES.getlist('Q7_Attach')
                Q7_Status = forms.cleaned_data['Q7_Status']
                Q7_Material_Required = forms.cleaned_data['Q7_Material_Required']
                Q7_Remarks = forms.cleaned_data['Q7_Remarks']
                Q8_Attach = request.FILES.getlist('Q8_Attach')
                Q8_Status = forms.cleaned_data['Q8_Status']
                Q8_Material_Required = forms.cleaned_data['Q8_Material_Required']
                Q8_Remarks = forms.cleaned_data['Q8_Remarks']
                Q9_Attach = request.FILES.getlist('Q9_Attach')
                Q9_Status = forms.cleaned_data['Q9_Status']
                Q9_Material_Required = forms.cleaned_data['Q9_Material_Required']
                Q9_Remarks = forms.cleaned_data['Q9_Remarks']
                Q10_Attach = request.FILES.getlist('Q10_Attach')
                Q10_Status = forms.cleaned_data['Q10_Status']
                Q10_Material_Required = forms.cleaned_data['Q10_Material_Required']
                Q10_Remarks = forms.cleaned_data['Q10_Remarks']
                
                reg = PMCL.objects.create(user=request.user,global_id=global_id,Q1_Status=Q1_Status,Q1_Material_Required=Q1_Material_Required,Q1_Remarks=Q1_Remarks,
                    Q2_Status=Q2_Status,Q2_Material_Required=Q2_Material_Required,Q2_Remarks=Q2_Remarks,
                    Q3_Status=Q3_Status,Q3_Material_Required=Q3_Material_Required,Q3_Remarks=Q3_Remarks,Q4_Status=Q4_Status,
                    Q4_Material_Required=Q4_Material_Required,Q4_Remarks=Q4_Remarks,Q5_Status=Q5_Status,Q5_Material_Required=Q5_Material_Required,
                    Q5_Remarks=Q5_Remarks,Q6_Status=Q6_Status,Q6_Material_Required=Q6_Material_Required,Q6_Remarks=Q6_Remarks,
                    Q7_Status=Q7_Status,Q7_Material_Required=Q7_Material_Required,Q7_Remarks=Q7_Remarks,
                    Q8_Status=Q8_Status,Q8_Material_Required=Q8_Material_Required,Q8_Remarks=Q8_Remarks,Q9_Status=Q9_Status,
                    Q9_Material_Required=Q9_Material_Required,Q9_Remarks=Q9_Remarks,Q10_Status=Q10_Status,Q10_Material_Required=Q10_Material_Required,
                    Q10_Remarks=Q10_Remarks)
                
                for q1 in Q1_Attach:
                    q1_obj = PreMonsoonImages.objects.create(images=q1)
                    reg.Q1_Attach.add(q1_obj)

                for q2 in Q2_Attach:
                    q2_obj = PreMonsoonImages.objects.create(images=q2)
                    reg.Q2_Attach.add(q2_obj)

                for q3 in Q3_Attach:
                    q3_obj = PreMonsoonImages.objects.create(images=q3)
                    reg.Q3_Attach.add(q3_obj)

                for q4 in Q4_Attach:
                    q4_obj = PreMonsoonImages.objects.create(images=q4)
                    reg.Q4_Attach.add(q4_obj)

                for q5 in Q5_Attach:
                    q5_obj = PreMonsoonImages.objects.create(images=q5)
                    reg.Q5_Attach.add(q5_obj)

                for q6 in Q6_Attach:
                    q6_obj = PreMonsoonImages.objects.create(images=q6)
                    reg.Q6_Attach.add(q6_obj)

                for q7 in Q7_Attach:
                    q7_obj = PreMonsoonImages.objects.create(images=q7)
                    reg.Q7_Attach.add(q7_obj)

                for q8 in Q8_Attach:
                    q8_obj = PreMonsoonImages.objects.create(images=q8)
                    reg.Q8_Attach.add(q8_obj)

                for q9 in Q9_Attach:
                    q9_obj = PreMonsoonImages.objects.create(images=q9)
                    reg.Q9_Attach.add(q9_obj)

                for q10 in Q10_Attach:
                    q10_obj = PreMonsoonImages.objects.create(images=q10)
                    reg.Q10_Attach.add(q10_obj)

                messages.success(request, 'Your data has been submitted successfully.')
                
                return redirect('mon_check')
            
            else:
                messages.error(request, 'Somethings went wrong, Please enter correct details.')

                return redirect('mon_check')
        else:
            return redirect('auth')


#################### Pre Monsoon Data Report ####################
class PreMonsoonReport(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            pagination_monsoon_report = PMCL.objects.filter().order_by('-date')
            paginator = Paginator(pagination_monsoon_report, 50, orphans=1)
            page_number = request.GET.get('page')
            data_obj = paginator.get_page(page_number)
            context = {'monsoon_report':data_obj, 'all_monsoon_data':pagination_monsoon_report}
            return render(request, 'app/reports/pre_monsoon_checklist.html', context)
        else:
            return redirect('auth')


#################### Pre Monsoon Filter Report ####################
class PreMonsoonFilterReport(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            if request.GET.get('start_date') and request.GET.get('end_date'):
                start_date = request.GET.get('start_date')
                end_date = request.GET.get('end_date')
                pmcl_report = PMCL.objects.filter(date__range=(start_date, end_date)).order_by('date')
                return render(request, 'app/reports/pre_monsoon_checklist_filter.html', {'pmcl_report':pmcl_report})
            elif request.GET.get('start_date'):
                start_date = request.GET.get('start_date')
                pmcl_report = PMCL.objects.filter(date=start_date).order_by('date')
                return render(request, 'app/reports/pre_monsoon_checklist_filter.html', {'pmcl_report':pmcl_report})
            elif request.GET.get('end_date'):
                end_date = request.GET.get('end_date')
                pmcl_report = PMCL.objects.filter(date=end_date).order_by('date')
                return render(request, 'app/reports/pre_monsoon_checklist_filter.html', {'pmcl_report':pmcl_report})
            else:
                return HttpResponse('<h5>Getting some error, Please try again. Back to <a href="/reports/pre-monsoon-checklist-report/">reports</a></h5>')
        else:
            return redirect('auth')


#################### Document Repository Data Upload Form ####################
class DocumentsRepoFormViews(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            form = DocumentsRepositoryForm()
            context = {'forms':form}
            return render(request, 'app/Docs_repo/documents_repo_form.html', context)
        else:
            return redirect('auth')

    def post(self, request):
        if request.user.is_authenticated:
            forms = DocumentsRepositoryForm(data=request.POST, files=request.FILES)
            if not forms.is_valid():
                project_type = forms.cleaned_data['project_type']
                region = forms.cleaned_data['region']
                site_docs_id = forms.cleaned_data['site_docs_id']
                circles = forms.cleaned_data['circles']
                file_category = forms.cleaned_data['file_category']
                documents = request.FILES.getlist('documents')
                # Generate Document ID:
                cap_alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                small_alpha = 'abcdefghijklmnopqrstuvwxyz'
                num_ber = '1234567890'
                all_id = cap_alpha + small_alpha + num_ber
                unique_id = ''.join(random.sample(all_id, 5))
                current_date = date.today().strftime('%m/%d/%Y')
                docs_id = f'DOC-{unique_id}-{site_docs_id}-{current_date}'
                # Generate Document ID End
                reg = DocumentRepository.objects.create(user=request.user, document_id=docs_id, project_type=project_type,region=region,
                site_docs_id=site_docs_id, circles=circles,file_category=file_category)
                # Save Documents:
                for dox in documents:
                    # Split File Name and Extention: 
                    ext = dox.name.split('.')[-1]            
                    f_name = dox.name.split('.')[0]            
                    file_nm = f'{f_name}-{site_docs_id}.{ext}'
                    # Split File Name and Extention End        
                    docs = DocumentsOfRepository.objects.create(user=request.user, file_name=file_nm, files=dox)
                    reg.documents.add(docs)
                
                messages.success(request, 'Your data has been upload successfully.')

                return redirect('documentsrepository_form')
            else:
                messages.error(request, 'Something went wrong, Please try again later or Contact with IT team.')

                return redirect('documentsrepository_form')
        else:
            return redirect('auth')
        

#################### Document Page ####################
class DocumentRepoViwer(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.circle == 'All' or request.user.region == 'All':
                docs_counts = DocumentRepository.objects.filter(user=request.user)
                context = {'search':'Search For Documents', 'col':2, 'creates':docs_counts.count()}
                return render(request, 'app/Docs_repo/documents_repo_reports.html', context)
            elif request.user.circle == 'All' and request.user.region == 'All':
                docs_counts = DocumentRepository.objects.filter(user=request.user)
                context = {'search':'Search For Documents', 'col':2, 'creates':docs_counts.count()}
                return render(request, 'app/Docs_repo/documents_repo_reports.html', context)
            else:
                docs_counts = DocumentRepository.objects.filter(user=request.user)
                context = {'search':'Search For Documents', 'col':3, 'creates':docs_counts.count()}
                return render(request, 'app/Docs_repo/documents_repo_reports.html', context)
        else:
            return redirect('auth')


#################### Document Repository Filter Data Report ####################
class DocumentRepoViwerFilter(TemplateView):
    def get(self, request):          
        if not request.user.is_authenticated:
            if request.GET.get('login_user_dt') or request.GET.get('site_docs_id_dt') or request.GET.get('project_dt_types') or request.GET.get('regions_dt') or request.GET.get('circles_dt'):
                if request.GET.get('login_user_circle') == 'All':
                    data = DocumentRepository.objects.filter(project_type__icontains=request.GET.get('project_dt_types'),
                    site_docs_id__icontains=request.GET.get('site_docs_id_dt'), region__icontains=request.GET.get('regions_dt'), 
                    circles__icontains=request.GET.get('circles_dt'))
                    context = {'search':'', 'docs_data':data, 'total':data.count()}
                    return render(request, 'app/Docs_repo/documents_repo_reports.html', context)
                else:
                    data = DocumentRepository.objects.filter(user=request.GET.get('login_user_dt'), project_type__icontains=request.GET.get('project_dt_types'),
                    site_docs_id__icontains=request.GET.get('site_docs_id_dt'))
                    context = {'search':'', 'docs_data':data, 'total':data.count()} 
                    return render(request, 'app/Docs_repo/documents_repo_reports.html', context)
                
            elif request.GET.get('login_user_dt') or request.GET.get('site_docs_id_dt') or request.GET.get('project_dt_types') or request.GET.get('regions_dt') or request.GET.get('circles_dt'):
                if request.GET.get('login_user_circle') == 'All':
                    data = DocumentRepository.objects.filter(project_type__icontains=request.GET.get('project_dt_types'),
                    region__icontains=request.GET.get('regions_dt'),site_docs_id__icontains=request.GET.get('site_docs_id_dt'),
                    circles__icontains=request.GET.get('circles_dt'))
                    context = {'search':'', 'docs_data':data, 'total':data.count()} 
                    return render(request, 'app/Docs_repo/documents_repo_reports.html', context)
                else:
                    data = DocumentRepository.objects.filter(user=request.GET.get('login_user_dt'),project_type__icontains=request.GET.get('project_dt_types'),
                    region__icontains=request.GET.get('regions_dt'),site_docs_id__icontains=request.GET.get('site_docs_id_dt'),
                    circles__icontains=request.GET.get('circles_dt'))
                    context = {'search':'', 'docs_data':data, 'total':data.count()} 
                    return render(request, 'app/Docs_repo/documents_repo_reports.html', context)
            else:
                messages.error(request, 'Something went wrong, Please contact IT team.')
                return render(request, 'app/Docs_repo/documents_repo_reports.html')
        else:
            if request.GET.get('login_user_circle') == 'All':
                if request.GET.get('site_docs_id_dt') or request.GET.get('project_dt_types') or request.GET.get('regions_dt') or request.GET.get('circles_dt'):
                    data = DocumentRepository.objects.filter(project_type__icontains=request.GET.get('project_dt_types'),
                    region__icontains=request.GET.get('regions_dt'),site_docs_id__icontains=request.GET.get('site_docs_id_dt'),
                    circles__icontains=request.GET.get('circles_dt'))
                    filter_data = {'site_id':request.GET.get('site_docs_id_dt'), 'project_type':request.GET.get('project_dt_types'),
                    'region':request.GET.get('regions_dt'), 'circle':request.GET.get('circles_dt')}
                    docs_counts = DocumentRepository.objects.filter(user=request.user)
                    context = {'search':'', 'docs_data':data, 'total':data.count(), 'filter_data':filter_data, 'creates':docs_counts.count(), 'col':2} 
                    return render(request, 'app/Docs_repo/documents_repo_reports.html', context)                
                elif request.GET.get('site_docs_id_dt') == '' and request.GET.get('project_dt_types') == '' and request.GET.get('regions_dt') =='' and request.GET.get('circles_dt') == '':
                    messages.warning(request, 'Please enter or select field to search.')
                    docs_counts = DocumentRepository.objects.filter(user=request.user)
                    context = {'search':'Search For Documents', 'creates':docs_counts.count(), 'col':2}
                    return render(request, 'app/Docs_repo/documents_repo_reports.html', context)
            else:
                if request.GET.get('site_docs_id_dt') or request.GET.get('project_dt_types'):
                    data = DocumentRepository.objects.filter(user=request.GET.get('login_user_dt'), project_type__icontains=request.GET.get('project_dt_types'),
                    site_docs_id__icontains=request.GET.get('site_docs_id_dt'))
                    filter_data = {'site_id':request.GET.get('site_docs_id_dt'), 'project_type':request.GET.get('project_dt_types'),}
                    docs_counts = DocumentRepository.objects.filter(user=request.user)
                    context = {'search':'', 'docs_data':data, 'total':data.count(), 'filter_data':filter_data, 'creates':docs_counts.count(), 'col':3} 
                    return render(request, 'app/Docs_repo/documents_repo_reports.html', context)  
                elif request.GET.get('site_docs_id_dt') == '' and request.GET.get('project_dt_types') == '':
                    messages.warning(request, 'Please enter or select field to search.')
                    docs_counts = DocumentRepository.objects.filter(user=request.user)
                    context = {'search':'Search For Documents', 'creates':docs_counts.count(), 'col':3}
                    return render(request, 'app/Docs_repo/documents_repo_reports.html', context)  
   
                                    
  


#################### Document Repository Add & Update Data ####################
class DocumentsRepositoryAddandUpdate(TemplateView):
    def get(self, request, repo_id):
        if request.user.is_authenticated:
            instance = get_object_or_404(DocumentRepository, pk=repo_id)
            docs_data = DocumentRepository.objects.get(pk=repo_id)
            repo_data = DocumentRepository.objects.filter(pk=repo_id)
            form = DocumentsRepositoryForm(instance=docs_data)
            context = {'docs_data':repo_data, 'id_dt':docs_data.id, 'instance':instance,
                       'forms':form}
            return render(request, 'app/Docs_repo/documents_repo_updates.html', context)
        else:
            return redirect('auth')
        
    def post(self, request, repo_id):
        if request.user.is_authenticated:
            instance = get_object_or_404(DocumentRepository, pk=repo_id)
            if instance:
                instance.project_type = request.POST.get('project_type')
                instance.region = request.POST.get('region')
                instance.site_docs_id = request.POST.get('site_docs_id')
                instance.circles = request.POST.get('circles')
                instance.file_category = request.POST.get('file_category')
                instance.save()

                if 'documents_dt' in request.FILES:
                    for files in request.FILES.getlist('documents_dt'):
                        ext = files.name.split('.')[-1]            
                        f_name = files.name.split('.')[0]            
                        file_nm = f'{f_name}-{instance.site_docs_id}.{ext}' 
                        file_instance = DocumentsOfRepository.objects.create(user=request.user, file_name=file_nm, files=files)
                        instance.documents.add(file_instance)
                
                docs_data = DocumentRepository.objects.get(pk=repo_id)

                messages.success(request, 'The data has been updated successfully.')

                return redirect('documentsrepository_add_update', docs_data.pk)
            else:
                messages.error(request, 'Something went wrong, Please try again or contact with IT team.')
        else:
            return redirect('auth')


#################### Document Repository Remove Files ####################
class DeleteDocumentsFIlesRepo(TemplateView):
    def post(self, request, repo_id, docs_id):
        if request.user.is_authenticated:
            repo_instance = get_object_or_404(DocumentRepository, pk=repo_id)
            docs_instance = get_object_or_404(DocumentsOfRepository, pk=docs_id)
            repo_instance.documents.remove(docs_instance)
            if docs_instance.files or os.path.isfile(docs_instance.files.path):
                os.remove(docs_instance.files.path)
            return redirect('documentsrepository_add_update', repo_instance.id)
        else:
            return redirect('auth')
        

#################### Remove Document Repository and Files ####################
# class RemoveDocumentsRepoAndFiles(TemplateView):
#     def post(self, request, repo_id, docs_id):
#         if request.user.is_authenticated:
#             pass
#         else:
#             return redirect('auth')



#################### Project Tracking Form ####################
class ProjectTrackingForm(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            ASM_data = Users.objects.filter(role='ASM')
            projects_types = ProjectTypeModel.objects.all()
            customers_data = CustomerDataModel.objects.all()
            Technician_data = Users.objects.filter(role='Technician')
            site_id = SiteFixed.objects.all()        
            if request.user.role == 'Sales':
                projects_data = ProjectsMasterModel.objects.filter(user=request.user, pendings='Yes', completed='No')
                projects_data_completes_counts = ProjectsMasterModel.objects.filter(user=request.user, pendings='No', completed='Yes') 
                paginator = Paginator(projects_data, 20, orphans=1)
                page_num = request.GET.get('page')
                projects_dt = paginator.get_page(page_num)
                context = {'site_id':site_id, 'ASM_data':ASM_data, 'Technician_data':Technician_data, 'pendings_counts':projects_data.count(),
                'completes_counts':projects_data_completes_counts.count(),'projects_types':projects_types, 'customers_data':customers_data, 'projects_data':projects_dt}
                return render(request, 'app/Project_tracker/tracker_form.html', context)
            elif request.user.role == 'ASM':
                asm_name = f'{request.user.first_name} {request.user.last_name}'
                projects_data = ProjectsMasterModel.objects.filter(assigned_to_asm=asm_name, pendings='Yes', completed='No')
                projects_data_completes_counts = ProjectsMasterModel.objects.filter(assigned_to_asm=asm_name, pendings='No', completed='Yes')
                paginator = Paginator(projects_data, 20, orphans=1)
                page_num = request.GET.get('page')
                projects_dt = paginator.get_page(page_num) 
                context = {'site_id':site_id, 'ASM_data':ASM_data, 'Technician_data':Technician_data, 'pendings_counts':projects_data.count(),
                'completes_counts':projects_data_completes_counts.count(),'projects_types':projects_types, 'customers_data':customers_data, 'projects_data':projects_dt}
                return render(request, 'app/Project_tracker/tracker_form.html', context)
            elif request.user.role == 'Technician':
                technician_name = f'{request.user.first_name} {request.user.last_name}'
                projects_data = ProjectsMasterModel.objects.filter(assigned_to_technician=technician_name, pendings='Yes', completed='No')
                projects_data_completes_counts = ProjectsMasterModel.objects.filter(assigned_to_technician=technician_name, pendings='No', completed='Yes') 
                paginator = Paginator(projects_data, 20, orphans=1)
                page_num = request.GET.get('page')
                projects_dt = paginator.get_page(page_num) 
                context = {'site_id':site_id, 'ASM_data':ASM_data, 'Technician_data':Technician_data, 'pendings_counts':projects_data.count(),
                'completes_counts':projects_data_completes_counts.count(),'projects_types':projects_types, 'customers_data':customers_data, 'projects_data':projects_dt}
                return render(request, 'app/Project_tracker/tracker_form.html', context)
            else:
                projects_data = ProjectsMasterModel.objects.filter(pendings='Yes', completed='No')
                projects_data_completes_counts = ProjectsMasterModel.objects.filter(pendings='No', completed='Yes') 
                paginator = Paginator(projects_data, 20, orphans=1)
                page_num = request.GET.get('page')
                projects_dt = paginator.get_page(page_num)
                context = {'site_id':site_id, 'ASM_data':ASM_data, 'Technician_data':Technician_data, 'pendings_counts':projects_data.count(),
                'completes_counts':projects_data_completes_counts.count(),'projects_types':projects_types, 'customers_data':customers_data, 'projects_data':projects_dt}
                return render(request, 'app/Project_tracker/tracker_form.html', context)
        else:
            return redirect('auth')
        
    def post(self, request):
        if request.user.is_authenticated:
            customers = request.POST.get('customer_name_dt')
            project_type = request.POST.get('project_types_dt')
            site_id = request.POST.get('site_id_dt')
            site_name = request.POST.get('site_name_dt')
            customer_expected_date = request.POST.get('customer_expected_date_dt')
            assigned_asm_id = request.POST.get('assigned_asm_id_dt')
            sales_remarks = request.POST.get('sales_remarks_dt')
            project_discreption = request.POST.get('project_discreption_dt')
            project_status = "Not Started"
            reg = ProjectsMasterModel(user=request.user,site_id=site_id,site_name=site_name,customer=customers,project_type=project_type,
            customer_expected_target_date=customer_expected_date,assigned_to_asm=assigned_asm_id,sales_remark=sales_remarks,
            project_description=project_discreption,pendings='Yes',completed='No', project_status=project_status)
            messages.success(request, 'Your project has been created successfully.')
            reg.save()
            return redirect('projectTrackingform')
        else:
            return redirect('auth')
        

#################### Project Tracking Completed Page ####################
class ProjectTrackingComplete(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.role == 'Sales':
                projects_data = ProjectsMasterModel.objects.filter(user=request.user, pendings='Yes', completed='No')
                projects_data_completes_counts = ProjectsMasterModel.objects.filter(user=request.user, pendings='No', completed='Yes') 
                paginator = Paginator(projects_data_completes_counts, 20, orphans=1)
                page_num = request.GET.get('page')
                projects_dt = paginator.get_page(page_num)
                context = {'pendings_counts':projects_data.count(),'completes_counts':projects_data_completes_counts.count(),'projects_data':projects_dt}
                return render(request, 'app/Project_tracker/tracker_complete.html', context)
            elif request.user.role == 'ASM':
                asm_name = f'{request.user.first_name} {request.user.last_name}'
                projects_data = ProjectsMasterModel.objects.filter(assigned_to_asm=asm_name, pendings='Yes', completed='No')
                projects_data_completes_counts = ProjectsMasterModel.objects.filter(assigned_to_asm=asm_name, pendings='No', completed='Yes')
                paginator = Paginator(projects_data_completes_counts, 20, orphans=1)
                page_num = request.GET.get('page')
                projects_dt = paginator.get_page(page_num) 
                context = {'pendings_counts':projects_data.count(),'completes_counts':projects_data_completes_counts.count(),'projects_data':projects_dt}
                return render(request, 'app/Project_tracker/tracker_complete.html', context)
            elif request.user.role == 'Technician':
                technician_name = f'{request.user.first_name} {request.user.last_name}'
                projects_data = ProjectsMasterModel.objects.filter(assigned_to_technician=technician_name, pendings='Yes', completed='No')
                projects_data_completes_counts = ProjectsMasterModel.objects.filter(assigned_to_technician=technician_name, pendings='No', completed='Yes') 
                paginator = Paginator(projects_data_completes_counts, 20, orphans=1)
                page_num = request.GET.get('page')
                projects_dt = paginator.get_page(page_num) 
                context = {'pendings_counts':projects_data.count(),'completes_counts':projects_data_completes_counts.count(),'projects_data':projects_dt}
                return render(request, 'app/Project_tracker/tracker_complete.html', context)
            else:
                projects_data = ProjectsMasterModel.objects.filter(pendings='Yes', completed='No')
                projects_data_completes_counts = ProjectsMasterModel.objects.filter(pendings='No', completed='Yes') 
                paginator = Paginator(projects_data_completes_counts, 20, orphans=1)
                page_num = request.GET.get('page')
                projects_dt = paginator.get_page(page_num)
                context = {'pendings_counts':projects_data.count(),'completes_counts':projects_data_completes_counts.count(),'projects_data':projects_dt}
                return render(request, 'app/Project_tracker/tracker_complete.html', context)
        else:
            return redirect('auth')
        

class ProjectsDataUpdatesAdd(TemplateView):
    def get(self, request, pk):
        if request.user.is_authenticated:
            instance = get_object_or_404(ProjectsMasterModel, pk=pk)
            projects_data = ProjectsMasterModel.objects.get(pk=pk)
            ASM_data = Users.objects.filter(role='ASM')
            projects_types = ProjectTypeModel.objects.all()
            customers_data = CustomerDataModel.objects.all()
            Technician_data = Users.objects.filter(role='Technician')
            site_id = SiteFixed.objects.all() 
            context = {'projects_data':projects_data, 'instance':instance, 'projects_types':projects_types,'customers_data':customers_data,
            'Technician_data':Technician_data,'site_id':site_id, 'ASM_data':ASM_data}
            return render(request, 'app/Project_tracker/update_project.html', context)
        else:
            return redirect('auth')

    def post(self, request, pk):
        if request.user.is_authenticated:
            instance = get_object_or_404(ProjectsMasterModel, pk=pk)
            if request.POST.get('hidden_dt') == 'Sales_data':
                if request.POST.get('sales_customer_expected_date_dt') == '':
                    instance.customer = request.POST.get('sales_customer_name_dt')
                    instance.project_type = request.POST.get('sales_project_types_dt')
                    instance.site_id = request.POST.get('sales_site_id_dt')
                    instance.site_name = request.POST.get('sales_site_name_dt')
                    instance.customer_expected_target_date = None
                    instance.assigned_to_asm = request.POST.get('sales_assigned_to_asm_id_dt')
                    instance.sales_remark = request.POST.get('sales_remarks_dt')
                    instance.project_description = request.POST.get('sales_project_discreption_dt')
                    messages.success(request, 'Your data has been update successfully.')
                    instance.save()
                    return redirect('projectsdataupdatesadd', instance.pk)
                else:
                    instance.customer = request.POST.get('sales_customer_name_dt')
                    instance.project_type = request.POST.get('sales_project_types_dt')
                    instance.site_id = request.POST.get('sales_site_id_dt')
                    instance.site_name = request.POST.get('sales_site_name_dt')
                    instance.customer_expected_target_date = request.POST.get('sales_customer_expected_date_dt')
                    instance.assigned_to_asm = request.POST.get('sales_assigned_to_asm_id_dt')
                    instance.sales_remark = request.POST.get('sales_remarks_dt')
                    instance.project_description = request.POST.get('sales_project_discreption_dt')
                    messages.success(request, 'Your data has been update successfully.')
                    instance.save()
                    return redirect('projectsdataupdatesadd', instance.pk)
            elif request.POST.get('hidden_dt') == 'ASM_data':
                if request.POST.get('asm_technician_target_date_dt') == '':
                    instance.assigned_to_technician = request.POST.get('asm_Technician_name_dt') 
                    instance.technician_target_date = None
                    instance.asm_remarks = request.POST.get('asm_technician_remarks_dt')
                    messages.success(request, 'Your project is successfully assigned to technician.')
                    instance.save()
                    return redirect('projectTrackingform')
                else:
                    instance.assigned_to_technician = request.POST.get('asm_Technician_name_dt')
                    instance.technician_target_date = request.POST.get('asm_technician_target_date_dt')
                    instance.asm_remarks = request.POST.get('asm_technician_remarks_dt')
                    messages.success(request, 'Your project is successfully assigned to technician.')
                    instance.save()
                    return redirect('projectTrackingform')
            elif request.POST.get('hidden_dt') == 'technicians_data':
                if request.POST.get('technicians_project_status_dt') == 'Not Started' or request.POST.get('technicians_project_status_dt') == 'In Progress':
                    if request.POST.get('technicians_completed_date_dt') == '':
                        instance.project_status = request.POST.get('technicians_project_status_dt')
                        instance.completed_date = None
                        instance.technician_remarks = request.POST.get('technician_last_remarks_dt')
                        messages.success(request, 'Your work is updated successfully done.')
                        instance.save()
                        return redirect('projectTrackingform')
                    else:
                        instance.project_status = request.POST.get('technicians_project_status_dt')
                        instance.completed_date = request.POST.get('technicians_completed_date_dt')
                        instance.technician_remarks = request.POST.get('technician_last_remarks_dt')
                        messages.success(request, 'Your work is updated successfully done.')
                        instance.save()
                        return redirect('projectTrackingform')
                elif request.POST.get('technicians_project_status_dt') == 'Complete':
                    instance.project_status = request.POST.get('technicians_project_status_dt')
                    instance.completed_date = request.POST.get('technicians_completed_date_dt')
                    instance.technician_remarks = request.POST.get('technician_last_remarks_dt')
                    instance.pendings = 'No'
                    instance.completed = 'Yes'  
                    messages.success(request, 'Your work completion is successfully done.')
                    instance.save()
                    return redirect('projectTrackingform')              
            else:
                messages.error(request, 'Something went wrong, Please try again or contact with IT team.')
                return redirect('projectsdataupdatesadd', instance.pk)
        else:
            return redirect('auth')
    

#################### User Logout ####################
class LogOut(LogoutView):
    next_page = '/accounts/authentications/'

