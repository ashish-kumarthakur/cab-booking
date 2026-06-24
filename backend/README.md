# Cab Booking Backend API

FastAPI backend for the Cab Booking Platform.

## Features

- FastAPI with async/await support
- PostgreSQL with PostGIS for geospatial queries
- JWT authentication (Clerk/Supabase compatible)
- Real-time updates via WebSocket (Socket.IO)
- Stripe payment integration
- Celery for background tasks
- Google Maps integration for distance/fare calculation

## Setup

### Prerequisites

- Python 3.11+
- PostgreSQL with PostGIS extension
- Redis
- Docker (optional, for containerized setup)

### Installation

1. Create virtual environment:
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

4. Set up database:
```bash
# Make sure PostgreSQL is running with PostGIS extension
# Create database: createdb cab_booking
# Enable PostGIS: psql -d cab_booking -c "CREATE EXTENSION postgis;"
```

5. Run migrations (when using Alembic):
```bash
alembic upgrade head
```

6. Run the server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

## Docker Setup

```bash
docker-compose up -d
```

This will start:
- PostgreSQL with PostGIS
- Redis
- FastAPI backend
- Celery worker

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       └── router.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── tasks/
├── alembic/
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## API Endpoints

- `POST /api/auth/session` - Verify authentication token
- `GET /api/users/me` - Get current user
- `GET /api/rides/estimate` - Get fare estimate
- `POST /api/rides/request` - Create ride request
- `GET /api/rides/{id}` - Get ride details
- `GET /api/rides/nearby/drivers` - Find nearby drivers
- `POST /api/payments/create-intent` - Create payment intent
- `POST /api/payments/webhooks/stripe` - Stripe webhook
- `POST /api/reviews/` - Create review

## Environment Variables

See `.env.example` for all required environment variables.

## Testing

```bash
pytest
```

## License

MIT


