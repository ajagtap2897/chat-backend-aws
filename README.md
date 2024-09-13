# chat-backend-aws

# FastAPI Backend for User and Messaging System

This is a FastAPI-based backend application designed to manage user data and messaging between users. It features endpoints for creating users, retrieving user data, sending messages, and retrieving chat history.

## Features

- **User Management**: Create, retrieve, and list users.
- **Messaging System**: Send messages between users and retrieve chat history.
- **Pydantic Models**: Validation of user and message data.
- **MongoDB**: Backend database for persistent storage (via `motor` library).
- **CORS Support**: Cross-Origin Resource Sharing (CORS) is enabled to allow connections from different domains.

## Prerequisites

Before running the project, ensure you have the following installed:

- **Python 3.8+**
- **FastAPI**
- **MongoDB** (running locally or via a cloud provider like MongoDB Atlas)
- **Uvicorn** (to serve the FastAPI app)
- **Motor** (MongoDB driver for asyncio)
- **Pydantic** (for data validation)

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   ```

2. Navigate to the project directory:

   ```bash
   cd <project-directory>
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory to set up environment variables like MongoDB URI:

   ```bash
   MONGO_URI="your-mongodb-connection-string"
   ```

## Running the Application

Start the FastAPI server with Uvicorn:

```bash
uvicorn main:app --reload
```

This will start the development server at `http://127.0.0.1:8000`.

## API Endpoints

### User Endpoints

1. **Create User**  
   **URL**: `/users/`  
   **Method**: `POST`  
   **Request Body**:
   ```json
   {
     "name": "string",
     "email": "string"
   }
   ```
   **Response**:  
   Creates a new user and returns the user data.

2. **Get User by Email**  
   **URL**: `/users/{email}`  
   **Method**: `GET`  
   **Response**:  
   Retrieves the user data based on their email.

3. **List All Users**  
   **URL**: `/users/`  
   **Method**: `GET`  
   **Response**:  
   Returns a list of all users in the system.

### Message Endpoints

1. **Send Message**  
   **URL**: `/messages/`  
   **Method**: `POST`  
   **Request Body**:
   ```json
   {
     "sender": "string",
     "receiver": "string",
     "content": "string"
   }
   ```
   **Response**:  
   Sends a message from one user to another.

2. **Chat History**  
   **URL**: `/chat-history/{user_id}/{contact_id}`  
   **Method**: `GET`  
   **Response**:  
   Retrieves the chat history between two users.

3. **Chat List**  
   **URL**: `/chat-list/{user_id}`  
   **Method**: `GET`  
   **Response**:  
   Returns the list of users that a particular user has interacted with and the last message exchanged.

## Static Files

Static files such as profile pictures are served under the `/static/` endpoint. When a new user is created, a default profile picture is generated with the user's ID.

## Middleware

- **CORS**: The application uses `CORSMiddleware` to handle Cross-Origin requests, allowing all origins (`*`), methods, and headers.

## Environment Variables

- `MONGO_URI`: The connection string for the MongoDB database.

## Technologies Used

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs.
- **MongoDB**: A NoSQL database used for storing user and message data.
- **Motor**: An asynchronous driver for MongoDB used with Python.
- **Pydantic**: For data validation and parsing using Python type annotations.
- **Uvicorn**: A lightning-fast ASGI server for serving FastAPI apps.
