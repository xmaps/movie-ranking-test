#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Personal Movie Ranking API tests"""
import unittest
import webtest

BASE_URL= 'http://localhost:8080/'

class LoginTestCase(unittest.TestCase):
    
    def test_endpoint_login_ok(self):
        """Validates that login is valid and json web token is present in response message.""" 
        
        testapp = webtest.TestApp(BASE_URL)
        msg = {'username':'test1','password':'test1password'} 
        resp = testapp.post_json('/_ah/api/movieranking/v1/login', msg)
        json_response = resp.json
        
        #validates that login is valid and json web token is present in response message
        jwt_token_presence = True
        if 'jwt' not in json_response:
            jwt_token_presence = False
        self.assertEqual(jwt_token_presence, True)
        
        #verify's that jwt has the right format
        jwtoken = json_response['jwt']
        valid_jwt = True
        splited_jwt = jwtoken.split('.')
        if len(splited_jwt) != 3:
            valid_jwt = False
        self.assertEqual(valid_jwt, True)
        
    def test_endpoint_login_unauthorized(self):
        """Validates that login is not present in the system and returns 401 error code."""
        testapp = webtest.TestApp(BASE_URL)
        msg = {'username':'false_login','password':'false_password'} 
        resp = testapp.post_json('/_ah/api/movieranking/v1/login', msg, expect_errors=True)
        self.assertEqual(resp.status, '401 Unauthorized')
        
class MovieListTestCase(unittest.TestCase):
    
    def test_endpoint_get_movies_list(self):
        """Validates that the message returns a list of movies."""
        testapp = webtest.TestApp(BASE_URL)
        
        #first logins to get jwt
        msg = {'username':'test1','password':'test1password'} 
        resp = testapp.post_json('/_ah/api/movieranking/v1/login', msg)
        json_response = resp.json
        jwtoken = json_response['jwt']
        header_parms = {'Authorization':str('Bearer '+jwtoken)}
        movies_resp = testapp.get('/_ah/api/movieranking/v1/movies', headers=header_parms)
        
        #check for valid response format
        valid_response_format = False
        if 'movies' in movies_resp:
            movies_list = movies_resp.json['movies']
            movie = movies_list[0]              #get just the first movie
            if 'id' in movie and 'number_of_users_who_voted' in movie and 'title' in movie and 'year' in movie:
                valid_response_format = True
        self.assertEqual(valid_response_format, True)
        
        #Lets Check for some movies
        all_present_movies = True
        list_of_valid_movies = [movie for movie in movies_list if movie['title'] == 'V for Vendetta']
        if len(list_of_valid_movies) < 1:
            all_present_movies = False
        list_of_valid_movies = [movie for movie in movies_list if movie['year'] == '1986']
        if len(list_of_valid_movies) < 1:
            all_present_movies = False

        self.assertEqual(all_present_movies, True)
        
    def test_endpoint_validates_jwt(self):
        """Validates that the api requests the Json Web token and see's if is valid"""
        testapp = webtest.TestApp(BASE_URL)
        resp = testapp.get('/_ah/api/movieranking/v1/movies', expect_errors=True)
        self.assertEqual(resp.status, '401 Unauthorized')
        
        header_parms = {'Authorization':str('Bearer sadffewfdfsadf.asfdfasdfsdf.asdfasdfdsf')}
        movies_resp = testapp.get('/_ah/api/movieranking/v1/movies', headers=header_parms, expect_errors=True) 
        self.assertEqual(movies_resp.status, '401 Unauthorized')
        
class GetMoviesTestCase(unittest.TestCase):

    def test_endpoint_get_valid_movie(self):
        """Validates that the API returns a valid Movie with the right message format"""
        testapp = webtest.TestApp(BASE_URL)
        
        #first logins to get jwt
        msg = {'username':'test1','password':'test1password'} 
        resp = testapp.post_json('/_ah/api/movieranking/v1/login', msg)
        json_response = resp.json
        jwtoken = json_response['jwt']
        
        #gets list of movies to get one valid movie id
        header_parms = {'Authorization':str('Bearer '+jwtoken)}
        movies_resp = testapp.get('/_ah/api/movieranking/v1/movies', headers=header_parms)
        movies_list = movies_resp.json['movies']
        movie = movies_list[0]         #get just the first movie
        
        #now the test
        movie_resp = testapp.get('/_ah/api/movieranking/v1/movie/'+movie['id'], headers=header_parms)
        movie_response = movie_resp.json
        #check for valid response format
        valid_response_format = False
        if 'id' in movie_response and 'number_of_users_who_voted' in movie_response and 'title' in movie_response and 'year' in movie_response:
            valid_response_format = True
        self.assertEqual(valid_response_format, True)      
        
    def test_endpoint_put_invalid_movie_id(self):
        """Validates that the API returns a valid error message if the ID of the movie is not valid"""
        testapp = webtest.TestApp(BASE_URL)
        
        #first logins to get jwt
        msg = {'username':'test1','password':'test1password'} 
        resp = testapp.post_json('/_ah/api/movieranking/v1/login', msg)
        json_response = resp.json
        jwtoken = json_response['jwt']
        
        #now the test
        header_parms = {'Authorization':str('Bearer '+jwtoken)}
        movie_resp = testapp.get('/_ah/api/movieranking/v1/movie/2342342342', headers=header_parms, expect_errors=True)
        self.assertEqual(movie_resp.status, '404 Not Found')
        
        movie_resp = testapp.get('/_ah/api/movieranking/v1/movie/sadfsf234df', headers=header_parms, expect_errors=True)
        self.assertEqual(movie_resp.status, '400 Bad Request')  
    
    def test_endpoint_validates_jwt(self):
        """Validates that the api requests the Json Web token and see's if is valid"""
        testapp = webtest.TestApp(BASE_URL)
        resp = testapp.get('/_ah/api/movieranking/v1/movie/4504699138998272', expect_errors=True)
        self.assertEqual(resp.status, '401 Unauthorized')
        
        header_parms = {'Authorization':str('Bearer sadffewfdfsadf.asfdfasdfsdf.asdfasdfdsf')}
        movies_resp = testapp.get('/_ah/api/movieranking/v1/movie/4504699138998272', headers=header_parms, expect_errors=True) 
        self.assertEqual(movies_resp.status, '401 Unauthorized')
        
