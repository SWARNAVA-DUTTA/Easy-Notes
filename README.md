# Easy Notes


![image](https://user-images.githubusercontent.com/46235752/156226771-a9207255-9636-43ae-8ebe-7b7c1cb2c716.png)
<br/><br/><br/>
This is how the data gets saved into database

![image](https://user-images.githubusercontent.com/46235752/156226806-57d9d18b-c3da-4d6e-9190-e73f2f4da0bc.png)
<br/><br/><br/><br/>
How to implement this:
1. Install XAMPP from <a href="https://www.apachefriends.org/index.html" target="_blank">https://www.apachefriends.org/index.html</a>
2. Compile and run the code. Make sure your MySQL Admin is running on Port: `3306`

![image](https://user-images.githubusercontent.com/46235752/156230520-143cbd98-81ba-4761-9eb2-d662fc409138.png)

<br/><br/>

-------------------------------------------------------------------------------------------------------------------------------------------------------------
Initialising the buttons 
```python
button_frame = tk.Frame(window)
photo_add = tk.PhotoImage(file="add.gif")
photo_edit = tk.PhotoImage(file="edit.gif")
photo_delete = tk.PhotoImage(file="delete.gif")
```
<br/>

This is used to connect to database
```python
conn = mysql.connector.connect(host="localhost", port=3306, user="root", passwd="")
```
<br/>

Creating the database
```python
def db_create_db(conn):
    mycursor = conn.cursor()
    query = "CREATE DATABASE IF NOT EXISTS EasyNotes"
    mycursor.execute(query)
```
<br/>

Creating a new table
```python
def db_create_table(conn):
    db_create_db(conn)
    conn.database = "EasyNotes"
    mycursor = conn.cursor()
    query = "CREATE TABLE IF NOT EXISTS notes (" \
            "id INT AUTO_INCREMENT PRIMARY KEY, " \
            "title VARCHAR(255) NOT NULL, " \
            "note VARCHAR(10000) NOT NULL)"
    mycursor.execute(query)
```
<br/>

Inserting a note in database
```python
def db_insert_note(conn, title, note):
    conn.database = "EasyNotes"
    mycursor = conn.cursor()
    query = "INSERT INTO notes (title, note) VALUES (%s, %s)"
    val = (title, note)
    mycursor.execute(query, val)
    conn.commit()
    return mycursor.lastrowid
```
<br/>

Showing all the notes from database
```python
def db_select_all_notes(conn):
    conn.database = "EasyNotes"
    query = "SELECT * from notes"
    mycursor = conn.cursor()
    mycursor.execute(query)
    return mycursor.fetchall()
```
<br/>

Selecting a specific note 
```python
def db_select_specific_note(conn, id):
    conn.database = "EasyNotes"
    mycursor = conn.cursor()
    mycursor.execute("SELECT title, note FROM notes WHERE id = " + str(id))
    return mycursor.fetchone()
```
<br/>

Updating a note
```python
def db_update_note(conn, title, note, id):
    conn.database = "EasyNotes"
    mycursor = conn.cursor()
    query = "UPDATE notes SET title = %s, note = %s WHERE id = %s"
    val = (title, note, id)
    mycursor.execute(query, val)
    conn.commit()
```
<br/>

Deleting a note
```python
def db_delete_note(conn, id):
    conn.database = "EasyNotes"
    mycursor = conn.cursor()
    query = "DELETE FROM notes WHERE id = %s"
    adr = (id,)
    mycursor.execute(query, adr)
    conn.commit()
```

