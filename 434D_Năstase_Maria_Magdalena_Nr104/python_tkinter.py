import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

# Funcție pentru conectarea la baza de date
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='2002',
            database='bazadedate'
        )
        return connection
    except Error as e:
        messagebox.showerror("Eroare", f"Nu s-a putut conecta la baza de date: {e}")
        return None
    
        
# Funcție pentru afișarea datelor din Sculptors
def show_sculptors():
    connection = connect_to_database()
    if not connection:
        return

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Sculptors")
        records = cursor.fetchall()

        for row in tree_sculptors.get_children():
            tree_sculptors.delete(row)

        for row in records:
            tree_sculptors.insert("", tk.END, values=row)
    except Error as e:
        messagebox.showerror("Eroare", f"Eroare la interogare: {e}")
    finally:
        connection.close()

# Funcție pentru adăugarea unui sculptor
def add_sculptor():
    def submit():
        connection = connect_to_database()
        if not connection:
            return
        try:
            cursor = connection.cursor()
            sql = "INSERT INTO Sculptors (Nume, Prenume, AnNastere, AnDeces, Nationalitate, StilArtistic) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (
                entry_name.get(), entry_surname.get(), entry_birth.get(),
                entry_death.get() or None, entry_nationality.get(), entry_style.get()
            ))
            connection.commit()
            messagebox.showinfo("Succes", "Sculptor adăugat cu succes!")
            add_window.destroy()
            show_sculptors()
        except Error as e:
            messagebox.showerror("Eroare", f"Eroare la adăugare: {e}")
        finally:
            connection.close()

    add_window = tk.Toplevel(root) #fereastra secundara
    add_window.title("Adaugă Sculptor")

    tk.Label(add_window, text="Nume:").grid(row=0, column=0, padx=10, pady=5)
    entry_name = tk.Entry(add_window)
    entry_name.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(add_window, text="Prenume:").grid(row=1, column=0, padx=10, pady=5)
    entry_surname = tk.Entry(add_window)
    entry_surname.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(add_window, text="An Naștere:").grid(row=2, column=0, padx=10, pady=5)
    entry_birth = tk.Entry(add_window)
    entry_birth.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(add_window, text="An Deces:").grid(row=3, column=0, padx=10, pady=5)
    entry_death = tk.Entry(add_window)
    entry_death.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(add_window, text="Naționalitate:").grid(row=4, column=0, padx=10, pady=5)
    entry_nationality = tk.Entry(add_window)
    entry_nationality.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(add_window, text="Stil Artistic:").grid(row=5, column=0, padx=10, pady=5)
    entry_style = tk.Entry(add_window)
    entry_style.grid(row=5, column=1, padx=10, pady=5)

    tk.Button(add_window, text="Adaugă", command=submit).grid(row=6, columnspan=2, pady=10)

# Funcție pentru ștergerea unui sculptor
def delete_sculptor():
    selected_item = tree_sculptors.selection()
    if not selected_item:
        messagebox.showwarning("Atenție", "Selectează un sculptor pentru ștergere!")
        return

    sculptor_id = tree_sculptors.item(selected_item, "values")[0]

    connection = connect_to_database()
    if not connection:
        return

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Sculptors WHERE SculptorID = %s", (sculptor_id,))
        connection.commit()
        messagebox.showinfo("Succes", "Sculptor șters cu succes!")
        show_sculptors()
    except Error as e:
        messagebox.showerror("Eroare", f"Eroare la ștergere: {e}")
    finally:
        connection.close()
        
   # Funcție pentru editarea unui sculptor     
