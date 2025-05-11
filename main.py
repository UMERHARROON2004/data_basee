import csv
import mysql.connector
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="------"   #set your password    
)
mycursor = con.cursor()
type_mapping = {
    "int": "INT",
    "str": "VARCHAR(255)",
    "float": "FLOAT"
}
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "user": {"password": "user123", "role": "user"}
}
def validate_input(value, data_type):
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
    db_name = input("Enter database name you want to create: ").strip()
    mycursor.execute("SHOW DATABASES")
    databases = [db[0] for db in mycursor.fetchall()]
    if db_name in databases:
        print(f"Database '{db_name}' already exists! Please choose a different name.")
        return
    mycursor.execute(f"CREATE DATABASE {db_name}")
    print(f"Database '{db_name}' created successfully!")
    con.database = db_name
    created_tables = {}
    while True:
        table_name = input("\nEnter a table name to create (or type 'done' to finish creating tables): ").strip()
        if table_name.lower() == "done":
            break
        print(f"Defining columns for table '{table_name}':")
        columns = {"id": "INT AUTO_INCREMENT PRIMARY KEY"}
        while True:
            col_name = input("Enter column name (or type 'done' to finish columns): ").strip()
            if col_name.lower() == "done":
                break
            while True:
                col_type_input = input(f"Enter data type for '{col_name}' (int, str, float): ").strip().lower()
                if col_type_input in type_mapping:
                    col_type = type_mapping[col_type_input]
                    break
                else:
                    print("Invalid data type! Please enter only 'int', 'str', or 'float'.")
            columns[col_name] = col_type
        # Optional foreign key setup
        add_fk = input("Do you want to add a FOREIGN KEY to another table? (yes/no): ").strip().lower()
        foreign_key = ""
        if add_fk == "yes" and created_tables:
            print("Available tables to reference:")
            for t in created_tables:
                print(f"- {t}")
            ref_table = input("Enter the table name").strip()
            if ref_table in created_tables:
                ref_col = input(f"Enter the column name from '{ref_table}' to link (e.g., id): ").strip()
                fk_col_name = input("Enter the name of the foreign key column in this table: ").strip()
                columns[fk_col_name] = "INT"
                foreign_key = f", FOREIGN KEY ({fk_col_name}) REFERENCES {ref_table}({ref_col})"
            else:
                print("Invalid reference table, skipping foreign key.")
        columns_query = ", ".join([f"{col} {typ}" for col, typ in columns.items()]) + foreign_key
        mycursor.execute(f"CREATE TABLE {table_name} ({columns_query})")
        created_tables[table_name] = columns
        print(f"Table '{table_name}' created successfully!")
    print(f"\nDatabase '{db_name}' setup complete with all tables!")
def show_tables():
    mycursor.execute("SHOW DATABASES")
    databases = [db[0] for db in mycursor.fetchall()]
    print("\nAvailable Databases:")
    for db in databases:
        print(f"- {db}")
    db_name = input("Enter the database name to view tables: ").strip()
    if db_name not in databases:
        print(f"Database '{db_name}' does not exist!")
        return
    con.database = db_name
    mycursor.execute("SHOW TABLES")
    tables = mycursor.fetchall()
    print(f"\nTables in '{db_name}':")
    for table in tables:
        print(f"- {table[0]}")
def view_table_records():
    mycursor.execute("SHOW DATABASES")
    databases = [db[0] for db in mycursor.fetchall()]
    print("\nAvailable Databases:")
    for db in databases:
        print(f"- {db}")
    db_name = input("Enter the database name to view table records: ").strip()
    if db_name not in databases:
        print(f"Database '{db_name}' does not exist!")
        return
    con.database = db_name
    mycursor.execute("SHOW TABLES")
    tables = [t[0] for t in mycursor.fetchall()]
    if not tables:
        print("No tables found!")
        return
    print("\nAvailable Tables:")
    for table in tables:
        print(f"- {table}")
    table_name = input("Enter table name to view its records: ").strip()
    if table_name not in tables:
        print(f"Table '{table_name}' does not exist!")
        return
    mycursor.execute(f"SELECT * FROM {table_name}")
    rows = mycursor.fetchall()
    if not rows:
        print("No records found.")
        return
    print("\nRecords:")
    for row in rows:
        print(row)
def show_databases():
    mycursor.execute("SHOW DATABASES")
    databases = mycursor.fetchall()
    print("\nExisting Databases:")
    for db in databases:
        print(f"- {db[0]}")
def delete_data():
    mycursor.execute("SHOW DATABASES")
    databases = [db[0] for db in mycursor.fetchall()]
    print("\nAvailable Databases:")
    for db in databases:
        print(f"- {db}")
    db_name = input("Enter the database name you want to work with: ").strip()
    if db_name not in databases:
        print(f"Database '{db_name}' does not exist!")
        return
    con.database = db_name
    mycursor.execute("SHOW TABLES")
    tables = [t[0] for t in mycursor.fetchall()]
    if not tables:
        print("No tables found in this database.")
        return
    print("\nAvailable Tables:")
    for table in tables:
        print(f"- {table}")
    delete_choice = input("What do you want to delete? (1: Table, 2: Records): ").strip()
    if delete_choice == "1":
        table_name = input("Enter the table name you want to delete: ").strip()
        if table_name in tables:
            confirm = input(f"Are you sure you want to delete the table '{table_name}'? (yes/no): ").strip().lower()
            if confirm == "yes":
                mycursor.execute(f"DROP TABLE {table_name}")
                print(f"Table '{table_name}' deleted successfully!")
            else:
                print("Operation canceled.")
        else:
            print(f"Table '{table_name}' does not exist!")
    elif delete_choice == "2":
        table_name = input("Enter the table name you want to delete records from: ").strip()
        if table_name not in tables:
            print(f"Table '{table_name}' does not exist!")
            return
        mycursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
        print("\nSample Records:")
        for row in mycursor.fetchall():
            print(row)
        condition = input("Enter the condition to delete records (e.g., id=1): ").strip()
        confirm = input(f"Are you sure you want to delete records where {condition}? (yes/no): ").strip().lower()
        if confirm == "yes":
            try:
                mycursor.execute(f"DELETE FROM {table_name} WHERE {condition}")
                con.commit()
                print("Records deleted successfully!")
            except mysql.connector.Error as err:
                print(f"Error deleting records: {err}")
        else:
            print("Operation canceled.")
    else:
        print("Invalid option selected.")

