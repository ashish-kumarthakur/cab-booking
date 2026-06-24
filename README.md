# Cab Booking Platform

A full-stack ride-hailing application built with Python (FastAPI) backend and Next.js frontend.

## Features

- **User Authentication**: Clerk/Supabase Auth integration
- **Ride Booking**: Create ride requests with fare estimation
- **Real-time Updates**: WebSocket support for live ride tracking
- **Payment Processing**: Stripe integration for secure payments
- **Google Maps**: Interactive maps with route visualization
- **Driver Matching**: PostGIS-powered nearby driver search
- **Background Tasks**: Celery for receipt generation and emails
- **Reviews & Ratings**: Rate drivers and riders after rides

## 📁 Project Structure

```
.
├── backend/          # FastAPI backend
│   ├── app/
│   │   ├── api/      # API endpoints
│   │   ├── core/     # Core configuration
│   │   ├── models/   # Database models
│   │   ├── schemas/  # Pydantic schemas
│   │   ├── services/ # Business logic
│   │   └── tasks/    # Celery tasks
│   ├── requirements.txt
│   └── docker-compose.yml
│
└── frontend/         # Next.js frontend
    ├── app/          # Next.js app directory
    ├── components/   # React components
    ├── lib/          # Utilities
    └── hooks/        # Custom hooks
```

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL + PostGIS** - Database with geospatial support
- **Redis** - Caching and message broker
- **Celery** - Background task processing
- **Stripe** - Payment processing
- **Google Maps API** - Distance and routing

### Frontend
- **Next.js 14** - React framework with App Router
- **Tailwind CSS** - Utility-first CSS
- **Clerk** - Authentication
- **Google Maps JS** - Interactive maps
- **Stripe Elements** - Payment UI

##  Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL with PostGIS extension
- Redis
- Docker (optional)

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Set up database:
```bash
# Create database and enable PostGIS
createdb cab_booking
psql -d cab_booking -c "CREATE EXTENSION postgis;"
```

6. Run migrations (when using Alembic):
```bash
alembic upgrade head
```

7. Start the server:
```bash
uvicorn app.main:app --reload
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env.local
# Edit .env.local with your configuration
```

4. Start the development server:
```bash
npm run dev
```

### Docker Setup

Run everything with Docker Compose:

```bash
cd backend
docker-compose up -d
```

This starts:
- PostgreSQL with PostGIS
- Redis
- FastAPI backend
- Celery worker

## 📚 API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🔑 Environment Variables

### Backend (.env)
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `JWT_SECRET_KEY` - JWT secret for token verification
- `STRIPE_SECRET_KEY` - Stripe secret key
- `GOOGLE_MAPS_API_KEY` - Google Maps API key
- `CLERK_SECRET_KEY` or `SUPABASE_KEY` - Auth provider key

### Frontend (.env.local)
- `NEXT_PUBLIC_API_URL` - Backend API URL
- `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` - Clerk publishable key
- `NEXT_PUBLIC_GOOGLE_MAPS_API_KEY` - Google Maps API key
- `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` - Stripe publishable key

## 🧪 Testing

### Backend
```bash
cd backend
pytest
```

## 📖 API Endpoints

### Authentication
- `POST /api/auth/session` - Verify authentication token

### Users
- `GET /api/users/me` - Get current user
- `PUT /api/users/me` - Update user profile

### Rides
- `GET /api/rides/estimate` - Get fare estimate
- `POST /api/rides/request` - Create ride request
- `GET /api/rides/{id}` - Get ride details
- `GET /api/rides` - Get ride history
- `GET /api/rides/nearby/drivers` - Find nearby drivers
- `PUT /api/rides/{id}/status` - Update ride status

### Payments
- `POST /api/payments/create-intent` - Create payment intent
- `POST /api/payments/webhooks/stripe` - Stripe webhook
- `GET /api/payments/{id}` - Get payment details

### Reviews
- `POST /api/reviews` - Create review
- `GET /api/reviews/ride/{ride_id}` - Get ride reviews
- `GET /api/reviews/user/{user_id}` - Get user reviews

### WebSocket
- `WS /api/ws/rider/{rider_id}` - Rider WebSocket connection
- `WS /api/ws/driver/{driver_id}` - Driver WebSocket connection

## 🚢 Deployment

### Backend
- Deploy to: Render, Railway, AWS ECS, DigitalOcean App Platform
- Ensure PostgreSQL with PostGIS and Redis are available
- Set all environment variables

### Frontend
- Deploy to: Vercel (recommended), Netlify, or any static host
- Set environment variables in deployment platform

## 📝 License

MIT

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues and questions, please open an issue on GitHub.

