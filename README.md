# Car Service Management System

A full-stack Tkinter application for managing car service operations with PostgreSQL database connectivity.

## Prerequisites

- Python 3.8 or higher
- PostgreSQL server
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd car-service-management
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your PostgreSQL credentials:
```env
DB_NAME=car_service
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

5. Create the database in PostgreSQL:
```sql
CREATE DATABASE car_service;
```

## Running the Application

1. Make sure your PostgreSQL server is running
2. Run the application:
```bash
python main.py
```

## Features

- Customer Management
  - Add new customers
  - View customer list
  - Delete customers

- Car Management
  - Add new cars
  - View car list
  - Delete cars

- Staff Management
  - Add new staff members
  - View staff list
  - Delete staff members

## Database Schema

The application uses the following main tables:
- Contact
- Customer
- Car
- Staff
- StaffDetail
- ServiceCategory
- And more...

## Error Handling

The application includes comprehensive error handling for:
- Database connection issues
- Invalid input data
- Failed operations
- Missing required fields

## Security

- Database credentials are stored in environment variables
- Input validation for all user inputs
- Proper error messages without exposing sensitive information

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 