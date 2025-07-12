import json
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['@','!', '#', '$', '%', '&', '(', ')', '*', '+']
    total_length = randint(8,12)
    num_symbols = randint(1,min(4,total_length -2))
    num_numbers = randint(1,min(4,total_length -num_symbols-1))

    num_letters = total_length - num_symbols - num_numbers
    password_letters = [choice(letters) for _ in range(num_letters)]
    password_symbols = [choice(symbols) for _ in range(num_symbols)]
    password_numbers = [choice(numbers) for _ in range(num_numbers)]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)
    password = "".join(password_list)

    if len(password) < 8 or len(password) > 12:
        messagebox.showwarning(title="Invalid Length", message="Password must be 8-12 characters.")
        return
    if not any(char in symbols for char in password):
        messagebox.showwarning(title="Missing Symbol",
                               message="Password must include at least one symbol (!, @, $, etc.)")
        return
    if not any(char in numbers for char in password):
        messagebox.showwarning(title="Missing Number", message="Password must include at least one number (0–9)")
        return

    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)
    messagebox.showinfo(title="Password Copied", message="Your password has been copied to clipboard.")

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['@','!', '#', '$', '%', '&', '(', ')', '*', '+']
    new_data = {
        website:{
            "email": email,
            "password":password,
        }
    }
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Error", message="Please fill all the fields")
        return
    if len(password) < 8 or len(password) > 12:
        messagebox.showwarning(title="Invalid Password", message="Password must be 8–12 characters long.")
        return
    if not any(char in symbols for char in password):
        messagebox.showwarning(title="Invalid Password",
                               message="Password must contain at least one symbol (!, #, $, etc.)")
        return
    if not any(char in numbers for char in password):
        messagebox.showwarning(title="Invalid Password", message="Password must contain at least one number (0–9)")
        return

    else:
        try:
            with open("database.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("database.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)

        else:
            data.update(new_data)
            with open("database.json", "w") as data_file:
                json.dump(data, data_file, indent=4)

        finally:
                website_entry.delete(0, END)
                email_entry.delete(0, END)
                password_entry.delete(0, END)

# ---------------------------- FIND PASSWORD ------------------------------- #

def find_password():
    website = website_entry.get()
    try:
        with open("database.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}.")
        else:
            messagebox.showinfo(title = "Error", message=f"No details for {website} found.")

            
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('Password Creator')
window.config(padx=50, pady=50, bg="YELLOW")

canvas  = Canvas(width=200, height=200, bg="YELLOW", highlightthickness=0)
logo_img = PhotoImage(file='logo.png')
canvas.create_image(100,100, image=logo_img)
canvas.grid(row=0, column=1)

website_label = Label(text="Website", font=("Arial", 10), bg="YELLOW")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username", font=("Arial", 10), bg="YELLOW")
email_label.grid(row=2, column=0)
password_label = Label(text="Password",font=("Arial", 10), bg="YELLOW")
password_label.grid(row=3, column=0)

website_entry = Entry(width=38)
website_entry.grid(row=1,column=1,columnspan=2)
website_entry.focus()
email_entry = Entry(width=38)
email_entry.grid(row=2,column=1, columnspan=2)
password_entry = Entry(width=22)
password_entry.grid(row=3,column=1,columnspan=1)

search_button = Button(text="Search",font=("Arial",7,"bold"),width=10,command = find_password)
search_button.grid(row=1,column=3)

generate_password_button = Button(text="Generate Password", command=generate_password, font=("Arial",7,"bold"))
generate_password_button.grid(row=3,column=2)

add_button = Button(text="Add", width=32, command=save_password, font=("Arial",9,"bold"))
add_button.grid(row=4,column=1,columnspan=2)

password_requirements = Label(
    text="• Password must be 8–12 characters long.\n"
         "• Must contain at least one symbol (!, @, #...)\n"
         "• Must contain at least one number (0–9)\n"
         "• Generated password is auto copied to clipboard.",
    font=("Arial", 10),
    fg="black",
    bg="YELLOW",
    justify="left"
)
password_requirements.grid(row=5, column=0, columnspan=3, sticky="w")

window.mainloop()