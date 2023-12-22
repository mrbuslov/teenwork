from account.models import Account
from board.models import Board, Rubric, Image
from rest_framework import serializers

class RubricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubric
        fields = ["id","name"]
 
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image']

class OwnerSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ['email', 'phone_number', 'name', 'image']
    
    def get_name(self, obj: Account):
        return f'{obj.first_name.strip()} {obj.last_name.strip()}'

class BoardSerializer(serializers.ModelSerializer):
    rubric = serializers.SlugRelatedField('name', read_only=True) # RubricSerializer(read_only=True)
    age = serializers.SlugRelatedField('name', read_only=True) 
    currency = serializers.SlugRelatedField('currency', read_only=True) 
    image_set = ImageSerializer(many=True, read_only=True)
    is_added_to_favourites = serializers.SerializerMethodField()
    author = OwnerSerializer(read_only=True)

    class Meta:
        model = Board
        fields = ('id', 'title', 'slug', 'content', 'price', 'published', 'rubric', 'city', 
                  'age', 'currency', 'workers_amount', 'author_name', 'phone_number', 'email', 
                  'image_set', 'is_added_to_favourites', 'author')
    
    def get_is_added_to_favourites(self, obj):
        return True