def edit_sculptor():
    selected_item = tree_sculptors.selection()
    if not selected_item:
        messagebox.showwarning("Atenție", "Selectează un sculptor pentru modificare!")
        return

    sculptor_id = tree_sculptors.item(selected_item, "values")[0]

    def submit():
        connection = connect_to_database()
        if not connection:
            return
        try:
            cursor = connection.cursor()
            sql = """
                UPDATE Sculptors
                SET Nume = %s, Prenume = %s, AnNastere = %s, AnDeces = %s, Nationalitate = %s, StilArtistic = %s
                WHERE SculptorID = %s
            """
            cursor.execute(sql, (
                entry_name.get(), entry_surname.get(), entry_birth.get(),
                entry_death.get() or None, entry_nationality.get(), entry_style.get(), sculptor_id
            ))
            connection.commit()
            messagebox.showinfo("Succes", "Sculptor modificat cu succes!")
            edit_window.destroy()
            show_sculptors()
        except Error as e:
            messagebox.showerror("Eroare", f"Eroare la modificare: {e}")
        finally:
            connection.close()

    edit_window = tk.Toplevel(root)
    edit_window.title("Modifică Sculptor")

    connection = connect_to_database()
    if not connection:
        return

    try:
        cursor = connection.cursor(dictionary=True)
        #preiau datele despre sculptor
        cursor.execute("SELECT * FROM Sculptors WHERE SculptorID = %s", (sculptor_id,))
        sculptor = cursor.fetchone()
    except Error as e:
        messagebox.showerror("Eroare", f"Eroare la încărcarea datelor: {e}")
        return
    finally:
        connection.close()

    tk.Label(edit_window, text="Nume:").grid(row=0, column=0, padx=10, pady=5)
    entry_name = tk.Entry(edit_window)
    entry_name.insert(0, sculptor["Nume"])
    entry_name.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(edit_window, text="Prenume:").grid(row=1, column=0, padx=10, pady=5)
    entry_surname = tk.Entry(edit_window)
    entry_surname.insert(0, sculptor["Prenume"])
    entry_surname.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(edit_window, text="An Naștere:").grid(row=2, column=0, padx=10, pady=5)
    entry_birth = tk.Entry(edit_window)
    entry_birth.insert(0, sculptor["AnNastere"])
    entry_birth.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(edit_window, text="An Deces:").grid(row=3, column=0, padx=10, pady=5)
    entry_death = tk.Entry(edit_window)
    entry_death.insert(0, sculptor["AnDeces"] or "")
    entry_death.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(edit_window, text="Naționalitate:").grid(row=4, column=0, padx=10, pady=5)
    entry_nationality = tk.Entry(edit_window)
    entry_nationality.insert(0, sculptor["Nationalitate"])
    entry_nationality.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(edit_window, text="Stil Artistic:").grid(row=5, column=0, padx=10, pady=5)
    entry_style = tk.Entry(edit_window)
    entry_style.insert(0, sculptor["StilArtistic"])
    entry_style.grid(row=5, column=1, padx=10, pady=5)

    tk.Button(edit_window, text="Salvează", command=submit).grid(row=6, columnspan=2, pady=10)

        
        
# Funcție pentru afișarea datelor din Sculptures
def show_sculptures():
    connection = connect_to_database()
    if not connection:
        return

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Sculptures")
        records = cursor.fetchall()

        for row in tree_sculptures.get_children():
            tree_sculptures.delete(row)

        for row in records:
            tree_sculptures.insert("", tk.END, values=row)
    except Error as e:
        messagebox.showerror("Eroare", f"Eroare la interogare: {e}")
    finally:
        connection.close()
      
        

