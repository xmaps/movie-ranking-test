# movie-ranking-test
Test using Google App Engine and Google Cloud Endpoints with Datastore. Personal Movie Ranking System.

*-* TODO *-*
Because time management reasons some simplifications here made:
1. The users password is stored in plain text;
2. The list of users is predefined so no "registration" functionality;
3. Delete of user votes as to suffer various changes:
3.1 Not deleting all user votes to add them again but see only the changes;
3.2 Change the way the movie voter count is changed because iterating the movies just to change the counter is not good.
4. Tests for in Angular functions


List of Pre-defined Users:
|Name | Username | Email | Password  | 
|John |	test1 | test1@mr.com | test1password |
|Mary |	test2 | test2@mr.com | test2password |
|Mario | test3 | test3@mr.com | test3password |
|Ben | test4 | email':'test4@mr.com | test4password |
|Johnson | test5 | test5@mr.com | test5password |
|Luis | test6 | test6@mr.com | test6password |
|Anne | test7 | test7@mr.com | test7password |
|Jane | test8 | test8@mr.com | test8password |
|Harper | test9 | test9@mr.com | test9password |
|Rui | test10 | test10@mr.com | test10password |
