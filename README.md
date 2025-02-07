
# InventoryNest - REST API

## Overview

**InventoryNest** is a robust, scalable, and secure REST API built with **Django**. It provides essential backend services to manage user accounts, resources, and data for web and mobile applications. The API is designed to support CRUD operations, user authentication, filtering, and search functionalities while ensuring secure access and performance optimization.

---

## Key Features

- **User Authentication**: Secure sign-up, login, and token-based authentication (JWT).
- **Data Management**: Perform CRUD operations on resources like products, users, and orders.
- **Order Management**: Create, update, cancel, and delete orders with email notifications.
- **Search & Filtering**: Filter and search through resources based on specific criteria.
- **Pagination**: Efficient data retrieval with pagination for large datasets.
- **Admin Controls**: Role management, access control, and monitoring for administrators.

---

## Objectives

- **User Account Management**: Enable users to sign up, log in, and manage their profiles securely.
- **Resource CRUD Operations**: Allow users to create, read, update, and delete resources such as products or orders.
- **Order Management**: Handle order creation, status updates, cancellation, and deletion with stock validation and email notifications.
- **Search & Filter**: Empower users to find resources quickly using search and filter features.
- **Token-based Authentication**: Provide secure API access through JWT-based authentication.
- **Admin Role Management**: Admins can manage user roles and monitor API usage.
- **Shop and Cart Management**: Create, update, delete, and manage the cart.
---

## API Endpoints

### User Management
- **POST /signup**: Register a new user.
- **POST /login**: User login with email and password.
- **GET /profile**: Retrieve user profile details.
- **PATCH /profile**: Update user profile.

### Resource Management
- **POST /products/create/**: Create a new resource (e.g., product).
- **GET /products/**: List resources with optional filtering.
- **GET /products/<int:pk>/**: Retrieve a resource by ID.
- **PUT/PATCH /products/<int:pk>/update/**: Update a resource by ID.
- **DELETE /products/<int:pk>/delete/**: Delete a resource.

### Cart Management
- **POST /cart/add/**: Add a product to the cart.
- **GET /cart/**: View the current cart.
- **PUT/PATCH /cart/update/**: Update the cart with new quantities or products.
- **DELETE /cart/remove/**: Remove a product from the cart.

### Shop Management
- **POST /shop/**: Create a new shop profile.
- **GET /shop/profile/**: Retrieve shop profile details.
- **PUT/PATCH /shop/update/**: Update the shop profile.
- **DELETE /shop/delete/**: Delete the shop profile.

### Order Management
- **POST /orders/create**: Create a new order (authenticated or guest users).
- **GET /orders**: List all orders (authenticated users only).
- **GET /orders/{id}**: Retrieve order details by ID.
- **PUT/PATCH /orders/{id}/update**: Update the status of an order.
- **DELETE /orders/{id}/delete**: Delete an order.

### Admin Features
- **GET /admin/users**: List all users (admin access only).
- **PUT /admin/users/{id}**: Update user roles and permissions (admin access only).

---

## Security

- **HTTPS**: All communication is encrypted using HTTPS.
- **Token-based Authentication**: Secure API access using JWT.
- **Password Hashing**: Passwords are securely hashed.

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/aqibcs/InventoryNest.git
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** for database configuration, JWT secret key, and other settings.

4. **Migrate the database**:
   ```bash
   python manage.py migrate
   ```

5. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

---

## Glossary

- **API**: Application Programming Interface.
- **JWT**: JSON Web Token, used for authentication.
- **CRUD**: Create, Read, Update, Delete operations.
- **Django**: A high-level Python web framework used to build this API.

---
