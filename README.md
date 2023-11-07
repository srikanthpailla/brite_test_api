# Brite Test

Below are the requirements

## 1. Fetch test data via https from OMDB API

- You should fetch 100 movies from OMDB API. It's up to you what kind of movies you will get.

- Movies should be saved in the database.

- This method should be ran only once if database is empty.

 

## 2. Implement an api

- The api should have a method that returns a list of movies from the database

    - There should be option to set how many records are returned in single API response (by default 10)

    - There should be pagination implemented in the backend

    - Data should be ordered by Title

- The api should have a method that returns a single movie from the database

    - There should be option to get the movie by title

- The api should have a method to add a movie to the database

    - Title should be provided in request

    - All movie details should be fetched from OMDB API and saved in the database

- The api should have a method to remove a movie from the database

    - There should be option to remove movie with it's id

    - This method should be protected so only authorized user can perform this action


## 3. Unit tests for all cases


---


Follow below steps to run tests:

1. Create python virtual environment and activate it
2. Install all the required pip packages from requirememts.txt file
3. from the root of the repo, run `pytest test/`

For the application to be successfully loaded you need to export below Environment Variables.

- DB_HOST : SQL server IP
- DB_USER : user to login to database, default value is `britetest-user`
- DB_APASS : password to login to database
- DB_NAME : database name, default value is `britetest-database`
- DB_PORT : database port, default value is `3306`
- TABLE_NAME : table name, default value is `omdb_movie_info`
- OMDB_URL : OMDB api url, default value is `https://www.omdbapi.com/`
- OMDB_API_KEY : OMDB api key

On app startup DB will be populated with 100 movies, it gets the 100 movies info from OMDB by using the query
`https://www.omdbapi.com/?apikey=ed3b1c76&s=marvel&page=1`, since OMDB returns 10 results for each page, we query
10 times changing the page number.

On app startup there is a check to see if table is empty or not, if empty only then DB gets populated with data.

once app is started you can open the url which redirects you to Swagger UI, where you can see what all routes are there.
