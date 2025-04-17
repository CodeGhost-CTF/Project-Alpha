#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

using namespace std;

class Employee {
private:
    int id;
    string name;
    double salary;
    string department;

public:
    // Constructor
    Employee(int id, string name, double salary, string department)
        : id(id), name(name), salary(salary), department(department) {}

    // Getters
    int getId() const { return id; }
    string getName() const { return name; }
    double getSalary() const { return salary; }
    string getDepartment() const { return department; }

    // Setters
    void setName(string newName) { name = newName; }
    void setSalary(double newSalary) { salary = newSalary; }
    void setDepartment(string newDept) { department = newDept; }

    void display() const {
        cout << "ID: " << id << endl;
        cout << "Name: " << name << endl;
        cout << "Salary: $" << salary << endl;
        cout << "Department: " << department << endl;
        cout << "--------------------------" << endl;
    }
};

vector<Employee> employees;

void addEmployee() {
    int id;
    string name, department;
    double salary;

    cout << "Enter Employee ID: ";
    cin >> id;
    cin.ignore(); // Clear buffer

    cout << "Enter Name: ";
    getline(cin, name);

    cout << "Enter Salary: $";
    cin >> salary;
    cin.ignore();

    cout << "Enter Department: ";
    getline(cin, department);

    employees.emplace_back(id, name, salary, department);
    cout << "Employee added successfully!" << endl;
}

void displayAll() {
    if(employees.empty()) {
        cout << "No employees to display!" << endl;
        return;
    }

    cout << "\nEmployee List:\n";
    for(const auto& emp : employees) {
        emp.display();
    }
}

void searchEmployee() {
    int searchId;
    cout << "Enter Employee ID to search: ";
    cin >> searchId;

    auto it = find_if(employees.begin(), employees.end(),
        [searchId](const Employee& emp) { return emp.getId() == searchId; });

    if(it != employees.end()) {
        it->display();
    } else {
        cout << "Employee not found!" << endl;
    }
}

void updateEmployee() {
    int updateId;
    cout << "Enter Employee ID to update: ";
    cin >> updateId;

    auto it = find_if(employees.begin(), employees.end(),
        [updateId](const Employee& emp) { return emp.getId() == updateId; });

    if(it != employees.end()) {
        string name, department;
        double salary;

        cin.ignore();
        cout << "Enter new Name: ";
        getline(cin, name);

        cout << "Enter new Salary: $";
        cin >> salary;
        cin.ignore();

        cout << "Enter new Department: ";
        getline(cin, department);

        it->setName(name);
        it->setSalary(salary);
        it->setDepartment(department);

        cout << "Employee updated successfully!" << endl;
    } else {
        cout << "Employee not found!" << endl;
    }
}

void deleteEmployee() {
    int deleteId;
    cout << "Enter Employee ID to delete: ";
    cin >> deleteId;

    auto it = remove_if(employees.begin(), employees.end(),
        [deleteId](const Employee& emp) { return emp.getId() == deleteId; });

    if(it != employees.end()) {
        employees.erase(it, employees.end());
        cout << "Employee deleted successfully!" << endl;
    } else {
        cout << "Employee not found!" << endl;
    }
}

int main() {
    int choice;

    do {
        cout << "\nEmployee Management System\n";
        cout << "1. Add Employee\n";
        cout << "2. Display All Employees\n";
        cout << "3. Search Employee\n";
        cout << "4. Update Employee\n";
        cout << "5. Delete Employee\n";
        cout << "6. Exit\n";
        cout << "Enter your choice: ";
        cin >> choice;

        switch(choice) {
            case 1: addEmployee(); break;
            case 2: displayAll(); break;
            case 3: searchEmployee(); break;
            case 4: updateEmployee(); break;
            case 5: deleteEmployee(); break;
            case 6: cout << "Exiting..."; break;
            default: cout << "Invalid choice!" << endl;
        }
    } while(choice != 6);

    return 0;
}
