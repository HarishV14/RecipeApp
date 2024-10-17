from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('recipes/', views.RecipeListView.as_view(), name='recipe_list'),
    path('recipes/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe_detail'),
    path('collections/', views.RecipeCollectionListView.as_view(), name='collection_list'),
    path('collections/<int:pk>/', views.RecipeCollectionDetailView.as_view(), name='collection_detail'),
]