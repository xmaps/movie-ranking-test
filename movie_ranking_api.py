#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Personal Movie Ranking API implemented using Google Cloud Endpoints."""

import endpoints
from protorpc import remote
from protorpc import message_types
from protorpc import messages
from movie_ranking_api_messages import LoginResponse, ListMoviesMessage,\
    MovieMessage, UserMessage, UserVoteRequest, LoginRequest
from models import RankingUser, Movie, MovieRankingUser
import jwt

JWT_SECRET_KEY = 'YOUR-SECRET-KEY'

@endpoints.api(name='movieranking', version='v1',
               description='Personal Movie Ranking API')
class MovieRankingApi(remote.Service):
    """Class which defines MovieRanking API v1.""" 

    @endpoints.method(LoginRequest, LoginResponse,
                      path='login', http_method='POST',
                      name='login.verify')
    def login_verify(self, request):
        """Exposes an API endpoint to verify if it is a valid user a returns a valid JWT to identify the user  
        Args:
            request: User Information -> Username and Password
        Returns:
            A JSON Web Token to identify the User
        """
        entity = RankingUser.query(RankingUser.username==request.username, RankingUser.password==request.password).get()
        if entity is not None:
            encoded_jwt = jwt.encode({'username': entity.username,'email':entity.email}, JWT_SECRET_KEY, algorithm='HS256')
        else:
            message = 'Not valid user credentials'
            raise endpoints.ForbiddenException(message)

        return LoginResponse(jwt=encoded_jwt)


    @endpoints.method(message_types.VoidMessage, ListMoviesMessage,
                      path='movies', http_method='GET',
                      name='movies.list')
    def movies_list(self, request):
        """Exposes an API endpoint to obtain the list of movies ordered by the most voted.
        Args:
            request: Void message request
        Returns:
            An Instance with a list of all the movies in the system ordered by the most voted
        """
        #get jwt and validates if user exists
        self.validateJWToken(self.request_state)
            
        list_of_movies = Movie.query().order(-Movie.number_of_users_who_voted, Movie.title).fetch()
        movies = [movie.to_message() for movie in list_of_movies]
        return ListMoviesMessage(movies=movies)

    ID_RESOURCE = endpoints.ResourceContainer(
      message_types.VoidMessage,
      id=messages.IntegerField(1, variant=messages.Variant.INT64))

    @endpoints.method(ID_RESOURCE, MovieMessage,
                        path='movie/{id}', http_method='GET',
                        name='movies.get')
    def movies_get(self, request):
        """Exposes an API endpoint to obtain the details of a Movie
        Args:
            request: Id of the movie
        Returns:
            An Instance containing the Movie Details
        """
        #get jwt and validates if user exists
        self.validateJWToken(self.request_state)
        
        selected_movie = Movie.get_by_id(request.id)
        if selected_movie is None:
            message = 'No movie with the id "%s" exists.' % request.id
            raise endpoints.NotFoundException(message)
        list_of_users_voted_movies_query = MovieRankingUser.query(MovieRankingUser.movie==selected_movie.key).fetch()
        list_of_users_voted = [RankingUser.query(RankingUser.key==user_movie_relation.user).get().to_simpler_message() for user_movie_relation in list_of_users_voted_movies_query]
        return selected_movie.to_message(users_who_voted=list_of_users_voted)
    
    @endpoints.method(message_types.VoidMessage, UserMessage,
                      path='users', http_method='GET',
                      name='users.get')
    def users_get(self, request):
        """Exposes an API endpoint to obtain the details of the User
        Args:
            request: Void message request, because the info comes from the JWT
        Returns:
            An Instance containing the User Details.
        """
        # Get the HTTP Authorization header.
        #get jwt and validates if user exists
        selected_user = self.validateJWToken(self.request_state)
        
        list_of_voted_movies_query = MovieRankingUser.query(MovieRankingUser.user==selected_user.key).fetch()
        list_of_voted_movies = []
        list_of_voted_movie_keys_to_exclude = []
        for user_movie_relation in list_of_voted_movies_query:
            current_movie = Movie.query(Movie.key==user_movie_relation.movie).get()
            list_of_voted_movies.append(current_movie.to_message())
            #puts the voted movie keys in a list to exclude
            list_of_voted_movie_keys_to_exclude.append(current_movie.key)
            
        #all movies in the system
        total_list_of_movies = Movie.query().order(Movie.title)
        #removes the voted movies from the total
        list_of_not_voted_movies_query = [res for res in total_list_of_movies.fetch() if res.key not in list_of_voted_movie_keys_to_exclude]
        #transforms the movies to messages
        list_of_not_voted_movies = [system_movie.to_message() for system_movie in list_of_not_voted_movies_query]
        return selected_user.to_message(votes_movies=list_of_voted_movies, not_votes_movies=list_of_not_voted_movies)
    
    @endpoints.method(UserVoteRequest, message_types.VoidMessage,
                      path='moviesvote', http_method='POST',
                      name='movies.vote')
    def movies_vote(self, request):
        """Exposes an API endpoint to insert the new votes from the user
        Args:
            request: A list of the movies the user currently likes and cast a vote.
        Returns:
            A void message if everthing goes well or an error.
        """
        #get jwt and validates if user exists
        selected_user = self.validateJWToken(self.request_state)
        
        list_of_voted_movies_query = MovieRankingUser.query(MovieRankingUser.user==selected_user.key).fetch()
        for user_movie_relation in list_of_voted_movies_query:
            current_movie = Movie.query(Movie.key==user_movie_relation.movie).get()
            current_counter = current_movie.number_of_users_who_voted
            current_movie.number_of_users_who_voted = current_counter - 1
            current_movie.put()
            user_movie_relation.key.delete()
            
        for voted_movie in request.voted_movies:
            current_movie = Movie.get_by_id(voted_movie.movie_identifier)
            current_counter = current_movie.number_of_users_who_voted
            current_movie.number_of_users_who_voted = current_counter + 1
            new_movie_user_vote = MovieRankingUser(user=selected_user.key,movie=current_movie.key)
            current_movie.put()
            new_movie_user_vote.put()
        return message_types.VoidMessage()
    
    @staticmethod
    def validateJWToken(request_state):
        # Get the HTTP Authorization header.
        auth_header = request_state.headers.get('authorization')
        if not auth_header:
            raise endpoints.UnauthorizedException("No authorization header.")

        # Get the encoded jwt token.
        auth_token = auth_header.split(' ').pop()

        # Decode and verify the token
        try:
            payload = jwt.decode(auth_token, JWT_SECRET_KEY, algorithms=['HS256'])
            # Do your own check here.
            entity = RankingUser.query(RankingUser.username==payload['username'], RankingUser.email==payload['email']).get()
            if entity is not None:
                return entity
            else:
                raise endpoints.UnauthorizedException("Invalid User Authentication.")
        except jwt.InvalidTokenError:
            raise endpoints.UnauthorizedException("Token validation failed.")
        
    
APPLICATION = endpoints.api_server([MovieRankingApi],
                                   restricted=False)