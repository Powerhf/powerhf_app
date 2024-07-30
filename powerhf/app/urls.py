from django.urls import path
from app.views import *

urlpatterns = [
    # Dashboard:
    path('', Index, name='index'),

    # Reports:
    path('reports/hoto-report/', Reports_Hoto, name='hoto_report'),    
    path('reports/energy/drf/', DRFReport.as_view(), name='atc_site_report'),
    path('reports/energy/fuel-drawn/', FuelDrawnReport.as_view(), name='fuel_drawn'),
    path('reports/energy/energy-reading/', EnergyReadingReport.as_view(), name='diesel_filling'),

    path('reports/pm/', PM_Reports.as_view(), name='pm_report'),
    path('reports/cm/', CM_Reports.as_view(), name='cm_report'),
    path('reports/diesel-filling-fsr/', Diese_Filling_FSR_Reports.as_view(), name='diese_filling_fsr_report'),

    # Filtering Reports:
    path('reports/energy-dfr-filter/', EnergyDFRFilters.as_view(), name='energy_dfr_filter'),
    path('reports/energy-reading-filter/', EnergyReadingFilters.as_view(), name='energy_reading_filter'),
    path('reports/fuel-drawn-filter/', FuelDrawnFilters.as_view(), name='fuel_drawn_filter'),

    path('reports/pre-monsoon-checklist-report-filter/', PreMonsoonFilterReport.as_view(), name='mon_check_report_Filter'),

    # Forms:
    # path('forms/diesel-meter/filling-reading-fill-form/', DieselFillingOrReadingViews.as_view(), name='atcform'),
    path('transactions/fuel-drawn/', FuelDrawnViews.as_view(), name='fueldrawnform'),

    path('transactions/diesel-filling/', Energy_Transactions.as_view(), name='atcform'),

    # Transactions:
    path('transactions/pm/', PM_Transactions.as_view(), name='pm_trans'),
    path('transactions/cm/', CM_Transactions.as_view(), name='cm_trans'),
    # path('transactions/energy/', Energy_Transactions.as_view(), name='energy_trans'),
    path('transactions/diesel-filling-fsr/', Diesel_Filling_FSR_Transactions.as_view(), name='diese_filling_fsr_transactions'),

    path('transactions/pre-monsoon-checklist/', PreMonsoonChecklist.as_view(), name='mon_check'),

    path('reports/pre-monsoon-checklist-report/', PreMonsoonReport.as_view(), name='mon_check_report'),

    # Document Repository:
    path('document-repository/documents-repository-form/', DocumentsRepoFormViews.as_view(), name='documentsrepository_form'),
    path('document-repository/documents-repository-reports/', DocumentRepoViwer.as_view(), name='documentsrepository_reports'),
    path('document-repository/documents-repository-filter/', DocumentRepoViwerFilter.as_view(), name='documentsrepository_reports_filters'),
    path('documents-repository-add-update/<repo_id>/', DocumentsRepositoryAddandUpdate.as_view(), name='documentsrepository_add_update'),
    path('documents-repository-delete/<repo_id>/<docs_id>/', DeleteDocumentsFIlesRepo.as_view(), name='documentsrepository_delete'),
    # path('remove_all-documents-repository/<repo_id>/<docs_id>/', RemoveDocumentsRepoAndFiles.as_view(), name='Removealldocumentsrepository'),

    # Project Tracking:
    path('project-tracking/', ProjectTrackingForm.as_view(), name='projectTrackingform'),
    path('project-tracking/completed/', ProjectTrackingComplete.as_view(), name='projectTrackingcomplete'),
    path('project-tracking/sales-asm-technicians/<int:pk>/', ProjectsDataUpdatesAdd.as_view(), name='projectsdataupdatesadd'),

    
    # Logout:
    path('user/logout/', LogOut.as_view(), name='logout'),
]