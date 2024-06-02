from django.urls import path

from AnimeApp import views

urlpatterns = [
    path('', views.fetch_anime_data, name='anime_list'),
    path('anime/<int:pk>/', views.anime_detail, name='anime_detail'),
    path('recommendations/', views.recommendations, name='recommendations'),
    path('character/<int:character_id>/', views.character_detail, name='character_detail'),
    path('search', views.search_anime, name='search'),
    
]
