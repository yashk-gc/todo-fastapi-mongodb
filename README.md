
# FastAPI + MongoDB Todo API

A simple Todo REST API built with **FastAPI** and **MongoDB**.  
It supports full CRUD operations, soft deletes, and timestamp tracking for each task.

## Features

- Create, read, update, delete todo items
- Soft delete using `is_deleted` flag (no hard delete)
- `created_at` and `updated_at` epoch timestamps
- Bulk create endpoint for multiple todos at once
- MongoDB Atlas (or local MongoDB) as the database

## Tech Stack

- Python
- FastAPI
- Uvicorn
- MongoDB (Atlas)
- PyMongo

## Project Structure


fastapi_todo/
│
├─ main.py               # FastAPI app and routes
├─ crud.py               # Database operations for todos
├─ configurations.py     # MongoDB client, db, and collection (local-only, gitignored)
├─ requirements.txt      # Python dependencies (optional)
├─ database/
│   ├─ models.py         # Pydantic Todo model
│   └─ schemas.py        # Helpers to shape MongoDB documents for responses
└─ venv/                 # Virtual environment (gitignored)


