# MyBlog

A Django-based blogging platform that enables users to create, manage, and publish blog content through a clean and scalable architecture. The project is designed following Django best practices and serves as a solid foundation for a full-featured content management system.

## Features

- User authentication and authorization
- Create, update, and delete blog posts
- Upload and manage post cover images
- Dynamic URL routing
- Organized static and media file handling
- SQLite(default, easily configurable to PostgreSQL/MySQL) database support
- Scalable application structure

---

## Technology Stack

| Layer | Technology |
|---------|------------|
| Backend | Python, Django |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript |
| Media Handling | Pillow |
| Server | Django Development Server |

---

## Project Structure

```text
myblog/
│
├── core/                         # Main application
│   ├── migrations/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── myblog/                       # Project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── static/                       # Static assets
│   ├── css/
│   └── js/
│
├── post_covers/                  # Uploaded media files
│
├── db.sqlite3
├── manage.py
├── requirements.txt
└── venv/
```

---

## Getting Started

### Prerequisites

Ensure the following tools are installed:

- Python
- pip

---

### Installation

Clone the repository:

```bash
git clone https://github.com/mahmudul58/Blog-Website.git
cd Blog-Website
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

**macOS / Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

Install project dependencies:

```bash
pip install -r requirements.txt
```

Apply database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Create an administrator account:

```bash
python manage.py createsuperuser
```

Start the development server:

```bash
python manage.py runserver
```

---

## Running the Application

After starting the server, visit:

| Service | URL |
|----------|-----|
| Application | http://127.0.0.1:8000 |
| Admin Panel | http://127.0.0.1:8000/admin |

---

## Media and Static Files

### Static Files

Frontend assets are stored inside:

```text
static/
```

Including:

- CSS
- JavaScript
- Images

### Media Files

Uploaded content such as post cover images are stored inside:

```text
post_covers/
```

---

## Database Configuration

The project uses SQLite by default.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

To use MySQL or PostgreSQL, update the `DATABASES` configuration inside:

```text
myblog/settings.py
```

---

## License

This project is intended for educational and learning purposes. Feel free to modify and extend it for personal or academic use.
