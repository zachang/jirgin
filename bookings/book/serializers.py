from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    """A serializer for Book object"""

    flight = serializers.IntegerField(source='flight_id')
    id = serializers.IntegerField(read_only=True)
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Book
        fields = ('id', 'flight_class', 'flight', 'user')
        extra_kwargs = {
            'flight_class': {'required': True},
            'flight': {'required': True}
        }
