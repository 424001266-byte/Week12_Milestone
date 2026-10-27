import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "employee_project.settings",
)

import django

django.setup()

from employees.models import Employee


class EmployeeManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management System")
        self.root.geometry("850x550")

        self.name_var = tk.StringVar()
        self.position_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready.")

        self.build_menu()
        self.build_interface()
        self.refresh_employees()

    def build_menu(self):
        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(
            label="Refresh Records",
            command=self.refresh_employees,
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Exit",
            command=self.root.destroy,
        )

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(
            label="About",
            command=self.show_about,
        )

        menu_bar.add_cascade(label="File", menu=file_menu)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menu_bar)

    def build_interface(self):
        ttk.Label(
            self.root,
            text="EMPLOYEE MANAGEMENT SYSTEM",
            font=("Arial", 16, "bold"),
        ).pack(pady=12)

        form = ttk.LabelFrame(
            self.root,
            text="Employee Information",
            padding=10,
        )
        form.pack(fill="x", padx=15, pady=5)

        ttk.Label(form, text="Employee Name:").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )

        self.name_entry = ttk.Entry(
            form,
            textvariable=self.name_var,
            width=35,
        )
        self.name_entry.grid(
            row=0, column=1, padx=5, pady=5, sticky="ew"
        )

        ttk.Label(form, text="Position:").grid(
            row=1, column=0, padx=5, pady=5, sticky="w"
        )

        ttk.Entry(
            form,
            textvariable=self.position_var,
            width=35,
        ).grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(
            form, text="Add Employee", command=self.add_employee
        ).grid(row=0, column=2, padx=5, pady=3)

        ttk.Button(
            form, text="Clear Fields", command=self.clear_fields
        ).grid(row=1, column=2, padx=5, pady=3)

        form.columnconfigure(1, weight=1)

        list_frame = ttk.LabelFrame(
            self.root,
            text="Employee Records",
            padding=10,
        )
        list_frame.pack(fill="both", expand=True, padx=15, pady=8)

        columns = ("id", "name", "position", "date_hired")

        self.tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings",
        )

        headings = {
            "id": "ID",
            "name": "Employee Name",
            "position": "Position",
            "date_hired": "Date Hired",
        }

        for column, heading in headings.items():
            self.tree.heading(column, text=heading)

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("name", width=220)
        self.tree.column("position", width=180)
        self.tree.column("date_hired", width=170)

        scrollbar = ttk.Scrollbar(
            list_frame,
            orient="vertical",
            command=self.tree.yview,
        )

        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        ttk.Button(
            self.root,
            text="Refresh List",
            command=self.refresh_employees,
        ).pack(side="left", padx=15, pady=5)

        ttk.Button(
            self.root,
            text="Delete Selected",
            command=self.delete_employee,
        ).pack(side="left", padx=5, pady=5)

        ttk.Label(
            self.root,
            textvariable=self.status_var,
            anchor="w",
        ).pack(fill="x", padx=15, pady=8)

    def add_employee(self):
        name = self.name_var.get().strip()
        position = self.position_var.get().strip()

        if not name or not position:
            messagebox.showerror(
                "Validation Error",
                "Employee name and position are required.",
            )
        elif len(name) > 100 or len(position) > 100:
            messagebox.showerror(
                "Validation Error",
                "Name and position must be 100 characters or fewer.",
            )
        else:
            try:
                employee = Employee.objects.create(
                    name=name,
                    position=position,
                )

                self.refresh_employees()
                self.clear_fields()

                self.status_var.set(
                    f"Added {employee.name}, ID {employee.id}."
                )

                messagebox.showinfo(
                    "Success",
                    "Employee record added successfully.",
                )

            except Exception as error:
                messagebox.showerror(
                    "Database Error",
                    f"Could not save employee:\n{error}",
                )

    def refresh_employees(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            employees = Employee.objects.all().order_by("name", "id")

            for employee in employees:
                hired = (
                    employee.date_hired.strftime("%Y-%m-%d %H:%M")
                    if employee.date_hired
                    else ""
                )

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        employee.id,
                        employee.name,
                        employee.position,
                        hired,
                    ),
                )

            self.status_var.set(
                f"Loaded {employees.count()} employee record(s)."
            )

        except Exception as error:
            messagebox.showerror(
                "Database Error",
                "Run Django migrations before using the application.\n"
                f"{error}",
            )

    def delete_employee(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Select an employee record first.",
            )
        else:
            values = self.tree.item(selected[0], "values")
            employee_id = int(values[0])

            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Delete employee {values[1]}?",
            )

            if confirm:
                try:
                    Employee.objects.filter(
                        pk=employee_id
                    ).delete()

                    self.clear_fields()
                    self.refresh_employees()

                    self.status_var.set(
                        f"Deleted employee ID {employee_id}."
                    )

                except Exception as error:
                    messagebox.showerror(
                        "Database Error",
                        str(error),
                    )

    def clear_fields(self):
        self.name_var.set("")
        self.position_var.set("")
        self.name_entry.focus_set()

    def show_about(self):
        messagebox.showinfo(
            "About",
            "Employee Management System\n"
            "PC15 Python Programming 2 with Lab\n"
            "Django ORM + Tkinter",
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeManagementApp(root)
    root.mainloop()
