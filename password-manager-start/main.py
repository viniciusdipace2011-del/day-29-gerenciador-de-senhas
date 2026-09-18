from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
#-----------------------------FIND PASSWORD---------------------------------------#
def find_password():
    try:
        with open("password.json","r") as data_file:
            search = website_entry.get()
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found")
    except json.decoder.JSONDecodeError:
        messagebox.showerror(title="Error", message="No Data File Found")
    else:
        if search in data:
            messagebox.showinfo(title="Password Found",message=f"Website Name: {search}"
                                                                f"\nEmail:  {data[search]['email']}"
                                                                f"\nPassword: {data[search]['password']}")
        else:
            messagebox.showinfo(title="No Details",message="No details for the website exists")
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    Letters = Letter_spinbox.get()
    Numbers = Num_spinbox.get()
    Symbols = Symbol_spinbox.get()
    nr_letters = int(Letters)
    nr_symbols = int(Symbols)
    nr_numbers = int(Numbers)

    password_list = [random.choice(letters) for char in range(nr_letters)]

    password_list += [random.choice(symbols) for char in range(nr_symbols)]

    password_list += [random.choice(numbers) for char in range(nr_numbers)]

    random.shuffle(password_list)

    password = "".join(password_list)

    encrypt = ["*" for char in password]

    password_entry.delete(0, END)
    password_entry.insert(0, encrypt)
    pyperclip.copy(password)
    return password
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_entry.get()
    username = username_entry.get()
    password = generate_password()
    encrypted = password_entry.get()
    new_data = {
        website:{
            "email":username,
            "password":password,
        }
    }
    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showerror(title="Error",message="Please fill all fields")
    else:
        is_ok = messagebox.askokcancel(title="Website",message=f"these are the details entered:\n Website: {website},"
                                                       f"\n Username: {username},\n Password: {encrypted}, "
                                                       f"Are you sure you want to continue?")
        if is_ok:
            try:
                with open("password.json","r") as data_file:
                    #Read old data
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("password.json","w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                #updates old data with new data
                data.update(new_data)

                with open("password.json","w") as data_file:
                    #Saving updated data
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50,pady=50)

canvas = Canvas(window, width=200, height=200)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, imag= logo_image)
canvas.grid(row=0,column=1)
#Labels
website_label = Label(text="Website:")
website_label.grid(row=1,column=0)
username_label = Label(text="Email/Username:")
username_label.grid(row=2,column=0)
password_label = Label(text="Password:")
password_label.grid(row=3,column=0)
Symbols_label = Label(text="#Symbols")
Symbols_label.grid(row=2,column=4)
Numbers_label = Label(text="#Numbers")
Numbers_label.grid(row=3,column=4)
Letters_label = Label(text="#Letters")
Letters_label.grid(row=4,column=4)
Warn_label = Label(text="#The real password will be added in the password.json file in your computer#")
Warn_label.grid(row=5,column=1,columnspan=2)
#Entry
website_entry = Entry(width=35)
website_entry.grid(row=1,column=1, columnspan=1)
website_entry.focus()
username_entry = Entry(width=35)
username_entry.grid(row=2,column=1, columnspan=1)
username_entry.insert(0,"viniciusdipace2011@gmail.com")
password_entry = Entry(width=35)
password_entry.grid(row=3,column=1)
#Button
add_button = Button(width=50,text = "Add",command=save_password)
add_button.grid(row=4,column=1, columnspan=2)
generate_button = Button(text="Generate Password", command=generate_password, width=15)
generate_button.grid(row=3,column=2)
search_button = Button(text="       Search      ", command=find_password, width=15)
search_button.grid(row=1,column=2)
#Spin box
Num_spinbox = Spinbox(from_=0, to=12, width=5)
Num_spinbox.grid(row=3,column=3)
Letter_spinbox = Spinbox(from_=0, to=12, width=5)
Letter_spinbox.grid(row=4,column=3)
Symbol_spinbox = Spinbox(from_=0, to=12, width=5)
Symbol_spinbox.grid(row=2,column=3)

window.mainloop()