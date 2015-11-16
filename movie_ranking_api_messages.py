#!/usr/bin/python
# -*- coding: utf-8 -*-
"""ProtoRPC message class definitions for Movie Ranking API."""


from protorpc import messages

class SimplerUserMessage(messages.Message):
    username = messages.StringField(2, required=True)

class MovieMessage(messages.Message):
    id = messages.IntegerField(1)
    title = messages.StringField(2, required=True)
    year = messages.IntegerField(3, required=True)
    number_of_users_who_voted = messages.IntegerField(4, default=0)
    users_who_voted = messages.MessageField(SimplerUserMessage, 5, repeated=True)

class ListMoviesMessage(messages.Message):
    movies = messages.MessageField(MovieMessage, 1, repeated=True)
    
class UserMessage(messages.Message):
    name = messages.StringField(1, required=True)
    username = messages.StringField(2, required=True)
    email = messages.StringField(3, required=True)
    joined_date = messages.StringField(4, required=True)
    votes_movies = messages.MessageField(MovieMessage, 5, repeated=True)
    not_votes_movies = messages.MessageField(MovieMessage, 6, repeated=True)
    
class MovieVoteMessage(messages.Message):
    title = messages.StringField(2, required=True)
    year = messages.IntegerField(3, required=True)
    
class UserVoteRequest(messages.Message):
    voted_movies = messages.MessageField(MovieVoteMessage, 1, repeated=True)

class LoginRequest(messages.Message):
    username = messages.StringField(1, required=True)
    password = messages.StringField(2, required=True)

class LoginResponse(messages.Message):
    jwt = messages.StringField(1, required=True)