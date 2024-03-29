// Définition du module
var app = angular.module('myApp', []);

// Définition du contrôleur
app.controller('MovieController', function($scope, $http) {
    $scope.movies = [];

    $http.get('/watch/list/')
        .then(function(response) {
            console.log(response.data)
            // Succès
            $scope.movies = response.data;
        }, function(error) {
            // Erreur
            console.error('Erreur lors de la récupération des données', error);
        });
});