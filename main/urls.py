from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view, name='main'),
    path('add_item/', views.add_item, name='add_item'),
    path('add_box/', views.add_box, name='add_box'),
    path('delete_box/<int:box_id>/', views.delete_box, name='delete_box'),
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
]
