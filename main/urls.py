from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('gardens/', views.gardens, name='gardens'),
    path('garden_details', views.garden_details, name='garden_details'),
    path('add_plant/', views.add_plant, name='add_plant'),
    path('delete_record/<int:record_id>/', views.delete_record, name='delete_record'),
    path('api/receive/', views.receive_data, name='receive_data'),
    path('latest_record/<int:plant_id>/', views.latest_record, name='latest_record'),
    path('plant_dashboard/<int:plant_id>/', views.plant_dashboard, name='plant_dashboard'),
    path("plant_data/<int:plant_id>/", views.plant_data, name="plant_data")

]
 