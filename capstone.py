import sqlite3

class Process:
    def __init__(self, name, material_cost, labor_cost, overhead_cost, units_produced, planned_cost):
        self.name = name
        self.material_cost = material_cost
        self.labor_cost = labor_cost
        self.overhead_cost = overhead_cost
        self.units_produced = units_produced
        self.planned_cost = planned_cost

    def total_cost(self):
        return self.material_cost + self.labor_cost + self.overhead_cost

    def get_units_produced(self):
        return self.units_produced

    def cost_per_unit(self):
        if self.units_produced == 0:
            return 0
        return self.total_cost() / self.units_produced

    def display(self):
        print(f"\n--- {self.name} Department ---")
        print(f"Material Cost: Php {self.material_cost}")
        print(f"Labor Cost: Php {self.labor_cost}")
        print(f"Overhead Cost: Php {self.overhead_cost}")
        print(f"Units Produced: {self.units_produced}")
        print(f"Total Cost: Php {self.total_cost()}")
        print(f"Cost Per Unit: Php {self.cost_per_unit()}")

def save_database(process):
    try:
        connection = sqlite3.connect('production_data.db')
        cursor = connection.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS production_orders (
                id INTEGER PRIMARY KEY,
                order_name TEXT NOT NULL,
                material_cost REAL,
                labor_cost REAL,
                overhead_cost REAL,
                units_produced INTEGER,
                total_cost REAL,
                planned_cost REAL
            )
        ''')
        
        cursor.execute('''
            INSERT INTO production_orders
            (order_name, material_cost, labor_cost, overhead_cost, units_produced, total_cost, planned_cost)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            process.name,
            process.material_cost,
            process.labor_cost,
            process.overhead_cost,
            process.units_produced,
            process.total_cost(),
            process.planned_cost
        ))
        
        connection.commit()
        print(f"\nData for {process.name} saved successfully to the database.")

    except sqlite3.Error as err:
        print(f"Error: {err}")
    finally:
        if connection:
            connection.close()

def view_data():
    try:
        connection = sqlite3.connect('production_data.db')
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM production_orders")
        records = cursor.fetchall()
        
        print("\n=== Past Production Orders ===")
        print("ID | Order Name | Material Cost | Labor Cost | Overhead Cost | Units Produced | Total Cost | Planned Cost")
        print("-------------------------------------------------------------------------------------------------------")
        for row in records:
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} | {row[6]} | {row[7]}")
            
    except sqlite3.Error as err:
        print(f"Error viewing data: {err}")
    finally:
        if connection:
            connection.close()

def delete_data():
    try:
        connection = sqlite3.connect('production_data.db')
        cursor = connection.cursor()

        view_data()

        record_id = input("\nEnter the ID of the record you want to delete: ")
        
        cursor.execute("DELETE FROM production_orders WHERE id = ?", (record_id,))
        connection.commit()
        
        print(f"\nRecord with ID {record_id} successfully deleted.")

    except sqlite3.Error as err:
        print(f"Error deleting data: {err}")
    finally:
        if connection:
            connection.close()

def main():
    while True:
        print("\n=== Production Cost Management System ===")
        print("1. Add New Production Order")
        print("2. View All Past Orders")
        print("3. Delete a Past Order")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            processes = []
            num_processes = int(input("Enter number of departments/processes: "))
            
            for i in range(num_processes):
                name = input(f"\nEnter name of process #{i + 1}: ")
                material = float(input("Enter material cost: Php "))
                labor = float(input("Enter labor cost: Php "))
                overhead = float(input("Enter overhead cost: Php "))
                units = int(input("Enter units produced: "))
                planned = float(input("Enter planned cost: Php "))
                processes.append(Process(name, material, labor, overhead, units, planned))
            
            for process in processes:
                process.display()
                save_database(process)
        
        elif choice == '2':
            view_data()
        
        elif choice == '3':
            delete_data()
        
        elif choice == '4':
            print("Exiting program.")
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()