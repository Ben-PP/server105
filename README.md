# server105
Server for my home IoT ecosystem

## Dev
Install required packages. On Ubuntu you need the following:
- python 3.9 or higher
- libpq-dev
- packages in requirements.txt

Go to a `src`       folder and copy `.env.example` as `.env`. Fill all the fields.
- `jwt_secret=`     this is any super secret character sequence
- `jwt_algorithm=`  algorithm to use with jwt things
- `db_name=`        name of the database
- `db_username=`    username to use when connecting to database
- `db_psswd=`       password for the db user
- `db_host=`        where the db is hosted
- `db_port=`        port that the db uses

### Run
Run the dev server with `uvicorn main:app --reload`. FastAPI SwaggerUI is in http://127.0.0.1:8000/docs.