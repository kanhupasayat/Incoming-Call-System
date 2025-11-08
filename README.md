# Incoming Call Management System

Django REST Framework webhook receiver for Tata Dealer incoming calls with Supabase PostgreSQL database.

## Setup Instructions

1. Clone repository
2. Install: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add your credentials
4. Run migrations: `python manage.py migrate`
5. Start server: `python manage.py runserver`

## Security

⚠️ **NEVER commit `.env` file to GitHub!**

All sensitive data is in `.env` which is excluded from git.
