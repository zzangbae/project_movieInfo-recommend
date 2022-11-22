from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import MovieListSerializer, MovieSerializer
from .serializers import ActorListSerializer, ActorSerializer 
from .serializers import DirectorListSerializer, DirectorSerializer
from .serializers import ReviewListSerializer, ReviewSerializer
from .serializers import GenreListSerializer, GenreSerializer
from .models import Movie, Actor, Director, Review, Genre
# Create your views here.
# df repr(????, reqe):
#     pass
@api_view(['GET'])
def movie_list(request):
    movies = get_list_or_404(Movie)
    if request.method == 'GET':
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def movie_search(request, search_data):
    movies = get_list_or_404(Movie)
    if request.method == 'GET':
        res_movies = []
        for movie in movies:
            print(movie.title)
            if movie.title == search_data:
                res_movies.append(movie)
        if request.method == 'GET':
            serializer = MovieListSerializer(res_movies, many=True)
            return Response(serializer.data)
 
@api_view(['GET'])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

@api_view(['GET'])
def actor_list(request):
    actors = get_list_or_404(Actor)
    if request.method == 'GET':
        serializer = ActorListSerializer(actors, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def actor_detail(request, actor_pk):
    actor = get_object_or_404(Actor, pk=actor_pk)
    if request.method == 'GET':
        serializer = ActorSerializer(actor)
        return Response(serializer.data)

@api_view(['GET'])
def director_list(request):
    directors = get_list_or_404(Director)
    if request.method == 'GET':
        serializer = DirectorListSerializer(directors, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
def director_detail(request, director_pk):
    director = get_object_or_404(Director, pk=director_pk)
    if request.method == 'GET':
        serializer = DirectorSerializer(director)
        return Response(serializer.data)

@api_view(['GET'])
def genre_list(request):
    genre = get_list_or_404(Genre)
    if request.method == 'GET':
        serializer = GenreListSerializer(genre, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def gerne_detail(request, genre_pk):
    genre = get_object_or_404(Genre, pk=genre_pk)
    if request.method == 'GET':
        serializer = GenreSerializer(genre)
        return Response(serializer.data)

@api_view(['GET'])
def review_list(request):
    reviews = get_list_or_404(Review)
    if request.method == 'GET':
        serializer = ReviewListSerializer(reviews, many=True)
        return Response(serializer.data)
    
@api_view(['GET', 'PUT', 'DELETE'])
def review_detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        review.delete()
        delete_message = { 'delete': f'review {review_pk} is deleted'}
        return Response(delete_message, status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
##############여기까진 잘돌아간다.###########################################

@api_view(['POST'])
def create_review(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie=movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# ###########################################################################

@api_view(['POST'])
def director_like(request, director_pk):
    director = get_object_or_404(Director, pk=director_pk)
    if director.like_users.filter(pk=request.user.pk).exists():
        director.like_users.remove(request.user.pk)
        director_liked = False
    else:
        director.like_users.add(request.user.pk)
        director_liked = True
    context={
        'director_liked': director_liked,
        'director_like_count': director.like_users.count()
    } 
    return Response(context)
