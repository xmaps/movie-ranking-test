AuthenticationService.$inject = ['$http', '$cookieStore', '$rootScope', '$timeout', 'MeetApiService'];
function AuthenticationService($http, $cookieStore, $rootScope, $timeout, MeetApiService) {
    var service = {};

    service.login = login;
    service.setCredentials = setCredentials;
    service.clearCredentials = clearCredentials;

    return service;

    function login(username, password, callback) {

    	MeetApiService.post('login', {'username': username, 'password': password})
    	.then(function(response) {
    		callback(response);
    	}, function(response) {
    		callback(response);
    	});
    }

    function setCredentials(jwtoken) {
    	
        $rootScope.globals = {jwt: jwtoken};

        $http.defaults.headers.common['Authorization'] = 'Bearer ' + jwtoken; //Json Web Token Saving User Information
        $cookieStore.put('globals', $rootScope.globals);
    }

    function clearCredentials() {
        $rootScope.globals = {};
        $cookieStore.remove('globals');
        $http.defaults.headers.common.Authorization = 'Bearer';
    }
}