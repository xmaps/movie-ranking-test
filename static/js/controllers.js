LoginController.$inject = ['$location', 'AuthenticationService'];
function LoginController($location, AuthenticationService) {
    var logger = this;

    logger.login = login;

    (function initController() {
        // reset login status
        AuthenticationService.clearCredentials();
    })();

    function login() {
        logger.dataLoading = true;
        AuthenticationService.login(logger.username, logger.password, function (response) {
            if (response.jwt) {
                AuthenticationService.setCredentials(response.jwt);
                $location.path('/');
            } else {
            	if (response.error.code == 403){
            		logger.error = response.error.message;
            	}else{
            		logger.error = 'Something went wrong with the request. Please try again later.';
            	}
                logger.dataLoading = false;
            }
        });
    };
}

UserController.$inject = ['$location', 'MeetApiService', 'AuthenticationService'];
function UserController($location, MeetApiService, AuthenticationService) {
    var user = this;
    
    user.name = '';
    user.username = '';
    user.email = '';
    user.joined_date = '';
    user.votedMovies = [];
    user.notVotesMovies = [];
    user.personal_info_error = '';
    user.newVotedMovies = null;
    user.vote_error = '';
    user.vote_success = '';
    user.dataLoading = false;
    
    user.moviesVote = moviesVote;
    user.logout = logout;
    
    initController();

    function initController() {
        loadCurrentUser();
    }

    function loadCurrentUser() {
    	MeetApiService.get('users', {})
    	.then(function(response) {
    		if (response.email){
    		    user.name = response.name;
    		    user.username = response.username;
    		    user.email = response.email;
    		    user.joined_date = response.joined_date;
    		    user.votedMovies = response.votes_movies;
    		    user.notVotesMovies = response.not_votes_movies;    			
    		}else{
    			user.personal_info_error = 'Something went wrong with the request. Please try again later.';
    		}
    	});
    }


    function moviesVote() {
	    	user.dataLoading = true;
	    	user.vote_error = '';
	    	user.vote_success = '';
	    	user.newVotedMovies = [];
			$('#voted_movies option').each(function(index) {
				user.newVotedMovies.push({"movie_identifier":this.value});
			});
	    	
			
			MeetApiService.post('moviesvote', {'voted_movies': user.newVotedMovies})
	    	.then(function(response) {
	    		user.vote_success = 'Voted successfully saved.';
	    	}, function(response) {
	    		user.vote_error = 'Something went wrong with the vote request. Please try again later.';
	    	});
	    	
	    	user.dataLoading = false; 
    }
    
    function logout(){
    	AuthenticationService.clearCredentials();
    	$location.path('/login');
    }
}

MovieListController.$inject = ['MeetApiService'];
function MovieListController(MeetApiService) {
    var moviesctrl = this;
    moviesctrl.movieslist = []
    moviesctrl.error = ''
    moviesctrl.get_movie_error = '';
    moviesctrl.has_movie_details = false;
    moviesctrl.getted_movie = {id:'', number_of_users_who_voted:'', title:'', year:'', users_who_voted:[]};
    
    moviesctrl.getMovie = getMovie;
    
    initController();

    function initController() {
        loadMoviesList();
    }

    function loadMoviesList() {
    	MeetApiService.get('movies', {})
    	.then(function(response) {
    		if (response.movies){
    			moviesctrl.movieslist = response.movies;			
    		}else{
    			moviesctrl.error = 'Something went wrong with the request. Please try again later.';
    		}
    	});
    }
    
    function getMovie(movie_identifier){
    	MeetApiService.get('movie/'+movie_identifier, {})
    	.then(function(response) {
    		if (response.id){
    			moviesctrl.getted_movie.id = response.id; 
    			moviesctrl.getted_movie.number_of_users_who_voted =  response.number_of_users_who_voted; 
    			moviesctrl.getted_movie.title =  response.title; 
    			moviesctrl.getted_movie.year =  response.year;
    			moviesctrl.getted_movie.users_who_voted = response.users_who_voted;
    			moviesctrl.has_movie_details = true;
    		}else{
    			moviesctrl.get_movie_error = 'Something went wrong with the request. Please try again later.';
    		}
    	});
    }

}