# Funcții pentru Sculptures
def add_sculpture():
    def submit():
        connection = connect_to_database()
        if not connection:
            return
        try:
            cursor = connection.cursor()
            sql = "INSERT INTO Sculptures (Titlu, Material, Inaltime, Greutate, AnCreatie, LocatieMuzeu) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (
                entry_title.get(), entry_material.get(), entry_height.get(),
                entry_weight.get(), entry_year.get(), entry_location.get()
            ))
            connection.commit()
            messagebox.showinfo("Succes", "Sculptură adăugată cu succes!")
            add_window.destroy()
            show_sculptures()
        except Error as e:
            messagebox.showerror("Eroare", f"Eroare la adăugare: {e}")
        finally:
            connection.close()

    add_window = tk.Toplevel(root)
    add_window.title("Adaugă Sculptură")

    tk.Label(add_window, text="Titlu:").grid(row=0, column=0, padx=10, pady=5)
    entry_title = tk.Entry(add_window)
    entry_title.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(add_window, text="Material:").grid(row=1, column=0, padx=10, pady=5)
    entry_material = tk.Entry(add_window)
    entry_material.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(add_window, text="Înălțime:").grid(row=2, column=0, padx=10, pady=5)
    entry_height = tk.Entry(add_window)
    entry_height.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(add_window, text="Greutate:").grid(row=3, column=0, padx=10, pady=5)
    entry_weight = tk.Entry(add_window)
    entry_weight.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(add_window, text="An Creație:").grid(row=4, column=0, padx=10, pady=5)
    entry_year = tk.Entry(add_window)
    entry_year.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(add_window, text="Locație Muzeu:").grid(row=5, column=0, padx=10, pady=5)
    entry_location = tk.Entry(add_window)
    entry_location.grid(row=5, column=1, padx=10, pady=5)

    tk.Button(add_window, text="Adaugă", command=submit).grid(row=6, columnspan=2, pady=10)

def delete_sculpture():
    selected_item = tree_sculptures.selection()
    if not selected_item:
        messagebox.showwarning("Atenție", "Selectează o sculptură pentru ștergere!")
        return

    sculpture_id = tree_sculptures.item(selected_item, "values")[0]

    connection = connect_to_database()
    if not connection:
        return

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Sculptures WHERE SculptureID = %s", (sculpture_id,))
        connection.commit()
        messagebox.showinfo("Succes", "Sculptură ștearsă cu succes!")
        show_sculptures()
    except Error as e:
        messagebox.showerror("Eroare", f"Eroare la ștergere: {e}")
    finally:
        connection.close()
        
def edit_sculpture():
    selected_item = tree_sculptures.selection()
    if not selected_item:
        messagebox.showwarning("Atenție", "Selectează o sculptură pentru modificare!")
        return

    sculpture_id = tree_sculptures.item(selected_item, "values")[0]

    def submit():
        connection = connect_to_database()
        if not connection:
            return
        try:
            cursor = connection.cursor()
            sql = """
                UPDATE Sculptures
                SET Titlu = %s, Material = %s, Inaltime = %s, Greutate = %s, AnCreatie = %s, LocatieMuzeu = %s
                WHERE SculptureID = %s
            """
            cursor.execute(sql, (
                entry_title.get(), entry_material.get(), entry_height.get(),
                entry_weight.get(), entry_year.get(), entry_location.get(), sculpture_id
            ))
            connection.commit()
            messagebox.showinfo("Succes", "Sculptură modificată cu succes!")
            edit_window.destroy()
            show_sculptures()
        except Error as e:
            messagebox.showerror("Eroare", f"Eroare la modificare: {e}")
        finally:
            connection.close()

    edit_window = tk.Toplevel(root)
    edit_window.title("Modifică Sculptură")

    connection = connect_to_database()
    if not connection:
        return

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Sculptures WHERE SculptureID = %s", (sculpture_id,))
        sculpture = cursor.fetchone()
    except Error as e:
        messagebox.showerror("Eroare", f"Eroare la încărcarea datelor: {e}")
        return
    finally:
        connection.close()

    tk.Label(edit_window, text="Titlu:").grid(row=0, column=0, padx=10, pady=5)
    entry_title = tk.Entry(edit_window)
    entry_title.insert(0, sculpture["Titlu"])
    entry_title.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(edit_window, text="Material:").grid(row=1, column=0, padx=10, pady=5)
    entry_material = tk.Entry(edit_window)
    entry_material.insert(0, sculpture["Material"])
    entry_material.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(edit_window, text="Înălțime:").grid(row=2, column=0, padx=10, pady=5)
    entry_height = tk.Entry(edit_window)
    entry_height.insert(0, sculpture["Inaltime"])
    entry_height.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(edit_window, text="Greutate:").grid(row=3, column=0, padx=10, pady=5)
    entry_weight = tk.Entry(edit_window)
    entry_weight.insert(0, sculpture["Greutate"])
    entry_weight.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(edit_window, text="An Creație:").grid(row=4, column=0, padx=10, pady=5)
    entry_year = tk.Entry(edit_window)
    entry_year.insert(0, sculpture["AnCreatie"])
    entry_year.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(edit_window, text="Locație Muzeu:").grid(row=5, column=0, padx=10, pady=5)
    entry_location = tk.Entry(edit_window)
    entry_location.insert(0, sculpture["LocatieMuzeu"])
    entry_location.grid(row=5, column=1, padx=10, pady=5)

    tk.Button(edit_window, text="Salvează", command=submit).grid(row=6, columnspan=2, pady=10)

        
        
    # Funcție pentru afișarea datelor din Sculpture_Sculptor
