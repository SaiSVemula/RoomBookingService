## Create conda environment

Create a conda environment for this project and activate the environment:

```console
$ conda create --name RoomBookingService python=3.11
$ conda activate RoomBookingService
```

## Django backend

The `backend` folder contains a [Django project]

```console
(RoomBookingService)$ django-admin startproject backend
```

### Install backend (Python) dependencies

With the conda environment active, install the backend (Python) dependencies:

```console
(RoomBookingService)$ cd backend
(RoomBookingService)$ pip install -r requirements.txt
```

### Start backend server

To start the backend server cd into the backend folder where the manage.py file is

```console
(RoomBookingService)$ cd backend
```

and run

```console
(RoomBookingService)$ python manage.py runserver
```

The server will start on http://localhost:8000

### API app

An "api" Django app has already been created with the command

```console
$ python manage.py startapp api
```

and can be tested by visiting http://localhost:8000/api/test.json

## Vue frontend

The `frontend` folder contains a [Vue/Vite project] and was created with:

```console
(RoomBookingService)$ npm create vite@latest
```

### Install frontend (JavaScript) dependencies

To install the frontend (JavaScript) dependencies cd into the frontend folder

```console
(RoomBookingService)$ cd frontend
```

and run:

```console
(RoomBookingService)$ npm install
```

The main frontend dependencies (see package.json) are [vue]

### Start frontend server

To start the frontend server run

```console
(RoomBookingService)$ npm run dev
```

and the server will start on http://localhost:5173
