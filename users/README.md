# InventoryNest API

## Project Overview

**InventoryNest** is a user authentication and profile management system. It allows users to register, log in, update their profiles, and delete their accounts. The backend is built using Django and Django Rest Framework (DRF), and it incorporates JWT (JSON Web Tokens) for secure user authentication. The API provides the following features:

- User Registration (Signup)
- User Login
- User Profile Management (Retrieve, Update)
- Account Deletion

The application is designed to interact with a PostgreSQL database and send email notifications to users during registration, login, and account deletion.

## Requirements

- Python 3.x
- Django 3.x+
- Django Rest Framework
- PostgreSQL
- django-environ (to manage environment variables)
- `django-rest-framework-simplejwt` for JWT authentication

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/aqibcs/InventoryNest.git
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up PostgreSQL database**:
   Ensure that you have PostgreSQL installed and set up the database with the configuration found in the `.env` file.

4. **Migrate the database**:
    ```bash
    python manage.py migrate
    ```

5. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

6. **Set up email**:
The email configuration is set up using `SMTP` via `youremail@gmail.com` for sending registration and account-related emails. Ensure that you have valid email credentials in the `.env` file.

<br>
<br>

# API Endpoints

Here are the available endpoints:

## 1. User Registration (Signup)

- **Endpoint**: `POST /signup/`
- **Description**: Registers a new user.

### Request Body:
```json
{
  "username": "user123",
  "first_name": "John",
  "last_name": "Doe",
  "email": "user123@example.com",
  "password1": "password123",
  "password2": "password123"
}
```

### Response:
```json
{
  "message": "User registered successfully.",
  "token": {
    "refresh": "jwt_refresh_token",
    "access": "jwt_access_token"
  }
}
```

---

## 2. User Login

- **Endpoint**: `POST /login/`
- **Description**: Logs a user into the system and returns a JWT token.

### Request Body:
```json
{
  "username": "user123",
  "password": "password123"
}
```

### Response:
```json
{
  "message": "User login successfully.",
  "token": {
    "refresh": "jwt_refresh_token",
    "access": "jwt_access_token"
  }
}
```

---

## 3. Get Profile

- **Endpoint**: `GET /profile/`
- **Description**: Retrieves the authenticated user's profile.
- **Request**: Requires authentication via JWT.

### Response:
```json
{
  "username": "user123",
  "first_name": "John",
  "last_name": "Doe",
  "email": "user123@example.com"
}
```

---

## 4. Update Profile

- **Endpoint**: `PATCH /profile/update/`
- **Description**: Updates the authenticated user's profile. Fields like `first_name`, `last_name`, and `email` can be updated.

### Request Body:
```json
{
  "first_name": "UpdatedFirstName"
}
```

### Response:
```json
{
  "message": "Profile updated successfully.",
  "data": {
    "username": "user123",
    "first_name": "UpdatedFirstName",
    "last_name": "Doe",
    "email": "user123@example.com"
  }
}
```

---

## 5. Delete Account

- **Endpoint**: `DELETE /delete-account/`
- **Description**: Deletes the authenticated user's account and sends a goodbye email.
- **Request**: Requires authentication via JWT.

### Response:
```json
{
  "message": "Your account has been deleted. We're sorry to see you go."
}
```


