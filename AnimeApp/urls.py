from django.urls import path

from AnimeApp import views

urlpatterns = [
    path('', views.fetch_anime_data, name='anime_list'),
     path('anime/<int:mal_id>/', views.anime_detail, name='anime_detail'),
    path('character/<int:character_id>/', views.character_detail, name='character_detail'),
    path('search', views.search_anime, name='search'),
    path('upcoming',views.upcoming_anime, name='upcoming'),
    path('genre/<str:genre>/', views.fetch_anime_by_genre, name='anime_genre'),     
    path('year/<int:year>/', views.fetch_anime_by_year, name='anime_year'),   
    
]
