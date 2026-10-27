# Industrial IoT Monitoring System

## Overview
A Django-based application for monitoring industrial machines, tracking temperatures, and identifying alerts.

## Technologies
- Python
- Django
- Django REST Framework
- SQLite
- HTML, CSS, JavaScript
- Postman

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /api/machines/ | List machines with pagination |
| POST | /api/machines/ | Create a machine |
| GET | /api/machines/M001/ | Retrieve one machine |
| PUT | /api/machines/M001/ | Fully update a machine |
| PATCH | /api/machines/M001/ | Partially update a machine |
| DELETE | /api/machines/M001/ | Delete a machine |
| GET | /api/machines/M001/temperature-history/ | View temperature history |
| GET | /api/alerts/ | View temperature alerts |

Replace M001 with the required machine ID.

## Temperature Alert Rules
- Below 60°C: Normal
- 60°C to below 70°C: Warning
- 70°C or above: Critical

## Automated Testing
The project currently has 12 automated tests passing.

## Run Locally
1. Activate the virtual environment.
2. Run `python manage.py migrate`.
3. Run `python manage.py runserver`.
4. Open http://127.0.0.1:8000/