def add_data():
    mycursor.execute("SHOW DATABASES")
    databases = [db[0] for db in mycursor.fetchall()]
    print("\nAvailable Databases:")
    for db in databases:
        print(f"- {db}")
    db_name = input("Enter the database name to add data to: ").strip()
    if db_name not in databases:
        print(f"Database '{db_name}' does not exist!")
        return
    con.database = db_name
    mycursor.execute("SHOW TABLES")
    tables = [t[0] for t in mycursor.fetchall()]
    if not tables:
        print("No tables exist in this database.")
        return
    print("\nAvailable Tables:")
    for table in tables:
        print(f"- {table}")
    table_name = input("Enter the table name you want to add data to: ").strip()
    if table_name not in tables:
        print(f"Table '{table_name}' does not exist!")
        return
    mycursor.execute(f"SHOW COLUMNS FROM {table_name}")
    columns = [col[0] for col in mycursor.fetchall() if col[5] != "auto_increment"]  
    while True:
        values = {}
        for col in columns:
            value = input(f"Enter value for '{col}': ").strip()
            values[col] = value
        print("\nYou have entered the following data:")
        for col, val in values.items():
            print(f"{col}: {val}")
        confirm = input("Do you want to save this data? (yes/y to save, no/n to re-enter): ").strip().lower()
        if confirm in ["yes", "y"]:
            columns_str = ", ".join(values.keys())
            placeholders = ", ".join(["%s"] * len(values))
            sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
            try:
                mycursor.execute(sql, tuple(values.values()))
                con.commit()
                print("Data inserted successfully!")
            except mysql.connector.Error as err:
                print(f"Error inserting data: {err}")
            break  
        elif confirm in ["no", "n"]:
            retry = input("Do you want to enter new data? (yes/y to continue, no/n to return to main menu): ").strip().lower()
            if retry not in ["yes", "y"]:
                print("Returning to main menu...")
                break  
def edit_data():
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
    condition = input("Enter the condition for the update (e.g., id=1): ").strip()
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
def export_table_to_csv():
    mycursor.execute("SHOW DATABASES")
    databases = [db[0] for db in mycursor.fetchall()]
    print("\nAvailable Databases:")
    for db in databases:
        print(f"- {db}")
    db_name = input("Enter the database name to export from: ").strip()
    if db_name not in databases:
        print(f"Database '{db_name}' does not exist!")
        return
    con.database = db_name
    mycursor.execute("SHOW TABLES")
    tables = [t[0] for t in mycursor.fetchall()]
    if not tables:
        print("No tables found!")
        return
    print("\nAvailable Tables:")
    for table in tables:
        print(f"- {table}")
    table_name = input("Enter the table name to export: ").strip()
    if table_name not in tables:
        print(f"Table '{table_name}' does not exist!")
        return
    mycursor.execute(f"SELECT * FROM {table_name}")
    rows = mycursor.fetchall()
    mycursor.execute(f"SHOW COLUMNS FROM {table_name}")
    headers = [col[0] for col in mycursor.fetchall()]
    file_name = input("Enter CSV file name (without .csv extension): ").strip() + ".csv"
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  
        writer.writerows(rows)    
    print(f"Table '{table_name}' exported successfully as '{file_name}'!")
def login():
    print("\t\t\t\t\t\t-------------------------\n\t\t\t\t\t\t|Welcome DataBase System|\n\t\t\t\t\t\t-------------------------")
    for attempt in range(3):
        username = input("Enter username:\n").strip()
        password = input("Enter password:\n").strip()
        user = users.get(username)
        if user and user["password"] == password:
            print(f"Login successful! Welcome, {username} ({user['role']})")
            return user["role"]
        else:
            print("Invalid credentials. Try again.")
    print("Too many failed attempts. Exiting.")
    exit()
role = login()
while True:
    print("\nWhat do you want to do?")
    print("\t1. Create a new database")
    print("\t2. Show existing databases")
    if role == "admin":
        print("\t3. Delete data")
    print("\t4. Edit data in a table")
    print("\t5. Add new data in records")
    print("\t6. Show all tables")
    print("\t7. View table records")
    print("\t8. Generate a CSV file")
    print("\t9. Exit")
    choice = input("Enter your choice (1-9):\n ").strip()
    if choice == "1":
        create_database()
    elif choice == "2":
        show_databases()
    elif choice == "3" and role == "admin":
        delete_data()
    elif choice == "4":
        edit_data()
    elif choice == "5":
        add_data()
    elif choice == "6":
        show_tables()
    elif choice == "7":
        view_table_records()
    elif choice == "8":
        export_table_to_csv()
    elif choice == "9":
        print("\t\t\t\tExiting the program.\n\t\t\t\t-----Goodbye!------")
        break
    else:
        if choice == "3" and role != "admin":
            print("Access denied. Only admins can delete data.")
        else:
            print("Invalid choice! Please enter a number between 1 and 9.")
con.close()
