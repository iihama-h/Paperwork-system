from django.urls import path
from.import views

app_name = 'client'
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
    path('delete/<int:pk>/', views.DeleteView.as_view(), name="delete"),
]
