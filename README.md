# Sola-Thomas LLC Website

A Django-based website for Sola-Thomas LLC, providing IT services and consulting solutions.

## Requirements

- Python 3.8+
- Django 4.2+
- PostgreSQL
- Node.js (for frontend assets)

## Setup

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Initialize the database:
```bash
python manage.py migrate
python manage.py createsuperuser
```

```bash 
python manage.py collectstatic
```

5. Run the development server:
```bash
python manage.py runserver
```

Visit http://localhost:8000 to view the site.

## Development

- Run tests: `python manage.py test`
- Check code style: `flake8`
- Generate migrations: `python manage.py makemigrations`

## Deployment

See `docs/DEPLOYMENT.md` for detailed deployment instructions.

## License

Copyright © 2024 Sola-Thomas LLC. All rights reserved.
