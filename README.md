<div align="center">

# ⚡ TaskStack

**Modern Project & Ticket Management Backend**

*Built with FastAPI · SQLAlchemy (Async) · Alembic · PostgreSQL*

<br/>

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=python&logoColor=white)](https://www.sqlalchemy.org/)
[![Alembic](https://img.shields.io/badge/Alembic-6DB33F?style=for-the-badge&logo=databricks&logoColor=white)](https://alembic.sqlalchemy.org/)
[![Python](https://img.shields.io/badge/Python_3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-F7C948?style=for-the-badge)](LICENSE)

<br/>

> 🚀 A **scalable, modular backend platform** for managing projects, tickets, comments, roles, and organizations.  
> Designed for modern **SaaS and enterprise** needs with robust authentication and fine-grained permissions.

</div>

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [📁 Project Structure](#-project-structure)
- [⚡ Quickstart](#-quickstart)
- [🔐 Authentication](#-authentication)
- [🛠️ API Usage](#️-api-usage)
- [🧩 Extending TaskStack](#-extending-taskstack)
- [🧪 Testing](#-testing)
- [📦 Deployment](#-deployment)
- [🤝 Contributing](#-contributing)

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🔐 Auth & Security
- JWT Bearer token authentication
- Role-based access control (RBAC)
- Roles: `Admin` · `Project Manager` · `Developer` · `Reporter`

### 🗂️ Project & Ticket Management
- Create and organize projects
- Manage tickets with assignments
- Full CRUD with permission checks

</td>
<td width="50%">

### 💬 Commenting System
- Add, update, and delete comments
- Permission-aware comment access

### 🏢 Multi-Tenant Support
- Organization & subscription management
- Built for SaaS and enterprise scale

### ⚙️ Technical Highlights
- Async SQLAlchemy ORM for high performance
- Alembic-powered database migrations
- Versioned RESTful API (`/api/v1/`)
- Modular, extensible architecture

</td>
</tr>
</table>

---

## 📁 Project Structure

```
taskstack/
│
├── 📄 main.py                  # App entry point
├── 📄 alembic.ini              # Alembic config
├── 📄 requirements.txt
│
├── 📂 alembic/
│   ├── env.py
│   └── versions/               # Migration files
│
└── 📂 app/
    ├── 📂 api/
    │   └── v1/                 # Versioned route handlers
    ├── 📂 authentication/      # JWT & auth logic
    ├── 📂 config/              # App configuration
    ├── 📂 constant/            # Shared constants & enums
    ├── 📂 models/              # SQLAlchemy ORM models
    ├── 📂 repositories/        # DB query layer
    ├── 📂 schemas/             # Pydantic schemas
    ├── 📂 services/            # Business logic layer
    └── 📂 utils/               # Helper utilities
```

---

## ⚡ Quickstart

### 1️⃣ Clone & Set Up Environment

```bash
git clone <repo-url>
cd taskstack

python3 -m venv taskstack-env
source taskstack-env/bin/activate        # Windows: taskstack-env\Scripts\activate

pip install -r requirements.txt
```

### 2️⃣ Configure Environment Variables

```bash
cp .env.example .env
```

Open `.env` and fill in your values:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost/taskstack
SECRET_KEY=your-super-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3️⃣ Run Database Migrations

```bash
alembic upgrade head
```

### 4️⃣ Start the Server

```bash
uvicorn main:app --reload
```

> 🟢 Server is live at **http://localhost:8000**  
> 📖 Interactive API docs at **http://localhost:8000/docs**

---

## 🔐 Authentication

TaskStack uses **JWT Bearer tokens** for all protected endpoints.

| Role | Access Level |
|------|-------------|
| 🟣 `system_admin` | Superuser — platform-wide control, manage organizations & subscriptions |
| 🔴 `admin` | Full access — all resources and settings |
| 🟠 `project_manager` | Manage projects, tickets, assignments |
| 🔵 `developer` | View and update assigned tickets |
| 🟢 `reporter` | Create tickets, add comments |

**Getting a token:**

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

**Using the token:**

```http
Authorization: Bearer <your_token_here>
```

---

## 🛠️ API Usage

All endpoints are versioned under **`/api/v1/`**

### 📌 Tickets

```http
# Create a ticket
POST /api/v1/tickets/
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Fix login bug",
  "description": "Users can't log in with Google OAuth",
  "project_id": "uuid-here",
  "priority": "high"
}
```

### 💬 Comments

```http
# Add a comment to a ticket
POST /api/v1/comments/
Authorization: Bearer <token>
Content-Type: application/json

{
  "ticket_id": "uuid-here",
  "content": "I reproduced this issue on Chrome v120."
}
```

### 🗂️ Projects

```http
# List all projects
GET /api/v1/projects/
Authorization: Bearer <token>
```

> 💡 Explore all endpoints via the **[Swagger UI](http://localhost:8000/docs)** or **[ReDoc](http://localhost:8000/redoc)** — auto-generated from your FastAPI app.

---

## 🧩 Extending TaskStack

Adding new features is straightforward thanks to the modular architecture:

| What you want | Where to add it |
|---------------|-----------------|
| New DB table / entity | `app/models/` |
| New API endpoint | `app/api/v1/` |
| Business logic | `app/services/` |
| DB queries | `app/repositories/` |
| Request/Response shape | `app/schemas/` |
| DB schema change | `alembic revision --autogenerate -m "description"` |



## 📦 Deployment

### Using Uvicorn (Production)

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Gunicorn + Uvicorn Workers

```bash
gunicorn main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --workers 4
```

### 🐳 Docker (coming soon)

A `Dockerfile` and `docker-compose.yml` can be added for containerized deployment. Environment variables should be passed via Docker secrets or a `.env` file.

---

## 🤝 Contributing

Contributions are welcome and appreciated! Here's how to get started:

1. 🍴 **Fork** this repository
2. 🌿 **Create** your feature branch: `git checkout -b feature/amazing-feature`
3. ✅ **Commit** your changes: `git commit -m 'Add amazing feature'`
4. 📤 **Push** to the branch: `git push origin feature/amazing-feature`
5. 🔁 **Open a Pull Request**

> Please open an **issue** first to discuss major changes.

---

## 📄 License

This project is licensed under the **[MIT License](LICENSE)** — free to use, modify, and distribute.

---

<div align="center">

**Made with ❤️ by [Het Govani](https://github.com/hetgovani)**

*If you find this project useful, please consider giving it a ⭐ on GitHub!*

</div>
