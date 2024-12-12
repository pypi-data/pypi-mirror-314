import pandas as pd
import duckdb
from importlib.resources import files

# Base class for reading CSV files
class CSVDataset:
    def __init__(self, file_name):
        self.file_name = file_name
        self.data = self.load_data()
    
    def load_data(self):
        """Load the data from the CSV file in the package."""
        try:
            file_path = files('ilimikudi.datasets').joinpath(self.file_name)
            return pd.read_csv(file_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file '{self.file_name}' not found in the datasets directory.")
        except Exception as e:
            raise RuntimeError(f"An error occurred while loading '{self.file_name}': {e}")
    
    def get_data(self):
        """Get the loaded dataset."""
        return self.data

# Specific CSV datasets
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

# Accessing DuckDB database
class DuckDBDatabase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = self.connect_to_db()
    
    def connect_to_db(self):
        """Establish a connection to the DuckDB database."""
        try:
            db_path = files('ilimikudi.databases').joinpath(self.db_name)
            return duckdb.connect(str(db_path))
        except FileNotFoundError:
            raise FileNotFoundError(f"DuckDB database '{self.db_name}' not found in the databases directory.")
        except Exception as e:
            raise RuntimeError(f"An error occurred while connecting to '{self.db_name}': {e}")
    
    def query(self, query=None):
        """Execute a query on the DuckDB database."""
        if query is None:
            query = "SELECT * FROM unified"
        try:
            return self.connection.execute(query).fetchdf()
        except Exception as e:
            raise RuntimeError(f"An error occurred while executing the query: {e}")

# Merged database
class MergedDB(DuckDBDatabase):
    def __init__(self):
        super().__init__('merged.db')

if __name__ == "__main__":
    data = OpayBlogPosts()
    print(data.get_data())
