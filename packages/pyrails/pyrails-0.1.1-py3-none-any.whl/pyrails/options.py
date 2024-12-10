from InquirerPy import inquirer

# Extended database configuration with async compatibility checks
DATABASES = [
    {"name": "PostgreSQL", "sync": "psycopg", "async": "asyncpg"},
    {"name": "MySQL", "sync": "mysqlclient", "async": "aiomysql"},
    {"name": "SQLite", "sync": "sqlite3", "async": "aiosqlite"},
    {"name": "Oracle", "sync": "cx_Oracle", "async": None},
    {"name": "SQL Server", "sync": "pyodbc", "async": None},
    {"name": "MongoDB", "sync": "pymongo", "async": "motor"},
    {"name": "MariaDB", "sync": "mariadb", "async": "aiomysql"},
    {"name": "Cassandra", "sync": "cassandra-driver", "async": None},
]

EMAIL_SERVERS = [
    "Gmail SMTP (smtp.gmail.com)",
    "Outlook SMTP (smtp.office365.com)",
    "Yahoo SMTP (smtp.mail.yahoo.com)",
    "Custom SMTP (enter manually)",
]

def get_database_selection(databases):
    """Prompt the user to select a database."""
    database_names = [db["name"] for db in databases]
    return inquirer.select("Select your database:", choices=database_names).execute()

def get_async_preference(available_async):
    """Ask the user if they prefer asynchronous drivers if available."""
    if not available_async:
        return False
    return inquirer.confirm("Do you want Async?").execute()

def get_email_server_choice():
    """Prompt the user to select an email server."""
    return inquirer.select("Select your email server (SMTP)", choices=EMAIL_SERVERS).execute()

def find_driver(database, async_mode):
    """Find the appropriate driver for the selected database."""
    selected_db = next((db for db in DATABASES if db["name"] == database), None)
    if not selected_db:
        raise ValueError(f"Database '{database}' not found.")
    return selected_db["async"] if async_mode else selected_db["sync"]

def main():
    """Main function to execute the script."""
    print("Welcome to the Database and Email Configuration Wizard!")

    # Database selection
    database = get_database_selection(DATABASES)

    # Determine async capability dynamically
    selected_db = next((db for db in DATABASES if db["name"] == database), None)
    async_capable = bool(selected_db and selected_db["async"])
    async_mode = get_async_preference(async_capable)

    driver = find_driver(database, async_mode)

    # Email server selection
    email_server = get_email_server_choice()

    print(f"\nConfiguration Complete!")
    print(f"Chosen Database: {database}")
    print(f"Driver: {driver}")
    print(f"Email Server: {email_server}")

if __name__ == "__main__":
    main()
