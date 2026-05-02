# Student Management & Analytics System

A comprehensive Python-based management system designed to streamline student data tracking, academic performance analysis, and attendance monitoring[cite: 2]. This project leverages Object-Oriented Programming (OOP) and data science libraries to provide actionable insights into class performance[cite: 2].

---

## 🚀 Features

*   **Student Records Management**: Full CRUD (Create, Read, Update, Delete) functionality for student profiles, including age, grade, and personal details[cite: 2, 4].
*   **Academic Tracking**: Add and manage marks across various subjects with automated grade calculation[cite: 2, 3].
*   **Attendance Monitoring**: Track attendance percentages with built-in eligibility warnings for students falling below the 75% threshold[cite: 2].
*   **Advanced Analytics**:
    *   **Class Reports**: Generates detailed DataFrames using **Pandas** to show averages and pass/fail status[cite: 2].
    *   **Statistical Analysis**: Computes class mean, median, standard deviation, and identifies top performers using **NumPy**[cite: 2].
*   **Data Visualization**: Generates and saves bar graphs for student performance, attendance trends, and subject-wise averages using **Matplotlib**[cite: 2].
*   **Persistent Storage**: Automatically saves and loads data from localized JSON files (`students.json`, `marks.json`) to ensure data remains intact between sessions[cite: 1, 2, 3, 4].

---

## 🛠️ Tech Stack

*   **Language**: Python 3.x[cite: 2]
*   **Libraries**:
    *   `Pandas`: For data manipulation and tabular reports[cite: 2].
    *   `NumPy`: For numerical computations and array-based logic[cite: 2].
    *   `Matplotlib`: For generating performance and attendance graphs[cite: 2].
    *   `JSON`: For lightweight data persistence[cite: 1, 2, 3, 4].

---

## 📂 Project Structure

```text
├── main.py              # Core application logic and Class definitions
├── students.json        # Persistent storage for student profile data
├── marks.json           # Persistent storage for academic records
├── attendance.json      # (Optional) Record of daily attendance logs
└── performance_graph.png # Generated visual analytics (after export)
```

---

## ⚙️ Installation & Usage

### Prerequisites
Ensure you have the required libraries installed:
```bash
pip install numpy pandas matplotlib
```

### Running the System
1. Clone the repository to your local machine.
2. Navigate to the directory and run the main script:
   ```bash
   python main.py
   ```
3. Use the interactive menu to manage students, input marks, or view class analytics[cite: 2].

---

## 📊 Sample Data Format

The system stores data in structured JSON formats to allow for easy portability and manual review:

**Student Profile Example (`students.json`)**:
```json
"102": {
    "name": "Diya",
    "age": "17",
    "grade": "11",
    "attendance_percentage": 0.0
}
```
[cite: 4]

**Marks Record Example (`marks.json`)**:
```json
"101": {
    "Math": 88,
    "Science": 92
}
```
[cite: 3]
```
