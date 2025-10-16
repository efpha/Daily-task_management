**API PROJECT
Project Title: Simple Task Management API**

**Project Description:**
    A RESTful API based app that allows users to manage their daily tasks. The API support account creation, logging in, and performing CRUD operations (Create, Read,         Update, Delete) on tasks. Focuses on structuring routes, handling requests/responses, basic authentication, and data validation.

**1. User Authentication**

   ~Users can register with name, email, and password.
   ~Users can log in and receive a token (e.g., JWT).
   ~Protected routes should require a valid token.

**2. Tasks CRUD**
- A logged-in user can:
    ~ Create a new task (title, description, due_date, status).
    ~ View all their tasks.
    ~ View a single task by ID.
    ~ Update a task’s information.
    ~ Delete a task.

**3. Task Model Fields**
    ~ id (auto)
    ~ title (string)
    ~ description (string)
    ~ due_date (date)
    ~ status (e.g., “pending”, “in-progress”, “completed”)
    ~ created_at, updated_at

**Technologies Used**
    Django framework
    Database - mysql
