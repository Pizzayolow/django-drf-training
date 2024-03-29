from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Review
        exclude = ('watchlist', )
        #fields = "__all__"

class WatchListSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = WatchList
        fields = "__all__"
        

class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)
    class Meta:
        model = StreamPlatform
        fields = "__all__"

# def name_length(value):
#     if len(value) < 2:
#         raise serializers.ValidationError('Name is too short')
#     return value

# # Définition de la classe MovieSerializer qui hérite de serializers.Serializer
# class MovieSerializer(serializers.Serializer):
#     # Définition des champs du modèle Movie
#     id = serializers.IntegerField(read_only=True)  # Un champ entier en lecture seule pour l'ID
#     name = serializers.CharField(validators=[name_length])  # Un champ de caractères pour le nom
#     description = serializers.CharField()  # Un champ de caractères pour la description
#     active = serializers.BooleanField()  # Un champ booléen pour l'état actif/inactif

#     # Définition de la méthode create qui crée une nouvelle instance de Movie
#     def create(self, validated_data):
#         # Création d'une nouvelle instance de Movie avec les données validées
#         return Movie.objects.create(**validated_data)
    
#     # Définition de la méthode update qui met à jour une instance existante de Movie
#     def update(self, instance, validated_data):
#         # Mise à jour du nom de l'instance avec les données validées, si elles existent
#         instance.name = validated_data.get('name', instance.name)
#         # Mise à jour de la description de l'instance avec les données validées, si elles existent
#         instance.description = validated_data.get('description', instance.description)
#         # Mise à jour de l'état actif/inactif de l'instance avec les données validées, si elles existent
#         instance.active = validated_data.get('active', instance.active)
#         # Sauvegarde de l'instance mise à jour
#         instance.save()
#         # Retour de l'instance mise à jour
#         return instance
    