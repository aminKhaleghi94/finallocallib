from rest_framework import serializers
from .models import Book,Author,BookInstance

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class AuthorSeializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookInstancesSeializer(serializers.ModelSerializer):
    class Meta:
        model = BookInstance
        fields = '__all__'
