import time 
#інтерфейс IEmployeedataSource з методами читпання та запису співробіників
class IEmployeedataSource:
    def read_employee(self,employee_id):
        pass

    def write_employee(self, employee_id,employee_data):
        pass
#реалізація класу IEmployeedataSource , що містить дпані про співробіників
class EmployeeDataSource(IEmployeedataSource):
    _database = {}

    def read_employee(self,employee_id):
        print(f"виконується запит для співробітника з  ID {employee_id}")
        time.sleep(2)
        return self._database.get(employee_id,"співробітника не знайдено")

    def write_employee(self,employee_id, employee_data):
        print(f"Запис даних про співробіника з ID {employee_id}")
        self._database[employee_id]= employee_data
        print("Дані успішно записано.")

#Фабричний метод для створення джерела даних про співробіників 
class DataSourceFactory:
    def create_employee_data_source():
        return EmployeeDataSource()


#Proxy-клас для конторолю доступу до EmployeeDataSource
class EmployeeDataSourceProxy(IEmployeedataSource):
    def _init_(self):
         self.data_source = DataSourceFactory.create_employee_data_source()
         self.cashe = {}
        
    def read_employee(self,employee_id):
        if employee_id in self.cashe:
            print(f"Дані для співробіників з ID {employee_id} отримані з кешу.")
            return self.cashe[employee_id]

        else:
            result = self.data_source.read_employee(employee_id)
            self.cashe[employee_id]= result
            return result

    def write_employee(self,employee_id, employee_data):
        print(f"Проксі:передача запиту на запис даних для співробіників з ID {employee_id} ")
        self.data_source.write_employee(employee_id,employee_data)
        #оновлення кешу
        self.cashe[employee_id ]= employee_data
    
def main():
    proxy = EmployeeDataSourceProxy()
    
    while True:
        print("\nОберіть дію:")
        print("1. Додати дані про співробітника")
        print("2. Отримати дані про співробітника")
        print("3. Вийти")
        choice = input("Введіть номер дії: ")
        
        if choice == '1':
            try:
                employee_id = int(input("Введіть ID співробітника: "))
                name = input("Введіть ім'я співробітника: ")
                position = input("Введіть посаду співробітника: ")
                employee_data = {"name": name, "position": position}
                proxy.write_employee(employee_id, employee_data)
            except ValueError:
                print("Некоректний ID співробітника. Спробуйте ще раз.")
                
        elif choice == '2':
            try:
                employee_id = int(input("Введіть ID співробітника: "))
                data = proxy.read_employee(employee_id)
                print(f"Дані про співробітника: {data}")
            except ValueError:
                print("Некоректний ID співробітника. Спробуйте ще раз.")
        
        elif choice == '3':
            print("Вихід з програми.")
            break
        else:
            print("Некоректний вибір. Спробуйте ще раз.")

# Запуск програми
if __name__ == "__main__":
    main()

