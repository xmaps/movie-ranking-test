# movie-ranking-test
First Test using Google App Engine and Google Cloud Endpoints with Datastore. Personal Movie Ranking System.

*-* TODO *-*
* Because time management reasons some simplifications here made:
** The users password is stored in plain text;
** The list of users is predefined so no "registration" functionality;
** The list of movies is predefined so no "add movies" functionality;
** Delete of user votes as to suffer various changes:
*** Not deleting all user votes to add them again but see only the changes;
*** Change the way the movie voter count is changed because iterating the movies just to change the counter is not good.
* Remove "SimplerUserMessage" and use only "UserMessage"
* Remove "MovieVoteMessage" and use only "MovieMessage"
* Function Documentation
* Tests for the API functions
* Tests for in Angular functions
* Better Sytling

* All this limited functionalities are to be added or changed in later versions.

List of Pre-defined Users:
* 'name':'John',	'username':'test1',		'email':'test1@mr.com',		'password':'test1password'
* 'name':'Mary',	'username':'test2',		'email':'test2@mr.com',		'password':'test2password'
* 'name':'Mario',	'username':'test3',		'email':'test3@mr.com',		'password':'test3password'
* 'name':'Ben',		'username':'test4',		'email':'test4@mr.com',		'password':'test4password'
* 'name':'Johnson',	'username':'test5',		'email':'test5@mr.com',		'password':'test5password'
* 'name':'Luis',	'username':'test6',		'email':'test6@mr.com',		'password':'test6password'
* 'name':'Anne',	'username':'test7',		'email':'test7@mr.com',		'password':'test7password'
* 'name':'Jane',	'username':'test8',		'email':'test8@mr.com',		'password':'test8password'
* 'name':'Harper',	'username':'test9',		'email':'test9@mr.com',		'password':'test9password'
* 'name':'Rui',		'username':'test10',	'email':'test10@mr.com',	'password':'test10password'
