# Cab Booking Frontend

Next.js frontend for the Cab Booking Platform.

## Features

- Next.js 14 with App Router
- React 18
- Tailwind CSS for styling
- Clerk authentication
- Google Maps integration
- Real-time ride updates
- Stripe payment integration

## Setup

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
# or
yarn install
```

2. Set up environment variables:
```bash
cp .env.example .env.local
# Edit .env.local with your configuration
```

3. Run the development server:
```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Environment Variables

- `NEXT_PUBLIC_API_URL` - Backend API URL
- `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` - Clerk publishable key
- `NEXT_PUBLIC_GOOGLE_MAPS_API_KEY` - Google Maps API key
- `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` - Stripe publishable key

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   └── sign-in/
├── components/
│   ├── MapComponent.tsx
│   ├── RideBookingForm.tsx
│   └── RideStatus.tsx
├── lib/
│   └── api.ts
├── hooks/
│   └── useAuth.ts
└── public/
```

## License

MIT


