import psycopg2
from psycopg2 import Error
from typing import List, Tuple, Optional
import os
from dotenv import load_dotenv

class DatabaseConnection:
    def __init__(self):
        load_dotenv()
        self.conn = None
        self.cursor = None
        self.db_params = {
            'dbname': os.getenv('DB_NAME', 'car_service'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', ''),
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432')
        }

    def connect(self):
        """Establish connection to the PostgreSQL database"""
        try:
            self.conn = psycopg2.connect(**self.db_params)
            self.cursor = self.conn.cursor()
            print("Successfully connected to PostgreSQL database")
            return True
        except Error as e:
            print(f"Database connection error: {e}")
            print("Please check your database credentials in the .env file")
            print("Current connection parameters:", self.db_params)
            return False

    def close(self):
        """Close the database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def execute_query(self, query: str, params: tuple = None) -> bool:
        """Execute a query that doesn't return results"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
            return True
        except Error as e:
            print(f"Query execution error: {e}")
            self.conn.rollback()
            return False

    def fetch_all(self, query: str, params: tuple = None) -> List[Tuple]:
        """Execute a query and return all results"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Fetch error: {e}")
            return []

    def fetch_one(self, query: str, params: tuple = None) -> Optional[Tuple]:
        """Execute a query and return one result"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchone()
        except Error as e:
            print(f"Fetch error: {e}")
            return None

    def create_tables(self):
        """Create all necessary tables"""
        try:
            # Check if tables exist
            self.cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            existing_tables = [table[0] for table in self.cursor.fetchall()]
            
            queries = [
                """CREATE TABLE IF NOT EXISTS Contact (
                    contact_id SERIAL PRIMARY KEY,
                    email VARCHAR(100) UNIQUE NOT NULL
                )""",
                """CREATE TABLE IF NOT EXISTS ContactPhone (
                    contact_id INTEGER NOT NULL,
                    phone_number VARCHAR(15) NOT NULL,
                    PRIMARY KEY (contact_id, phone_number),
                    FOREIGN KEY (contact_id) REFERENCES Contact(contact_id) ON DELETE CASCADE
                )""",
                """CREATE TABLE IF NOT EXISTS Identity (
                    identity_id SERIAL PRIMARY KEY,
                    id_number VARCHAR(20) UNIQUE NOT NULL,
                    issued_date DATE NOT NULL
                )""",
                """CREATE TABLE IF NOT EXISTS Customer (
                    customer_id SERIAL PRIMARY KEY,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    contact_id INTEGER NOT NULL,
                    identity_id INTEGER NOT NULL,
                    FOREIGN KEY (contact_id) REFERENCES Contact(contact_id) ON DELETE CASCADE,
                    FOREIGN KEY (identity_id) REFERENCES Identity(identity_id) ON DELETE CASCADE
                )""",
                """CREATE TABLE IF NOT EXISTS Staff (
                    staff_id SERIAL PRIMARY KEY,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    role VARCHAR(50) NOT NULL,
                    contact_id INTEGER NOT NULL,
                    FOREIGN KEY (contact_id) REFERENCES Contact(contact_id) ON DELETE CASCADE
                )""",
                """CREATE TABLE IF NOT EXISTS StaffDetail (
                    staff_id INTEGER PRIMARY KEY,
                    address TEXT NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    join_date DATE NOT NULL,
                    full_details TEXT,
                    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id) ON DELETE CASCADE
                )""",
                """CREATE TABLE IF NOT EXISTS Admin (
                    admin_id SERIAL PRIMARY KEY,
                    staff_id INTEGER UNIQUE,
                    customer_id INTEGER UNIQUE,
                    username VARCHAR(50) NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    role VARCHAR(20) NOT NULL,
                    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id) ON DELETE SET NULL,
                    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) ON DELETE SET NULL
                )""",
                """CREATE TABLE IF NOT EXISTS Car (
                    car_id SERIAL PRIMARY KEY,
                    model VARCHAR(50) NOT NULL,
                    brand VARCHAR(50) NOT NULL,
                    number_plate VARCHAR(20) UNIQUE NOT NULL,
                    customer_id INTEGER NOT NULL,
                    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) ON DELETE CASCADE
                )""",
                """CREATE TABLE IF NOT EXISTS Discount (
                    discount_id SERIAL PRIMARY KEY,
                    percentage_discount DECIMAL(5,2) NOT NULL
                )""",
                """CREATE TABLE IF NOT EXISTS Payment (
                    payment_id SERIAL PRIMARY KEY,
                    amount DECIMAL(10,2) NOT NULL,
                    discount_id INTEGER,
                    status VARCHAR(20) CHECK (status IN ('Completed', 'Pending', 'Failed')),
                    FOREIGN KEY (discount_id) REFERENCES Discount(discount_id) ON DELETE SET NULL
                )""",
                """CREATE TABLE IF NOT EXISTS Feedback (
                    feedback_id SERIAL PRIMARY KEY,
                    customer_id INTEGER NOT NULL,
                    comments TEXT NOT NULL,
                    feedback_date DATE NOT NULL,
                    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
                    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) ON DELETE CASCADE
                )""",
                """CREATE TABLE IF NOT EXISTS ServiceCategory (
                    servicecategory_id SERIAL PRIMARY KEY,
                    category_name VARCHAR(100) UNIQUE NOT NULL
                )""",
                """CREATE TABLE IF NOT EXISTS VehicleList (
                    vehiclelist_id SERIAL PRIMARY KEY,
                    number_plate VARCHAR(20) NOT NULL,
                    servicecategory_id INTEGER NOT NULL,
                    registration_date DATE NOT NULL,
                    vehicle_type VARCHAR(50),
                    FOREIGN KEY (number_plate) REFERENCES Car(number_plate) ON DELETE CASCADE,
                    FOREIGN KEY (servicecategory_id) REFERENCES ServiceCategory(servicecategory_id) ON DELETE CASCADE
                )""",
                """CREATE TABLE IF NOT EXISTS Sparepart (
                    sparepart_id SERIAL PRIMARY KEY,
                    part_name VARCHAR(100) NOT NULL,
                    price DECIMAL(10,2) NOT NULL
                )""",
                """CREATE TABLE IF NOT EXISTS Report (
                    report_id SERIAL PRIMARY KEY,
                    report_date DATE NOT NULL,
                    description_text TEXT NOT NULL,
                    staff_id INTEGER NOT NULL,
                    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id) ON DELETE CASCADE
                )""",
                """CREATE TABLE IF NOT EXISTS ServiceComplete (
                    servicecomplete_id SERIAL PRIMARY KEY,
                    time_completion TIME NOT NULL,
                    customer_id INTEGER NOT NULL,
                    completion_date DATE NOT NULL,
                    staff_id INTEGER NOT NULL,
                    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) ON DELETE CASCADE,
                    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id) ON DELETE CASCADE
                )""",
                """CREATE TABLE IF NOT EXISTS Emergency (
                    emergency_id SERIAL PRIMARY KEY,
                    phone_number VARCHAR(15) UNIQUE NOT NULL
                )"""
            ]

            for query in queries:
                self.execute_query(query)
            
            print("Tables created successfully")
            return True
        except Error as e:
            print(f"Error creating tables: {e}")
            return False

    def insert_sample_data(self):
        """Insert sample data into the database"""
        try:
            # Insert sample data for Contact
            self.execute_query("INSERT INTO Contact (email) VALUES (%s) ON CONFLICT DO NOTHING", ("john.doe@email.com",))
            self.execute_query("INSERT INTO Contact (email) VALUES (%s) ON CONFLICT DO NOTHING", ("jane.smith@email.com",))
            
            # Insert sample data for Customer
            self.execute_query("""
                INSERT INTO Customer (first_name, last_name, contact_id, identity_id)
                VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING
            """, ("John", "Doe", 1, 1))
            
            # Insert sample data for Car
            self.execute_query("""
                INSERT INTO Car (model, brand, number_plate, customer_id)
                VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING
            """, ("Civic", "Honda", "TN10AB1234", 1))
            
            # Insert sample data for ServiceCategory
            self.execute_query("""
                INSERT INTO ServiceCategory (category_name)
                VALUES (%s) ON CONFLICT DO NOTHING
            """, ("Oil Change",))
            
            # Insert sample data for Staff
            self.execute_query("""
                INSERT INTO Staff (first_name, last_name, role, contact_id)
                VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING
            """, ("Michael", "Scott", "Manager", 1))
            
            print("Sample data inserted successfully")
            return True
        except Error as e:
            print(f"Error inserting sample data: {e}")
            return False

    def get_customers(self) -> List[Tuple]:
        """Get all customers"""
        return self.fetch_all("""
            SELECT c.customer_id, c.first_name, c.last_name, co.email
            FROM Customer c
            JOIN Contact co ON c.contact_id = co.contact_id
        """)

    def get_cars(self) -> List[Tuple]:
        """Get all cars"""
        return self.fetch_all("""
            SELECT car_id, model, brand, number_plate, customer_id
            FROM Car
        """)

    def get_staff(self) -> List[Tuple]:
        """Get all staff members"""
        return self.fetch_all("""
            SELECT s.staff_id, s.first_name, s.last_name, s.role, sd.email
            FROM Staff s
            JOIN StaffDetail sd ON s.staff_id = sd.staff_id
        """)

    def add_customer(self, first_name: str, last_name: str, email: str) -> bool:
        """Add a new customer"""
        try:
            # Start transaction
            self.cursor.execute("BEGIN")
            
            # Insert contact
            self.cursor.execute(
                "INSERT INTO Contact (email) VALUES (%s) RETURNING contact_id",
                (email,)
            )
            contact_id = self.cursor.fetchone()[0]
            
            # Insert identity
            self.cursor.execute(
                "INSERT INTO Identity (id_number, issued_date) VALUES (%s, CURRENT_DATE) RETURNING identity_id",
                (f"ID{contact_id}",)
            )
            identity_id = self.cursor.fetchone()[0]
            
            # Insert customer
            self.cursor.execute(
                "INSERT INTO Customer (first_name, last_name, contact_id, identity_id) VALUES (%s, %s, %s, %s)",
                (first_name, last_name, contact_id, identity_id)
            )
            
            self.conn.commit()
            return True
        except Error as e:
            self.conn.rollback()
            print(f"Error adding customer: {e}")
            return False

    def add_car(self, model: str, brand: str, number_plate: str, customer_id: int) -> bool:
        """Add a new car"""
        return self.execute_query("""
            INSERT INTO Car (model, brand, number_plate, customer_id)
            VALUES (%s, %s, %s, %s)
        """, (model, brand, number_plate, customer_id))

    def add_staff(self, first_name: str, last_name: str, role: str, email: str, address: str) -> bool:
        """Add a new staff member"""
        try:
            # Start transaction
            self.cursor.execute("BEGIN")
            
            # Insert contact
            self.cursor.execute(
                "INSERT INTO Contact (email) VALUES (%s) RETURNING contact_id",
                (email,)
            )
            contact_id = self.cursor.fetchone()[0]
            
            # Insert staff
            self.cursor.execute(
                "INSERT INTO Staff (first_name, last_name, role, contact_id) VALUES (%s, %s, %s, %s) RETURNING staff_id",
                (first_name, last_name, role, contact_id)
            )
            staff_id = self.cursor.fetchone()[0]
            
            # Insert staff detail
            self.cursor.execute(
                "INSERT INTO StaffDetail (staff_id, address, email, join_date, full_details) VALUES (%s, %s, %s, CURRENT_DATE, %s)",
                (staff_id, address, email, f"New staff member: {first_name} {last_name}")
            )
            
            self.conn.commit()
            return True
        except Error as e:
            self.conn.rollback()
            print(f"Error adding staff: {e}")
            return False

    def delete_customer(self, customer_id: int) -> bool:
        """Delete a customer"""
        return self.execute_query("DELETE FROM Customer WHERE customer_id = %s", (customer_id,))

    def delete_car(self, car_id: int) -> bool:
        """Delete a car"""
        return self.execute_query("DELETE FROM Car WHERE car_id = %s", (car_id,))

    def delete_staff(self, staff_id: int) -> bool:
        """Delete a staff member"""
        return self.execute_query("DELETE FROM Staff WHERE staff_id = %s", (staff_id,)) 