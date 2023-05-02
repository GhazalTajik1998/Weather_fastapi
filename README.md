# Weather api

`Weather api` is an api which gives you cities pollution and current weather by using OpenWeatherAPI.

<hr>

### How to run Locally?


To run the backend, you need to have local mongodb instance running on you can setup a deployed instance using [MongoDB Atlas](https://www.mongodb.com/atlas/database).

### Setting up python environment

Run the following to create a virtual environment for the project. (Assuming you have python installed on local machine)

```bash
python -m virtualenv env
# OR
python -m venv env
#OR
python -m venv --system-site-packages env
#OR
python3 -m venv env

```

If you're running the deployed instance, make sure to change the database connection string in `.env` file on the backend.

### Setting up `.env` file

To setup `.env` file on the backend, create a file named `.env` in `/backend/app`.
Add the following in the `.env` file.

```txt
JWT_SECRET_KEY=<RAMDOM_STRING>
JWT_REFRESH_SECRET_KEY=<RANDOM_SECTURE_LONG_STRING>
MONGO_CONNECTION_STRING=<MONGO_DB_CONNECTION_STRING>
# mongodb://localhost:27017/ <-- for local running instances
```

### Installing dependencies

Assuming you are in the base directory.

```bash
cd backend
pip install -r requirements.txt
```

### Activating virtual environment

```bash
# Windows
env/Scripts/activate

# MacOs + Linux
source env/bin/activate
```

### Running the backend

Assuming you are in the backend directory.

```bash
uvicorn app.app:app --reload
```

### Using Docker
First you need to create the image
```bash
docker build -t [YOUR-NAME-OF-IMAGE] .

```

then run the image 
```bash
docker run -p 8000:8000 [YOUR-NAME-OF-IMAGE]

```
