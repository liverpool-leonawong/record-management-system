"""
Airlines Page Class

Contains the Airlines Records Table as the main content.
"""
from tkinter import ttk
import customtkinter as ctk
from components.utility import DateFormatter
from ..base import BasePage

class AirlinesPage(BasePage):
    """ Airlines Page Class """

    def __init__(self, parent, navigation_callback):
        super().__init__(parent, navigation_callback)  # Initialize the base page first

        # Initialize attributes first
        self.airlines = []  # Initialize airlines list
        self.tree = None   # Initialize tree

        # Create page header using base method
        self.create_header(
            title="Airlines",
            description="Create, edit, or manage airline companies"
        )

        # Fetch data before creating content
        self.fetch_airlines()

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
        """Setup the main content of the airlines page"""
        try:
            # Add New Client Button
            self.create_action_buttons()

            # Create Table
            self.create_airline_table()
        except Exception as e:
            print(f"Error setting up content: {e}")

    def create_action_buttons(self):
        """Create action button to add a new airline"""
        button_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        button_frame.pack(fill="x", padx=10, pady=(0, 10))

        new_airline_btn = ctk.CTkButton(
            button_frame,
            text="+ New Airline",
            command=self.on_new_airline_click
        )
        new_airline_btn.pack(side="right")

    def create_airline_table(self):
        """Create the airline table"""
        # Create a frame to hold both table and scrollbar
        table_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Table Columns
        columns = ("ID", "Airlines", "Country",
                   "Created On", "Action")

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
        """Populate table with airline data"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add data to table
        for airline in self.airlines:
            formatted_created_date = DateFormatter.to_display_format(
                airline["created_date"])
            self.tree.insert("", "end", values=(
                airline["id"],
                airline["company_name"],
                airline["country"],
                formatted_created_date
            ))

    def fetch_airlines(self):
        """
        Fetch airlines data from your data source
        For now, using sample data
        """
        try:
            # This is sample data - replace with your actual data fetching logic
            self.airlines = [
                {
                    "id": "A0001",
                    "type": "Airline",
                    "company_name": "Cathay Pacific Airways",
                    "country": "Hong Kong",
                    "created_date": "2025-03-01T00:00:00Z"
                },
                {
                    "id": "A0002",
                    "type": "Airline",
                    "company_name": "British Airways",
                    "country": "United Kingdom",
                    "created_date": "2025-03-01T00:00:00Z"
                }
            ]
        except Exception as e:
            print(f"Error fetching airlines: {e}")
            self.airlines = []

    def refresh_airlines(self):
        """Refresh the airlines table"""
        self.fetch_airlines()
        self.populate_table()

    def on_new_airline_click(self):
        """Handle new airline button click"""
        self.navigation_callback("add_new_airline")
