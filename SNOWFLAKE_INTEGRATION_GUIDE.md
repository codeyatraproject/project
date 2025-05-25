# Snowflake Integration Guide for Incredible India Data Story

This guide provides step-by-step instructions for integrating Snowflake with the Incredible India Data Story application. Follow these instructions if you want to use Snowflake as your data backend instead of local CSV files.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Setup Process](#setup-process)
3. [Configuration Options](#configuration-options)
4. [Data Migration](#data-migration)
5. [Troubleshooting](#troubleshooting)
6. [Best Practices](#best-practices)

## Prerequisites

Before integrating Snowflake, ensure you have:

- A Snowflake account with admin privileges
- Python 3.8 or higher installed
- Required Python packages:
  - snowflake-connector-python
  - snowflake-snowpark-python
  - pyarrow<19.0.0 (compatibility requirement)

## Setup Process

### 1. Install Required Dependencies

```bash
pip install snowflake-connector-python snowflake-snowpark-python "pyarrow<19.0.0"
```

### 2. Configure Snowflake Credentials

Create a `.streamlit/secrets.toml` file with your Snowflake credentials:

```toml
[snowflake]
account = "your-account-id"  # e.g., xy12345.us-east-1
user = "your-username"
password = "your-password"
warehouse = "COMPUTE_WH"  # Default or your custom warehouse
database = "INCREDIBLE_INDIA"  # Will be created during setup
schema = "PUBLIC"
role = "ACCOUNTADMIN"  # Or any role with appropriate permissions
```

Alternatively, you can set environment variables:

```bash
export SNOWFLAKE_ACCOUNT=your-account-id
export SNOWFLAKE_USER=your-username
export SNOWFLAKE_PASSWORD=your-password
export SNOWFLAKE_WAREHOUSE=COMPUTE_WH
export SNOWFLAKE_DATABASE=INCREDIBLE_INDIA
export SNOWFLAKE_SCHEMA=PUBLIC
export SNOWFLAKE_ROLE=ACCOUNTADMIN
```

### 3. Run Snowflake Setup Script

Create a `snowflake_setup.py` file with the following content:

```python
import os
import pandas as pd
import snowflake.connector
from pathlib import Path

def get_snowflake_credentials():
    """Get Snowflake credentials from secrets.toml or environment variables"""
    # Try to get from secrets.toml first
    secrets_path = Path(".streamlit/secrets.toml")
    if secrets_path.exists():
        with open(secrets_path, 'r') as f:
            content = f.read()
            if "[snowflake]" in content:
                # Parse the credentials (simplified parsing)
                import re
                account = re.search(r'account\s*=\s*"([^"]+)"', content)
                user = re.search(r'user\s*=\s*"([^"]+)"', content)
                password = re.search(r'password\s*=\s*"([^"]+)"', content)
                warehouse = re.search(r'warehouse\s*=\s*"([^"]+)"', content)
                database = re.search(r'database\s*=\s*"([^"]+)"', content)
                schema = re.search(r'schema\s*=\s*"([^"]+)"', content)
                role = re.search(r'role\s*=\s*"([^"]+)"', content)
                
                if account and user and password:
                    return {
                        'account': account.group(1),
                        'user': user.group(1),
                        'password': password.group(1),
                        'warehouse': warehouse.group(1) if warehouse else "COMPUTE_WH",
                        'database': database.group(1) if database else "INCREDIBLE_INDIA",
                        'schema': schema.group(1) if schema else "PUBLIC",
                        'role': role.group(1) if role else "ACCOUNTADMIN"
                    }
    
    # Try environment variables as fallback
    if os.environ.get("SNOWFLAKE_ACCOUNT") and os.environ.get("SNOWFLAKE_USER") and os.environ.get("SNOWFLAKE_PASSWORD"):
        return {
            'account': os.environ.get("SNOWFLAKE_ACCOUNT"),
            'user': os.environ.get("SNOWFLAKE_USER"),
            'password': os.environ.get("SNOWFLAKE_PASSWORD"),
            'warehouse': os.environ.get("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
            'database': os.environ.get("SNOWFLAKE_DATABASE", "INCREDIBLE_INDIA"),
            'schema': os.environ.get("SNOWFLAKE_SCHEMA", "PUBLIC"),
            'role': os.environ.get("SNOWFLAKE_ROLE", "ACCOUNTADMIN")
        }
    
    return None

def setup_snowflake():
    """Set up Snowflake database and tables"""
    print("Setting up Snowflake database and tables...")
    
    # Get credentials
    creds = get_snowflake_credentials()
    if not creds:
        print("Error: Snowflake credentials not found. Please set up credentials first.")
        return False
    
    try:
        # Connect to Snowflake
        conn = snowflake.connector.connect(
            account=creds['account'],
            user=creds['user'],
            password=creds['password'],
            warehouse=creds['warehouse'],
            role=creds['role']
        )
        
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {creds['database']}")
        
        # Use the database and schema
        cursor.execute(f"USE DATABASE {creds['database']}")
        cursor.execute(f"USE SCHEMA {creds['schema']}")
        
        # Create tables from local CSV files
        data_dir = Path("data")
        if data_dir.exists():
            for csv_file in data_dir.glob("*.csv"):
                table_name = csv_file.stem.upper()
                print(f"Creating table {table_name}...")
                
                # Read CSV to get column names and types
                df = pd.read_csv(csv_file)
                
                # Generate column definitions
                columns = []
                for col in df.columns:
                    # Map pandas dtypes to Snowflake types
                    if pd.api.types.is_numeric_dtype(df[col]):
                        if pd.api.types.is_integer_dtype(df[col]):
                            col_type = "INTEGER"
                        else:
                            col_type = "FLOAT"
                    else:
                        col_type = "VARCHAR(16777216)"  # Max size in Snowflake
                    
                    # Clean column name for Snowflake
                    clean_col = col.replace(" ", "_").replace("(", "").replace(")", "").replace("%", "PCT").upper()
                    columns.append(f'"{clean_col}" {col_type}')
                
                # Create table
                create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
                cursor.execute(create_table_sql)
                
                # Load data
                # For simplicity, we'll use Snowflake's COPY command
                # In a real implementation, you might want to use Snowpark or other methods
                stage_name = f"{table_name}_STAGE"
                cursor.execute(f"CREATE OR REPLACE STAGE {stage_name}")
                
                # Upload file to stage
                cursor.execute(f"PUT file://{csv_file.absolute()} @{stage_name}")
                
                # Copy from stage to table
                copy_sql = f"""
                COPY INTO {table_name}
                FROM @{stage_name}/{csv_file.name}
                FILE_FORMAT = (TYPE = CSV FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1)
                """
                cursor.execute(copy_sql)
                
                print(f"Successfully loaded data into {table_name}")
        
        cursor.close()
        conn.close()
        
        print("Snowflake setup completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error setting up Snowflake: {e}")
        return False

def test_connection():
    """Test the Snowflake connection"""
    print("Testing Snowflake connection...")
    
    creds = get_snowflake_credentials()
    if not creds:
        print("Error: Snowflake credentials not found.")
        return False
    
    try:
        conn = snowflake.connector.connect(
            account=creds['account'],
            user=creds['user'],
            password=creds['password'],
            warehouse=creds['warehouse'],
            database=creds['database'],
            schema=creds['schema'],
            role=creds['role']
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT current_version()")
        version = cursor.fetchone()[0]
        print(f"Successfully connected to Snowflake! (Version: {version})")
        
        # Test accessing tables
        cursor.execute(f"SHOW TABLES IN {creds['database']}.{creds['schema']}")
        tables = cursor.fetchall()
        if tables:
            print(f"Available tables: {', '.join([t[1] for t in tables])}")
        else:
            print("No tables found. You may need to run the setup process.")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Connection test failed: {e}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Snowflake setup for Incredible India Data Story")
    parser.add_argument("--test", action="store_true", help="Test Snowflake connection")
    parser.add_argument("--setup", action="store_true", help="Set up Snowflake database and tables")
    
    args = parser.parse_args()
    
    if args.test:
        test_connection()
    elif args.setup:
        setup_snowflake()
    else:
        # If no args provided, run both
        if test_connection():
            setup_snowflake()
```

Then run:

```bash
python snowflake_setup.py --setup
```

### 4. Update Application Configuration

Create a `modules/config.py` file with the following content to allow switching between local and Snowflake data sources:

```python
import streamlit as st
import os
from pathlib import Path

# Constants
APP_VERSION = "1.0.0"
APP_NAME = "Incredible India | A Data-Driven Journey"
DATA_DIR = Path("data")

# Function to check if Snowflake is configured
def is_snowflake_configured():
    """Check if Snowflake credentials are properly configured"""
    # Check for credentials in secrets.toml
    secrets_path = Path(".streamlit/secrets.toml")
    if secrets_path.exists():
        with open(secrets_path, 'r') as f:
            content = f.read()
            if "[snowflake]" in content and "<your-snowflake-account>" not in content:
                return True
    
    # Check for environment variables
    if (os.environ.get("SNOWFLAKE_ACCOUNT") and 
        os.environ.get("SNOWFLAKE_USER") and 
        os.environ.get("SNOWFLAKE_PASSWORD")):
        return True
    
    return False

# Function to add data source indicator to UI
def add_data_source_indicator():
    """Add a visual indicator of the current data source to the UI"""
    if st.session_state.get('use_snowflake', False):
        source_text = "📊 Data Source: Snowflake Cloud"
        source_color = "#29B5E8"  # Snowflake blue
    else:
        source_text = "📁 Data Source: Local Files"
        source_color = "#FAFAFA"  # White
    
    st.markdown(f"""
    <div style="position: absolute; top: 10px; right: 15px; font-size: 0.8rem; 
    background-color: rgba(0,0,0,0.3); padding: 3px 8px; border-radius: 4px; color: {source_color};">
    {source_text}
    </div>
    """, unsafe_allow_html=True)

# Function to handle missing data
def handle_missing_data(dataset_name):
    """Handle missing data by providing fallback options"""
    st.warning(f"Could not load {dataset_name} data. Using default values.")
    
    # Return empty dataframe or default data based on dataset type
    import pandas as pd
    
    if dataset_name == "state":
        return pd.DataFrame({
            "State": ["Maharashtra", "Tamil Nadu", "Karnataka"],
            "Population (millions)": [112.4, 72.1, 61.1],
            "Region": ["West", "South", "South"]
        })
    # Add other dataset types as needed
    
    return pd.DataFrame()
```

## Data Migration

To migrate your data from local CSV files to Snowflake:

1. Ensure all your CSV files are in the `data/` directory
2. Run the Snowflake setup script:
   ```bash
   python snowflake_setup.py --setup
   ```
3. Verify data migration:
   ```bash
   python snowflake_setup.py --test
   ```

## Troubleshooting

### Common Issues

1. **Connection Errors**:
   - Verify account identifier format (e.g., xy12345.us-east-1)
   - Check network connectivity and firewall settings
   - Ensure credentials are correct

2. **Permission Issues**:
   - Verify your role has appropriate permissions
   - Try using ACCOUNTADMIN role temporarily

3. **Data Type Errors**:
   - Check for data format inconsistencies in CSV files
   - Manually specify column types if automatic detection fails

4. **Package Conflicts**:
   - Ensure pyarrow version is compatible (<19.0.0)
   - Create a separate virtual environment for isolation

### Diagnostic Steps

1. Test basic connection:
   ```python
   import snowflake.connector
   conn = snowflake.connector.connect(
       account='your-account-id',
       user='your-username',
       password='your-password'
   )
   cursor = conn.cursor()
   cursor.execute("SELECT current_version()")
   print(cursor.fetchone()[0])
   ```

2. Check warehouse availability:
   ```python
   cursor.execute("SHOW WAREHOUSES")
   warehouses = cursor.fetchall()
   print(warehouses)
   ```

## Best Practices

1. **Security**:
   - Never commit credentials to version control
   - Use environment variables in production
   - Rotate passwords regularly

2. **Performance**:
   - Use appropriate warehouse sizes
   - Implement caching for frequently accessed data
   - Consider data clustering for large tables

3. **Cost Management**:
   - Auto-suspend warehouses when not in use
   - Monitor credit usage
   - Use resource monitors to set spending limits

4. **Development Workflow**:
   - Develop with local files first
   - Test with Snowflake using a development account
   - Use separate databases for development and production

## Advanced Configuration

For advanced Snowflake integration, consider:

1. **Snowpark for Python**:
   - Use Snowpark DataFrame API for more efficient data processing
   - Push computation to Snowflake instead of pulling data to Python

2. **Streamlit Caching**:
   - Use `@st.cache_data` to cache query results
   - Set TTL appropriate to your data refresh needs

3. **Snowflake Tasks**:
   - Schedule data refreshes using Snowflake Tasks
   - Implement ELT processes directly in Snowflake

4. **Snowpipe**:
   - For continuous data ingestion scenarios
   - Automate loading of new data files

By following this guide, you should be able to successfully integrate Snowflake with your Incredible India Data Story application, providing a robust cloud-based data backend for your visualizations and analyses. 