def show_associations():
    connection = connect_to_database()
    if not connection:
        return

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT ss.SculptureID, s.Titlu AS TitluSculptura, ss.SculptorID, sc.Nume AS NumeSculptor, sc.Prenume AS PrenumeSculptor FROM Sculpture_Sculptor ss JOIN Sculptures s ON ss.SculptureID = s.SculptureID JOIN Sculptors sc ON ss.SculptorID = sc.SculptorID")
        records = cursor.fetchall()

        for row in tree_associations.get_children():
            tree_associations.delete(row)

        for row in records:
            tree_associations.insert("", tk.END, values=row)
    except Error as e:
        messagebox.showerror("Eroare", f"Eroare la interogare: {e}")
    finally:
        connection.close()



# Funcție pentru adăugarea unei asocieri

def add_association():
    def submit():
        connection = connect_to_database()
        if not connection:
            return
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT SculptureID FROM Sculptures WHERE Titlu = %s", (combo_sculpture.get(),))
            sculpture_id = cursor.fetchone()[0]

            cursor.execute("SELECT SculptorID FROM Sculptors WHERE Nume = %s", (combo_sculptor.get(),))
            sculptor_id = cursor.fetchone()[0]

            sql = "INSERT INTO Sculpture_Sculptor (SculptureID, SculptorID) VALUES (%s, %s)"
            cursor.execute(sql, (sculpture_id, sculptor_id))
            connection.commit()
            messagebox.showinfo("Succes", "Asociere adăugată cu succes!")
            add_window.destroy()
            show_associations()
        except Error as e:
            messagebox.showerror("Eroare", f"Eroare la adăugare: {e}")
        finally:
            connection.close()

    add_window = tk.Toplevel(root)
    add_window.title("Adaugă Asociere")

    connection = connect_to_database()
    if not connection:
        return

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT Titlu FROM Sculptures")
        sculptures = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT Nume FROM Sculptors")
        sculptors = [row[0] for row in cursor.fetchall()]
    except Error as e:
        messagebox.showerror("Eroare", f"Eroare la încărcarea datelor: {e}")
        return
    finally:
        connection.close()

    tk.Label(add_window, text="Sculptură:").grid(row=0, column=0, padx=10, pady=5)
    combo_sculpture = ttk.Combobox(add_window, values=sculptures, state="readonly")
    combo_sculpture.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(add_window, text="Sculptor:").grid(row=1, column=0, padx=10, pady=5)
    combo_sculptor = ttk.Combobox(add_window, values=sculptors, state="readonly")
    combo_sculptor.grid(row=1, column=1, padx=10, pady=5)

    tk.Button(add_window, text="Adaugă", command=submit).grid(row=2, columnspan=2, pady=10)

