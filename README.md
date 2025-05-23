
# Blog Project

This is a blog platform project built with *Django* and *PostgreSQL*.  
It is currently under development and features like user profiles, post creation with images, post editing, post deletion, commenting, ticket creation for support, sending tickets via email, and search functionality are being added step by step.

این یک پروژه پلتفرم بلاگ است که با *Django* و *PostgreSQL* ساخته شده است.  
این پروژه در حال توسعه است و ویژگی‌هایی مانند پروفایل کاربران، ایجاد پست به همراه تصویر، ویرایش پست، حذف پست، کامنت‌گذاری، ثبت تیکت برای پشتیبانی و ارسال تیکت به ایمیل و قابلیت جستجو را دارد.

## Features / ویژگی‌ها

- [x] User registration and login / ثبت‌نام و ورود کاربران  
- [x] Blog posts management (create, edit, delete) / مدیریت پست‌های بلاگ (ایجاد، ویرایش، حذف)  
- [x] Post categories / دسته‌بندی پست‌ها  
- [x] Post comments / کامنت‌گذاری روی پست‌ها  
- [x] Create posts with images / ایجاد پست به همراه تصویر  
- [x] Ticket creation for support / ثبت تیکت برای پشتیبانی  
- [x] Send tickets via email / ارسال تیکت به ایمیل  
- [ ] Post search functionality / قابلیت جستجوی پست‌ها  
- [ ] User profiles / پروفایل‌های کاربران  

## Installation / نصب

To run this project locally, follow these steps:

برای اجرای این پروژه به‌صورت محلی، مراحل زیر را دنبال کنید:

1. Clone the repository

```bash
git clone https://github.com/fatemefarajian/blog_project.git
cd blog_project

2. Install the dependencies



pip install -r requirements.txt

3. Set up PostgreSQL database



Make sure you have PostgreSQL installed on your machine. Create a database and user for the project, then configure the database settings in settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

4. Apply migrations



python manage.py migrate

5. Run the development server



python manage.py runserver

Then open your browser and go to:

سپس مرورگر خود را باز کنید و به آدرس زیر بروید:

http://127.0.0.1:8000/

Technologies Used / تکنولوژی‌های استفاده‌شده

Python 3

Django

PostgreSQL

Django Jalaali (for Persian calendar support)

HTML & CSS

JavaScript (for interactivity)


Status / وضعیت پروژه

This project is a work in progress.


این پروژه در حال توسعه است.


Author / نویسنده
 Fateme Farajian
