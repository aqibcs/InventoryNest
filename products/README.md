# InventoryNest - Product Management API

## Overview
**InventoryNest** is a product management application that allows users to manage products in their inventory. The app provides a RESTful API for users to create, read, update, and delete products, with full authentication and user-specific access.

This README provides an overview of the app, details on setting it up, and documentation for the API endpoints.

## Features
- **User Authentication**: Only authenticated users can manage their own products.
- **CRUD Operations**: Users can create, view, update, and delete products.
- **Search & Pagination**: The API supports searching by product name and pagination for listing products.
- **Ordering**: Products can be ordered by creation date or price.

## Requirements
- Python 3.x
- Django
- Django REST Framework
- PostgreSQL (or any other database of your choice)

## Apply Migrations:
```bash
python manage.py migrate
```

## Start the server
```bash
python manage.py runserver
```
The application will be running at `http://127.0.0.1:8000/`.

---
# API Endpoints
## 1. Create Product (POST request)
- **URL:** `/products/create/`
- **Request Body:**
```json
{
  "name": "Product Name",
  "description": "Product Description",
  "price": "19.99",
  "stock": 100
}
```

## 2. List Products (GET request)
-  **URL:** `products/`
- **Query Parameters:**
    -   `search`: (Optional) Search for products by name (e.g., `?search=product`).
    - `ordering`: (Optional) Specify the ordering of the products. Options are `created_at`, `-created_at`, `price`, `-price` (e.g., `?ordering=price`).

## 3. Retrieve single Product (GET request)
- **URL:** `/products/{id}/`

## 4. Update Product (PUT/PATCH request)
- **URL:** `/products/{id}/update/`
- **Request Body:**
```json
{
  "name": "Updated Product Name",
  "description": "Updated Description",
  "price": "25.00",
  "stock": 80
}
```

## Delete Product (DELETE request)
- **URL:** `/products/{id}/delete/`