# GoViral

## Backend

# 1. Go to server folder ($ cd server) then:
# 2. Create virtual env: $ python -m venv venv
# keep this structure:
server/
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── manage.py
├── venv/

# 3. Activate virtual env: 
    windows: $ source venv/Scripts/activate  OR ./venv/Scripts/activate
    Linux/Mac: $ source venv/bin/activate

# 4. Now, create the Django project: $ python -m django startproject BE_PROJECT_NAME .        (Preferred Name: config)
# 5. Install minimum required packages:
    $ pip install django djangorestframework python-dotenv
    $ pip install djangorestframework-simplejwt

# 6. Set up .env from .env.example
# 7. Then, create Django Apps. Create apps by responsibility, not features:
    $ python manage.py startapp users
    $ python manage.py startapp authn

    App	        Responsibility
    users	    User model, roles, profiles
    authn	    OTP, login, verification

# 8. Updated (Recommended) Folder Structure:

server/
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── users/
│   ├── models/
│   │   ├── user.py
│   │   ├── company.py
│   │   └── influencer.py
│   ├── serializers/
│   ├── views/
│   ├── permissions.py
│   └── admin.py
├── authn/
│   ├── models.py        # OTP model
│   ├── services.py      # OTP logic
│   ├── views.py
│   └── utils.py
├── manage.py
├── venv/


# 9. USER & ROLE MODEL (DESIGN IDEA)
    Keeps User clean
    Allows different fields
    Scales well

# Core User
    Email (unique, login field)
    Role (COMPANY, INFLUENCER, ADMIN)
    Status (PENDING, ACTIVE, BLOCKED)
    Email verified (bool)

# Profiles (One-to-One)
    CompanyProfile
    InfluencerProfile


# 10. AUTHENTICATION FLOW (Email + OTP)

# Flow:
    a. User enters email
    b. OTP generated & stored (short expiry)
    c. OTP emailed (Google App Password)
    d. User submits OTP
    e. If valid:
        User created (or fetched)
        JWT issued
    f. If first login:
        Force role selection
        Force profile completion


# OTP Model (Concept)
# Fields:
    email
    otp
    expires_at
    attempts
    is_used

# Rules:
    Expire after 5 mins
    Max retry limit
    One active OTP per email

This prevents abuse.


# 11. Role Selection & Profile Completion
# First login logic (important)
User state:
    role = NULL
    profile_completed = False

Backend must:
    Block access to all APIs
    Except:
        /select-role
        /complete-profile

Once done:
    Update role
    Create respective profile
    Set status:
        Company → ACTIVE
        Influencer → PENDING (admin approval)


# 12. Authorization & Permissions

Create custom permission classes:

Examples:
    IsAuthenticatedAndActive
    IsCompany
    IsInfluencer
    IsAdmin

These are used in DRF views.
This is where your ownership table gets enforced.


# 13. Test Using Postman

Before any frontend:
    Test OTP flow
    Test role selection
    Test blocked users
    Test influencer pending approval
    Test admin approval

If Postman works → frontend will be easy.


# Important Rules (Don’t Break These)

❌ Don’t mix OTP logic inside views

❌ Don’t put business rules in serializers

❌ Don’t let users access APIs before profile completion

❌ Don’t hardcode email credentials

✅ Always validate user status in permissions




# NEXT STEP (After This)

Once auth & profile flow is stable, next phases:
    Campaign app
    Bid app
    Admin controls
    State enforcement

