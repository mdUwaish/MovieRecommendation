from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import  APIView 

from .permissions import IsMovieOwnerOrReadOnly, IsReviewOwner
from .serializers import ActorSerializer, GenreSerializer, MovieSerializer, ReviewSerializer
from .models import Actor, Genre, Movie, Review

# Create your views here.
class CreateMovie(APIView):
    permission_classes=[IsAuthenticated, IsMovieOwnerOrReadOnly]

    def get(self, request, format=None):
        snippets = Movie.objects.all()
        serializer = MovieSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk, format=None):
        product = get_object_or_404(Movie, pk=pk)
        serializer = MovieSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product = get_object_or_404(Movie, pk=pk)
        product.delete()
        return Response({'message':"Movie Deleted."}, status=status.HTTP_204_NO_CONTENT)
    

class GenreListCreateView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenreDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk, format=None):
        genre = get_object_or_404(Genre, pk=pk)
        serializer = GenreSerializer(genre)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        genre = get_object_or_404(Genre, pk=pk)
        serializer = GenreSerializer(genre, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        genre = get_object_or_404(Genre, pk=pk)
        genre.delete()
        return Response({'message': "Genre Deleted."}, status=status.HTTP_204_NO_CONTENT)


class ActorDetails(APIView):
    permission_classes=[IsAuthenticated, IsMovieOwnerOrReadOnly]

    def get(self, request, format=None):
        snippets = Actor.objects.all()
        serializer = ActorSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ActorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk, format=None):
        product = get_object_or_404(Actor, pk=pk)
        serializer = ActorSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product = get_object_or_404(Actor, pk=pk)
        product.delete()
        return Response({'message':"Movie Deleted."}, status=status.HTTP_204_NO_CONTENT)


class ReviewCreate(APIView):
    permission_classes = [IsAuthenticated, IsReviewOwner]

    def get(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        reviews = Review.objects.filter(movie=movie)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(movie=movie, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)