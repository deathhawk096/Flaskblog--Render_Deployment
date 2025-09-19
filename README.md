

# Flask Blog Application 📝
This is my **first ever Flask web application**.  
Most of the code is inspired by following along [Corey Schafer’s Flask tutorial series](https://www.youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH), but I also made my own tweaks and deployed it.

A full-featured blog web application built with **Flask**, featuring user authentication, password reset via email, and CRUD operations for posts.  

---

## 🚀 Features
- User authentication (Register, Login, Logout).
- Profile management (username, email, profile picture).
- Password reset with email verification.
- Create, Read, Update, and Delete blog posts.
- Secure password hashing with **Flask-Bcrypt**.
- Database migrations with **Flask-Migrate**.
- Email integration with **SendGrid API (via official Python SDK)**
- Modular structure with Blueprints.

---

## 🛠 Tech Stack
- **Backend**: Flask (Python)
- **Database**: PostgreSQL (or SQLite for development)
- **ORM**: SQLAlchemy
- **Authentication**: Flask-Login
- **Migrations**: Alembic (via Flask-Migrate)
- **Mail Service**: SendGrid (REST API with Python SDK)
- **Cloud Storage**: Cloudinary(with Python SDK)

---
🔑 Environment Variables

Make sure to configure the following in your .env file or system environment:

SECRET_KEY

SQLALCHEMY_DATABASE_URI

SENDGRID_API_KEY

VERIFIED_SENDER_EMAIL

CLOUDINARY_CLOUD_NAME

CLOUDINARY_API_KEY

CLOUDINARY_API_SECRET


## Live Demo
👉 [Check out the app here](https://flaskblog-render-deployment.onrender.com/)

