#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Helper model class for Movie Ranking API.
Defines models for persisting and querying Users of the system and Present Movies
"""

import endpoints
from google.appengine.ext import ndb
from movie_ranking_api_messages import UserMessage, MovieMessage,\
    SimplerUserMessage

class RankingUser(ndb.Model):
    """Model to store the users of the system and is selected movies.
    For simplicity reasons currently the password's of the created users are stored in plain text.
    """
    name = ndb.StringProperty(required=True)
    username = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    joined_date = ndb.DateTimeProperty(auto_now_add=True)
    
    def to_message(self, votes_movies=[], not_votes_movies=[]):
        """Turns the RankingUser entity into a ProtoRPC object.
        This is necessary so the entity can be returned in an API request.
        Returns:
            An instance of UserMessage with all the details
            of the user, a list of his voted movies and a list of all movies he didn't vote 
        """
        return UserMessage(name=self.name,
                                    username=self.username,
                                    email=self.email,
                                    joined_date=self.joined_date.strftime("%Y-%m-%d %H:%M:%S"),
                                    votes_movies=votes_movies,
                                    not_votes_movies=not_votes_movies)
        
    def to_simpler_message(self):
        """Turns the RankingUser entity into a ProtoRPC object.
        This is necessary so the entity can be returned in an API request.
        Returns:
            An instance of UserMessage with all the details
            of the user, a list of his voted movies and a list of all movies he didn't vote 
        """
        return SimplerUserMessage(username=self.username)
    
class Movie(ndb.Model):
    """Model to store the movies present in the system.
    """    
    title = ndb.StringProperty(required=True)
    year = ndb.IntegerProperty(required=True)
    number_of_users_who_voted = ndb.IntegerProperty(required=True)

    def to_message(self, users_who_voted=[]):
        """Turns the Movie entity into a ProtoRPC object.
        This is necessary so the entity can be returned in an API request.
        Returns:
            An instance of MovieMessage with the ID of the Movie, the details of the movie,
            a calculation of the number of votes and a list of users who voted
        """
        return MovieMessage(id=self.key.id(),
                                    title=self.title,
                                    year=self.year,
                                    number_of_users_who_voted=self.number_of_users_who_voted,
                                    users_who_voted=users_who_voted)
    
class MovieRankingUser(ndb.Model):
    """
    Relation between movies and the users that vote on them
    """
    user = ndb.KeyProperty(kind=RankingUser)
    movie = ndb.KeyProperty(kind=Movie)
    
    @classmethod
    def query_get_user_voted_movies(cls, user):
        """Creates a query for the movies voted from a user.
        Returns:
            An ndb.Query object bound the user in question order by title
        """
        return cls.query(cls.user == user).order(cls.movie.title)
    
    @classmethod
    def query_get_users_who_voted_in_movie(cls, movie):
        """Creates a query for the users who voted in a film.
        Returns:
            An ndb.Query object bound the movie in question order by username.
        """
        return cls.query(cls.movie == movie).order(cls.user.username)
    


