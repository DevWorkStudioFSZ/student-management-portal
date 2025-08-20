from student import Student

def cli():
    student = Student()

    while True:
        print("\n STUDENT MANAGEMENT SYSTEM")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Exit")

        choice = input("Choose option (1–5): ")

        if choice == '1':
            name = input("Name: ")
            age = int(input("Age: "))
            grade = input("Grade: ")
            student.add(name, age, grade)

        elif choice == '2':
            student.view_all()

        elif choice == '3':
            sid = int(input("Student ID to update: "))
            name = input("New name: ")
            age = int(input("New age: "))
            grade = input("New grade: ")
            student.update(sid, name, age, grade)

        elif choice == '4':
            sid = int(input("Student ID to delete: "))
            student.delete(sid)

        elif choice == '5':
            print(" Goodbye")
            student.close_connection()
            break

        else:
            print("Invalid option. Try again!")

if __name__ == "__main__":
    cli()
