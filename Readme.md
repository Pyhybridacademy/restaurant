# Restaurant Management System

A full-stack restaurant website built with Django, Django REST Framework, and React (via CDN). Features include menu browsing, cart management, order processing with manual payment verification, and a comprehensive admin interface.

## Features

### Customer Features
- **Menu Browsing**: Browse food items by category with search and filtering
- **Shopping Cart**: Add items to cart, modify quantities, and manage orders
- **User Authentication**: Register, login, and manage user accounts
- **Order Management**: Place orders, upload payment receipts, and track order status
- **Order Tracking**: Real-time order status updates with estimated delivery times

### Admin Features
- **Dashboard**: Comprehensive overview with order statistics and analytics
- **Order Management**: Process orders, update status, and manage payments
- **Menu Management**: Add/edit food items, categories, and availability
- **Customer Management**: View customer information and order history
- **Receipt Verification**: View and verify uploaded payment receipts

## Technology Stack

- **Backend**: Django 4.2, Django REST Framework
- **Frontend**: React 18 (via CDN), Tailwind CSS
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Authentication**: Django's built-in authentication system
- **File Storage**: Local storage (development), cloud storage ready

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Quick Start

1. **Clone and Setup**
   \`\`\`bash
   git clone <repository-url>
   cd restaurant-django
   pip install -r requirements.txt
   \`\`\`

2. **Database Setup**
   \`\`\`bash
   python scripts/setup_database.py
   \`\`\`
   This script will:
   - Create database migrations
   - Apply migrations
   - Create a superuser (optional)
   - Populate sample menu data

3. **Run Development Server**
   \`\`\`bash
   python manage.py runserver
   \`\`\`

4. **Access the Application**
   - Website: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/
   - API Endpoints: http://127.0.0.1:8000/api/

### Manual Setup (Alternative)

If you prefer manual setup:

\`\`\`bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Populate sample data
python manage.py populate_menu

# Run server
python manage.py runserver
\`\`\`

## Project Structure

\`\`\`
restaurant-django/
├── restaurant_site/          # Main Django project
│   ├── settings.py           # Django settings
│   ├── urls.py              # Main URL configuration
│   └── admin.py             # Custom admin site
├── account/                  # User authentication app
├── menu/                     # Menu and food items app
├── cart/                     # Shopping cart app
├── order/                    # Order processing app
├── templates/               # HTML templates
│   ├── base.html            # Base template with React CDN
│   ├── menu/                # Menu page templates
│   ├── cart/                # Cart page templates
│   ├── order/               # Order page templates
│   └── account/             # Authentication templates
├── scripts/                 # Utility scripts
├── static/                  # Static files
├── media/                   # User uploaded files
└── requirements.txt         # Python dependencies
\`\`\`

## API Endpoints

### Menu API
- `GET /menu/api/categories/` - List all categories
- `GET /menu/api/foods/` - List all available foods
- `GET /menu/api/foods/category/<id>/` - Foods by category

### Cart API
- `GET /cart/api/items/` - Get cart items
- `POST /cart/api/add/` - Add item to cart
- `PUT /cart/api/update/<id>/` - Update cart item quantity
- `DELETE /cart/api/remove/<id>/` - Remove item from cart

### Order API
- `POST /order/api/checkout/` - Create new order
- `GET /order/api/status/<id>/` - Get order status
- `GET /order/api/list/` - List user orders
- `POST /order/api/cancel/<id>/` - Cancel order

### Account API
- `POST /account/api/register/` - User registration
- `POST /account/api/login/` - User login
- `POST /account/api/logout/` - User logout
- `GET /account/api/profile/` - Get user profile

## Configuration

### Environment Variables

Create a `.env` file in the project root:

\`\`\`env
SECRET_KEY=your-secret-key-here
DEBUG=True
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@restaurant.com
\`\`\`

### Email Configuration

For production, configure email settings to send order confirmations:

1. Set up an email service (Gmail, SendGrid, etc.)
2. Update email settings in `.env`
3. Change `EMAIL_BACKEND` to `django.core.mail.backends.smtp.EmailBackend`

## Usage

### For Customers

1. **Browse Menu**: Visit the homepage and click "View Menu"
2. **Add to Cart**: Click "Add to Cart" on any food item
3. **Checkout**: Go to cart and click "Proceed to Checkout"
4. **Payment**: Fill in details and upload payment receipt
5. **Track Order**: Use the tracking link or "My Orders" page

### For Restaurant Staff

1. **Access Admin**: Go to `/admin/` and login with superuser credentials
2. **Dashboard**: View order statistics and pending orders
3. **Manage Orders**: Update order status, view receipts
4. **Manage Menu**: Add/edit food items and categories
5. **Customer Service**: View customer details and order history

## Customization

### Adding New Food Items

1. Go to Admin Panel → Menu → Foods
2. Click "Add Food"
3. Fill in details and upload image
4. Set availability status

### Managing Orders

1. Go to Admin Panel → Orders → Orders
2. Click on any order to view details
3. Update status using the dropdown
4. Use bulk actions for multiple orders

### Customizing Templates

Templates use React components with Tailwind CSS. Edit files in `templates/` directory to customize the UI.

## Deployment

### Vercel Deployment

1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel`
3. Configure environment variables in Vercel dashboard
4. Set up PostgreSQL database (recommended: Neon, Supabase)

### Traditional Hosting

1. Set `DEBUG=False` in production
2. Configure `ALLOWED_HOSTS`
3. Set up PostgreSQL database
4. Configure static file serving
5. Set up email service

## Support

For issues and questions:
1. Check the Django documentation
2. Review the code comments
3. Test with sample data provided

## License

This project is open source and available under the MIT License.
