import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Student(Person):
    def __init__(self, name, stu_id, age, grade, attendance_percentage=0.0):
        super().__init__(name, age)
        self.stu_id = stu_id
        self.grade = grade
        self.attendance_percentage = attendance_percentage
        self.subs = []
        self.marks = {}

    def print_details(self):
        print(f"Name: {self.name} | ID: {self.stu_id} | Age: {self.age}")
        print(f"Grade: {self.grade} | Attendance: {self.attendance_percentage}%")
        print(f"Subjects: {self.subs}")
        print(f"Marks: {self.marks}")
        print("-" * 40)

class School:
    def __init__(self):
        self.students = {}

    def save_data(self):
        students_data = {}
        marks_data = {}

        for sid, s in self.students.items():
            students_data[sid] = {
                "name": s.name, 
                "age": s.age, 
                "grade": s.grade, 
                "subs": s.subs,
                "attendance_percentage": s.attendance_percentage
            }
            marks_data[sid] = s.marks

        with open("students.json", "w") as f: json.dump(students_data, f, indent=4)
        with open("marks.json", "w") as f: json.dump(marks_data, f, indent=4)
        print("Data Saved.")

    def load_data(self):
        try:
            with open("students.json", "r") as f: students_data = json.load(f)
            with open("marks.json", "r") as f: marks_data = json.load(f)
        except FileNotFoundError:
            print("No data found. Starting fresh.")
            return

        for sid, info in students_data.items():
            sid = int(sid)
            att_pct = info.get("attendance_percentage", 0.0)
            
            s = Student(info["name"], sid, info["age"], info["grade"], att_pct)
            s.subs = info.get("subs", [])
            s.marks = marks_data.get(str(sid), {})
            self.students[sid] = s
        print("Database Loaded.")

    def add_student(self):
        try:
            sid = int(input("Enter Student ID: "))
        except ValueError:
            print("ID must be a number.")
            return

        if sid in self.students:
            print("Student already exists")
            return

        name = input("Name: ")
        age = input("Age: ")
        grade = input("Grade: ")
        
        try:
            att_pct = float(input("Enter Attendance Percentage (0-100): "))
        except ValueError:
            att_pct = 0.0

        self.students[sid] = Student(name, sid, age, grade, att_pct)
        self.save_data()
        print("Student added")

    def delete_students(self):
        try:
            sid = int(input("Enter Student ID: "))
        except ValueError: return
        
        if sid in self.students:
            del self.students[sid]
            self.save_data()
            print("Student deleted")
        else:
            print("Student not found")

    def update_students(self):
        try:
            sid = int(input("Enter Student ID: "))
        except ValueError: return

        if sid in self.students:
            s = self.students[sid]
            
            print(f"Updating {s.name} (Press Enter to skip)")
            
            name = input(f"New Name ({s.name}): ").strip()
            if name: 
                s.name = name
            age = input(f"New Age ({s.age}): ").strip()
            if age:
                 s.age = age
            grade = input(f"New Grade ({s.grade}): ").strip()
            if grade: 
                s.grade = grade
            att_input = input(f"New Attendance % ({s.attendance_percentage}): ").strip()
            if att_input:
                try:
                    s.attendance_percentage = float(att_input)
                except ValueError:
                    print("Invalid number for attendance, skipping update.")

            self.save_data()
            print("Updated.")
        else:
            print("Not found.")

    def view_students(self):
        if not self.students:
            print("No students available")
        else:
            for s in self.students.values():
                s.print_details()

    def attendance(self):
        try:
            sid = int(input("Student ID: "))
        except ValueError: return

        if sid in self.students:
            s = self.students[sid]
            print(f"\nCurrent Attendance: {s.attendance_percentage}%")
            
            if input("Update Percentage? (y/n): ").lower() == 'y':
                try:
                    new_pct = float(input("Enter new percentage (0-100): "))
                    if 0 <= new_pct <= 100:
                        s.attendance_percentage = new_pct
                        self.save_data()
                        print("Updated.")
                    else:
                        print("Must be between 0 and 100.")
                except ValueError:
                    print("Invalid number.")
            
            if s.attendance_percentage < 75:
                print("WARNING: You won't be allowed to sit in the exam!")
            else:
                print("Eligible for exam.")
        else:
            print("Student not found.")

    def marks(self):
        try:
            sid = int(input("Student ID: "))
        except ValueError: return

        if sid in self.students:
            s = self.students[sid]
            while True:
                sub = input("Subject: ").capitalize()
                try:
                    mark = float(input("Marks: "))
                except ValueError: continue

                if 0 <= mark <= 100:
                    s.marks[sub] = mark
                    if sub not in s.subs:
                        s.subs.append(sub)
                    print(f"Saved {sub}: {mark}")
                else:
                    print("Marks must be 0-100.")

                if input("Add more? (y/n): ").lower() == 'n':
                    break
            self.save_data()
        else:
            print("Student not found.")

    def student_report(self):
        try:
            sid = int(input("Student ID: "))
        except ValueError: return

        if sid in self.students:
            s = self.students[sid]
            if not s.marks:
                print("No marks available")
                return

            avg = np.mean(list(s.marks.values()))
            print(f"\nReport for {s.name}")
            print(f"   Average: {avg:.2f}")
            print(f"   Attendance: {s.attendance_percentage}%")

            if 90 <= avg <= 100: print("   Grade: A")
            elif 80 <= avg < 90: print("   Grade: B")
            elif 70 <= avg < 80: print("   Grade: C")
            elif 60 <= avg < 70: print("   Grade: D")
            else: print("   Grade: F")

            print("   --- Highlights ---")
            for sub, score in s.marks.items():
                if score >= 90: print(f"   Top performer in {sub}")
                elif score < 40: print(f"   Failed in {sub}")
        else:
            print("Student not found.")

    def get_class_dataframe(self):
        data = []
        for s in self.students.values():
            if s.marks:
                marks_array = np.array(list(s.marks.values()))
                avg = np.mean(marks_array)
                status = "Pass" if np.greater(avg, 40) else "Fail"
            else:
                avg = 0
                status = "No Data"
            
            data.append({
                "Name": s.name, 
                "Average": avg, 
                "Status": status,
                "Attendance %": s.attendance_percentage
            })
        return pd.DataFrame(data)

    def class_performance_report(self):
        print("\n--- CLASS ANALYTICS ---")
        if not self.students:
            print("No students enrolled.")
            return

        df = self.get_class_dataframe()
        
        if df.empty:
            print("No data available.")
        else:
            print(df.to_string(index=False)) # no index i.e no student at index 0 and to_string so that each data is printed
            
            print("\nSTATISTICS")
            avg_array = df["Average"].to_numpy() # converts avg named col to numpy
            # Numerical analysis
            print(f"Class Mean: {np.mean(avg_array):.2f}")
            print(f"Highest:    {np.max(avg_array):.2f}")
            print(f"Lowest:     {np.min(avg_array):.2f}")
            print(f"Median:     {np.median(avg_array):.2f}") 
            print(f"Std Dev:    {np.std(avg_array):.2f}")

    def view_top_performers(self):
        print("\nTOP PERFORMERS")
        df = self.get_class_dataframe()
        if not df.empty:
            top_df = df.sort_values(by="Average", ascending=False).head(3) # data in desc and only top 3 performers
            print(top_df[["Name", "Average", "Status"]].to_string(index=False))
        else:
            print("No data.")

    def view_low_attendance_list(self):
        print("\nLOW ATTENDANCE LIST (<75%)")
        df = self.get_class_dataframe()
        if not df.empty:
            low_att = df[df["Attendance %"] < 75] # df["Attendance %"]<75 tells true if condn satifies and false if not and the outer df gives only the "true" value!!
            if not low_att.empty:
                print(low_att[["Name", "Attendance %"]].to_string(index=False))
            else:
                print("Everyone has good attendance!")
        else:
            print("No data.")

    def generate_graphs(self):
        print("\n--- GENERATING GRAPHS ---")
        print("1. Student Performance (Average Marks)")
        print("2. Attendance Percentage")
        print("3. Subject-wise Class Performance")
        
        try:
            choice = int(input("Choose graph type (1-3): "))
        except ValueError: return

        df = self.get_class_dataframe()
        if df.empty:
            print("No data to plot.")
            return

        if choice == 1:
            df.plot(kind='bar', x='Name', y='Average', color='skyblue', legend=False)
            plt.title("Student Performance")
            plt.ylabel("Average Marks")
            plt.xlabel("Student List")
            plt.ylim(0, 100)
            plt.savefig("performance_graph.png")
            print("Saved as 'performance_graph.png'")
            plt.show()

        elif choice == 2:
            df.plot(kind='bar', x='Name', y='Attendance %', color='lightgreen', legend=False)
            plt.title("Attendance Percentage")
            plt.ylabel("Percentage (%)")
            plt.xlabel("Student List")
            plt.ylim(0, 100)
            plt.axhline(y=75, color='r', linestyle='--', label='75% Threshold') # line on graph
            plt.legend()
            plt.savefig("attendance_graph.png")
            print("Saved as 'attendance_graph.png'")
            plt.show()

        elif choice == 3:
            subject_totals = {}
            subject_counts = {}
            for s in self.students.values():
                for sub, mark in s.marks.items():
                    subject_totals[sub] = subject_totals.get(sub, 0) + mark # so for a student s that exists in self.students and has got marks for a sub we sum the total marks of all subjects for all students one-by-one if sub doesnt exist give 0 else add the marks of s1 with s2
                    subject_counts[sub] = subject_counts.get(sub, 0) + 1 # so count students who has got marks for a sub and if sub doesnt exist give 0
            
            if subject_totals:
                subjects = list(subject_totals.keys())
                avgs = [np.divide(subject_totals[s], subject_counts[s]) for s in subjects]
                plt.bar(subjects, avgs, color='orange')
                plt.title("Class Average per Subject")
                plt.ylabel("Marks")
                plt.xlabel("Subjects")
                plt.ylim(0, 100)
                plt.savefig("subject_graph.png")
                print("Saved as 'subject_graph.png'")
                plt.show()
            else:
                print("No subject data available.")

if __name__ == "__main__":
    obj = School()
    obj.load_data()

    while True:
        print("\n" + "="*30)
        print("1. Add Student")
        print("2. Update Student")
        print("3. Delete Student")
        print("4. View All Students")
        print("5. Attendance (Update/Check)")
        print("6. Add Marks")
        print("7. View Student Report")
        print("8. Class Analytics (Pandas)")
        print("9. Generate Graphs & Save")
        print("10. View Top Performers")
        print("11. Check Low Attendance")
        print("12. Exit")

        try:
            ch = int(input("Choice: "))
        except ValueError: continue

        if ch == 1: obj.add_student()
        elif ch == 2: obj.update_students()
        elif ch == 3: obj.delete_students()
        elif ch == 4: obj.view_students()
        elif ch == 5: obj.attendance()
        elif ch == 6: obj.marks()
        elif ch == 7: obj.student_report()
        elif ch == 8: obj.class_performance_report()
        elif ch == 9: obj.generate_graphs()
        elif ch == 10: obj.view_top_performers()
        elif ch == 11: obj.view_low_attendance_list()
        elif ch == 12:
            print("Goodbye")
            break