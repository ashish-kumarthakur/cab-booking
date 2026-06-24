# Quick Start Guide - See Live Preview

## Step 1: Create Frontend Environment File

Create `frontend/.env.local` with minimal configuration:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_placeholder
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_key_here
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_placeholder
```

**Note:** For full functionality, you'll need real API keys from:
- Clerk: https://clerk.com (for authentication)
- Google Maps: https://console.cloud.google.com (for maps)
- Stripe: https://stripe.com (for payments)

## Step 2: Start Frontend (Quick Preview)

```bash
cd frontend
npm run dev
```

Then open: **http://localhost:3000**

## Step 3: Start Backend (For Full Functionality)

### Option A: Docker (Easiest)
```bash
cd backend
docker-compose up -d
```

### Option B: Manual Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Create .env file with your database and API keys
uvicorn app.main:app --reload
```

Backend will run at: **http://localhost:8000**
API Docs: **http://localhost:8000/docs**

## What You'll See

### Frontend Only (Without Backend)
- UI will load
- Authentication pages (sign-in/sign-up)
- Map component (if Google Maps key is set)
- Some features won't work without backend

### Full Stack (Frontend + Backend)
- Complete ride booking flow
- Real-time updates
- Payment processing
- All features functional

## Troubleshooting

1. **Port 3000 already in use?**
   - Change port: `npm run dev -- -p 3001`

2. **Clerk errors?**
   - Create account at https://clerk.com
   - Get publishable key from dashboard
   - Add to `.env.local`

3. **Google Maps not loading?**
   - Get API key from Google Cloud Console
   - Enable "Maps JavaScript API"
   - Add to `.env.local`

4. **Backend connection errors?**
   - Make sure backend is running on port 8000
   - Check `NEXT_PUBLIC_API_URL` in `.env.local`


