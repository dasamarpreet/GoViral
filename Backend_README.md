# GoViral Backend (Django + DRF + JWT)

## 📌 Project Overview

GoViral is a SaaS platform connecting **Companies** and **Creators
(Influencers)**.

This backend currently supports:

-   Custom Email-based Authentication
-   JWT Login System
-   Role Selection (Company / Creator)
-   Profile Completion Flow
-   PostgreSQL Database Integration
-   REST API tested via Postman

------------------------------------------------------------------------

## 🏗 Tech Stack

-   Python 3.x
-   Django
-   Django REST Framework (DRF)
-   PostgreSQL
-   SimpleJWT (JWT Authentication)
-   dotenv (.env config)

------------------------------------------------------------------------

## 📂 Project Structure

    server/
    │
    ├── accounts/
    │   ├── models.py
    │   ├── managers.py
    │   ├── serializers.py
    │   ├── views.py
    │   ├── urls.py
    │
    ├── server/
    │   ├── settings.py
    │   ├── urls.py
    │
    ├── manage.py

------------------------------------------------------------------------

## 🧠 Authentication Flow

### 1️⃣ Register

-   User registers using email + password
-   User is created
-   `role = NULL`
-   `is_profile_completed = False`

### 2️⃣ Login

-   User logs in using email + password
-   JWT Access + Refresh tokens returned
-   Response includes:
    -   role
    -   profile_completed flag

### 3️⃣ Role Selection

-   User selects role: COMPANY or CREATOR
-   Role stored in User model

### 4️⃣ Profile Completion

-   Based on role:
    -   CompanyProfile created
    -   CreatorProfile created
-   `is_profile_completed = True`

------------------------------------------------------------------------

## 🗄 Database Models

### User

-   email (unique)
-   role (COMPANY / CREATOR / ADMIN)
-   is_active
-   is_profile_completed
-   created_at

### CompanyProfile

-   user (OneToOne)
-   company_name
-   website
-   social links

### CreatorProfile

-   user (OneToOne)
-   full_name
-   age
-   sex
-   platform
-   followers
-   social links

------------------------------------------------------------------------

## 🔐 API Endpoints

Base URL:

    http://127.0.0.1:8000/api/auth/

------------------------------------------------------------------------

### 🔹 Register

**POST** `/register/`

Body:

``` json
{
  "email": "test@test.com",
  "password": "123456"
}
```

Response:

``` json
{
  "message": "User registered successfully"
}
```

------------------------------------------------------------------------

### 🔹 Login

**POST** `/login/`

Body:

``` json
{
  "email": "test@test.com",
  "password": "123456"
}
```

Response:

``` json
{
  "access": "JWT_ACCESS_TOKEN",
  "refresh": "JWT_REFRESH_TOKEN",
  "role": null,
  "profile_completed": false
}
```

------------------------------------------------------------------------

### 🔹 Select Role

**POST** `/select-role/`

Headers:

    Authorization: Bearer <access_token>

Body:

``` json
{
  "role": "COMPANY"
}
```

Response:

``` json
{
  "message": "Role selected successfully"
}
```

------------------------------------------------------------------------

### 🔹 Complete Profile

**POST** `/complete-profile/`

Headers:

    Authorization: Bearer <access_token>

Body (Company):

``` json
{
  "company_name": "ABC Pvt Ltd",
  "website": "https://abc.com"
}
```

Body (Creator):

``` json
{
  "full_name": "John Doe",
  "age": 25,
  "sex": "MALE",
  "platform": "Instagram",
  "followers": 5000
}
```

Response:

``` json
{
  "message": "Profile created"
}
```

------------------------------------------------------------------------

## 🔧 Environment Variables (.env)

    SECRET_KEY=your_secret_key
    DEBUG=True
    ALLOWED_HOSTS=127.0.0.1,localhost

    <!-- PostgreSQL -->
    DB_NAME=goviral_db
    DB_USER=goviral_user
    DB_PASSWORD=your_password
    DB_HOST=localhost
    DB_PORT=5432

------------------------------------------------------------------------

## 🛠 Setup Instructions

1.  Create virtual environment

2.  Install dependencies:

        pip install -r requirements.txt

3.  Setup PostgreSQL database

4.  Run migrations:

        python manage.py makemigrations
        python manage.py migrate

5.  Run server:

        python manage.py runserver

------------------------------------------------------------------------

## 🚀 Next Planned Features

-   OTP Email Verification
-   Admin Approval System
-   Role-Based Permissions
-   Campaign Management
-   Bidding System

------------------------------------------------------------------------

## 📌 Current Status

✔ Custom User Model\
✔ JWT Authentication\
✔ Role-based onboarding\
✔ PostgreSQL Integration

------------------------------------------------------------------------

Built with scalable backend architecture in mind.
