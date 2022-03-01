import os
from tkinter import *
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from tkinter.messagebox import *
from tkinter.filedialog import *

window = tk.Tk()
window.title("Easy Notes")
ids = []
selected_index = 0
file = None


def onselect(evt):
    global selected_index
    # Note here that Tkinter passes an event object to onselect()
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    selected_index = index
    display_note(index, value)


thisMenuBar = Menu(window)
thisFileMenu = Menu(thisMenuBar, tearoff=0)
label = tk.Label(window, text="Created by Swarnava Dutta").pack()
top_frame = tk.Frame(window)
scroll_list = tk.Scrollbar(top_frame)
scroll_list.pack(side=tk.RIGHT, fill=tk.Y)

list_notes = tk.Listbox(top_frame, height=15, width=40)
list_notes.bind('<<ListboxSelect>>', onselect)
list_notes.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0), pady=(10, 10))

scroll_list.config(command=list_notes.yview)
list_notes.config(yscrollcommand=scroll_list.set, cursor="hand2", background="#fff5e6", highlightbackground="grey",
                  bd=0, selectbackground="#c9b922")
top_frame.pack(side=tk.TOP, padx=(0, 5))

text_frame = tk.Frame(window)
note_title = tk.Entry(text_frame, width=39, font="Helvetica 13")
note_title.insert(tk.END, "Title")
note_title.config(background="#F4F6F7", highlightbackground="grey")
note_title.pack(side=tk.TOP, pady=(0, 5), padx=(0, 10))


# def saveFile():
#     file = None
#     if file == None:
#         # Save as new file
#         file = asksaveasfilename(initialfile=note_title.get(),
#                                  defaultextension=".txt",
#                                  filetypes=[("Text Documents", "*.txt")])
#         if file == "":
#             file = None
#         else:
#             # Try to save the file
#             file = open(file, "w")
#             file.write(note_text.get(1.0, END))
#             file.close()
#             # Change the window title
#             window.title(os.path.basename(file) + " - Notepad")


scroll_text = tk.Scrollbar(text_frame)
scroll_text.pack(side=tk.RIGHT, fill=tk.Y)
note_text = tk.Text(text_frame, height=7, width=40, font="Helvetica 13")
note_text.pack(side=tk.TOP, fill=tk.Y, padx=(5, 0), pady=(0, 5))
note_text.tag_config("tag_your_message", foreground="blue")
note_text.insert(tk.END, "Notes")
scroll_text.config(command=note_text.yview)
note_text.config(yscrollcommand=scroll_text.set, background="#F4F6F7", highlightbackground="grey")

text_frame.pack(side=tk.TOP)

button_frame = tk.Frame(window)
photo_add = tk.PhotoImage(file="add.gif")
photo_edit = tk.PhotoImage(file="edit.gif")
photo_delete = tk.PhotoImage(file="delete.gif")

btn_save = tk.Button(button_frame, text="Add", command=lambda: SaveInDatabase(), image=photo_add)
btn_edit = tk.Button(button_frame, text="Update", command=lambda: update_note(), state=tk.DISABLED, image=photo_edit)
btn_delete = tk.Button(button_frame, text="Delete", command=lambda: delete_note(), state=tk.DISABLED,
                       image=photo_delete)

btn_save.grid(row=0, column=1)
btn_edit.grid(row=0, column=2)
btn_delete.grid(row=0, column=3)

button_frame.pack(side=tk.TOP)

# DATABASE FUNCTIONS STARTS
conn = mysql.connector.connect(host="localhost", port=3306, user="root", passwd="")


def db_create_db(conn):
    mycursor = conn.cursor()
    query = "CREATE DATABASE IF NOT EXISTS EasyNotes"
    mycursor.execute(query)


def db_create_table(conn):
    db_create_db(conn)
    conn.database = "EasyNotes"
    mycursor = conn.cursor()
    query = "CREATE TABLE IF NOT EXISTS notes (" \
            "id INT AUTO_INCREMENT PRIMARY KEY, " \
            "title VARCHAR(255) NOT NULL, " \
            "note VARCHAR(10000) NOT NULL)"
    mycursor.execute(query)


def db_insert_note(conn, title, note):
    conn.database = "EasyNotes"
    mycursor = conn.cursor()
    query = "INSERT INTO notes (title, note) VALUES (%s, %s)"
    val = (title, note)
    mycursor.execute(query, val)
    conn.commit()
    return mycursor.lastrowid


