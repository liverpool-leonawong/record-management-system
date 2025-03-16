"""
Clients Page Class

Contains the Clients Records Table as the main content.
"""
from tkinter import ttk
import customtkinter as ctk
from components.utility import DateFormatter
from ..base import BasePage


class ClientsPage(BasePage):
    """ Clients Page Class """

    def __init__(self, parent, navigation_callback):
        super().__init__(parent, navigation_callback)  # Initialize the base page first

        # Initialize attributes first
        self.clients = []  # Initialize clients list
        self.tree = None   # Initialize tree

        # Create page header using base method
        self.create_header(
            title="Clients",
            description="Create, edit, or manage client records"
        )

        # Fetch data before creating content
        self.fetch_clients()

        # Create main content
        self.setup_content()

    def show_loading(self):
        """Show loading indicator"""
        self.loading_label = ctk.CTkLabel(
            self.content_frame,
            text="Loading...",
            font=("Arial", 14)
        )
        self.loading_label.pack(pady=20)

    def hide_loading(self):
        """Hide loading indicator"""
        if hasattr(self, 'loading_label'):
            self.loading_label.destroy()

    def setup_content(self):
        """Setup the main content of the clients page"""
        try:
            # Add New Client Button
            self.create_action_buttons()

            # Create Table
            self.create_client_table()
        except Exception as e:
            print(f"Error setting up content: {e}")

    def create_action_buttons(self):
        """Create action button to add new client"""
        button_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        button_frame.pack(fill="x", padx=10, pady=(0, 10))

        new_client_btn = ctk.CTkButton(
            button_frame,
            text="+ New Client",
            command=self.on_new_client_click
        )
        new_client_btn.pack(side="right")

    def create_client_table(self):
        """Create the clients table"""
        # Create a frame to hold both table and scrollbar
        table_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Table Columns
        columns = ("ID", "Name", "City", "Country", "Phone",
                   "Email", "Created On", "Action")

        # Initialize and configure Treeview
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        # Configure column headings and widths
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        # Create scrollbar first
        scrollbar = ttk.Scrollbar(
            self.content_frame,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Pack scrollbar and tree
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Insert the sample data
        self.populate_table()

    def populate_table(self):
        """Populate table with client data"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add data to table
        for client in self.clients:
            formatted_created_date = DateFormatter.to_display_format(
                client["created_date"])
            self.tree.insert("", "end", values=(
                client["id"],
                client["name"],
                client["city"],
                client["country"],
                client["phone"],
                client["email"],
                formatted_created_date
            ))

    def fetch_clients(self):
        """
        Fetch clients data from your data source
        For now, using sample data
        """
        try:
            # This is sample data - replace with your actual data fetching logic
            self.clients = [
                {
                    "id": "C0001",
                    "type": "Client",
                    "name": "Leona Wong",
                    "address_line1": "Unit 1208, Tower A",
                    "address_line2": "Enterprise Square",
                    "address_line3": "9 Sheung Yuet Road",
                    "city": "Kowloon Bay",
                    "state": "Kowloon",
                    "zip_code": "00000",
                    "country": "Hong Kong",
                    "phone": "+852 9123 4567",
                    "email": "w.wong12@liverpool.ac.uk",
                    "created_date": "2025-03-01T00:00:00Z"
                },
                {
                    "id": "C0002",
                    "type": "Client",
                    "name": "Tommy Bowden",
                    "address_line1": "42 Oxford Street",
                    "address_line2": "Apartment 15B",
                    "address_line3": "Westminster",
                    "city": "London",
                    "state": "Greater London",
                    "zip_code": "W1D 2DW",
                    "country": "United Kingdom",
                    "phone": "+44 7700 900123",
                    "email": "t.bowden@liverpool.ac.uk",
                    "created_date": "2025-03-02T00:00:00Z"
                }
            ]
        except Exception as e:
            print(f"Error fetching clients: {e}")
            self.clients = []

    def refresh_clients(self):
        """Refresh the clients table"""
        self.fetch_clients()
        self.populate_table()

    def on_new_client_click(self):
        """Handle new client button click"""
        self.navigation_callback("add_new_client")
