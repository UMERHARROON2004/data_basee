import mysql.connector

# Establish connection
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="umer1234"
)
mycursor = con.cursor()

type_mapping = {
    "int": "INT",
    "str": "VARCHAR(255)",
    "float": "FLOAT"
}

def validate_input(value, data_type):
    """Validates user input based on shorthand data types."""
    data_type = data_type.lower()
    if data_type == "int":
        return value.isdigit()
    elif data_type == "float":
        try:
            float(value)
            return True
        except ValueError:
            return False
    elif data_type == "str":
        return isinstance(value, str)
    return True

def create_database():
    """Creates a new database and tables with user-defined columns."""
    db_name = input("Enter database name you want to create: ").strip()
    mycursor.execute("SHOW DATABASES")
    databases = [db[0] for db in mycursor.fetchall()]

    if db_name in databases:
        print(f"Database '{db_name}' already exists! Please choose a different name.")
        return

    mycursor.execute(f"CREATE DATABASE {db_name}")
    print(f"Database '{db_name}' created successfully!")
    con.database = db_name

    num_tables = int(input("How many tables do you want to create? ").strip())

    for i in range(num_tables):
        table_name = input(f"Enter name for table {i+1}: ").strip()
        print(f"Defining columns for table '{table_name}':")
        columns = {}

        while True:
            col_name = input("Enter column name (or type 'done' to finish columns): ").strip()
            if col_name.lower() == "done":
                break
            col_type = input(f"Enter data type for '{col_name}' (int, str, float): ").strip().lower()
            col_type = type_mapping.get(col_type, col_type)
            columns[col_name] = col_type

        if not columns:
            print(f"No columns added for table '{table_name}'! Table creation skipped.")
            continue

        columns_query = ", ".join([f"{col} {typ}" for col, typ in columns.items()])
        mycursor.execute(f"CREATE TABLE {table_name} ({columns_query})")
        print(f"Table '{table_name}' created successfully!")

        while True:
            print(f"\nEnter data for table '{table_name}':")
            values = {}

            for col, typ in columns.items():
                while True:
                    val = input(f"Enter value for '{col}' ({typ}): ").strip()
                    if validate_input(val, typ):
                        values[col] = val
                        break
                    else:
                        print(f"Invalid input! '{col}' must be of type {typ}.")

            columns_str = ", ".join(values.keys())
            placeholders = ", ".join(["%s"] * len(values))
            sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
            mycursor.execute(sql, tuple(values.values()))
            con.commit()
            print("Data inserted successfully!")

            more_data = input("Do you want to enter more data? (yes/no): ").strip().lower()
            if more_data != "yes":
                print("-----Thank you!----")
                break

def show_databases():
    """Displays all existing databases."""
    mycursor.execute("SHOW DATABASES")
    databases = mycursor.fetchall()
    print("\nExisting Databases:")
    for db in databases:
        print(f"- {db[0]}")

def delete_database():
    """Deletes an existing database after confirmation."""
    mycursor.execute("SHOW DATABASES")
    databases = [db[0] for db in mycursor.fetchall()]
    db_name = input("Enter the database name you want to delete: ").strip()

    if db_name in databases:
        confirm = input(f"Are you sure you want to delete '{db_name}'? (yes/no): ").strip().lower()
        if confirm == "yes":
            mycursor.execute(f"DROP DATABASE {db_name}")
            print(f"Database '{db_name}' deleted successfully!")
        else:
            print("Operation canceled.")
    else:
        print(f"Database '{db_name}' does not exist!")

def edit_data():
    """Edits existing data in a selected database and table."""
    mycursor.execute("SHOW DATABASES")
    databases = [db[0] for db in mycursor.fetchall()]
    print("\nAvailable Databases:")
    for db in databases:
        print(f"- {db}")
    db_name = input("Enter the database name you want to edit: ").strip()
    if db_name not in databases:
        print(f"Database '{db_name}' does not exist!")
        return
    con.database = db_name
    print(f"Connected to database '{db_name}'")

    mycursor.execute("SHOW TABLES")
    tables = [t[0] for t in mycursor.fetchall()]
    if not tables:
        print("No tables exist in this database.")
        return
    print("\nAvailable Tables:")
    for table in tables:
        print(f"- {table}")

    table_name = input("Enter the table name you want to edit: ").strip()
    if table_name not in tables:
        print(f"Table '{table_name}' does not exist!")
        return

    mycursor.execute(f"SHOW COLUMNS FROM {table_name}")
    columns = [col[0] for col in mycursor.fetchall()]
    print("\nAvailable Columns:")
    for col in columns:
        print(f"- {col}")

    col_name = input("Enter the column name you want to edit: ").strip()
    if col_name not in columns:
        print(f"Column '{col_name}' does not exist in table '{table_name}'!")
        return

    print("\nExisting Data:")
    mycursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
    for row in mycursor.fetchall():
        print(row)

    condition = input("Enter the condition for the update (e.g., firstname='John'): ").strip()
    new_value = input(f"Enter the new value for '{col_name}': ").strip()

    confirm = input("Are you sure you want to update these rows? (yes/no): ").strip().lower()
    if confirm == "yes":
        update_query = f"UPDATE {table_name} SET {col_name} = %s WHERE {condition};"
        try:
            mycursor.execute(update_query, (new_value,))
            con.commit()
            print("Data updated successfully!")
        except mysql.connector.Error as err:
            print(f"Error updating data: {err}")
    else:
        print("Update canceled.")

while True:
    print("\nWhat do you want to do?")
    print("1. Create a new database")
    print("2. Show existing databases")
    print("3. Delete a database")
    print("4. Edit data in a database")
    print("5. Exit")
    choice = input("Enter your choice (1/2/3/4/5): ").strip()
    if choice == "1":
        create_database()
    elif choice == "2":
        show_databases()
    elif choice == "3":
        delete_database()
    elif choice == "4":
        edit_data()
    elif choice == "5":
        print("Exiting the program.\n-----Goodbye!-----")
        break
    else:
        print("Invalid choice! Please enter a number between 1 and 5.")

con.close()
