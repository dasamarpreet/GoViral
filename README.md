# GoViral 🚀

---

## 📦 Backend Setup Guide
---

## 1️⃣ Navigate to Backend Folder

```bash
cd server
```

---

## 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
```

### Initial Folder Structure
```
server/
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── manage.py
├── venv/
```

---

## 3️⃣ Activate Virtual Environment

**Windows**
```bash
source venv/Scripts/activate
# OR
./venv/Scripts/activate
```

**Linux / Mac**
```bash
source venv/bin/activate
```

---

## 4️⃣ Create Django Project

```bash
python -m django startproject config .
```

> **Preferred project name:** `config`

---

## 5️⃣ Install Required Packages

```bash
pip install django djangorestframework python-dotenv
pip install djangorestframework-simplejwt
```

---

## 6️⃣ Environment Variables

Create `.env` file using `.env.example` as reference.

⚠️ **Never commit `.env` to git**

---

## 7️⃣ Create Django Apps (By Responsibility)

```bash
python manage.py startapp users
python manage.py startapp authn
```

### Responsibility-Based Design

| App Name | Responsibility |
|--------|---------------|
| users  | User model, roles, profiles |
| authn  | OTP, login, verification |

---

## 8️⃣ Recommended Folder Structure

```
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
│   ├── services.py      # OTP business logic
│   ├── views.py
│   └── utils.py
├── manage.py
├── venv/
```

---

## 9️⃣ User & Role Model (Design Concept)

### Why This Design?
- Keeps core User clean
- Supports multiple roles cleanly
- Easy to scale

### Core User Fields
- **Email** (unique, login field)
- **Role** → `COMPANY | INFLUENCER | ADMIN`
- **Status** → `PENDING | ACTIVE | BLOCKED`
- **Email Verified** → `True / False`

### One-to-One Profiles
- `CompanyProfile`
- `InfluencerProfile`

---

## 🔐 10️⃣ Authentication Flow (Email + OTP)

### Flow Overview
1. User enters email
2. OTP generated & stored (short expiry)
3. OTP sent via email (Google App Password)
4. User submits OTP
5. If OTP is valid:
   - User created or fetched
   - JWT issued
6. First-time users:
   - Must select role
   - Must complete profile

---

### OTP Model (Concept)

**Fields**
- email
- otp
- expires_at
- attempts
- is_used

**Rules**
- Expires in **5 minutes**
- Max retry limit
- One active OTP per email

✅ Prevents abuse & brute-force attempts

---

## 🧩 11️⃣ Role Selection & Profile Completion

### First Login State
```
role = NULL
profile_completed = False
```

### Backend Enforcement
❌ Block all APIs  
✅ Allow only:
- `/select-role`
- `/complete-profile`

### After Completion
- Assign role
- Create respective profile
- Update status:
  - **Company** → `ACTIVE`
  - **Influencer** → `PENDING` (admin approval)

---

## 🛡️ 12️⃣ Authorization & Permissions

Create **custom DRF permission classes**:

- `IsAuthenticatedAndActive`
- `IsCompany`
- `IsInfluencer`
- `IsAdmin`

🔐 All access control & ownership rules live here.
These are used in DRF views.
This is where your ownership table gets enforced.

---

## 🧪 13️⃣ Test Using Postman (Mandatory)

Before frontend integration:
- Test OTP flow
- Test role selection
- Test blocked users
- Test influencer approval
- Test admin actions

✔️ If Postman works → frontend will be smooth.

---

## 🚫 Important Rules (Do Not Break)

❌ Don’t mix OTP logic inside views  
❌ Don’t put business rules in serializers  
❌ Don’t let users access APIs before profile completion  
❌ Don’t hardcode email credentials  

✅ Always validate user **status & role** in permissions

---

## 🔜 Next Steps

Once auth & profile flow is stable:
- Campaign app
- Bid app
- Admin controls
- State enforcement

---

### ✨ Built for scale. Designed for clarity.
