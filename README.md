# FinSight - Personal Finance Manager

A modern personal finance management application built with Django, PostgreSQL, and Svelte.

## Features (Planned)

- Transaction tracking and categorization
- Budget planning and monitoring
- Financial goals tracking
- Expense analytics and reporting
- Multi-currency support
- Secure user authentication
- REST API backend
- Modern reactive frontend

## Tech Stack

### Backend
- Python 3.11
- Django 5.0
- Django REST Framework
- PostgreSQL 15
- Celery (for background tasks)
- Redis (for caching and Celery broker)

### Frontend
- Svelte
- TypeScript
- TailwindCSS
- Chart.js (for financial visualizations)

## Development Setup

### Prerequisites
- Docker
- Docker Compose

### Getting Started

1. Clone the repository:
```bash
git clone <repository-url>
cd finsight
```

2. Start the development environment:
```bash
docker compose up --build
```

3. Access the applications:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/api/docs/

## Project Structure

```
finsight/
├── backend/             # Django backend
│   ├── api/            # REST API endpoints
│   ├── core/           # Core application logic
│   └── config/         # Django settings
├── frontend/           # Svelte frontend
│   ├── src/           # Source code
│   └── public/        # Static files
└── docker/            # Docker configuration
```

## Contributing

1. Create a feature branch
2. Commit your changes
3. Push to the branch
4. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
