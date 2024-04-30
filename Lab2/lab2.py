# Create class employee with the following characteristics: 
import sqlite3

class Employee:
    employees = []
    def __init__(self, first_name, last_name, age, department, salary):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.department = department
        self.salary = salary
        Employee.employees.append(self)
        self.insert_into_db()
        
    def insert_into_db(self):
        connection = sqlite3.connect('employee.db')
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employee (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                age INTEGER,
                department TEXT,
                salary REAL
            )
        ''')
        cursor.execute('''
            INSERT INTO employee (first_name, last_name, age, department, salary)
            VALUES (?, ?, ?, ?, ?)
        ''', (self.first_name, self.last_name, self.age, self.department, self.salary))
        connection.commit()
        connection.close()
        
    def transfer(self, new_department):
        self.department = new_department
        connection = sqlite3.connect('employee.db')
        cursor = connection.cursor()
        cursor.execute('''
            UPDATE employee
            SET department = ?
            WHERE first_name = ? AND last_name = ?
        ''', (new_department, self.first_name, self.last_name))
        connection.commit()
        connection.close()
        
    def fire(self):
        Employee.employees.remove(self)
        connection = sqlite3.connect('employee.db')
        cursor = connection.cursor()
        cursor.execute('''
            DELETE FROM employee
            WHERE first_name = ? AND last_name = ?
        ''', (self.first_name, self.last_name))
        connection.commit()
        connection.close()

    def show(self):
        print(f"First Name: {self.first_name}")
        print(f"Last Name: {self.last_name}")
        print(f"Age: {self.age}")
        print(f"Department: {self.department}")
        print(f"Salary: {self.salary}")
        
    @classmethod
    def list_employees(cls):
        connection = sqlite3.connect('employee.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM employee')
        employees = cursor.fetchall()
        for emp in employees:
            print(f"ID: {emp[0]}, First Name: {emp[1]}, Last Name: {emp[2]}, Age: {emp[3]}, Department: {emp[4]}, Salary: {emp[5]}")
        connection.close()

class Manager(Employee):
    def __init__(self, first_name, last_name, age, department, salary, managed_department):
        super().__init__(first_name, last_name, age, department, salary)
        self.managed_department = managed_department
        
    def show(self):
        print(f"First Name: {self.first_name}")
        print(f"Last Name: {self.last_name}")
        print(f"Age: {self.age}")
        print(f"Department: {self.department}")
        print("Salary: Confidential")
        print(f"Managed Department: {self.managed_department}")
        
def command_line_interface():
    while True:
        print("\nMenu:")
        print("1. Add a new employee (enter 'add')")
        print("2. Transfer an employee (enter 'transfer')")
        print("3. Fire an employee (enter 'fire')")
        print("4. List all employees (enter 'list')")
        print("5. Exit the program (enter 'q')")
        
        command = input("\nEnter your choice: ").strip().lower()
        
        if command == "add":
            role = input("If manager press 'm', if employee press 'e': ").strip().lower()
            if role == 'e':
                first_name = input("First Name: ")
                last_name = input("Last Name: ")
                age = int(input("Age: "))
                department = input("Department: ")
                salary = float(input("Salary: "))
                Employee(first_name, last_name, age, department, salary)
                print("Employee added successfully!")
            elif role == 'm':
                first_name = input("First Name: ")
                last_name = input("Last Name: ")
                age = int(input("Age: "))
                department = input("Department: ")
                salary = float(input("Salary: "))
                managed_department = input("Managed Department: ")
                Manager(first_name, last_name, age, department, salary, managed_department)
                print("Manager added successfully!")
            else:
                print("Invalid input. Please try again.")
        elif command == "transfer":
            first_name = input("First Name of the employee to transfer: ")
            last_name = input("Last Name of the employee to transfer: ")
            new_department = input("New Department: ")
            for employee in Employee.employee_list:
                if employee.first_name == first_name and employee.last_name == last_name:
                    employee.transfer(new_department)
                    print("Employee transferred successfully!")
                    break
            else:
                print("Employee not found.")
        elif command == "fire":
            first_name = input("First Name of the employee to fire: ")
            last_name = input("Last Name of the employee to fire: ")
            for employee in Employee.employee_list:
                if employee.first_name == first_name and employee.last_name == last_name:
                    employee.fire()
                    print("Employee fired successfully!")
                    break
            else:
                print("Employee not found.")
        elif command == "list":
            Employee.list_employees()
        elif command == "q":
            print("Exiting the program.")
            break
        
        else:
            print("Invalid choice. Please try again.")

# Run the command-line interface
command_line_interface()