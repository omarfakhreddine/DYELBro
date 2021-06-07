# CS_340_database_group_project
This repo is for our CS 340 portfolio database project using Flask/Python and MySQL.

The purpose of this web app is to enable users to interact with the exercise database using CRUD functionality.

TODO:
- implement update functionality (for other tables besides Exercises)
- implement delete functionality (for other tables besides Exercises)
- Filter/search functionality in exercises page for other entities besides exercise name
- drop down lists for insertion
- drop down lists for update (show row above form)
- fix search bar CSS/HTML on Training Types, Muscle Groups and Movement Types pages


Useful commands:

`mysql -u cs340_YOUROSUUSERNAME -pMYSQLPASSWORD -h classmysql.engr.oregonstate.edu`
# use the above code to access flip mysql servers
                                                    
`source ./venv/bin/activate`                          # activate virtual environment

`python -m flask run -h 0.0.0.0 -p PORT# --reload`    # run app with flask, change port

`gunicorn --bind 0.0.0.0:PORT# wsgi:app -D`           # run the app permanantly (gunicorn)

`ps ufx | grep gunicorn`                              # see gunicorn processes

`kill PROCESS#`                                       # kill top process after above com.
