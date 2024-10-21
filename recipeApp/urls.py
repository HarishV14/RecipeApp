from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('recipes/', views.RecipeListView.as_view(), name='recipe_list'),
    path('recipes/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipes/create/', views.RecipeCreateView.as_view(), name='recipe-create'),
    path('recipes/<int:pk>/edit/',views.RecipeUpdateView.as_view(), name='recipe_edit'),
    path('recipes/<int:pk>/delete/', views.RecipeDeleteView.as_view(), name='recipe_delete'),
    path('collections/', views.RecipeCollectionListView.as_view(), name='collection_list'),
    path('collections/<int:pk>/', views.RecipeCollectionDetailView.as_view(), name='collection_detail'),
    path('collections/create/', views.RecipeCollectionCreateView.as_view(), name='collection_create'),
    path('collections/<int:pk>/edit/',views.RecipeCollectionUpdate.as_view(), name='collection_edit'),
    path('collections/<int:pk>/delete/', views.RecipeCollectionDeleteView.as_view(), name='collection_delete'),
]