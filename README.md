# Phrasee FS Offline Technical Assignment

This project is a full-stack application with a **FastAPI backend** and a **React frontend**. 

This project appears to be a notification service designed as a separate entity from the main social website. The separation likely serves to better manage the high volume of notifications without disrupting the primary functionalities of the core platform. Based on my understanding, this service is intended to interface with consumers connected to a Kafka or AWS SNS topic, where notifications are generated from events occurring on the main website.

To ensure scalability, I choose to minimize the number of database tables and keep queries as simple as possible, allowing the system to handle a big number of notifications efficiently.

That said, there are several enhancements still needed, including:

### Backend Improvements:

- Dockerization for consistent deployments.
- Caching mechanisms to improve performance.
- Expanded test coverage for reliability.
- Implementing authentication for secure access.

### Frontend Enhancements:

- Notifications should refresh at regular intervals (e.g., every few seconds).
- Ideally, long polling or a similar mechanism should be implemented to provide real-time updates without unnecessary requests.

---

## Table of Contents

1. [Technologies Used](#technologies-used)
2. [Backend Setup (FastAPI)](#backend-setup-fastapi)
3. [Frontend Setup (React)](#frontend-setup-react)
4. [Running the Application](#running-the-application)
5. [API Documentation](#api-documentation)
6. [Testing](#testing)

---

## Technologies Used

- **Backend**: FastAPI & SQLModel
- **Frontend**: React, TypeScript, Tailwind CSS
- **Database/Storage**: SQLite for now (Not to be usedon production)
- **Other Tools**: Pytest for testing (No tests on frontend)

---

## Getting Started

## Backend Setup (FastAPI)

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv env
   source env/bin/activate  # Mac/Linux
   env\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create the database Tables
   ```bash
   python initial_migrations.py
   ```

5. Run the server:
   ```bash
   uvicorn main:app --reload --port 8000 --host 0.0.0.0
   ```

5. The backend server will be running at `http://0.0.0.0:8000`.

---

## Frontend Setup (React)

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. The frontend server will be running at `http://localhost:3000`.

---

## Running the Application

1. Start the **FastAPI backend** server:
   ```bash
   uvicorn main:app --reload
   ```

2. Start the **React frontend**:
   ```bash
   npm start
   ```

3. Open your browser and navigate to `http://localhost:3000`.

4. Feed the notifications-feed.json content to the swagger /notifications/consume endpoint to get some data in the database

5. Go back to `http://localhost:3000` and check your notifications.

---

## API Documentation

FastAPI provides built-in interactive API documentation:
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

These endpoints allow you to test and understand the backend API structure.

---

## Testing

### Backend Tests
To run backend tests using **Pytest**, navigate to the backend directory and execute:
```bash
pytest
```

### Frontend Tests
N/A
