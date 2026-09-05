# Auth Login & Protect API

A secure authentication API built with **Python, FastAPI, and Supabase Auth**.

This project implements user signup, login, JWT authentication, protected routes, logout, and Swagger API documentation.

## 🚀 Features

* User signup with email and password
* User login with Supabase Authentication
* JWT access token authentication
* Refresh token support
* Public API route
* Protected API routes
* JWT token verification
* Reusable authentication dependency
* Protected logout
* Swagger/OpenAPI documentation
* Environment variables for secure configuration

## 🛠️ Technologies Used

* Python 3.10+
* FastAPI
* Uvicorn
* Supabase Auth
* Pydantic
* python-dotenv
* JWT

## 📁 Project Structure

```text
Auth-Login-Protect/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env
```

> `.env` is intentionally excluded from GitHub because it contains private Supabase credentials.

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/mshahzaibawan123/week-4-Auth---Login-protect.git
```

### 2. Open the project folder

```bash
cd week-4-Auth---Login-protect
```

### 3. Create a virtual environment

Windows:

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_key
PORT=8000
```

Replace the placeholder values with your own Supabase project credentials.

**Never upload your `.env` file or expose your Supabase secret keys publicly.**

## ▶️ Running the API

Start the FastAPI server:

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## 📚 Swagger Documentation

FastAPI automatically provides interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger can be used to test all API endpoints.

## 🔗 API Endpoints

### 1. Home

```http
GET /
```

Checks whether the server is running and connected to Supabase.

### 2. Signup

```http
POST /auth/signup
```

Creates a new user using an email address and password.

Example request:

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

### 3. Login

```http
POST /auth/login
```

Authenticates an existing user and returns:

* Access token
* Refresh token

Example request:

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

### 4. Public Information

```http
GET /public/info
```

This endpoint does not require authentication.

### 5. Protected Profile

```http
GET /protected/profile
```

Requires a valid JWT access token.

Authorization header:

```text
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### 6. Protected Dashboard

```http
GET /protected/dashboard
```

Requires a valid JWT access token.

### 7. Logout

```http
POST /auth/logout
```

Requires authentication and signs the user out through Supabase Auth.

## 🔑 Authentication Flow

The authentication flow works as follows:

```text
User
  │
  ├── Signup
  │      │
  │      ▼
  │   Supabase Auth
  │
  ├── Login
  │      │
  │      ▼
  │   Access Token + Refresh Token
  │      │
  │      ▼
  │   Protected Routes
  │      │
  │      ▼
  │   JWT Verification
  │      │
  │      ▼
  │   Authorized User
  │
  └── Logout
         │
         ▼
      Supabase Auth
```

## 🛡️ Protected Routes

Protected endpoints use a reusable authentication dependency to verify the JWT access token.

The API rejects:

* Missing authentication token
* Invalid token
* Expired token
* Malformed authentication requests

Protected endpoints return an HTTP `401 Unauthorized` response when authentication fails.

## 🧪 Testing

The API can be tested using the built-in Swagger interface:

```text
http://127.0.0.1:8000/docs
```

Recommended testing order:

1. `GET /`
2. `POST /auth/signup`
3. `POST /auth/login`
4. Copy the returned access token
5. Click **Authorize** in Swagger
6. Enter the access token
7. Test `/protected/profile`
8. Test `/protected/dashboard`
9. Test `/auth/logout`

## 📌 Project Requirements

This project demonstrates:

* Supabase project configuration
* FastAPI server setup
* User registration
* User authentication
* JWT-based authorization
* Protected API routes
* Reusable authentication dependency
* Logout functionality
* Swagger/OpenAPI documentation
* Secure environment variable management
* Git and GitHub version control

## 👨‍💻 Author

**Shahzaib Awan**

GitHub:

https://github.com/mshahzaibawan123

## 📄 License

This project was created for educational and internship assignment purposes.

## Stage 1 - Authentication

Implemented Supabase authentication with:

- User signup using email and password
- User login using email and password
- Access token generation
- Refresh token generation

## Stage 2 - Public and Protected Routes

Implemented:

- Public information endpoint
- Protected profile endpoint
- Authentication requirement for protected resources

## Stage 3 - JWT Verification

Protected routes verify the Supabase access token before allowing access to protected resources.