# Funcție pentru modificarea unei asocieri
def edit_association():
    def submit():
        connection = connect_to_database()
        if not connection:
            return
        try:
            cursor = connection.cursor()

            cursor.execute("SELECT SculptureID FROM Sculptures WHERE Titlu = %s", (combo_sculpture.get(),))
            new_sculpture_id = cursor.fetchone()[0]

            cursor.execute("SELECT SculptorID FROM Sculptors WHERE Nume = %s", (combo_sculptor.get(),))
            new_sculptor_id = cursor.fetchone()[0]

            sql = "UPDATE Sculpture_Sculptor SET SculptureID = %s, SculptorID = %s WHERE SculptureID = %s AND SculptorID = %s"
            cursor.execute(sql, (new_sculpture_id, new_sculptor_id, sculpture_id, sculptor_id))
            connection.commit()
            messagebox.showinfo("Succes", "Asociere modificată cu succes!")
            edit_window.destroy()
            show_associations()
        except Error as e:
            messagebox.showerror("Eroare", f"Eroare la modificare: {e}")
        finally:
            connection.close()

    selected_item = tree_associations.selection()
    if not selected_item:
        messagebox.showwarning("Atenție", "Selectează o asociere pentru modificare!")
        return

    sculpture_id = tree_associations.item(selected_item, "values")[0]
    sculptor_id = tree_associations.item(selected_item, "values")[2]

    edit_window = tk.Toplevel(root)
    edit_window.title("Modifică Asociere")

    connection = connect_to_database()
    if not connection:
        return

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT Titlu FROM Sculptures")
        sculptures = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT Nume FROM Sculptors")
        sculptors = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT Titlu FROM Sculptures WHERE SculptureID = %s", (sculpture_id,))
        current_sculpture = cursor.fetchone()[0]

        cursor.execute("SELECT Nume FROM Sculptors WHERE SculptorID = %s", (sculptor_id,))
        current_sculptor = cursor.fetchone()[0]
    except Error as e:
        messagebox.showerror("Eroare", f"Eroare la încărcarea datelor: {e}")
        return
    finally:
        connection.close()

    tk.Label(edit_window, text="Sculptură:").grid(row=0, column=0, padx=10, pady=5)
    combo_sculpture = ttk.Combobox(edit_window, values=sculptures, state="readonly")
    combo_sculpture.grid(row=0, column=1, padx=10, pady=5)
    combo_sculpture.set(current_sculpture)

    tk.Label(edit_window, text="Sculptor:").grid(row=1, column=0, padx=10, pady=5)
    combo_sculptor = ttk.Combobox(edit_window, values=sculptors, state="readonly")
    combo_sculptor.grid(row=1, column=1, padx=10, pady=5)
    combo_sculptor.set(current_sculptor)

    tk.Button(edit_window, text="Salvează", command=submit).grid(row=2, columnspan=2, pady=10)
    
    # Funcție pentru ștergerea unei asocieri
def delete_association():
    selected_item = tree_associations.selection()
    if not selected_item:
        messagebox.showwarning("Atenție", "Selectează o asociere pentru ștergere!")
        return

    sculpture_id = tree_associations.item(selected_item, "values")[0]
    sculptor_id = tree_associations.item(selected_item, "values")[2] 
    # SculptureID și SculptorID sunt pe pozițiile 0 și 2

    connection = connect_to_database()
    if not connection:
        return

    try:
        cursor = connection.cursor()
        sql = "DELETE FROM Sculpture_Sculptor WHERE SculptureID = %s AND SculptorID = %s"
        cursor.execute(sql, (sculpture_id, sculptor_id))
        connection.commit()
        messagebox.showinfo("Succes", "Asociere ștearsă cu succes!")
        show_associations()
    except Error as e:
        messagebox.showerror("Eroare", f"Eroare la ștergere: {e}")
    finally:
        connection.close()





# Configurarea ferestrei principale
root = tk.Tk()
root.title("Aplicație Sculptori, Sculpturi și Asocieri")
root.geometry("1200x800")

# Tabs pentru gestionare
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# Tab Sculptors
tab_sculptors = tk.Frame(notebook)
notebook.add(tab_sculptors, text="Sculptori")

btn_frame_sculptors = tk.Frame(tab_sculptors)
btn_frame_sculptors.pack(pady=10)

