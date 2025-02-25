# Flight Ticket Booking System

## Project Overview
This project is a Django-based flight ticket booking system that allows users to book flights, manage orders, and receive tickets via email.

## Features
- **JWT Authentication**
- **Flight Management**: Create, list, and retrieve flight details.
- **Airplane & Route Management**: Manage airplanes and flight routes efficiently.
- **Order Processing**: Users can book tickets for available flights.
- **PDF Ticket Generation**: Automatically generate a PDF ticket upon booking.
- **Email Notifications**: Send tickets via email after booking.

## Installation



### Setup Instructions
```sh
# Clone the repository
git clone https://github.com/VovaGld/API-airport.git
cd api-airport

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Run the development server
python manage.py runserver
```


## API Documentation
API endpoints are documented using **drf-spectacular**:
```
http://127.0.0.1:8000/api/schema/swagger/
```

