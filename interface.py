import tkinter as tk
from tkinter import messagebox, simpledialog
from main import run_bot, courses  

class BotInterface:
    def __init__(self, master):
        self.master = master
        master.title("ATACS Bot Interface")
        self.driver = None   # 🔑 Selenium driver referansı

        # Username
        tk.Label(master, text="Username:").grid(row=0, column=0, sticky="e")
        self.username_entry = tk.Entry(master)
        self.username_entry.grid(row=0, column=1)

        # Password
        tk.Label(master, text="Password:").grid(row=1, column=0, sticky="e")
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.grid(row=1, column=1)

        # Course listbox
        tk.Label(master, text="Courses:").grid(row=2, column=0, sticky="ne")
        self.course_listbox = tk.Listbox(master, height=5, width=30)
        self.course_listbox.grid(row=2, column=1)

        # Buttons
        button_frame = tk.Frame(master)
        button_frame.grid(row=3, column=1, sticky="w")

        self.add_button = tk.Button(button_frame, text="Add", command=self.add_course)
        self.add_button.pack(side="left", padx=2)

        self.edit_button = tk.Button(button_frame, text="Edit", command=self.edit_course)
        self.edit_button.pack(side="left", padx=2)

        self.delete_button = tk.Button(button_frame, text="Delete", command=self.delete_course)
        self.delete_button.pack(side="left", padx=2)

        # Start and Close bot buttons
        self.start_button = tk.Button(master, text="Start Bot", command=self.start_bot)
        self.start_button.grid(row=4, column=1, sticky="w")

        self.close_button = tk.Button(master, text="Close Bot", command=self.close_bot)
        self.close_button.grid(row=5, column=1, sticky="w")

        # Load existing courses
        for course_code, section in courses:
            self.course_listbox.insert(tk.END, f"{course_code} - {section}")

    def add_course(self):
        course_code = simpledialog.askstring("Course Code", "Enter course code (e.g., CMPE323):")
        section = simpledialog.askstring("Section", "Enter section (e.g., SEC-01):")
        if course_code and section:
            courses.append([course_code, section])
            self.course_listbox.insert(tk.END, f"{course_code} - {section}")

    def edit_course(self):
        selected_index = self.course_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a course to edit.")
            return

        index = selected_index[0]
        course_code, section = courses[index]

        new_course_code = simpledialog.askstring("Edit Course", "Enter new course code:", initialvalue=course_code)
        new_section = simpledialog.askstring("Edit Section", "Enter new section:", initialvalue=section)

        if new_course_code and new_section:
            courses[index] = [new_course_code, new_section]
            self.course_listbox.delete(index)
            self.course_listbox.insert(index, f"{new_course_code} - {new_section}")

    def delete_course(self):
        selected_index = self.course_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a course to delete.")
            return

        index = selected_index[0]
        del courses[index]
        self.course_listbox.delete(index)

    def start_bot(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Username and password are required!")
            return

        try:
            self.driver = run_bot(username, password)  # driver saklanıyor
            messagebox.showinfo("Bot Started", "Bot started successfully.")
        except Exception as e:
            messagebox.showerror("Bot Error", str(e))

    def close_bot(self):
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
                messagebox.showinfo("Bot Closed", "Bot has been closed successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Error closing bot: {e}")
        else:
            messagebox.showwarning("Warning", "No bot is currently running.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BotInterface(root)
    root.mainloop()
