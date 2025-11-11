import tkinter as tk
from tkinter import messagebox, simpledialog
import os

# --- Set your diary password ---
PASSWORD = "kanchan123"

# --- Main Diary App Window ---
def open_diary():
    login_window.destroy()

    window = tk.Tk()
    window.title("Kanchan's Personal Diary")
    window.geometry("500x500")
    window.config(bg="#fcefee")

    # Create folder for diary entries
    if not os.path.exists("MyDiary"):
        os.makedirs("MyDiary")

    # --- Save New Entry ---
    def save_entry():
        content = text_area.get("1.0", tk.END).strip()
        if content == "":
            messagebox.showwarning("Empty Entry", "Write something before saving! ")
            return

        filename = simpledialog.askstring("File Name", "Enter a name for your diary entry:")
        if not filename:
            messagebox.showinfo("Cancelled", "Save cancelled.")
            return

        filename = filename.strip() + ".txt"
        filepath = os.path.join("MyDiary", filename)

        if os.path.exists(filepath):
            overwrite = messagebox.askyesno("File Exists", "File already exists! Overwrite it?")
            if not overwrite:
                return

        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

        messagebox.showinfo("Saved ", f"Your entry has been saved as {filename}")
        text_area.delete("1.0", tk.END)

    # --- View, Edit, Delete Entries ---
    def view_entries():
        files = os.listdir("MyDiary")
        if not files:
            messagebox.showinfo("No Entries", "No diary entries found yet! ")
            return

        entries_window = tk.Toplevel(window)
        entries_window.title(" Your Saved Entries")
        entries_window.geometry("400x450")
        entries_window.config(bg="#fcefee")

        listbox = tk.Listbox(entries_window, font=("Helvetica", 12), bg="#fff0f5", fg="#5d1451")
        listbox.pack(padx=20, pady=20, fill="both", expand=True)

        for f in files:
            listbox.insert(tk.END, f)

        # --- Edit Entry Function ---
        def edit_entry():
            selected = listbox.curselection()
            if not selected:
                messagebox.showwarning("No Selection", "Please select an entry to edit.")
                return
            filename = listbox.get(selected[0])
            filepath = os.path.join("MyDiary", filename)

            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()

            edit_window = tk.Toplevel(entries_window)
            edit_window.title(f" Edit - {filename}")
            edit_window.geometry("500x500")
            edit_window.config(bg="#fcefee")

            edit_text = tk.Text(edit_window, wrap="word", font=("Helvetica", 12),
                                bg="#fffaf0", fg="#2b2b2b")
            edit_text.insert("1.0", content)
            edit_text.pack(fill="both", expand=True, padx=10, pady=10)

            def save_edited_entry():
                new_content = edit_text.get("1.0", tk.END).strip()
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                messagebox.showinfo("Updated ✅", f"'{filename}' has been updated successfully!")
                edit_window.destroy()

            save_edit_button = tk.Button(edit_window, text="Save Changes",
                                         command=save_edited_entry,
                                         bg="#ffc8dd", fg="black",
                                         font=("Helvetica", 12, "bold"))
            save_edit_button.pack(pady=10)

        # --- Delete Entry Function ---
        def delete_entry():
            selected = listbox.curselection()
            if not selected:
                messagebox.showwarning("No Selection", "Please select an entry to delete.")
                return

            filename = listbox.get(selected[0])
            filepath = os.path.join("MyDiary", filename)

            confirm = messagebox.askyesno("Delete Entry ",
                                          f"Are you sure you want to delete '{filename}'?")
            if confirm:
                os.remove(filepath)
                listbox.delete(selected[0])
                messagebox.showinfo("Deleted ", f"'{filename}' has been deleted successfully!")

        # --- Buttons for Edit and Delete ---
        btn_frame = tk.Frame(entries_window, bg="#fcefee")
        btn_frame.pack(pady=10)

        edit_button = tk.Button(btn_frame, text=" Edit Selected Entry",
                                command=edit_entry, bg="#bde0fe",
                                fg="black", font=("Helvetica", 12, "bold"))
        edit_button.grid(row=0, column=0, padx=10)

        delete_button = tk.Button(btn_frame, text="🗑️ Delete Selected Entry",
                                  command=delete_entry, bg="#ffafcc",
                                  fg="black", font=("Helvetica", 12, "bold"))
        delete_button.grid(row=0, column=1, padx=10)

    # --- Main UI Layout ---
    title_label = tk.Label(window, text=" Kanchan’s Personal Diary ",
                           font=("Helvetica", 16, "bold"), bg="#fcefee", fg="#b5179e")
    title_label.pack(pady=20)

    text_area = tk.Text(window, wrap="word", font=("Helvetica", 13),
                        bg="#fffaf0", fg="#3c096c", height=15)
    text_area.pack(padx=20, pady=10, fill="both", expand=True)

    button_frame = tk.Frame(window, bg="#fcefee")
    button_frame.pack(pady=10)

    save_button = tk.Button(button_frame, text="Save Entry ",
                            command=save_entry, bg="#ffc8dd", fg="black",
                            font=("Helvetica", 12, "bold"), width=15)
    save_button.grid(row=0, column=0, padx=10)

    view_button = tk.Button(button_frame, text="View/Edit/Delete ",
                            command=view_entries, bg="#bde0fe", fg="black",
                            font=("Helvetica", 12, "bold"), width=15)
    view_button.grid(row=0, column=1, padx=10)

    footer_label = tk.Label(window, text="Made with  by Kanchan",
                            bg="#fcefee", fg="#7209b7", font=("Helvetica", 10))
    footer_label.pack(side="bottom", pady=10)

    window.mainloop()

# --- Password Protection ---
def check_password():
    entered = password_entry.get()
    if entered == PASSWORD:
        open_diary()
    else:
        messagebox.showerror("Access Denied", "Wrong password! Try again ")
        password_entry.delete(0, tk.END)

# --- Login Window ---
login_window = tk.Tk()
login_window.title(" Diary Login")
login_window.geometry("400x250")
login_window.config(bg="#fcefee")

login_label = tk.Label(login_window, text=" Welcome to Kanchan’s Diary ",
                       font=("Helvetica", 16, "bold"), bg="#fcefee", fg="#b5179e")
login_label.pack(pady=20)

password_label = tk.Label(login_window, text="Enter Password:",
                          font=("Helvetica", 12), bg="#fcefee", fg="#3c096c")
password_label.pack(pady=10)

password_entry = tk.Entry(login_window, show="*", width=25,
                          font=("Helvetica", 12), justify="center")
password_entry.pack(pady=5)

login_button = tk.Button(login_window, text="Unlock ", command=check_password,
                         bg="#ffb6c1", fg="black", font=("Helvetica", 12, "bold"))
login_button.pack(pady=15)

footer = tk.Label(login_window, text="Made with  by Kanchan",
                  bg="#fcefee", fg="#7209b7", font=("Helvetica", 9))
footer.pack(side="bottom", pady=10)

login_window.mainloop()
