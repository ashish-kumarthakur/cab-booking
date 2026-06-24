# Project Structure

## Backend (FastAPI)

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   │
│   ├── api/                    # API layer
│   │   └── v1/
│   │       ├── router.py       # Main API router
│   │       └── endpoints/      # API endpoints
│   │           ├── auth.py     # Authentication endpoints
│   │           ├── users.py    # User management
│   │           ├── drivers.py  # Driver registration & status
│   │           ├── rides.py    # Ride booking & management
│   │           ├── payments.py # Payment processing
│   │           ├── reviews.py  # Reviews & ratings
│   │           └── websocket.py # WebSocket endpoints
│   │
│   ├── core/                   # Core configuration
│   │   ├── config.py           # Settings & environment variables
│   │   ├── database.py         # Database connection & session
│   │   └── security.py         # JWT & authentication
│   │
│   ├── models/                 # SQLAlchemy models
│   │   ├── user.py             # User model
│   │   ├── driver.py           # Driver model
│   │   ├── ride.py             # Ride model
│   │   ├── payment.py          # Payment model
│   │   └── review.py           # Review model
│   │
│   ├── schemas/                # Pydantic schemas
│   │   ├── user.py             # User request/response schemas
│   │   ├── ride.py             # Ride schemas
│   │   ├── payment.py          # Payment schemas
│   │   └── review.py           # Review schemas
│   │
│   ├── services/               # Business logic services
│   │   ├── maps.py             # Google Maps integration
│   │   └── payment.py          # Stripe integration
│   │
│   └── tasks/                  # Celery background tasks
│       ├── celery_app.py       # Celery configuration
│       └── receipts.py         # Receipt generation tasks
│
├── alembic/                    # Database migrations
│   ├── env.py
│   └── versions/
│
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose setup
├── alembic.ini                 # Alembic configuration
├── .env.example               # Environment variables template
├── setup.sh                   # Setup script (Linux/Mac)
├── setup.bat                  # Setup script (Windows)
└── README.md                  # Backend documentation
```

## Frontend (Next.js)

```
frontend/
├── app/                        # Next.js App Router
│   ├── layout.tsx             # Root layout
│   ├── page.tsx               # Home page
│   ├── globals.css            # Global styles
│   ├── providers.tsx          # Clerk provider wrapper
│   ├── sign-in/               # Sign in page
│   └── sign-up/               # Sign up page
│
├── components/                # React components
│   ├── MapComponent.tsx       # Google Maps component
│   ├── RideBookingForm.tsx    # Ride booking form
│   └── RideStatus.tsx         # Ride status display
│
├── lib/                       # Utilities
│   └── api.ts                 # API client
│
├── hooks/                     # Custom React hooks
│   └── useAuth.ts             # Authentication hook
│
├── public/                    # Static assets
│
├── package.json               # Node dependencies
├── tsconfig.json              # TypeScript configuration
├── next.config.js             # Next.js configuration
├── tailwind.config.js         # Tailwind CSS configuration
├── postcss.config.js          # PostCSS configuration
├── .env.example              # Environment variables template
├── setup.sh                  # Setup script (Linux/Mac)
├── setup.bat                 # Setup script (Windows)
└── README.md                 # Frontend documentation
```

## Key Files

### Backend
- `app/main.py` - FastAPI application entry point
- `app/core/config.py` - Configuration management
- `app/core/database.py` - Database connection
- `app/models/` - Database models (SQLAlchemy)
- `app/api/v1/endpoints/` - REST API endpoints
- `app/services/` - Business logic services

### Frontend
- `app/page.tsx` - Main application page
- `components/` - Reusable React components
- `lib/api.ts` - API client for backend communication
- `hooks/useAuth.ts` - Authentication hook

## Database Schema

### Users Table
- id (UUID)
- name, email, phone
- role (rider/driver/admin)
- rating_avg, wallet_balance

### Drivers Table
- id (UUID)
- user_id (FK to users)
- vehicle_info, vehicle_number, license_number
- verified (boolean)
- current_location (PostGIS Point)
- status (active/offline/on_ride)

### Rides Table
- id (UUID)
- rider_id, driver_id (FK to users)
- pickup_point, drop_point (PostGIS Points)
- pickup_address, drop_address
- status, fare_estimate, fare_actual
- distance_meters, duration_secs
- created_at, started_at, completed_at

### Payments Table
- id (UUID)
- ride_id (FK to rides)
- stripe_payment_intent_id
- amount, currency, status
- created_at, completed_at

### Reviews Table
- id (UUID)
- ride_id (FK to rides)
- rater_id, rated_id (FK to users)
- rating (1-5), comment
- created_at


