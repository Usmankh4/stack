# E-commerce Platform

A modern e-commerce platform built with Django REST Framework (backend) and Next.js (frontend) for selling phones and accessories.

## Features

- **Product Management**: Add, edit, and manage phones and accessories
- **Homepage Sections**: Featured flash deals, new arrivals, and best sellers
- **Responsive Design**: Mobile-friendly interface
- **Stripe Integration**: Secure payment processing
- **Admin Dashboard**: Easy product and order management

## Tech Stack

- **Backend**: Django 4.2+, Django REST Framework, PostgreSQL
- **Frontend**: Next.js 13+, React 18+
- **Styling**: CSS Modules
- **Payment**: Stripe
- **Database**: PostgreSQL

## Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL 13+
- pip (Python package manager)
- npm or yarn

## Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd stack/backend
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   If requirements.txt doesn't exist, install these packages:
   ```bash
   pip install django djangorestframework django-cors-headers pillow stripe psycopg2-binary python-dotenv
   ```

4. **Set up the database**
   - Create a PostgreSQL database
   - Update database settings in `backend/store/settings.py` if needed

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## Frontend Setup

1. **Navigate to the frontend directory**
   ```bash
   cd ../frontend
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Set up environment variables**
   Create a `.env.local` file in the frontend directory with:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000/api/
   NEXT_PUBLIC_STRIPE_PUBLIC_KEY=your_stripe_public_key
   ```

4. **Start the development server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

## Running the Application

1. Start the backend server:
   ```bash
   cd backend
   python manage.py runserver
   ```

2. In a new terminal, start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

3. Access the application at `http://localhost:3000`
4. Access the admin panel at `http://localhost:8000/admin`

## API Endpoints

- `GET /api/homepage/` - Get all homepage sections
- `GET /api/flash-deals/` - Get flash deals
- `GET /api/new-arrivals/` - Get new arrivals
- `GET /api/best-sellers/` - Get best sellers
- `GET /api/phones/<slug>/` - Get phone details
- `GET /api/accessories/<slug>/` - Get accessory details

## Environment Variables

### Backend
- `SECRET_KEY` - Django secret key
- `DEBUG` - Set to `True` in development, `False` in production
- `DATABASE_URL` - PostgreSQL database URL
- `STRIPE_SECRET_KEY` - Stripe secret key
- `STRIPE_PUBLISHABLE_KEY` - Stripe publishable key

### Frontend
- `NEXT_PUBLIC_API_URL` - Backend API URL
- `NEXT_PUBLIC_STRIPE_PUBLIC_KEY` - Stripe publishable key

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
