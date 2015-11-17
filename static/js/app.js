(function(){
	'use strict';

    var movieranking = angular.module('movieranking',['ngRoute', 'ngCookies']).config(config).run(run);
	movieranking.factory('AuthenticationService', AuthenticationService);
	movieranking.factory('MeetApiService', MeetApiService);
	movieranking.controller('LoginController', LoginController);
	movieranking.controller('UserController', UserController);
	movieranking.controller('MovieListController', MovieListController);
	
	config.$inject = ['$routeProvider', '$locationProvider'];
	function config($routeProvider, $locationProvider) {
	    $routeProvider
	        .when('/', {
	            controller: 'UserController',
	            templateUrl: 'templates/profile.view.html',
	            controllerAs: 'user'
	        })
	
	        .when('/login', {
	            controller: 'LoginController',
	            templateUrl: 'templates/login.view.html',
	            controllerAs: 'logger'
	        })
	
	        .when('/movieslist', {
	            controller: 'MovieListController',
	            templateUrl: 'templates/listmovies.view.html',
	            controllerAs: 'moviesctrl'
	        })
	
	        .otherwise({ redirectTo: '/login' });
	}

	run.$inject = ['$rootScope', '$location', '$cookieStore', '$http'];
	function run($rootScope, $location, $cookieStore, $http) {
	    // keep user logged in after page refresh
	    $rootScope.globals = $cookieStore.get('globals') || {};
	    if ($rootScope.globals.jwt) {
	        $http.defaults.headers.common['Authorization'] = 'Bearer '+$rootScope.globals.jwt; //Json Web Token Saving User Information
	    }
	
	    $rootScope.$on('$locationChangeStart', function (event, next, current) {
	        // redirect to login page if not logged in and trying to access a restricted page
	        var restrictedPage = $.inArray($location.path(), ['/login']) === -1;
	        var loggedIn = $rootScope.globals.jwt;
	        if (restrictedPage && !loggedIn) {
	            $location.path('/login');
	        }
	    });
	}
})();
