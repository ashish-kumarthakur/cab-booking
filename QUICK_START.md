# Quick Start Guide

## Prerequisites

Before you begin, ensure you have:

- **Python 3.11+** installed
- **Node.js 18+** installed
- **PostgreSQL** with PostGIS extension
- **Redis** server
- **Docker** (optional, for containerized setup)

## Quick Setup (5 minutes)

### Option 1: Docker (Recommended)

1. **Backend Setup:**
```bash
cd backend
docker-compose up -d
```

This will start:
- PostgreSQL with PostGIS
- Redis
- FastAPI backend (http://localhost:8000)
- Celery worker

2. **Frontend Setup:**
```bash
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local with your API keys
npm run dev
```

Frontend will be available at http://localhost:3000

### Option 2: Manual Setup

#### Backend

1. **Navigate to backend:**
```bash
cd backend
```

2. **Run setup script:**
```bash
# Linux/Mac
chmod +x setup.sh
./setup.sh

# Windows
setup.bat
```

3. **Configure environment:**
```bash
# Edit .env file with your keys:
# - DATABASE_URL
# - REDIS_URL
# - JWT_SECRET_KEY
# - STRIPE_SECRET_KEY
# - GOOGLE_MAPS_API_KEY
```

4. **Set up database:**
```bash
# Create database
createdb cab_booking

# Enable PostGIS
psql -d cab_booking -c "CREATE EXTENSION postgis;"
```

5. **Start backend:**
```bash
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn app.main:app --reload
```

#### Frontend

1. **Navigate to frontend:**
```bash
cd frontend
```

2. **Run setup script:**
```bash
# Linux/Mac
chmod +x setup.sh
./setup.sh

# Windows
setup.bat
```

3. **Configure environment:**
```bash
# Edit .env.local with your keys:
# - NEXT_PUBLIC_API_URL=http://localhost:8000
# - NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY
# - NEXT_PUBLIC_GOOGLE_MAPS_API_KEY
# - NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY
```

4. **Start frontend:**
```bash
npm run dev
```

## Getting API Keys

### 1. Clerk (Authentication)
- Sign up at https://clerk.com
- Create a new application
- Copy publishable key and secret key

### 2. Google Maps
- Go to https://console.cloud.google.com
- Create a new project
- Enable Maps JavaScript API and Distance Matrix API
- Create API key

### 3. Stripe
- Sign up at https://stripe.com
- Get test API keys from dashboard
- Set up webhook endpoint: `http://localhost:8000/api/payments/webhooks/stripe`

### 4. Supabase (Alternative to Clerk)
- Sign up at https://supabase.com
- Create a new project
- Get URL and anon key from project settings

## Testing the Application

1. **Start backend:**
```bash
cd backend
uvicorn app.main:app --reload
```

2. **Start frontend:**
```bash
cd frontend
npm run dev
```

3. **Access the app:**
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

4. **Test flow:**
   - Sign up/Sign in
   - Book a ride
   - View ride status
   - Complete payment
   - Leave a review

## Common Issues

### PostgreSQL Connection Error
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- Verify PostGIS extension is installed

### Redis Connection Error
- Ensure Redis is running: `redis-cli ping`
- Check REDIS_URL in .env

### Google Maps Not Loading
- Verify API key is set in frontend .env.local
- Check browser console for errors
- Ensure Maps JavaScript API is enabled

### Authentication Not Working
- Verify Clerk keys are correct
- Check middleware configuration
- Ensure CORS is properly configured

## Next Steps

1. **Customize fare calculation** in `backend/app/services/maps.py`
2. **Add driver matching logic** in `backend/app/api/v1/endpoints/rides.py`
3. **Implement email service** in `backend/app/tasks/receipts.py`
4. **Add more features:**
   - Promo codes
   - Ride scheduling
   - Multiple payment methods
   - Push notifications

## Production Deployment

### Backend
- Use managed PostgreSQL (Supabase, AWS RDS)
- Use managed Redis (Redis Cloud, AWS ElastiCache)
- Deploy to: Render, Railway, AWS ECS, DigitalOcean
- Set up environment variables
- Configure CORS for production domain

### Frontend
- Deploy to Vercel (recommended)
- Set production environment variables
- Configure Clerk for production domain
- Set up Stripe webhook for production URL

## Support

For issues or questions:
1. Check the README.md files
2. Review API documentation at /docs
3. Check logs for error messages
4. Open an issue on GitHub


