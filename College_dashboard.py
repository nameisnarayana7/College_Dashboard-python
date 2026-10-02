"""
College Dashboard System (Tkinter + SQLite + Matplotlib)
Single-file example application demonstrating:
- Attendance module
- Marks module
- Reports module (charts)
- Admin module (manage students)

"""

import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

DB_FILE = "college_dashboard.db"

# ----------------------------- Database Layer -----------------------------
class Database:
    def __init__(self, db_file=DB_FILE):
        self.conn = sqlite3.connect(db_file)
        self.create_tables()

    def create_tables(self):
        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                roll TEXT UNIQUE,
                name TEXT,
                dept TEXT
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                date TEXT,
                status TEXT,
                FOREIGN KEY(student_id) REFERENCES students(id)
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS marks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                subject TEXT,
                marks INTEGER,
                FOREIGN KEY(student_id) REFERENCES students(id)
            )
        ''')
        self.conn.commit()

    # Students
    def add_student(self, roll, name, dept):
        try:
            c = self.conn.cursor()
            c.execute("INSERT INTO students (roll, name, dept) VALUES (?,?,?)", (roll, name, dept))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def update_student(self, student_id, roll, name, dept):
        c = self.conn.cursor()
        c.execute("UPDATE students SET roll=?, name=?, dept=? WHERE id=?", (roll, name, dept, student_id))
        self.conn.commit()

    def delete_student(self, student_id):
        c = self.conn.cursor()
        c.execute("DELETE FROM students WHERE id=?", (student_id,))
        c.execute("DELETE FROM attendance WHERE student_id=?", (student_id,))
        c.execute("DELETE FROM marks WHERE student_id=?", (student_id,))
        self.conn.commit()

    def get_students(self, search=""):
        c = self.conn.cursor()
        if search:
            like = f"%{search}%"
            c.execute("SELECT id, roll, name, dept FROM students WHERE roll LIKE ? OR name LIKE ? OR dept LIKE ? ORDER BY roll", (like, like, like))
        else:
            c.execute("SELECT id, roll, name, dept FROM students ORDER BY roll")
        return c.fetchall()

    def get_student(self, student_id):
        c = self.conn.cursor()
        c.execute("SELECT id, roll, name, dept FROM students WHERE id=?", (student_id,))
        return c.fetchone()

    # Attendance
    def mark_attendance(self, student_id, date, status):
        c = self.conn.cursor()
        c.execute("INSERT INTO attendance (student_id, date, status) VALUES (?,?,?)", (student_id, date, status))
        self.conn.commit()

    def get_attendance(self, date_from=None, date_to=None):
        c = self.conn.cursor()
        q = "SELECT a.id, s.roll, s.name, s.dept, a.date, a.status, a.student_id FROM attendance a JOIN students s ON a.student_id=s.id"
        if date_from and date_to:
            q += " WHERE date BETWEEN ? AND ?"
            c.execute(q + " ORDER BY a.date DESC", (date_from, date_to))
        else:
            c.execute(q + " ORDER BY a.date DESC")
        return c.fetchall()

    def get_attendance_summary(self):
        c = self.conn.cursor()
        c.execute("SELECT s.name, s.roll, SUM(CASE WHEN a.status='Present' THEN 1 ELSE 0 END) as present_count, COUNT(a.id) as total FROM students s LEFT JOIN attendance a ON s.id=a.student_id GROUP BY s.id")
        return c.fetchall()

    # Marks
    def add_mark(self, student_id, subject, marks):
        c = self.conn.cursor()
        c.execute("INSERT INTO marks (student_id, subject, marks) VALUES (?,?,?)", (student_id, subject, marks))
        self.conn.commit()

    def get_marks(self):
        c = self.conn.cursor()
        c.execute("SELECT m.id, s.roll, s.name, m.subject, m.marks FROM marks m JOIN students s ON m.student_id=s.id ORDER BY s.roll")
        return c.fetchall()

    def get_marks_summary(self):
        c = self.conn.cursor()
        c.execute("SELECT s.name, s.roll, AVG(m.marks) as avg_marks FROM students s LEFT JOIN marks m ON s.id=m.student_id GROUP BY s.id")
        return c.fetchall()

    def close(self):
        self.conn.close()

# ----------------------------- GUI Application -----------------------------
class CollegeDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("College Dashboard System")
        self.geometry("1000x650")

        self.db = Database()

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.admin_frame = AdminFrame(self.notebook, self.db)
        self.attendance_frame = AttendanceFrame(self.notebook, self.db)
        self.marks_frame = MarksFrame(self.notebook, self.db)
        self.reports_frame = ReportsFrame(self.notebook, self.db)

        self.notebook.add(self.admin_frame, text="Admin")
        self.notebook.add(self.attendance_frame, text="Attendance")
        self.notebook.add(self.marks_frame, text="Marks")
        self.notebook.add(self.reports_frame, text="Reports")

        # Menu
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Import sample data", command=self.import_sample_data)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.on_exit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)

    def import_sample_data(self):
        # Add a few students and marks for demo
        sample_students = [
            ("101", "Narayana", "CSE"),
            ("201", "Sri Lakshmi", "CSE"),
            ("301", "Lakshmi Narayana", "EEE"),
            ("401", "Basha", "MECH"),
        ]
        for roll, name, dept in sample_students:
            self.db.add_student(roll, name, dept)
        # Add some marks
        students = self.db.get_students()
        subjects = ["Maths", "Physics", "Programming"]
        import random
        for sid, roll, name, dept in students:
            for sub in subjects:
                self.db.add_mark(sid, sub, random.randint(50, 95))
        messagebox.showinfo("Import", "Sample data imported. Refresh the tabs to see data.")
        # Refresh
        self.admin_frame.refresh()
        self.marks_frame.refresh()
        self.reports_frame.refresh()

    def on_exit(self):
        self.db.close()
        self.destroy()

# ----------------------------- Admin Frame -----------------------------
class AdminFrame(ttk.Frame):
    def __init__(self, parent, db: Database):
        super().__init__(parent)
        self.db = db
        self.setup_ui()

    def setup_ui(self):
        top = ttk.Frame(self)
        top.pack(fill=tk.X, padx=8, pady=6)
        ttk.Label(top, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(top, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, padx=4)
        ttk.Button(top, text="Search", command=self.refresh).pack(side=tk.LEFT, padx=4)
        ttk.Button(top, text="Add Student", command=self.add_student_dialog).pack(side=tk.RIGHT)

        # Treeview
        cols = ("id", "roll", "name", "dept")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
        self.tree.column("id", width=50)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=8, pady=6)
        ttk.Button(btn_frame, text="Edit", command=self.edit_student).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Delete", command=self.delete_student).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh).pack(side=tk.RIGHT)

        self.refresh()

    def add_student_dialog(self):
        dlg = StudentDialog(self, "Add Student")
        self.wait_window(dlg)
        if dlg.result:
            roll, name, dept = dlg.result
            ok = self.db.add_student(roll, name, dept)
            if not ok:
                messagebox.showerror("Error", "Roll number already exists.")
            self.refresh()

    def edit_student(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Please select a student")
            return
        item = self.tree.item(sel[0])
        sid = item['values'][0]
        data = self.db.get_student(sid)
        dlg = StudentDialog(self, "Edit Student", initial=(data[1], data[2], data[3]))
        self.wait_window(dlg)
        if dlg.result:
            roll, name, dept = dlg.result
            self.db.update_student(sid, roll, name, dept)
            self.refresh()

    def delete_student(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Please select a student")
            return
        item = self.tree.item(sel[0])
        sid = item['values'][0]
        if messagebox.askyesno("Confirm", "Delete selected student and related data?"):
            self.db.delete_student(sid)
            self.refresh()

    def refresh(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        rows = self.db.get_students(self.search_var.get())
        for row in rows:
            self.tree.insert('', tk.END, values=row)

class StudentDialog(tk.Toplevel):
    def __init__(self, parent, title, initial=None):
        super().__init__(parent)
        self.title(title)
        self.result = None
        self.transient(parent)
        self.grab_set()
        ttk.Label(self, text="Roll:").grid(row=0, column=0, padx=8, pady=6)
        ttk.Label(self, text="Name:").grid(row=1, column=0, padx=8, pady=6)
        ttk.Label(self, text="Dept:").grid(row=2, column=0, padx=8, pady=6)
        self.roll_var = tk.StringVar(value=initial[0] if initial else "")
        self.name_var = tk.StringVar(value=initial[1] if initial else "")
        self.dept_var = tk.StringVar(value=initial[2] if initial else "")
        ttk.Entry(self, textvariable=self.roll_var).grid(row=0, column=1)
        ttk.Entry(self, textvariable=self.name_var).grid(row=1, column=1)
        ttk.Entry(self, textvariable=self.dept_var).grid(row=2, column=1)
        bframe = ttk.Frame(self)
        bframe.grid(row=3, column=0, columnspan=2, pady=8)
        ttk.Button(bframe, text="OK", command=self.on_ok).pack(side=tk.LEFT, padx=4)
        ttk.Button(bframe, text="Cancel", command=self.destroy).pack(side=tk.LEFT)

    def on_ok(self):
        roll = self.roll_var.get().strip()
        name = self.name_var.get().strip()
        dept = self.dept_var.get().strip()
        if not (roll and name and dept):
            messagebox.showwarning("Empty", "All fields are required")
            return
        self.result = (roll, name, dept)
        self.destroy()

# ----------------------------- Attendance Frame -----------------------------
class AttendanceFrame(ttk.Frame):
    def __init__(self, parent, db: Database):
        super().__init__(parent)
        self.db = db
        self.setup_ui()

    def setup_ui(self):
        top = ttk.Frame(self)
        top.pack(fill=tk.X, padx=8, pady=6)
        ttk.Button(top, text="Mark Today's Attendance", command=self.mark_today).pack(side=tk.LEFT)
        ttk.Button(top, text="Export CSV", command=self.export_csv).pack(side=tk.RIGHT)
        ttk.Button(top, text="Refresh", command=self.refresh).pack(side=tk.RIGHT)

        cols = ("id", "roll", "name", "dept", "date", "status")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
        self.tree.column("id", width=50)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.refresh()

    def mark_today(self):
        students = self.db.get_students()
        date = datetime.now().strftime('%Y-%m-%d')
        for sid, roll, name, dept in students:
            # Ask for each student - in a real app you'd show a better UI; here simple dialog
            resp = messagebox.askyesno("Attendance", f"Is {name} ({roll}) present?")
            status = 'Present' if resp else 'Absent'
            self.db.mark_attendance(sid, date, status)
        messagebox.showinfo("Done", "Today's attendance recorded")
        self.refresh()

    def export_csv(self):
        rows = self.db.get_attendance()
        if not rows:
            messagebox.showwarning("No data", "No attendance records to export")
            return
        path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files','*.csv')])
        if not path:
            return
        with open(path, 'w', encoding='utf-8') as f:
            f.write('id,roll,name,dept,date,status\n')
            for r in rows:
                f.write(','.join(str(x) for x in r[:6]) + '\n')
        messagebox.showinfo("Exported", f"Saved to {path}")

    def refresh(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        rows = self.db.get_attendance()
        for row in rows:
            self.tree.insert('', tk.END, values=row[:6])

# ----------------------------- Marks Frame -----------------------------
class MarksFrame(ttk.Frame):
    def __init__(self, parent, db: Database):
        super().__init__(parent)
        self.db = db
        self.setup_ui()

    def setup_ui(self):
        top = ttk.Frame(self)
        top.pack(fill=tk.X, padx=8, pady=6)
        ttk.Button(top, text="Add Mark", command=self.add_mark_dialog).pack(side=tk.LEFT)
        ttk.Button(top, text="Refresh", command=self.refresh).pack(side=tk.RIGHT)

        cols = ("id", "roll", "name", "subject", "marks")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
        self.tree.column("id", width=50)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.refresh()

    def add_mark_dialog(self):
        students = self.db.get_students()
        if not students:
            messagebox.showwarning("No students", "Add students first")
            return
        # A simple dialog: choose student by roll
        choices = [f"{r[1]} - {r[2]}" for r in students]
        choice = simpledialog.askstring("Add Mark", "Enter: roll,subject,marks\n(e.g. 101,Programming,85)")
        if not choice:
            return
        try:
            roll, subject, marks = [x.strip() for x in choice.split(',')]
            marks = int(marks)
        except Exception:
            messagebox.showerror("Error", "Invalid input format")
            return
        # Find student id
        sid = None
        for r in students:
            if r[1] == roll:
                sid = r[0]
                break
        if not sid:
            messagebox.showerror("Error", "Roll not found")
            return
        self.db.add_mark(sid, subject, marks)
        messagebox.showinfo("Added", "Mark recorded")
        self.refresh()

    def refresh(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        rows = self.db.get_marks()
        for row in rows:
            self.tree.insert('', tk.END, values=row)

# ----------------------------- Reports Frame -----------------------------
class ReportsFrame(ttk.Frame):
    def __init__(self, parent, db: Database):
        super().__init__(parent)
        self.db = db
        self.setup_ui()

    def setup_ui(self):
        top = ttk.Frame(self)
        top.pack(fill=tk.X, padx=8, pady=6)
        ttk.Button(top, text="Attendance Summary", command=self.plot_attendance_summary).pack(side=tk.LEFT)
        ttk.Button(top, text="Marks Summary", command=self.plot_marks_summary).pack(side=tk.LEFT)
        ttk.Button(top, text="Refresh", command=self.refresh).pack(side=tk.RIGHT)

        # Chart area
        self.chart_frame = ttk.Frame(self)
        self.chart_frame.pack(fill=tk.BOTH, expand=True)

        self.refresh()

    def clear_chart(self):
        for w in self.chart_frame.winfo_children():
            w.destroy()

    def plot_attendance_summary(self):
        self.clear_chart()
        rows = self.db.get_attendance_summary()
        names = [r[0] for r in rows]
        present = [r[2] for r in rows]
        total = [r[3] for r in rows]
        fig = Figure(figsize=(7,4))
        ax = fig.add_subplot(111)
        ax.bar(names, present)
        ax.set_title('Present Count per Student')
        ax.set_ylabel('Present Count')
        ax.tick_params(axis='x', rotation=30)
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def plot_marks_summary(self):
        self.clear_chart()
        rows = self.db.get_marks_summary()
        names = [r[0] for r in rows]
        avg = [r[2] if r[2] is not None else 0 for r in rows]
        fig = Figure(figsize=(7,4))
        ax = fig.add_subplot(111)
        ax.plot(names, avg, marker='o')
        ax.set_title('Average Marks per Student')
        ax.set_ylabel('Average Marks')
        ax.tick_params(axis='x', rotation=30)
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def refresh(self):
        self.clear_chart()
        # Show a welcome text
        lbl = ttk.Label(self.chart_frame, text="Use the buttons above to generate reports.", anchor='center')
        lbl.pack(expand=True)

# ----------------------------- Run App -----------------------------
if __name__ == '__main__':
    app = CollegeDashboard()
    app.mainloop()
