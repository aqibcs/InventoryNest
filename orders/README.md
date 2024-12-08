# Orders App - **InventoryNest**

---

## **Key Features**

- **Order Management**: Create, retrieve, update, cancel, and delete orders.
- **Stock Management**: Automatically adjusts the stock of associated products when orders are created or canceled.
- **Notifications**: Sends email notifications to users and product owners regarding order status changes or cancellations.
- **Authenticated and Guest Orders**: Supports both registered users and guests by allowing guest email-based orders.

---

## **API Endpoints**

### **1. Create Order**
- **URL**: `/orders/create/`
- **Method**: `POST`
- **Description**: Allows authenticated users or guests to create an order.
- **Permissions**: `AllowAny`
- **Request Payload**:
    ```json
    {
        "product": 1,
        "quantity": 2,
        "guest_email": "guest@example.com"  // Optional for authenticated users
    }
    ```

### **2. List Orders**
- **URL**: `/orders/`
- **Method**: `GET`
- **Description**: Retrieves all orders.
- **Permissions**: `IsAuthenticated`

### **3. Get Order**
- **URL**: `/orders/<int:pk>/`
- **Method**: `GET`
- **Description**: Retrieves a specific order by its ID.
- **Permissions**: `IsAuthenticated`

### **4. Update Order**
- **URL**: `/orders/<int:order_id>/update/`
- **Method**: `PUT` or `PATCH`
- **Description**: Updates the details or status of an order.
- **Permissions**: `IsAuthenticated`
- **Request Payload**:
    ```json
    {
        "status": "processing"
    }
    ```

### **5. Cancel Order**
- **URL**: `/orders/<int:pk>/cancel/`
- **Method**: `POST`
- **Description**: Allows a user to cancel their own order.
- **Permissions**: `IsAuthenticated`

### **6. Delete Order**
- **URL**: `/orders/<int:pk>/delete/`
- **Method**: `DELETE`
- **Description**: Deletes an order and restores the product stock.
- **Permissions**: `IsAuthenticated`

---