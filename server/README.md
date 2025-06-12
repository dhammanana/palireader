# Nissaya Translation Viewer

A Flask web application to view and navigate Pali text translations with their original sources.

## Features

- Modular Flask application using SQLAlchemy ORM
- Two navigation approaches:
  - Select a channel first, then see available books
  - Select a book first, then see available translation channels
- Display original Pali sentences alongside their translations
- Parse and display nissaya format translations
- Clean, responsive UI with modern design

## Project Structure

```
nissaya_translation_app/
│
├── app/
│   ├── __init__.py          # Application factory
│   ├── config.py            # Configuration settings
│   ├── models/              # SQLAlchemy models
│   ├── controllers/         # Route handlers
│   ├── services/            # Business logic
│   ├── static/              # Static files (CSS, JS, images)
│   └── templates/           # Jinja2 templates
│
├── migrations/              # Alembic migration files 
│
├── requirements.txt         # Project dependencies
└── run.py                   # Application entry point
```

## Setup Instructions

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Initialize the database:
   ```
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```
5. Run the application:
   ```
   python run.py
   ```
   
The application will be available at http://localhost:5000

## Database Migration to PostgreSQL

To switch from SQLite to PostgreSQL:

1. Install PostgreSQL and create a new database
2. Update the `SQLALCHEMY_DATABASE_URI` in `app/config.py` to use PostgreSQL:
   ```python
   SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/database_name'
   ```
3. Run database migrations:
   ```
   flask db migrate -m "Migrate to PostgreSQL"
   flask db upgrade
   ```

## License

[MIT License](LICENSE)