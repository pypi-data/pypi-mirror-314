import pandas as pd
import duckdb
import os

# Base class for reading CSV files
class CSVDataset:
    def __init__(self, file_name):
        self.file_path = os.path.join('datasets', file_name)
        self.data = self.load_data()
    
    def load_data(self):
        """Load the data from the CSV file."""
        if os.path.exists(self.file_path):
            return pd.read_csv(self.file_path)
        else:
            raise FileNotFoundError(f"File {self.file_path} not found.")
    
    def get_data(self):
        """Get the dataset."""
        return self.data

# Classes for specific CSV files
class GTBSupportPosts(CSVDataset):
    def __init__(self):
        super().__init__('gtb_support_posts.csv')

class MergedData(CSVDataset):
    def __init__(self):
        super().__init__('merged.csv')

class MoniepointBlogPosts(CSVDataset):
    def __init__(self):
        super().__init__('moniepoint_blog_posts.csv')

class OpayBlogPosts(CSVDataset):
    def __init__(self):
        super().__init__('opay_blog_posts.csv')

class PaystackBlogPosts(CSVDataset):
    def __init__(self):
        super().__init__('paystack_blog_posts.csv')

class PaystackSupportPosts(CSVDataset):
    def __init__(self):
        super().__init__('paystack_support_posts.csv')

# Class for accessing the DuckDB database
class DuckDBDatabase:
    def __init__(self, db_name):
        self.db_path = os.path.join('databases', db_name)
        self.connection = self.connect_to_db()
    
    def connect_to_db(self):
        """Establish a connection to the DuckDB database."""
        if os.path.exists(self.db_path):
            return duckdb.connect(self.db_path)
        else:
            raise FileNotFoundError(f"Database {self.db_path} not found.")
    
    def query(self, query=None):
        """Execute a query on the DuckDB database.
        By default, fetch data from the 'unified' table if no query is provided.
        """
        if query is None:
            query = "SELECT * FROM unified"
        return self.connection.execute(query).fetchdf()

# Class for merged database
class MergedDB(DuckDBDatabase):
    def __init__(self):
        super().__init__('merged.db')