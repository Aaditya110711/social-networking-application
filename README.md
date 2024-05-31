# [Social Networking Application](https://github.com/Aaditya110711/social-networking-application)

Simple starter built with Python / Django Rest / Sqlite3 and JWT Auth. The authentication flow is built with [json web tokens](https://jwt.io).

## Features:

- ✅ Django / DRF / SQLite3 - a simple, easy to use backend
- ✅ `JWT Authentication` (login, logout, register)
- ✅ Docker

## ✨ Quick Start in `Docker`

> 👉 Get the code

```bash
$ git clone https://github.com/Aaditya110711/social-networking-application.git
$ cd social-networking-application
```

> 👉 Start the app in Docker

```bash
$ docker-compose up --build
```

The API server will start using the PORT `8000`.

## ✨ How to use the code

> 👉 **Step #1** - Clone the sources

```bash
$ git https://github.com/Aaditya110711/social-networking-application.git
$ cd social-networking-application
```

<br />

> 👉 **Step #2** - Create a virtual environment

```bash
$ python3 -m venv venv
$ source venv/bin/activate
```

<br />

> 👉 **Step #3** - Install dependencies using PIP

```bash
$ pip install -r requirements.txt
```

<br />

> 👉 **Step #4** - Start the API server

```bash
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```

The API server will start using the default port `8000`.

## ✨ API

For a fast set up, use this POSTMAN file: [Api_sample](https://github.com/Aaditya110711/social-networking-application/blob/master/Social_Networking_Application.postman_collection.json)

> **Register** - `api/signup/`

```
POST api/signup/
Content-Type: application/json

{
    "name":"test",
    "email":"test@example.com",
    "password":"pass",
    "password2":"pass",
    "tc":true
}
```

<br />

> **Login** - `api/login/`

```
POST /api/login/
Content-Type: application/json

{
    "email":"test@appseed.us",
    "password":"pass"
}
```

<br />

> **Search** - `api/search/`

```
GET api/search/?q=John
Authorization: Bearer <token>
```

<br />

> **Send Friend Request** - `api/send-request/`

```
POST api/respond-request/
Content-Type: application/json
Authorization: Bearer <token>

{
    "friend_request_id": 1,
    "action": "accept"
}

```

<br />

> **List Friends** - `api/friends/`

```
GET api/friends/
Authorization: Bearer <token>
```

<br />

> **List Pending Friend Requests** - `api/pending-requests/`

```
GET api/pending-requests/
Authorization: Bearer <token>
```

<br />

> **Respond to Friend Request** - `api/respond-request/`

```
POST api/respond-request/
Authorization: Bearer <token>

{
    "friend_request_id": 4,
    "action": "accept"
}

```

## ✨ Authentication

Most endpoints require the user to be authenticated. Use the token obtained from the login endpoint to authenticate your requests by including it in the Authorization header as a Bearer token:

```
Authorization: Bearer <token>
```

## ✨ Rate Limiting

Sending friend requests is rate-limited to a maximum of 3 requests per minute. If this limit is exceeded, a 429 Too Many Requests status will be returned.

## ✨ Error Responses

Common error responses include:

- 400 Bad Request: Invalid input or request parameters.
- 401 Unauthorized: Missing or invalid authentication token.
- 403 Forbidden: Access to the requested resource is forbidden.
- 404 Not Found: Resource not found.
  <br />

---


