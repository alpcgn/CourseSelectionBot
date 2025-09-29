import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
from main import run_interface, courses, stop_bot
import threading

class BotInterface:
    def __init__(self, master):
        self.master = master
        master.title("ATACS Bot by @alpcgn")
        self.driver = None 
        self.bot_thread = None

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
        button_frame.grid(row=4, column=1, sticky="w")

        self.add_button = tk.Button(button_frame, text="Add", command=self.add_course)
        self.add_button.pack(side="left", padx=2)

        self.edit_button = tk.Button(button_frame, text="Edit", command=self.edit_course)
        self.edit_button.pack(side="left", padx=2)

        self.delete_button = tk.Button(button_frame, text="Delete", command=self.delete_course)
        self.delete_button.pack(side="left", padx=2)

        # Week selection
        tk.Label(master, text="Week:").grid(row=3, column=0, sticky="e", padx=5, pady=5)

        self.week_var = tk.StringVar()
        self.week_var.set("firstweek")

        self.radio_frame = tk.Frame(master)
        self.radio_frame.grid(row=3, column=1, sticky="w")

        tk.Radiobutton(self.radio_frame, text="First Week", variable=self.week_var, value="firstweek").pack(side="left")
        tk.Radiobutton(self.radio_frame, text="Add/Drop", variable=self.week_var, value="adddrop").pack(side="left")

        # Start and Stop bot buttons
        button_frame = tk.Frame(master)
        button_frame.grid(row=5, column=1, sticky="w")
        self.start_button = tk.Button(button_frame, text="Start Bot", command=self.start_bot)
        self.start_button.pack(side="left", padx=2)

        self.stop_button = tk.Button(button_frame, text="Stop bot", command=self.stop_bot, state="disabled")
        self.stop_button.pack(side="left", padx=2)

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

    def run_bot_thread(self, username, password, selected_week):
        """Runs the bot in a separate thread"""
        self.update_status("Bot is running...")
        driver = run_interface(username, password, selected_week)
        
        if driver is None:
            self.update_status("Bot was stopped by user")
            self.enable_interface()
        elif driver is False:
            messagebox.showinfo("Login failed", "Username or password is incorrect!")
            self.update_status("Login failed")
            self.enable_interface()
        else:
            self.driver = driver
            messagebox.showinfo("Info", "Bot has finished its operation. Don't close bot yet after checking the basket send it to your academic advisor.")
            self.update_status("Bot completed successfully") 
            self.enable_interface()

    def start_bot(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        selected_week = self.week_var.get()

        if not username or not password:
            messagebox.showerror("Error", "Username and password are required!")
            return

        self.disable_interface()
        
        self.bot_thread = threading.Thread(target=self.run_bot_thread, args=(username,password,selected_week))
        self.bot_thread.daemon = True  
        self.bot_thread.start()
        
    def stop_bot(self):
        """Stop the bot and close the browser"""
        stop_bot()  # Set the global flag to False
        self.update_status("Stopping bot...")
        
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
                self.update_status("Bot stopped")
            except Exception as e:
                messagebox.showerror("Error", f"Error closing bot: {e}")
        else:
            self.update_status("Bot stopped")
        
        self.enable_interface()

    def disable_interface(self):
        """Disable interface elements while bot is running"""
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.username_entry.config(state="disabled")
        self.password_entry.config(state="disabled")
        self.add_button.config(state="disabled")
        self.edit_button.config(state="disabled")
        self.delete_button.config(state="disabled")
        for radio in self.radio_frame.winfo_children():
            radio.config(state="disabled")

    def enable_interface(self):
        """Enable interface elements after bot stops"""
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.username_entry.config(state="normal")
        self.password_entry.config(state="normal")
        self.add_button.config(state="normal")
        self.edit_button.config(state="normal")
        self.delete_button.config(state="normal")
        for radio in self.radio_frame.winfo_children():
            radio.config(state="normal")

    def update_status(self, message):
        """Update status label safely from any thread"""
        self.master.after(0, lambda: self.status_label.config(text=f"Status: {message}"))

if __name__ == "__main__":
    root = tk.Tk()
    app = BotInterface(root)
    root.mainloop()