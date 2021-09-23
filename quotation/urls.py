from django.urls import path
from.import views

app_name = 'quotation'
urlpatterns = [
    path(
        'registration/',
        views.RegistrationView.as_view(),
        name="registration"),
    path('list/', views.ListView.as_view(), name="list"),
    path(
        'reference/<int:pk>/',
        views.ReferenceView.as_view(),
        name="reference"),
    path(
        'filedownload/<int:pk>/',
        views.file_download_view,
        name="filedownload"),
    path('filedelete/<int:pk>/', views.file_delete_view, name="filedelete"),
    path(
        'exceldownload/<int:pk>/',
        views.excel_download_view,
        name="exceldownload"),
    path('delete/<int:pk>/', views.DeleteView.as_view(), name="delete"),
]