def db_select_all_notes(conn):
    conn.database = "EasyNotes"
    query = "SELECT * from notes"
    mycursor = conn.cursor()
    mycursor.execute(query)
    return mycursor.fetchall()


def db_select_specific_note(conn, id):
    conn.database = "EasyNotes"
    mycursor = conn.cursor()
    mycursor.execute("SELECT title, note FROM notes WHERE id = " + str(id))
    return mycursor.fetchone()


def db_update_note(conn, title, note, id):
    conn.database = "EasyNotes"
    mycursor = conn.cursor()
    query = "UPDATE notes SET title = %s, note = %s WHERE id = %s"
    val = (title, note, id)
    mycursor.execute(query, val)

    conn.commit()


def db_delete_note(conn, id):
    conn.database = "EasyNotes"
    mycursor = conn.cursor()
    query = "DELETE FROM notes WHERE id = %s"
    adr = (id,)
    mycursor.execute(query, adr)
    conn.commit()


def init(conn):
    db_create_db(conn)  # create database if not exist
    db_create_table(conn)  # create table if not exist

    # select data
    notes = db_select_all_notes(conn)

    for note in notes:
        list_notes.insert(tk.END, note[1])
        ids.append(note[0])  # save the id


init(conn)


def SaveInDatabase():
    global conn
    title = note_title.get()

    if len(title) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="You MUST enter the note title")
        return

    note = note_text.get("1.0", tk.END)
    if len(note.rstrip()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="You MUST enter the notes")
        return

    # Check if title exist
    title_exist = False
    existing_titles = list_notes.get(0, tk.END)

    for t in existing_titles:
        if t == title:
            title_exist = True
            break

    if title_exist is True:
        tk.messagebox.showerror(title="ERROR!!!", message="Note title already exist. Please choose a new title")
        return

    # MsgBox = tk.messagebox.askquestion('Save Note', 'Do you want to save your note in local storage also?',
    #                                    icon='warning')
    # if MsgBox == 'yes':
    #     save_note()
    #     saveFile()
    # else:
    save_note()
    tk.messagebox.showinfo('Saved', 'Your note is saved in the database')


# BUTTON CLICK FUNCTION STARTS
def save_note():
    title = note_title.get()
    print(type(note_title.get()))
    print(title)
    note = note_text.get("1.0", tk.END)

    # save in database
    inserted_id = db_insert_note(conn, title, note)

    # print("Last inserted id is: " + str(inserted_id))

    # insert into the listbox
    list_notes.insert(tk.END, title)

    ids.append(inserted_id)  # save notes id

    # clear UI
    note_title.delete(0, tk.END)
    note_text.delete('1.0', tk.END)


def update_note():
    global selected_index, conn

    title = note_title.get()

    if len(title) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="You MUST enter the note title")
        return

    note = note_text.get("1.0", tk.END)
    if len(note.rstrip()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="You MUST enter the notes")
        return

    id = ids[selected_index]  # get the id of the selected note

    result = tk.messagebox.askquestion("Update", "Are you sure you want to update?", icon='warning')
    if result == 'yes':
        # save in database
        db_update_note(conn, title, note, id)
        tk.messagebox.showerror(title="Update", message="Your Note is Updated")
        # update list_note
        list_notes.delete(selected_index)
        list_notes.insert(selected_index, title)

        # clear UI
        note_title.delete(0, tk.END)
        note_text.delete('1.0', tk.END)


def delete_note():
    global selected_index, conn, ids
    title = note_title.get()
    notes = note_text.get("1.0", tk.END)

    print("Selected note is: " + str(selected_index))

    if len(title) < 1 or len(notes.rstrip()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="Please select a note to delete")
        return

    result = tk.messagebox.askquestion("Delete", "Are you sure you want to delete?", icon='warning')

    if result == 'yes':
        
        # remove notes from db
        id = ids[selected_index]
        db_delete_note(conn, id)
        del ids[selected_index]

        # remove from UI
        note_title.delete(0, tk.END)
        note_text.delete('1.0', tk.END)
        list_notes.delete(selected_index)
        tk.messagebox.showerror(title="Delete", message="Your Note is Deleted")


def display_note(index, value):
    global ids, conn
    # clear the fields
    note_title.delete(0, tk.END)
    note_text.delete('1.0', tk.END)

    note = db_select_specific_note(conn, ids[index])

    # insert data
    note_title.insert(tk.END, note[0])
    note_text.insert(tk.END, note[1])

    btn_delete.config(state=tk.NORMAL)
    btn_edit.config(state=tk.NORMAL)


window.mainloop()
