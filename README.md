## Create conda environment

Create a conda environment for this project and activate the environment:

```console
create --name RoomBookingService python=3.11
activate RoomBookingService
```

## Django backend

### Install backend (Python) dependencies

With the conda environment active, install the backend (Python) dependencies:

```console
cd backend
pip install -r requirements.txt
```

### Start backend server

To start the backend server cd into the backend folder where the manage.py file is

```console
cd backend
```

and run

```console
python manage.py runserver
```

The server will start on http://localhost:8000

## Vue frontend

### Install frontend (JavaScript) dependencies

To install the frontend (JavaScript) dependencies cd into the frontend folder

```console
cd frontend
```

and run:

```console
npm install
```

The main frontend dependencies (see package.json) are [vue]

### Start frontend server

To start the frontend server run

```console
npm run dev
```

and the server will start on http://localhost:5173
