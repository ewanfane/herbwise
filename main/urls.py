from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('gardens/', views.gardens, name='gardens'), 
    path('gardens/<int:garden_id>/', views.garden_details, name='garden_detail_alt'),
    path('garden_details/<int:garden_id>/', views.garden_details, name='garden_details'),
    path('add_plant/<int:garden_id>/', views.add_plant, name='add_plant'),
    path('delete_record/<int:record_id>/', views.delete_record, name='delete_record'),
    path('api/receive/', views.receive_data, name='receive_data'),
    path('latest_record/<int:plant_id>/', views.latest_record, name='latest_record'),
    path('plant_dashboard/<int:plant_id>/', views.plant_dashboard, name='plant_dashboard'),
    path("plant_data/<int:plant_id>/", views.plant_data, name="plant_data"),
    path('create_garden/', views.create_garden, name='create_garden'),
    path('gardens/<int:garden_id>/rename/', views.rename_garden, name='rename_garden'),
    path('gardens/<int:garden_id>/delete/', views.delete_garden, name='delete_garden'),


]
 