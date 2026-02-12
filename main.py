from tkinter import *
from tkinter import messagebox
import random
import string
import json

# ----------------- Modern Color Palette -----------------
BG_COLOR = "#F0F4F8"
LABEL_COLOR = "#1F3A93"
BUTTON_COLOR = "#27AE60"
BUTTON_TEXT = "#FFFFFF"
ENTRY_BG = "#FFFFFF"

LABEL_FONT = ("Helvetica", 12, "bold")
ENTRY_FONT = ("Helvetica", 12)
BUTTON_FONT = ("Helvetica", 12, "bold")
GEN_BUTTON_FONT = ("Helvetica", 10, "bold")

# -------------- Password Search -----------------------
def find_password():
    website = website_entry.get()
    try:
        with open("D:/Python/password_manager_tkinter/data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")

# -------------- Password Generator -----------------------
def generate_password():
    letters = string.ascii_letters
    numbers = string.digits
    symbols = "!@#$%^&*()_+-="

    password_list = (
        random.choices(letters, k=8) +
        random.choices(numbers, k=4) +
        random.choices(symbols, k=3)
    )

    random.shuffle(password_list)
    password = "".join(password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, password)
    
    # Copy to clipboard automatically
    window.clipboard_clear()
    window.clipboard_append(password)

# -------------- Save Password ----------------------------
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title="Oops", message="Please don't leave fields empty!")
    else:
        try:
            with open("D:/Python/password_manager_tkinter/data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            # Create file if not found or if file is empty
            with open("D:/Python/password_manager_tkinter/data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)
            with open("D:/Python/password_manager_tkinter/data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            messagebox.showinfo(title="Success", message="Details saved successfully.")

# ----------------- UI Setup -----------------
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg=BG_COLOR)

# Logo (Ensure 'logo.png' is in the same folder or update path)
canvas = Canvas(height=200, width=200, bg=BG_COLOR, highlightthickness=0)
try:
    logo_img = PhotoImage(file="D:\Python\password_manager_tkinter\password.png") 
    canvas.create_image(100, 100, image=logo_img)
except:
    canvas.create_text(100, 100, text="🔒", font=("Arial", 80))
canvas.grid(row=0, column=1, pady=10)

# Labels
website_label = Label(text="Website:", bg=BG_COLOR, fg=LABEL_COLOR, font=LABEL_FONT)
website_label.grid(row=1, column=0, sticky="E", padx=10, pady=5)

email_label = Label(text="Email/User:", bg=BG_COLOR, fg=LABEL_COLOR, font=LABEL_FONT)
email_label.grid(row=2, column=0, sticky="E", padx=10, pady=5)

password_label = Label(text="Password:", bg=BG_COLOR, fg=LABEL_COLOR, font=LABEL_FONT)
password_label.grid(row=3, column=0, sticky="E", padx=10, pady=5)

# Entries
website_entry = Entry(width=34, font=ENTRY_FONT, bg=ENTRY_BG)
website_entry.grid(row=1, column=1, padx=10, pady=5)
website_entry.focus()

email_entry = Entry(width=50, font=ENTRY_FONT, bg=ENTRY_BG)
email_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=5)
email_entry.insert(0, "dummy@email.com")

password_entry = Entry(width=34, font=ENTRY_FONT, bg=ENTRY_BG)
password_entry.grid(row=3, column=1, padx=10, pady=5)

# Buttons
search_button = Button(
    text="Search",
    width=14,
    command=find_password, # Fixed reference
    bg=BUTTON_COLOR,
    fg=BUTTON_TEXT,
    font=GEN_BUTTON_FONT
)
search_button.grid(row=1, column=2, padx=10, pady=5)

generate_password_button = Button(
    text="Generate",
    width=14,
    command=generate_password,
    bg=BUTTON_COLOR,
    fg=BUTTON_TEXT,
    font=GEN_BUTTON_FONT
)
generate_password_button.grid(row=3, column=2, padx=10, pady=5)

add_button = Button(
    text="Add to Manager",
    width=45,
    command=save,
    bg=BUTTON_COLOR,
    fg=BUTTON_TEXT,
    font=BUTTON_FONT
)
add_button.grid(row=4, column=1, columnspan=2, pady=20)

window.mainloop()