class GetUserTestCase(unittest.TestCase):
    
    def test_endpoint_gets_user_from_jwt(self):
        """Validates that the api requests the Json Web token and gets the current user from that token returning 
            the User information with a valid format and his the same user of Login."""
        testapp = webtest.TestApp(BASE_URL)
        #first logins to get jwt
        msg = {'username':'test1','password':'test1password'} 
        resp = testapp.post_json('/_ah/api/movieranking/v1/login', msg)
        json_response = resp.json
        jwtoken = json_response['jwt']
        
        #now the test
        header_parms = {'Authorization':str('Bearer '+jwtoken)}
        user_response = testapp.get('/_ah/api/movieranking/v1/users', headers=header_parms)
        user_info = user_response.json
        
        valid_user_info_format = False
        if 'name' in user_info and 'username' in user_info and 'email' in user_info\
         and 'joined_date' in user_info:
            valid_user_info_format = True
        self.assertEqual(valid_user_info_format, True)
        
        #checks to see if it is the same user of the login
        self.assertEqual(user_info['username'],'test1')
        self.assertEqual(user_info['email'], 'test1@mr.com')
        
        #if the user has voted movies check movie message format
        if 'votes_movies' in user_info:
            voted_movies = user_info['votes_movies']
            one_movie = voted_movies[0]
            #check for valid response format
            valid_response_format = False
            if 'id' in one_movie and 'number_of_users_who_voted' in one_movie and 'title' in one_movie and 'year' in one_movie:
                valid_response_format = True
            self.assertEqual(valid_response_format, True)   
            
    def test_endpoint_validates_jwt(self):
        """Validates that the api requests the Json Web token and see's if is valid"""
        testapp = webtest.TestApp(BASE_URL)
        resp = testapp.get('/_ah/api/movieranking/v1/users', expect_errors=True)
        self.assertEqual(resp.status, '401 Unauthorized')
        
        header_parms = {'Authorization':str('Bearer sadffewfdfsadf.asfdfasdfsdf.asdfasdfdsf')}
        movies_resp = testapp.get('/_ah/api/movieranking/v1/users', headers=header_parms, expect_errors=True) 
        self.assertEqual(movies_resp.status, '401 Unauthorized')       
            
class UserVoteTestCase(unittest.TestCase):
    
    def test_endpoint_user_vote(self):
        """Validates that the user casts a vote in his favorite movies and that the change is saved. """
        testapp = webtest.TestApp(BASE_URL)
        #first logins to get jwt
        msg = {'username':'test10','password':'test10password'} 
        resp = testapp.post_json('/_ah/api/movieranking/v1/login', msg)
        json_response = resp.json
        jwtoken = json_response['jwt']
        
        #now the test
        header_parms = {'Authorization':str('Bearer '+jwtoken)}
        #its necessary valid movie ids
        msg = {"voted_movies": [{"movie_identifier": "4504699138998272"},
                                {"movie_identifier":"4512395720392704"},
                                {"movie_identifier":"4573968371548160"},
                                {"movie_identifier":"4583863976198144"}]}
        vote_response = testapp.post_json('/_ah/api/movieranking/v1/moviesvote', msg, headers=header_parms)
        vote_res = vote_response.json
        #changes made with success
        self.assertEqual(vote_res['status_msg'], 'Vote casted with success.')
        
        #gets user info to check if vote has saved.
        user_response = testapp.get('/_ah/api/movieranking/v1/users', headers=header_parms)
        user_info = user_response.json
        
        #if the user has voted movies check movie message format
        voted_movies = user_info['votes_movies']
        movies_in_voted = True
        list_of_valid_movies = [movie for movie in voted_movies if movie['title'] == 'Star Wars']
        if len(list_of_valid_movies) < 1:
            movies_in_voted = False
        list_of_valid_movies = [movie for movie in voted_movies if movie['title'] == 'No Country for Old Men']
        if len(list_of_valid_movies) < 1:
            movies_in_voted = False
        list_of_valid_movies = [movie for movie in voted_movies if movie['title'] == 'Inception']
        if len(list_of_valid_movies) < 1:
            movies_in_voted = False
        list_of_valid_movies = [movie for movie in voted_movies if movie['title'] == 'The Grapes of Wrath']
        if len(list_of_valid_movies) < 1:
            movies_in_voted = False

        self.assertEqual(movies_in_voted, True)

        
        
if __name__ == '__main__':
    unittest.main()
