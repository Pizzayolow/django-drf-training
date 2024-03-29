import json
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework import status, generics, mixins
from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from django.views.generic import TemplateView
from rest_framework.renderers import TemplateHTMLRenderer


class Index(TemplateView):
    template_name = 'base.html'



# --- WATCHLIST --- #
class WatchListAV(APIView):


    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            # Si les données sont valides, nous sauvegardons le film dans la base de données
            serializer.save()
            # Nous retournons une réponse contenant les données du film sérialisées
            return Response(serializer.data)
        else:
            # Si les données ne sont pas valides, nous retournons une réponse contenant les erreurs
            return Response(serializer.errors)
        
    
    
        
class WatchDetailAV(APIView):
    
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error': 'Not found!'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)
        
    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    
    # --- STREAMPLATFORMS --- #
    
class StreamPlatformAV(APIView):
         
    def get(self, request):
        streamplatforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(streamplatforms, many=True, context={'request': request})
        return Response(serializer.data)
         
    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    
class StreamPlatformDetailAV(APIView):
    
    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Not found!'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StreamPlatformSerializer(platform, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
        # --- REVIEW --- #
        
# La classe ReviewList hérite de ListAPIView qui est une vue générique qui fournit une méthode 'get' pour lire une liste d'instances de modèle
class ReviewList(generics.ListAPIView):
    # Nous définissons le serializer_class qui est la classe utilisée pour créer la réponse
    serializer_class = ReviewSerializer
    
    # Nous définissons la méthode get_queryset qui est appelée pour récupérer le queryset qui sera utilisé pour lister les objets
    # Dans ce cas, nous filtrons les objets Review par l'attribut 'watchlist' qui correspond à la clé primaire (pk) passée dans l'URL
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
    

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = WatchList.objects.get(pk=pk)
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=movie, review_user=review_user)
        
        if review_queryset.exists():
            raise ValidationError('You already create a review for this!')
        
        serializer.save(watchlist=movie, review_user=review_user)
    
    
    
    
# La classe ReviewList hérite de ListModelMixin, CreateModelMixin et GenericAPIView
# ListModelMixin fournit une méthode pour lister un queryset
# CreateModelMixin fournit une méthode pour créer de nouveaux objets
# GenericAPIView est la classe de base générique pour toutes les autres vues basées sur des classes dans le DRF
# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     # Nous définissons le queryset qui est un ensemble de tous les objets Review
#     queryset = Review.objects.all()
#     # Nous définissons le serializer_class qui est la classe utilisée pour créer la réponse
#     serializer_class = ReviewSerializer
    
#     # Nous définissons la méthode get qui est appelée lorsque une requête GET est faite sur cette vue
#     # Elle appelle la méthode list de ListModelMixin qui renvoie une liste de tous les objets Review
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     # Nous définissons la méthode post qui est appelée lorsque une requête POST est faite sur cette vue
#     # Elle appelle la méthode create de CreateModelMixin qui crée un nouvel objet Review
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
    
    
# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    
    
    
    
    
    
# # Définition de la vue pour obtenir la liste de tous les films
# @api_view(['GET', 'POST'])
# def movie_list(request):
    
#     if request.method == 'GET':
#         # Si la méthode de la requête est GET, nous récupérons tous les films de la base de données
#         movies = Movie.objects.all()
#         # Nous sérialisons ces films en format JSON
#         serializer = MovieSerializer(movies, many=True)
#         # Nous retournons une réponse contenant les films sérialisés
#         return Response(serializer.data)
    
#     if request.method == 'POST':
#         # Si la méthode de la requête est POST, nous créons un nouveau film
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             # Si les données sont valides, nous sauvegardons le film dans la base de données
#             serializer.save()
#             # Nous retournons une réponse contenant les données du film sérialisées
#             return Response(serializer.data)
#         else:
#             # Si les données ne sont pas valides, nous retournons une réponse contenant les erreurs
#             return Response(serializer.errors)

# # Définition de la vue pour obtenir les détails d'un film spécifique
# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request, pk):
#     # Si la méthode de la requête est GET
#     if request.method == 'GET':
#         try:
#             # Nous essayons de récupérer le film spécifique par son identifiant primaire (pk)
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             # Si le film n'existe pas, nous retournons une réponse avec une erreur
#             return Response({'Error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
#         # Nous sérialisons le film en format JSON
#         serializer = MovieSerializer(movie)
#         # Nous retournons une réponse contenant le film sérialisé
#         return Response(serializer.data)
    
#     # Si la méthode de la requête est PUT
#     if request.method == 'PUT':
#         # Nous récupérons le film spécifique par son identifiant primaire (pk)
#         movie = Movie.objects.get(pk=pk)
#         # Nous sérialisons les données de la requête avec l'instance du film
#         serializer = MovieSerializer(movie, data=request.data)
#         # Si les données sont valides
#         if serializer.is_valid():
#             # Nous sauvegardons les modifications dans la base de données
#             serializer.save()
#             # Nous retournons une réponse contenant les données du film sérialisées
#             return Response(serializer.data)
#         else:
#             # Si les données ne sont pas valides, nous retournons une réponse contenant les erreurs
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)