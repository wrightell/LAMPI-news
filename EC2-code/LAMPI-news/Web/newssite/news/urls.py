from django.urls import path
from . import views

urlpatterns = [
    path('reading-list/', views.reading_list, name='reading_list'),
    path('delete/<int:pk>/', views.delete_news_item, name='delete_news_item'),
]
