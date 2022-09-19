# url_shortener
This is a small web app to help shorten a given url as well as return the original url using the generated short url.
There are 3 functions the system supports:
1. Shorten a valid url provided by user that is shorter than 355 characters
2. Given a valid short url, the system converts that into the original url
3. Provides a list of all original urls and their short urls

# Installation steps
1. Install python 3.9.x
2. Install Flask, mysqldb abd sqlalchamey using the following commands:
  - `pip3.9 install -U Flask`
  - `pip3.9 install flask-mysqldb`
  - `pip3.9 install flask-sqlalchemy`

3. To run the system, we need to create a database called `url_shortener` in the local database. For this, lets login to the local db using the following command:
`mysql -h 127.0.0.1 -u root`
4. This opens a mysql shell that shall help us create a database in local. Run the following command to create the database url_shortener
`create database url_shortener;`

5. Exit the shell and have the current path in your command line to the folder where the main `app.py` file in the project is present. Then run the following commands to help create the table needed for the application:
  - `export FLASK_APP=app`
  - `flask shell`
  - `python3.9 test.py`

6. This creates a table short_url in the db. You can verify this by checking the table in mysql. Let's login again and check if the table is created:
  - `mysql -h 127.0.0.1 -u root`
  - `use url_shortener;`
  - `show tables;`

7. This completes the setup. To run the command, please go to folder in your local and run the following command to start the server:
flask run
and then, in browser, go to `127.0.0.1:5000` to start using the application
