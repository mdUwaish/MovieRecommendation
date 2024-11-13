from django.urls import path
from .views import ActorDetails, CreateMovie, GenreDetailView, GenreListCreateView, MovieSearchView, ReviewCreate

urlpatterns = [
    path('create/', CreateMovie.as_view()),
    path('list/', CreateMovie.as_view()),
    path('update/<int:pk>/', CreateMovie.as_view()),
    path('delete/<int:pk>/', CreateMovie.as_view()),
    path('actor/create/', ActorDetails.as_view()),
    path('actor/list/', ActorDetails.as_view()),
    path('actor/update/<int:pk>/', ActorDetails.as_view()),
    path('actor/delete/<int:pk>/', ActorDetails.as_view()),
    path('review/<int:pk>/', ReviewCreate.as_view()),
    path('genres/', GenreListCreateView.as_view()),
    path('genres/<int:pk>/', GenreDetailView.as_view()),
    path('search/', MovieSearchView.as_view({'get': 'list'})),
]
