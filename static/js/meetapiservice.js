MeetApiService.$inject = ['$q','$http'];
function MeetApiService($q, $http) {
  var AppSettings = {};
  AppSettings.defaultApiVersion = 'v1';
  AppSettings.apiUrl = '/_ah/api';
  AppSettings.projectName = 'movieranking';
    
  var service = {};

  var createEndpointUrl = function(endpoint, version) {
      version = version || AppSettings.defaultApiVersion;
      endpoint = endpoint.replace('.', '/');
  return [
    AppSettings.apiUrl,
    AppSettings.projectName,
    version,
    endpoint
  ].join('/');
  };

  service.get = function(endpoint, args, version) {
    var deferred = $q.defer();

    $http({url: createEndpointUrl(endpoint, version), method: "GET", params: args}).success(function(data) {
        deferred.resolve(data);
    }).error(function(err, status) {
        deferred.reject(err, status);
    });

    return deferred.promise;
  };

  service.post = function(endpoint, args, version) {
    var deferred = $q.defer();

    $http.post(createEndpointUrl(endpoint, version), args).success(function(data) {
        deferred.resolve(data);
    }).error(function(err, status) {
        deferred.reject(err, status);
    });

    return deferred.promise;
  };

  return service;
}