tree_sculptors = ttk.Treeview(tab_sculptors, columns=("ID", "Nume", "Prenume", "An Naștere", "An Deces", "Naționalitate", "Stil Artistic"), show="headings")
for col in tree_sculptors["columns"]:
    tree_sculptors.heading(col, text=col)
    tree_sculptors.column(col, anchor="center")

tree_sculptors.pack(fill=tk.BOTH, expand=True)

btn_show_sculptors = tk.Button(btn_frame_sculptors, text="Afișează Sculptori", command=show_sculptors)
btn_show_sculptors.pack(side=tk.LEFT, padx=5)

btn_add_sculptor = tk.Button(btn_frame_sculptors, text="Adaugă", command=add_sculptor)
btn_add_sculptor.pack(side=tk.LEFT, padx=5)

btn_edit_sculptor = tk.Button(btn_frame_sculptors, text="Modifică", command=edit_sculptor)
btn_edit_sculptor.pack(side=tk.LEFT, padx=5)

btn_delete_sculptor = tk.Button(btn_frame_sculptors, text="Șterge", command=delete_sculptor)
btn_delete_sculptor.pack(side=tk.LEFT, padx=5)

# Tab Sculptures
tab_sculptures = tk.Frame(notebook)
notebook.add(tab_sculptures, text="Sculpturi")

btn_frame_sculptures = tk.Frame(tab_sculptures)
btn_frame_sculptures.pack(pady=10)

tree_sculptures = ttk.Treeview(tab_sculptures, columns=("ID", "Titlu", "Material", "Înălțime", "Greutate", "An Creație", "Locație"), show="headings")
for col in tree_sculptures["columns"]:
    tree_sculptures.heading(col, text=col)
    tree_sculptures.column(col, anchor="center")

tree_sculptures.pack(fill=tk.BOTH, expand=True)

btn_show_sculptures = tk.Button(btn_frame_sculptures, text="Afișează Sculpturi", command=show_sculptures)
btn_show_sculptures.pack(side=tk.LEFT, padx=5)

btn_add_sculpture = tk.Button(btn_frame_sculptures, text="Adaugă", command=add_sculpture)
btn_add_sculpture.pack(side=tk.LEFT, padx=5)

btn_edit_sculpture = tk.Button(btn_frame_sculptures, text="Modifică", command=edit_sculpture)
btn_edit_sculpture.pack(side=tk.LEFT, padx=5)

btn_delete_sculpture = tk.Button(btn_frame_sculptures, text="Șterge", command=delete_sculpture)
btn_delete_sculpture.pack(side=tk.LEFT, padx=5)

# Tab Associations
tab_associations = tk.Frame(notebook)
notebook.add(tab_associations, text="Asocieri")

btn_frame_associations = tk.Frame(tab_associations)
btn_frame_associations.pack(pady=10)

tree_associations = ttk.Treeview(tab_associations, columns=("ID Sculptură", "Titlu Sculptură", "ID Sculptor", "Nume Sculptor", "Prenume Sculptor"), show="headings")
for col in tree_associations["columns"]:
    tree_associations.heading(col, text=col)
    tree_associations.column(col, anchor="center")

tree_associations.pack(fill=tk.BOTH, expand=True)

btn_show_associations = tk.Button(btn_frame_associations, text="Afișează Asocieri", command=show_associations)
btn_show_associations.pack(side=tk.LEFT, padx=5)

btn_add_association = tk.Button(btn_frame_associations, text="Adaugă", command=add_association)
btn_add_association.pack(side=tk.LEFT, padx=5)

btn_edit_association = tk.Button(btn_frame_associations, text="Modifică", command=edit_association)
btn_edit_association.pack(side=tk.LEFT, padx=5)

btn_delete_association = tk.Button(btn_frame_associations, text="Șterge", command=delete_association)
btn_delete_association.pack(side=tk.LEFT, padx=5)


# Pornirea aplicației
root.mainloop()
