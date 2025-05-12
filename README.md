# Lost and Found Service - CampusConnect

This service handles the lost and found functionality of the CampusConnect platform, allowing users to report lost items or items they have found on campus.

## Technologies
- Python 3.x
- Flask (Web Framework)
- SQLAlchemy ORM
- PostgreSQL Database
- gRPC for inter-service communication
- AI-powered similarity search
- Docker for containerization
- Image processing and storage

## Project Structure
```
CC-lost-found-backend/
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
├── grpc_client/             # gRPC client for auth service
├── grpc_server/             # gRPC server implementation for lost and found service
├── models/                  # Database models
├── routes/                  # API route definitions
│   ├── user_routes.py       # User-related routes
│   ├── item_routes.py       # Item management routes
│   ├── image_upload_routes.py # Image upload handling
│   ├── auth_routes.py       # Authentication routes
│   └── ai_routes.py         # AI features routes
└── services/                # Business logic implementations
```

## API Routes

All routes require authentication using a JWT token in the Authorization header: `Authorization: Bearer <token>`

### Item Management

#### Get All Items
- **Endpoint:** `GET /item/`
- **Response:**
  - Success (200):
    ```json
    {
      "items": [
        {
          "id": "item1",
          "title": "Lost Wallet",
          "description": "Black leather wallet lost in Library",
          "user_id": "user123",
          "item_category": "lost",
          "image_url": "https://storage-url/image1.jpg",
          "created_at": "2023-05-01T12:30:45",
          "updated_at": "2023-05-01T12:30:45"
        },
        ...
      ]
    }
    ```

#### Get Item by ID
- **Endpoint:** `GET /item/<string:item_id>`
- **Response:**
  - Success (200):
    ```json
    {
      "id": "item1",
      "title": "Lost Wallet",
      "description": "Black leather wallet lost in Library",
      "user_id": "user123",
      "username": "John Doe",  
      "item_category": "lost",
      "image_url": "https://storage-url/image1.jpg",
      "created_at": "2023-05-01T12:30:45",
      "updated_at": "2023-05-01T12:30:45"
    }
    ```
  - Error (400): `{ "error": "No item ID provided" }`
  - Error (404): `{ "error": "Item not found" }`

#### Create Item
- **Endpoint:** `POST /item/create`
- **Content-Type:** `application/json` or `multipart/form-data` (for image uploads)
- **Parameters (JSON):**
  ```json
  {
    "title": "Lost Wallet",
    "description": "Black leather wallet lost in Library",
    "user_id": "user123",
    "item_category": "lost"
  }
  ```
- **Parameters (multipart/form-data):**
  - `title`: Item title
  - `description`: Item description
  - `user_id`: ID of the user creating the item
  - `item_category`: Either "lost" or "found"
  - `image_file`: Image file (optional)

- **Response:**
  - Success (201):
    ```json
    {
      "message": "Item created successfully",
      "item": {
        "id": "item1",
        "title": "Lost Wallet",
        "description": "Black leather wallet lost in Library",
        "user_id": "user123",
        "item_category": "lost",
        "image_url": "https://storage-url/image1.jpg",
        "created_at": "2023-05-01T12:30:45",
        "updated_at": "2023-05-01T12:30:45"
      }
    }
    ```
  - Error (400): `{ "error": "Invalid item data" }`

#### Update Item
- **Endpoint:** `POST /item/update`
- **Parameters:**
  ```json
  {
    "item_id": "item1",
    "title": "Updated Title",
    "description": "Updated description",
    "item_category": "lost"
  }
  ```
- **Response:**
  - Success (200):
    ```json
    {
      "message": "Item updated successfully",
      "item": {
        "id": "item1",
        "title": "Updated Title",
        "description": "Updated description",
        "user_id": "user123",
        "item_category": "lost",
        "image_url": "https://storage-url/image1.jpg",
        "created_at": "2023-05-01T12:30:45",
        "updated_at": "2023-05-02T14:20:15"
      }
    }
    ```
  - Error (404): `{ "error": "Item not found" }`
  - Error (403): `{ "error": "You do not have permission to update this item" }`

#### Delete Item
- **Endpoint:** `POST /item/delete`
- **Parameters:**
  ```json
  {
    "item_id": "item1"
  }
  ```
- **Response:**
  - Success (200): `{ "message": "Item deleted successfully" }`
  - Error (404): `{ "error": "Item not found" }`
  - Error (403): `{ "error": "You do not have permission to delete this item" }`

#### Get Multiple Items
- **Endpoint:** `POST /item/getItems`
- **Parameters:**
  ```json
  {
    "item_ids": ["item1", "item2", "item3"]
  }
  ```
- **Response:**
  - Success (200):
    ```json
    {
      "items": [
        {
          "id": "item1",
          "title": "Lost Wallet",
          "description": "Black leather wallet lost in Library",
          "user_id": "user123",
          "item_category": "lost",
          "image_url": "https://storage-url/image1.jpg",
          "created_at": "2023-05-01T12:30:45",
          "updated_at": "2023-05-01T12:30:45"
        },
        ...
      ]
    }
    ```
  - Error (400): `{ "error": "No item IDs provided" }`

### Image Upload Routes

#### Upload Image for Item
- **Endpoint:** `POST /image/upload`
- **Content-Type:** `multipart/form-data`
- **Parameters:**
  - `image_file`: Image file
  - `item_id`: ID of the item to associate the image with
- **Response:**
  - Success (200):
    ```json
    {
      "message": "Image uploaded successfully",
      "image_url": "https://storage-url/image1.jpg"
    }
    ```
  - Error (400): `{ "error": "No file provided" }` or `{ "error": "Invalid file format" }`

### AI Features

#### Object Recognition
- **Endpoint:** `POST /ai/recognize`
- **Content-Type:** `multipart/form-data`
- **Parameters:**
  - `image_file`: Image file to analyze
- **Response:**
  - Success (200):
    ```json
    {
      "objects": [
        {
          "label": "wallet",
          "confidence": 0.94
        },
        {
          "label": "keys",
          "confidence": 0.85
        }
      ]
    }
    ```
  - Error (400): `{ "error": "No file provided" }`

## gRPC Services

The service also provides gRPC endpoints for internal service communication with the central server.

## Setup and Deployment

### Environment Variables

Create an `.env` file with the following variables:
```
FLASK_APP=run.py
FLASK_ENV=development
DATABASE_URI=sqlite:///lostfound.db
JWT_SECRET_KEY=your_jwt_secret_key
AUTH_SERVICE_URL=localhost:50053
GRPC_SERVER=0.0.0.0:50052
UPLOAD_FOLDER=./uploads
```

### Running the Service

```bash
# Set up virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Initialize the database
flask db upgrade

# Run the server
flask run --port=5000
```

### Docker Deployment
The service is configured to run in the Docker Compose setup of the CampusConnect platform.

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
    "image": "string (optional)",
    "item_category": "string (LOST || FOUND)"
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
