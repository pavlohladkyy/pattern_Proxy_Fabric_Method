import time 

# Interface IEmployeeDataSource with methods for reading and writing employee data
class IEmployeeDataSource:
    def read_employee(self, employee_id):
        pass

    def write_employee(self, employee_id, employee_data):
        pass

# Implementation of IEmployeeDataSource class that holds employee data
class EmployeeDataSource(IEmployeeDataSource):
    _database = {}

    def read_employee(self, employee_id):
        print(f"Executing request for employee with ID {employee_id}")
        time.sleep(2)
        return self._database.get(employee_id, "Employee not found")

    def write_employee(self, employee_id, employee_data):
        print(f"Writing data for employee with ID {employee_id}")
        self._database[employee_id] = employee_data
        print("Data successfully written.")

# Factory method for creating an employee data source
class DataSourceFactory:
    @staticmethod
    def create_employee_data_source():
        return EmployeeDataSource()

# Proxy class to control access to EmployeeDataSource
class EmployeeDataSourceProxy(IEmployeeDataSource):
    def __init__(self):
         self.data_source = DataSourceFactory.create_employee_data_source()
         self.cache = {}
        
    def read_employee(self, employee_id):
        if employee_id in self.cache:
            print(f"Data for employee with ID {employee_id} retrieved from cache.")
            return self.cache[employee_id]
        else:
            result = self.data_source.read_employee(employee_id)
            self.cache[employee_id] = result
            return result

    def write_employee(self, employee_id, employee_data):
        print(f"Proxy: forwarding request to write data for employee with ID {employee_id}")
        self.data_source.write_employee(employee_id, employee_data)
        # Update cache
        self.cache[employee_id] = employee_data

def main():
    proxy = EmployeeDataSourceProxy()
    
    while True:
        print("\nChoose an action:")
        print("1. Add data about employee")
        print("2. Get data about employee")
        print("3. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            try:
                employee_id = int(input("Enter Employee ID: "))
                name = input("Enter Employee name: ")
                position = input("Enter Employee position: ")
                employee_data = {"name": name, "position": position}
                proxy.write_employee(employee_id, employee_data)
            except ValueError:
                print("Invalid Employee ID. Please try again.")
                
        elif choice == '2':
            try:
                employee_id = int(input("Enter Employee ID: "))
                data = proxy.read_employee(employee_id)
                print(f"Employee Data: {data}")
            except ValueError:
                print("Invalid Employee ID. Please try again.")
        
        elif choice == '3':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
