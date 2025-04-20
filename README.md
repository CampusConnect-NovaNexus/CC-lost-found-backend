# API Documentation for Lost and Found Backend

This documentation provides details about the available API endpoints, their required inputs, and expected responses for the Lost and Found application backend.

## Base URL

All API endpoints are prefixed with: `/api/v1`

## Authentication

Most endpoints require authentication via JWT token. Include the token in the Authorization header:
```
Authorization: Bearer <access_token>
```

## Health Check

### Check API Health
- **URL**: `/`
- **Method**: `GET`
- **Description**: Simple health check endpoint
- **Response**:
  ```json
  {
    "status": "healthy"
  }
  ```
- **Status Code**: 200

## User Management

### Register User
- **URL**: `/user/register`
- **Method**: `POST`
- **Description**: Create a new user account
- **Request Body**:
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string"
  }
  ```
- **Response**:
  ```json
  {
    "message": "User registered successfully",
    "user": {
      "id": "string",
      "username": "string",
      "email": "string"
    },
    "access_token": "string",
    "refresh_token": "string"
  }
  ```
- **Status Codes**:
  - 201: User created successfully
  - 400: Missing required fields
  - 409: Email already registered
  - 500: Server error

### Get All Users
- **URL**: `/user/`
- **Method**: `GET`
- **Description**: Retrieve a list of all users
- **Response**: Array of user objects
  ```json
  [
    {
      "id": "string",
      "username": "string",
      "email": "string"
    }
  ]
  ```
- **Status Codes**:
  - 200: Success
  - 500: Server error

### Get User by ID
- **URL**: `/user/<user_id>`
- **Method**: `GET`
- **Description**: Retrieve a specific user by ID
- **Response**:
  ```json
  {
    "id": "string",
    "username": "string",
    "email": "string"
  }
  ```
- **Status Codes**:
  - 200: Success
  - 404: User not found
  - 500: Server error

### Update User
- **URL**: `/user/update`
- **Method**: `POST`
- **Description**: Update user information
- **Request Body**:
  ```json
  {
    "_id": "string",
    "username": "string (optional)",
    "email": "string (optional)",
    "currentPassword": "string (optional)",
    "newPassword": "string (optional)"
  }
  ```
- **Response**:
  ```json
  {
    "message": "User updated successfully",
    "user": {
      "id": "string",
      "username": "string",
      "email": "string"
    }
  }
  ```
- **Status Codes**:
  - 200: User updated successfully
  - 404: User not found
  - 500: Server error

### Delete User
- **URL**: `/user/delete`
- **Method**: `POST`
- **Description**: Delete a user account
- **Request Body**:
  ```json
  {
    "_id": "string"
  }
  ```
- **Response**:
  ```json
  {
    "message": "User deleted successfully"
  }
  ```
- **Status Codes**:
  - 200: User deleted successfully
  - 404: User not found
  - 500: Server error

## Authentication

### Login
- **URL**: `/auth/login`
- **Method**: `POST`
- **Description**: Authenticate a user and get access tokens
- **Request Body**:
  ```json
  {
    "email": "string",
    "password": "string"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Login successful",
    "access_token": "string",
    "refresh_token": "string",
    "user": {
      "id": "string",
      "username": "string",
      "email": "string"
    }
  }
  ```
- **Status Codes**:
  - 200: Login successful
  - 400: Missing email or password
  - 401: Invalid email or password
  - 500: Server error

## Item Management

### Get All Items
- **URL**: `/item/`
- **Method**: `GET`
- **Description**: Retrieve a list of all items
- **Response**: Array of item objects
  ```json
  [
    {
      "id": "string",
      "item_title": "string",
      "item_description": "string",
      "item_image": "string"
    }
  ]
  ```
- **Status Codes**:
  - 200: Success
  - 500: Server error

### Get Item by ID
- **URL**: `/item/<item_id>`
- **Method**: `GET`
- **Description**: Retrieve a specific item by ID
- **Response**:
  ```json
  {
    "id": "string",
    "item_title": "string",
    "item_description": "string",
    "item_image": "string"
  }
  ```
- **Status Codes**:
  - 200: Success
  - 404: Item not found
  - 500: Server error

### Get Multiple Items
- **URL**: `/item/getItems`
- **Method**: `POST`
- **Description**: Retrieve multiple items by their IDs
- **Request Body**:
  ```json
  {
    "item_ids": ["string", "string", ...]
  }
  ```
- **Response**: Array of item objects
  ```json
  [
    {
      "id": "string",
      "item_title": "string",
      "item_description": "string",
      "item_image": "string"
    }
  ]
  ```
- **Status Codes**:
  - 200: Success
  - 400: No item IDs provided
  - 404: Items not found
  - 500: Server error

### Create Item
- **URL**: `/item/create`
- **Method**: `POST`
- **Description**: Create a new item
- **Request Body**:
  ```json
  {
    "title": "string",
    "description": "string",
    "image": "string (optional)"
  }
  ```
- **Response**:
  ```json
  {
    "status": "Item created successfully",
    "item_id": "string"
  }
  ```
- **Status Codes**:
  - 201: Item created successfully
  - 500: Server error

### Update Item
- **URL**: `/item/update`
- **Method**: `POST`
- **Description**: Update an existing item
- **Request Body**:
  ```json
  {
    "_id": "string",
    "title": "string (optional)",
    "description": "string (optional)",
    "image": "string (optional)"
  }
  ```
- **Response**:
  ```json
  {
    "status": "Item updated successfully"
  }
  ```
- **Status Codes**:
  - 200: Item updated successfully
  - 404: Item not found
  - 500: Server error

### Delete Item
- **URL**: `/item/delete`
- **Method**: `POST`
- **Description**: Delete an item
- **Request Body**:
  ```json
  {
    "_id": "string"
  }
  ```
- **Response**:
  ```json
  {
    "status": "Item deleted successfully"
  }
  ```
- **Status Codes**:
  - 200: Item deleted successfully
  - 404: Item not found
  - 500: Server error

## AI Services

### Store Item Embeddings
- **URL**: `/ai/embed_store`
- **Method**: `POST`
- **Description**: Create and store vector embeddings for an item description
- **Request Body**:
  ```json
  {
    "itemDesc": "string",
    "_id": "string"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Successfully inserted vectors"
  }
  ```
- **Status Codes**:
  - 200: Success
  - 400: Error processing request

### Query Similar Items
- **URL**: `/ai/query`
- **Method**: `POST`
- **Description**: Find items with similar descriptions using vector similarity search
- **Request Body**:
  ```json
  {
    "itemDesc": "string"
  }
  ```
- **Response**:
  ```json
  {
    "similar_complaints": [
      {
        "_id": "string",
        "content_preview": "string"
      }
    ]
  }
  ```
- **Status Codes**:
  - 200: Success
  - 400: Error processing request

## Error Responses

All API endpoints may return error responses in the following format:
```json
{
  "error": "Error message description"
}
```
