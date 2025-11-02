# 🔒 Authentication & Authorization Microservice

A **FastAPI**-based microservice for managing user **authentication** and **authorization**. This project provides secure JWT-based authentication, role-based access control (RBAC), and token management with PostgreSQL and Redis integration.

---

## 📋 Table of Contents

- [🌟 Features](#-features)
- [🛠️ Tech Stack](#%EF%B8%8F-tech-stack)
- [📝 Prerequisites](#-prerequisites)
- [⚙️ Setup Instructions](#%EF%B8%8F-setup-instructions)
- [🌐 API Endpoints](#-api-endpoints)
- [🗄️ Database Migrations](#%EF%B8%8F-database-migrations)
- [🚀 Running the Application](#-running-the-application)
- [🧪 Testing](#-testing)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)

---

## 🌟 Features

- 🔐 **User Authentication**: Secure signup and login with JWT access and refresh tokens.
- 🔄 **Token Management**: Refresh tokens for session renewal and logout with token blacklisting.
- 🎭 **Role-Based Access Control (RBAC)**: Assign and manage user roles and permissions.
- ⚡ **Async Database Operations**: Leverages SQLAlchemy with asyncpg for PostgreSQL.
- 🗳️ **Redis Integration**: Efficient token blacklisting for secure logout.
- 📖 **Interactive API Docs**: Auto-generated Swagger UI at `/docs`.
- 🧩 **Modular Codebase**: Business logic separated into services for maintainability.

---

## 🛠️ Tech Stack

| **Component**          | **Technology**         |
|------------------------|------------------------|
| **Framework**          | FastAPI               |
| **Language**           | Python 3.12           |
| **Database**           | PostgreSQL            |
| **Cache**              | Redis                 |
| **ORM**                | SQLAlchemy (async)    |
| **Authentication**     | JWT, OAuth2           |
| **Dependency Manager** | Poetry                |
| **Migrations**         | Alembic               |
| **Libraries**          | python-jose, passlib, aioredis, pydantic-settings |

---

## 📝 Prerequisites

Before you begin, ensure you have the following installed:

- [x] **Python 3.12+** ([Download](https://www.python.org/downloads/))
- [x] **PostgreSQL** (Local or Docker: `docker run -p 5432:5432 postgres`)
- [x] **Redis** (Local or Docker: `docker run -p 6379:6379 redis`)
- [x] **Poetry** (`pip install poetry`)
- [x] **Git** (`git --version` to check)

---

## ⚙️ Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/auth-service.git
   cd auth-service
   ```

2. **Install dependencies** using Poetry:
   ```bash
   poetry install
   poetry shell
   ```

3. **Configure environment variables**:
   Copy the example `.env` file and update it with your credentials:
   ```bash
   cp .env.example .env
   ```
   Example `.env` content:
   ```
   DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/auth_db
   REDIS_URL=redis://localhost:6379/0
   JWT_SECRET=your_jwt_secret_key_here
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=15
   REFRESH_TOKEN_EXPIRE_DAYS=7
   ```

4. **Set up PostgreSQL**:
   Create a database:
   ```sql
   psql -U postgres
   CREATE DATABASE auth_db;
   \q
   ```

5. **Run database migrations**:
   ```bash
   alembic upgrade head
   ```

6. **Start Redis**:
   Ensure Redis is running (e.g., `redis-server` or via Docker).

---

## 🌐 API Endpoints

The API is documented via Swagger UI at `http://localhost:8000/docs`. Key endpoints include:

| **Method** | **Endpoint**            | **Description**                          | **Access**         |
|------------|-------------------------|------------------------------------------|--------------------|
| POST       | `/auth/signup`          | Register a new user                      | Public             |
| POST       | `/auth/login`           | Authenticate and receive tokens          | Public             |
| POST       | `/auth/refresh`         | Refresh access and refresh tokens        | Public             |
| POST       | `/auth/logout`          | Blacklist access token for logout        | Authenticated      |
| GET        | `/users/me`             | Get authenticated user's profile         | Authenticated      |
| PUT        | `/users/me`             | Update authenticated user's profile      | Authenticated      |
| GET        | `/users/`               | List all users                          | Superadmin         |
| DELETE     | `/users/{user_id}`      | Delete a user                           | Superadmin         |
| POST       | `/roles/`               | Create a new role                       | Superadmin         |

> **Note**: Use the Swagger UI for detailed request/response schemas and testing.

---

## 🗄️ Database Migrations

To manage database schema changes with Alembic:

- **Generate a new migration**:
  ```bash
  alembic revision --autogenerate -m "Description of changes"
  ```

- **Apply migrations**:
  ```bash
  alembic upgrade head
  ```

To verify tables:
```sql
psql -U postgres -d auth_db
\dt
```

---

## 🚀 Running the Application

Start the FastAPI server:
```bash
# from project root (Windows PowerShell)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Access the API at:
- **Swagger UI**: `http://localhost:8000/docs`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

> **Tip**: The `--reload` flag enables auto-reload during development.

---

## 🧪 Testing

To run tests (assuming tests are implemented):
1. Install test dependencies:
   ```bash
   poetry add pytest pytest-asyncio httpx --group dev
   ```

2. Run tests:
   ```bash
   pytest
   ```

> **Placeholder**: Add test cases for `/auth/*` and `/users/*` endpoints in the `tests/` directory.

---

## 🤝 Contributing

We welcome contributions! Follow these steps:

1. **Fork** the repository.
2. Create a new **branch**:
   ```bash
   git checkout -b feature/your-feature
   ```
3. **Commit** your changes:
   ```bash
   git commit -m "Add your feature"
   ```
4. **Push** to the branch:
   ```bash
   git push origin feature/your-feature
   ```
5. Open a **Pull Request** on GitHub.

Please ensure your code follows the project's coding standards and includes tests.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE). See the [LICENSE](LICENSE) file for details.

---

## 📸 Screenshots

*Coming soon: Add screenshots of Swagger UI or API responses.*

---

*Built with ❤️ using FastAPI and Python.*