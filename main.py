import tkinter as tk
from tkinter import ttk, messagebox
from database_connection import DatabaseConnection
from datetime import datetime
import os
from dotenv import load_dotenv

class CarServiceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Car Service Management System")
        self.root.geometry("1200x800")
        
        # Initialize status variable
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        
        # Load environment variables
        load_dotenv()
        
        # Initialize database connection
        self.db = DatabaseConnection()
        if not self.db.connect():
            messagebox.showerror("Error", "Failed to connect to database")
            return
        
        # Create tables and insert sample data
        self.db.create_tables()
        self.db.insert_sample_data()
        
        # Create main notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Create tabs
        self.customers_tab = ttk.Frame(self.notebook)
        self.cars_tab = ttk.Frame(self.notebook)
        self.staff_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.customers_tab, text="Customers")
        self.notebook.add(self.cars_tab, text="Cars")
        self.notebook.add(self.staff_tab, text="Staff")
        
        # Initialize tabs
        self.setup_customers_tab()
        self.setup_cars_tab()
        self.setup_staff_tab()
        
        # Add status bar
        status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Add menu
        self.create_menu()
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def show_about(self):
        messagebox.showinfo("About", "Car Service Management System\nVersion 1.0")
    
    def setup_customers_tab(self):
        # Create treeview
        columns = ("ID", "First Name", "Last Name", "Email")
        self.customers_tree = ttk.Treeview(self.customers_tab, columns=columns, show="headings")
        
        # Set column headings
        for col in columns:
            self.customers_tree.heading(col, text=col)
            self.customers_tree.column(col, width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.customers_tab, orient=tk.VERTICAL, command=self.customers_tree.yview)
        self.customers_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        self.customers_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add buttons frame
        btn_frame = ttk.Frame(self.customers_tab)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_customers).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Add Customer", command=self.add_customer).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Customer", command=self.delete_customer).pack(side=tk.LEFT, padx=5)
        
        # Load initial data
        self.refresh_customers()
    
    def setup_cars_tab(self):
        # Create treeview
        columns = ("ID", "Model", "Brand", "Number Plate", "Customer ID")
        self.cars_tree = ttk.Treeview(self.cars_tab, columns=columns, show="headings")
        
        # Set column headings
        for col in columns:
            self.cars_tree.heading(col, text=col)
            self.cars_tree.column(col, width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.cars_tab, orient=tk.VERTICAL, command=self.cars_tree.yview)
        self.cars_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        self.cars_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add buttons frame
        btn_frame = ttk.Frame(self.cars_tab)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_cars).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Add Car", command=self.add_car).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Car", command=self.delete_car).pack(side=tk.LEFT, padx=5)
        
        # Load initial data
        self.refresh_cars()
    
    def setup_staff_tab(self):
        # Create treeview
        columns = ("ID", "First Name", "Last Name", "Role", "Email")
        self.staff_tree = ttk.Treeview(self.staff_tab, columns=columns, show="headings")
        
        # Set column headings
        for col in columns:
            self.staff_tree.heading(col, text=col)
            self.staff_tree.column(col, width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.staff_tab, orient=tk.VERTICAL, command=self.staff_tree.yview)
        self.staff_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        self.staff_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add buttons frame
        btn_frame = ttk.Frame(self.staff_tab)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_staff).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Add Staff", command=self.add_staff).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Staff", command=self.delete_staff).pack(side=tk.LEFT, padx=5)
        
        # Load initial data
        self.refresh_staff()
    
    def refresh_customers(self):
        # Clear existing items
        for item in self.customers_tree.get_children():
            self.customers_tree.delete(item)
        
        # Fetch and display customers
        customers = self.db.get_customers()
        for customer in customers:
            self.customers_tree.insert("", tk.END, values=customer)
        
        self.status_var.set(f"Customers refreshed at {datetime.now().strftime('%H:%M:%S')}")
    
    def refresh_cars(self):
        # Clear existing items
        for item in self.cars_tree.get_children():
            self.cars_tree.delete(item)
        
        # Fetch and display cars
        cars = self.db.get_cars()
        for car in cars:
            self.cars_tree.insert("", tk.END, values=car)
        
        self.status_var.set(f"Cars refreshed at {datetime.now().strftime('%H:%M:%S')}")
    
    def refresh_staff(self):
        # Clear existing items
        for item in self.staff_tree.get_children():
            self.staff_tree.delete(item)
        
        # Fetch and display staff
        staff = self.db.get_staff()
        for member in staff:
            self.staff_tree.insert("", tk.END, values=member)
        
        self.status_var.set(f"Staff refreshed at {datetime.now().strftime('%H:%M:%S')}")
    
    def add_customer(self):
        # Create a new window for adding customer
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Customer")
        add_window.geometry("400x300")
        
        # Create form
        ttk.Label(add_window, text="First Name:").grid(row=0, column=0, padx=5, pady=5)
        first_name = ttk.Entry(add_window)
        first_name.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(add_window, text="Last Name:").grid(row=1, column=0, padx=5, pady=5)
        last_name = ttk.Entry(add_window)
        last_name.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(add_window, text="Email:").grid(row=2, column=0, padx=5, pady=5)
        email = ttk.Entry(add_window)
        email.grid(row=2, column=1, padx=5, pady=5)
        
        def save_customer():
            if not first_name.get() or not last_name.get() or not email.get():
                messagebox.showerror("Error", "All fields are required")
                return
            
            if self.db.add_customer(first_name.get(), last_name.get(), email.get()):
                messagebox.showinfo("Success", "Customer added successfully")
                add_window.destroy()
                self.refresh_customers()
            else:
                messagebox.showerror("Error", "Failed to add customer")
        
        ttk.Button(add_window, text="Save", command=save_customer).grid(row=3, column=0, columnspan=2, pady=10)
    
    def add_car(self):
        # Create a new window for adding car
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Car")
        add_window.geometry("400x300")
        
        # Create form
        ttk.Label(add_window, text="Model:").grid(row=0, column=0, padx=5, pady=5)
        model = ttk.Entry(add_window)
        model.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(add_window, text="Brand:").grid(row=1, column=0, padx=5, pady=5)
        brand = ttk.Entry(add_window)
        brand.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(add_window, text="Number Plate:").grid(row=2, column=0, padx=5, pady=5)
        number_plate = ttk.Entry(add_window)
        number_plate.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(add_window, text="Customer ID:").grid(row=3, column=0, padx=5, pady=5)
        customer_id = ttk.Entry(add_window)
        customer_id.grid(row=3, column=1, padx=5, pady=5)
        
        def save_car():
            try:
                customer_id_int = int(customer_id.get())
            except ValueError:
                messagebox.showerror("Error", "Customer ID must be a number")
                return
            
            if not model.get() or not brand.get() or not number_plate.get():
                messagebox.showerror("Error", "All fields are required")
                return
            
            if self.db.add_car(model.get(), brand.get(), number_plate.get(), customer_id_int):
                messagebox.showinfo("Success", "Car added successfully")
                add_window.destroy()
                self.refresh_cars()
            else:
                messagebox.showerror("Error", "Failed to add car")
        
        ttk.Button(add_window, text="Save", command=save_car).grid(row=4, column=0, columnspan=2, pady=10)
    
    def add_staff(self):
        # Create a new window for adding staff
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Staff")
        add_window.geometry("400x300")
        
        # Create form
        ttk.Label(add_window, text="First Name:").grid(row=0, column=0, padx=5, pady=5)
        first_name = ttk.Entry(add_window)
        first_name.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(add_window, text="Last Name:").grid(row=1, column=0, padx=5, pady=5)
        last_name = ttk.Entry(add_window)
        last_name.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(add_window, text="Role:").grid(row=2, column=0, padx=5, pady=5)
        role = ttk.Entry(add_window)
        role.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(add_window, text="Email:").grid(row=3, column=0, padx=5, pady=5)
        email = ttk.Entry(add_window)
        email.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(add_window, text="Address:").grid(row=4, column=0, padx=5, pady=5)
        address = ttk.Entry(add_window)
        address.grid(row=4, column=1, padx=5, pady=5)
        
        def save_staff():
            if not first_name.get() or not last_name.get() or not role.get() or not email.get() or not address.get():
                messagebox.showerror("Error", "All fields are required")
                return
            
            if self.db.add_staff(first_name.get(), last_name.get(), role.get(), email.get(), address.get()):
                messagebox.showinfo("Success", "Staff added successfully")
                add_window.destroy()
                self.refresh_staff()
            else:
                messagebox.showerror("Error", "Failed to add staff")
        
        ttk.Button(add_window, text="Save", command=save_staff).grid(row=5, column=0, columnspan=2, pady=10)
    
    def delete_customer(self):
        selected_item = self.customers_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a customer to delete")
            return
        
        customer_id = self.customers_tree.item(selected_item[0])['values'][0]
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this customer?"):
            if self.db.delete_customer(customer_id):
                messagebox.showinfo("Success", "Customer deleted successfully")
                self.refresh_customers()
            else:
                messagebox.showerror("Error", "Failed to delete customer")
    
    def delete_car(self):
        selected_item = self.cars_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a car to delete")
            return
        
        car_id = self.cars_tree.item(selected_item[0])['values'][0]
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this car?"):
            if self.db.delete_car(car_id):
                messagebox.showinfo("Success", "Car deleted successfully")
                self.refresh_cars()
            else:
                messagebox.showerror("Error", "Failed to delete car")
    
    def delete_staff(self):
        selected_item = self.staff_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a staff member to delete")
            return
        
        staff_id = self.staff_tree.item(selected_item[0])['values'][0]
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this staff member?"):
            if self.db.delete_staff(staff_id):
                messagebox.showinfo("Success", "Staff member deleted successfully")
                self.refresh_staff()
            else:
                messagebox.showerror("Error", "Failed to delete staff member")

if __name__ == "__main__":
    root = tk.Tk()
    app = CarServiceApp(root)
    root.mainloop() 