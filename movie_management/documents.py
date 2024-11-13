from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Movie

@registry.register_document
class MovieDocument(Document):
    actors = fields.ObjectField(properties={
        'name': fields.TextField(),
    })
    genres = fields.ObjectField(properties={
        'name': fields.TextField(),
    })

    class Index:
        name = 'movie_index'

    class Django:
        model = Movie
        fields = [
            'title',
            'description',
            'release_date',
            'rating',
            'duration',
        ]
