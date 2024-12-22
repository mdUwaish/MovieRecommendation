from rest_framework import serializers
from .models import Actor, Genre, Movie, Review
from user_management.models import User


class GenreSerializer(serializers.ModelSerializer):
    full_path = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = ['id', 'name', 'parent', 'full_path']

    def get_full_path(self, obj):
        full_path = [obj.name]
        parent = obj.parent
        while parent is not None:
            full_path.append(parent.name)
            parent = parent.parent
        return ' > '.join(full_path[::-1])
    
    def create(self, validated_data):
        parent_data = validated_data.get('parent', None)
        if parent_data:
            parent = Genre.objects.get(id=parent_data.id)
            validated_data['parent'] = parent
        return super().create(validated_data)
    

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields= ['name', 'birth_date', 'biography']


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    actors = ActorSerializer(many=True)

    class Meta:
        model = Movie
        fields = ['title', 'description', 'release_date', 'rating', 'duration', 'genres', 'actors']


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['user', 'rating', 'comment', 'created_at']