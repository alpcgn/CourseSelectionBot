import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
from main import run_interface, courses  

class BotInterface:
    def __init__(self, master):
        self.master = master
        master.title("ATACS Bot by @alpcgn")
        self.driver = None 

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

        # Week selection
        tk.Label(master, text="Week:").grid(row=6, column=0, sticky="e", padx=5, pady=5)

        self.week_var = tk.StringVar()
        self.week_var.set("firstweek") 

        self.radio_frame = tk.Frame(master)
        self.radio_frame.grid(row=6, column=1, sticky="w")

        tk.Radiobutton(self.radio_frame, text="First Week", variable=self.week_var, value="firstweek").pack(side="left")
        tk.Radiobutton(self.radio_frame, text="Add/Drop", variable=self.week_var, value="adddrop").pack(side="left")

        # Start and Close bot buttons
        self.start_button = tk.Button(master, text="Start Bot", command=self.start_bot)
        self.start_button.grid(row=4, column=1, sticky="w")

        self.close_button = tk.Button(master, text="Stop bot (tab will close)", command=self.close_bot)
        self.close_button.grid(row=5, column=1, sticky="w")

        # Load existing courses
        for course_code, section in courses:
            self.course_listbox.insert(tk.END, f"{course_code} - {section}")

    def add_course(self):
        course_code = simpledialog.askstring("Course Code", "Enter course code (e.g., CMPE323):")
        section = simpledialog.askstring("Section", "Enter section (e.g., 01 , 02):")
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

        new_course_code = simpledialog.askstring("Edit Course", "Enter course code (e.g., CMPE323):", initialvalue=course_code)
        new_section = simpledialog.askstring("Edit Section", "Enter section (e.g., 01 , 02):", initialvalue=section)

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
        selected_week = self.week_var.get()

        if not username or not password:
            messagebox.showerror("Error", "Username and password are required!")
            return
        while True:
            driver = run_interface(username,password,selected_week)  
            if driver is False:
                messagebox.showinfo("Login failed", "Username or password is incorrect!")
                break
            else:
                messagebox.showinfo("Info", "Bot has finished its operation. After checking the terminal, don’t forget to send it to your academic advisor.")
                self.driver = driver
                break
        
    def close_bot(self):
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
            except Exception as e:
                messagebox.showerror("Error", f"Error closing bot: {e}")
        else:
            messagebox.showwarning("Warning", "Bot isn't running.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BotInterface(root)
    root.mainloop()
