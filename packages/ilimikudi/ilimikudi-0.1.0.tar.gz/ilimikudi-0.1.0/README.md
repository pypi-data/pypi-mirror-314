# IlimiKudi

**IlimiKudi** provides access to Fintech and Banking datasets like blog posts and support articles from platforms such as GTBank, Paystack, Moniepoint, and OPay. It is designed for use in AI-powered customer applications, including retrieval-augmented generation (RAG) for NLP.

## Features
- Access datasets stored in CSV format.
- Query an integrated database with multiple data sources.

## Installation

Install the required dependencies via `pip`:

```bash
pip install pandas duckdb
```

## Usage

### Accessing CSV Datasets

Load datasets using the following classes:

```python
from ilimikudi import GTBSupportPosts

# Access GTB Support Posts data
gtb_posts = GTBSupportPosts()
data = gtb_posts.get_data()  # Return as pandas DataFrame
print(data.head())
```

Available classes for CSV files:
- `GTBSupportPosts`
- `MergedData`
- `MoniepointBlogPosts`
- `OpayBlogPosts`
- `PaystackBlogPosts`
- `PaystackSupportPosts`

### Querying the Integrated Database

Query the integrated database:

```python
from ilimikudi import MergedDB

# Query the integrated database
db = MergedDB()
result = db.query()  # Default: SELECT * FROM unified
print(result.head())
```

Custom queries can also be executed:

```python
custom_query = "SELECT column_name FROM unified WHERE condition"
result = db.query(custom_query)
print(result)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
