    import sqlite3
from typing import List, Tuple, Optional

class DatabaseConnection:
    def __init__(self, db_name: str = "car_service.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish connection to the database"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            return True
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return False

    def close(self):
        """Close the database connection"""
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
        except sqlite3.Error as e:
            print(f"Query execution error: {e}")
            return False

    def fetch_all(self, query: str, params: tuple = None) -> List[Tuple]:
        """Execute a query and return all results"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
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
        except sqlite3.Error as e:
            print(f"Fetch error: {e}")
            return None

    def create_tables(self):
        """Create all necessary tables"""
        queries = [
            """CREATE TABLE IF NOT EXISTS Contact (
                contact_id INTEGER PRIMARY KEY AUTOINCREMENT,
                email VARCHAR(100) UNIQUE NOT NULL
            )""",
            """CREATE TABLE IF NOT EXISTS ContactPhone (
                contact_id INTEGER NOT NULL,
                phone_number VARCHAR(15) NOT NULL,
                PRIMARY KEY (contact_id, phone_number),
                FOREIGN KEY (contact_id) REFERENCES Contact(contact_id) ON DELETE CASCADE
            )""",
            """CREATE TABLE IF NOT EXISTS Identity (
                identity_id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_number VARCHAR(20) UNIQUE NOT NULL,
                issued_date DATE NOT NULL
            )""",
            """CREATE TABLE IF NOT EXISTS Customer (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                contact_id INTEGER NOT NULL,
                identity_id INTEGER NOT NULL,
                FOREIGN KEY (contact_id) REFERENCES Contact(contact_id) ON DELETE CASCADE,
                FOREIGN KEY (identity_id) REFERENCES Identity(identity_id) ON DELETE CASCADE
            )""",
            """CREATE TABLE IF NOT EXISTS Staff (
                staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
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
                admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
                staff_id INTEGER UNIQUE,
                customer_id INTEGER UNIQUE,
                username VARCHAR(50) NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role VARCHAR(20) NOT NULL,
                FOREIGN KEY (staff_id) REFERENCES Staff(staff_id) ON DELETE SET NULL,
                FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) ON DELETE SET NULL
            )""",
            """CREATE TABLE IF NOT EXISTS Car (
                car_id INTEGER PRIMARY KEY AUTOINCREMENT,
                model VARCHAR(50) NOT NULL,
                brand VARCHAR(50) NOT NULL,
                number_plate VARCHAR(20) UNIQUE NOT NULL,
                customer_id INTEGER NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) ON DELETE CASCADE
            )""",
            """CREATE TABLE IF NOT EXISTS Discount (
                discount_id INTEGER PRIMARY KEY AUTOINCREMENT,
                percentage_discount DECIMAL(5,2) NOT NULL
            )""",
            """CREATE TABLE IF NOT EXISTS Payment (
                payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount DECIMAL(10,2) NOT NULL,
                discount_id INTEGER,
                status VARCHAR(20) CHECK (status IN ('Completed', 'Pending', 'Failed')),
                FOREIGN KEY (discount_id) REFERENCES Discount(discount_id) ON DELETE SET NULL
            )""",
            """CREATE TABLE IF NOT EXISTS Feedback (
                feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                comments TEXT NOT NULL,
                feedback_date DATE NOT NULL,
                rating INTEGER CHECK (rating BETWEEN 1 AND 5),
                FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) ON DELETE CASCADE
            )""",
            """CREATE TABLE IF NOT EXISTS ServiceCategory (
                servicecategory_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_name VARCHAR(100) UNIQUE NOT NULL
            )""",
            """CREATE TABLE IF NOT EXISTS VehicleList (
                vehiclelist_id INTEGER PRIMARY KEY AUTOINCREMENT,
                number_plate VARCHAR(20) NOT NULL,
                servicecategory_id INTEGER NOT NULL,
                registration_date DATE NOT NULL,
                vehicle_type VARCHAR(50),
                FOREIGN KEY (number_plate) REFERENCES Car(number_plate) ON DELETE CASCADE,
                FOREIGN KEY (servicecategory_id) REFERENCES ServiceCategory(servicecategory_id) ON DELETE CASCADE
            )""",
            """CREATE TABLE IF NOT EXISTS Sparepart (
                sparepart_id INTEGER PRIMARY KEY AUTOINCREMENT,
                part_name VARCHAR(100) NOT NULL,
                price DECIMAL(10,2) NOT NULL
            )""",
            """CREATE TABLE IF NOT EXISTS Report (
                report_id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_date DATE NOT NULL,
                description_text TEXT NOT NULL,
                staff_id INTEGER NOT NULL,
                FOREIGN KEY (staff_id) REFERENCES Staff(staff_id) ON DELETE CASCADE
            )""",
            """CREATE TABLE IF NOT EXISTS ServiceComplete (
                servicecomplete_id INTEGER PRIMARY KEY AUTOINCREMENT,
                time_completion TIME NOT NULL,
                customer_id INTEGER NOT NULL,
                completion_date DATE NOT NULL,
                staff_id INTEGER NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) ON DELETE CASCADE,
                FOREIGN KEY (staff_id) REFERENCES Staff(staff_id) ON DELETE CASCADE
            )""",
            """CREATE TABLE IF NOT EXISTS Emergency (
                emergency_id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number VARCHAR(15) UNIQUE NOT NULL
            )"""
        ]

        for query in queries:
            self.execute_query(query)

    def insert_sample_data(self):
        """Insert sample data into the database"""
        # Insert sample data for Contact
        self.execute_query("INSERT OR IGNORE INTO Contact (email) VALUES (?)", ("john.doe@email.com",))
        self.execute_query("INSERT OR IGNORE INTO Contact (email) VALUES (?)", ("jane.smith@email.com",))
        
        # Insert sample data for Customer
        self.execute_query("""
            INSERT OR IGNORE INTO Customer (first_name, last_name, contact_id, identity_id)
            VALUES (?, ?, ?, ?)
        """, ("John", "Doe", 1, 1))
        
        # Insert sample data for Car
        self.execute_query("""
            INSERT OR IGNORE INTO Car (model, brand, number_plate, customer_id)
            VALUES (?, ?, ?, ?)
        """, ("Civic", "Honda", "TN10AB1234", 1))
        
        # Insert sample data for ServiceCategory
        self.execute_query("""
            INSERT OR IGNORE INTO ServiceCategory (category_name)
            VALUES (?)
        """, ("Oil Change",))
        
        # Insert sample data for Staff
        self.execute_query("""
            INSERT OR IGNORE INTO Staff (first_name, last_name, role, contact_id)
            VALUES (?, ?, ?, ?)
        """, ("Michael", "Scott", "Manager", 1))

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