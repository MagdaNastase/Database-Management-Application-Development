from flask import Flask, request, jsonify, render_template_string
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='2002',
            database='bazadedate'
        )
        if connection.is_connected():
            print("Conexiune reușită la baza de date.")
        return connection
    except Error as e:
        print(f"Eroare la conectarea la baza de date: {e}")
        return None

@app.route('/')
def home():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8"> 
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Aplicația Sculpturi API</title>
        <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh; /* întreaga înălțime a ecranului */
                margin: 0;
                font-family: Arial, sans-serif;
                text-align: center;
                background-image: url('https://images.unsplash.com/photo-1529154166925-574a0236a4f4?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }
            .container { /*Un div central cu fundal semi-transparent, culoare albă și colțuri rotunjite */
                max-width: 600px;
                background-color: rgba(0.1, 0.2, 0.5, 0.8); /* Fundal semi-transparent */
                padding: 20px;
                border-radius: 15px; /* Rotunjirea colțurilor */
                color: white; /* Text alb */
            }
            h1 {
                font-size: 2.5em;
                margin-bottom: 20px;
            }
            .actions button {
                margin: 10px;
                padding: 10px 20px;
                font-size: 1em;
                cursor: pointer;
                border: none;
                border-radius: 5px;
                background-color: #007bff;
                color: white;
                transition: background-color 0.3s;
            }
            .actions button:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Bine ai venit!</h1>
            <p>Selectează acțiunea dorită:</p>
            <div class="actions">
                <button onclick="window.location.href='/sculptors';">Vezi Sculptori</button>
                <button onclick="window.location.href='/associations';">Vezi Asocieri</button>
                <button onclick="window.location.href='/sculptures';">Vezi Sculpturi</button>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)


# RUTE SCULPTORI
@app.route('/sculptors', methods=['GET'])
def get_sculptors():
    connection = connect_to_database()
    if not connection:
        return jsonify({"error": "Nu s-a putut conecta la baza de date"}), 500

    try:
        cursor = connection.cursor(dictionary=True) # rezultatele să fie dicționare
        cursor.execute("SELECT * FROM Sculptors")
        sculptors = cursor.fetchall() #aduce toate înregistrările într-o listă de dicționare
        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Lista Sculptorilor</title>
            {styles}
        </head>
        <body>
            <h1>Lista Sculptorilor</h1>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Nume</th>
                    <th>Prenume</th>
                    <th>An Naștere</th>
                    <th>An Deces</th>
                    <th>Naționalitate</th>
                    <th>Stil Artistic</th>
                    <th>Acțiuni</th>
                </tr>
        """.format(styles=css_styles)
        for sculptor in sculptors:
            html += f"""
                <tr>
                    <td>{sculptor['SculptorID']}</td>
                    <td>{sculptor['Nume']}</td>
                    <td>{sculptor['Prenume']}</td>
                    <td>{sculptor['AnNastere']}</td>
                    <td>{sculptor['AnDeces']}</td>
                    <td>{sculptor['Nationalitate']}</td>
                    <td>{sculptor['StilArtistic']}</td>
                    <td>
                        <form action='/edit_sculptor/{sculptor['SculptorID']}' method='GET' style='display:inline;'>
                            <button class="edit-button">Modifică</button>
                        </form>
                        <form action='/delete_sculptor/{sculptor['SculptorID']}' method='POST' style='display:inline;'>
                            <button class="delete-button">Șterge</button>
                        </form>
                    </td>
                </tr>
            """
        html += """
            </table>
            <div class="container">
                <button class="add-button" onclick="window.location.href='/add_sculptor';">Adaugă Sculptor</button>
                <a href='/'>Înapoi la Home</a>
            </div>
        </body>
        </html>
        """
        return render_template_string(html)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

@app.route('/add_sculptor', methods=['GET', 'POST'])
def add_sculptor():
    if request.method == 'POST':
        data = request.form
        connection = connect_to_database()
        if not connection:
            return jsonify({"error": "Nu s-a putut conecta la baza de date"}), 500

        try:
            cursor = connection.cursor()
            sql = "INSERT INTO Sculptors (Nume, Prenume, AnNastere, AnDeces, Nationalitate, StilArtistic) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (
                data['Nume'], data['Prenume'], data['AnNastere'], data.get('AnDeces'), data['Nationalitate'], data['StilArtistic']
            ))
            connection.commit()
            return """<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sculptor Adăugat</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                margin-top: 50px;
            }
            .success-message {
                font-size: 1.5em;
                font-weight: bold;
                color: #28a745;
            }
            .back-button {
                display: inline-block;
                text-decoration: none;
                background-color: #007bff;
                color: white;
                padding: 12px 20px;
                font-size: 1.2em;
                border-radius: 15px;
                transition: background-color 0.3s;
                margin-top: 20px;
            }
            .back-button:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="success-message">Sculptor adăugat cu succes!</div>
        <a href="/sculptors" class="back-button">Înapoi la lista sculptorilor</a>
    </body>
    </html>
        """, 201
        except Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            connection.close()

    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Adaugă Sculptor</title>
        {styles}
    </head>
    <body>
        <h1>Adaugă Sculptor</h1>
        <form method="POST">
            <label for="nume">Nume:</label>
            <input type="text" id="nume" name="Nume" required>

            <label for="prenume">Prenume:</label>
            <input type="text" id="prenume" name="Prenume" required>

            <label for="an_nastere">An Naștere:</label>
            <input type="number" id="an_nastere" name="AnNastere" required>

            <label for="an_deces">An Deces:</label>
            <input type="number" id="an_deces" name="AnDeces">

            <label for="nationalitate">Naționalitate:</label>
            <input type="text" id="nationalitate" name="Nationalitate" required>

            <label for="stil_artistic">Stil Artistic:</label>
            <input type="text" id="stil_artistic" name="StilArtistic" required>
            <div class="container">
            <button type="submit">Adaugă</button>
            <a href='/sculptors'>Înapoi la lista sculptorilor</a>
        </form>
        </div>
    </body>
    </html>
    """.format(styles=css_styles)
    return render_template_string(html)

@app.route('/delete_sculptor/<int:id>', methods=['POST'])
def delete_sculptor(id):
    connection = connect_to_database()
    if not connection:
        return jsonify({"error": "Nu s-a putut conecta la baza de date"}), 500

    try:
        cursor = connection.cursor()

        # Găsește sculpturile asociate sculptorului
        find_sculptures_sql = """
            SELECT SculptureID FROM Sculpture_Sculptor WHERE SculptorID = %s
        """
        cursor.execute(find_sculptures_sql, (id,))
        associated_sculptures = cursor.fetchall()

        # Șterge sculptorul
        delete_sculptor_sql = "DELETE FROM Sculptors WHERE SculptorID = %s"
        cursor.execute(delete_sculptor_sql, (id,))
        connection.commit()

        # Verifică dacă sculpturile asociate mai au alți sculptori
        for sculpture in associated_sculptures:
            sculpture_id = sculpture[0]
            check_association_sql = """
                SELECT COUNT(*) FROM Sculpture_Sculptor WHERE SculptureID = %s
            """
            cursor.execute(check_association_sql, (sculpture_id,))
            count = cursor.fetchone()[0]

            # Dacă sculptura nu mai are alte asocieri, șterge sculptura
            if count == 0:
                delete_sculpture_sql = "DELETE FROM Sculptures WHERE SculptureID = %s"
                cursor.execute(delete_sculpture_sql, (sculpture_id,))
                connection.commit()

        # Reindexare ID-uri pentru tabelul Sculptors
        cursor.execute("SET @new_id = 0;")
        cursor.execute("UPDATE Sculptors SET SculptorID = (@new_id := @new_id + 1);")
        cursor.execute("ALTER TABLE Sculptors AUTO_INCREMENT = 1;")
        connection.commit()

        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Sculptor Șters</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    text-align: center;
                    margin-top: 50px;
                }
                .success-message {
                    font-size: 1.5em;
                    font-weight: bold;
                    color: #28a745;
                }
                .back-button {
                    display: inline-block;
                    text-decoration: none;
                    background-color: #007bff;
                    color: white;
                    padding: 12px 20px;
                    font-size: 1.2em;
                    border-radius: 15px;
                    transition: background-color 0.3s;
                    margin-top: 20px;
                }
                .back-button:hover {
                    background-color: #0056b3;
                }
            </style>
        </head>
        <body>
            <div class="success-message">Sculptor șters cu succes!</div>
            <a href="/sculptors" class="back-button">Înapoi la lista sculptorilor</a>
        </body>
        </html>
        """, 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()



@app.route('/edit_sculptor/<int:id>', methods=['GET', 'POST'])
def edit_sculptor(id):
    connection = connect_to_database()
    if not connection:
        return jsonify({"error": "Nu s-a putut conecta la baza de date"}), 500

    if request.method == 'POST':
        data = request.form
        try:
            cursor = connection.cursor()
            sql = "UPDATE Sculptors SET Nume = %s, Prenume = %s, AnNastere = %s, AnDeces = %s, Nationalitate = %s, StilArtistic = %s WHERE SculptorID = %s"
            cursor.execute(sql, (
                data['Nume'], data['Prenume'], data['AnNastere'], data.get('AnDeces'), data['Nationalitate'], data['StilArtistic'], id
            ))
            connection.commit()
            return """  <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sculptor Adăugat</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                margin-top: 50px;
            }
            .success-message {
                font-size: 1.5em;
                font-weight: bold;
                color: #28a745;
            }
            .back-button {
                display: inline-block;
                text-decoration: none;
                background-color: #007bff;
                color: white;
                padding: 12px 20px;
                font-size: 1.2em;
                border-radius: 15px;
                transition: background-color 0.3s;
                margin-top: 20px;
            }
            .back-button:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="success-message">Sculptor actualizat cu succes!</div>
        <a href="/sculptors" class="back-button">Înapoi la lista sculptorilor</a>
    </body>
    </html> 
        
        """, 200
        except Error as e: 
            return jsonify({"error": str(e)}), 500
        finally:
            connection.close()

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Sculptors WHERE SculptorID = %s", (id,))
        sculptor = cursor.fetchone()
        if not sculptor:
            return "<h1>Sculptorul nu a fost găsit!</h1><a href='/sculptors'>Înapoi la lista sculptorilor</a>", 404

        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Editează Sculptor</title>
            {css_styles}
        </head>
        <body>
            <h1>Editează Sculptor</h1>
            <form method="POST">
                <label for='nume'>Nume:</label>
                <input type='text' id='nume' name='Nume' value='{sculptor['Nume']}' required>

                <label for='prenume'>Prenume:</label>
                <input type='text' id='prenume' name='Prenume' value='{sculptor['Prenume']}' required>

                <label for='an_nastere'>An Naștere:</label>
                <input type='number' id='an_nastere' name='AnNastere' value='{sculptor['AnNastere']}' required>

                <label for='an_deces'>An Deces:</label>
                <input type='number' id='an_deces' name='AnDeces' value='{sculptor['AnDeces']}'>

                <label for='nationalitate'>Naționalitate:</label>
                <input type='text' id='nationalitate' name='Nationalitate' value='{sculptor['Nationalitate']}' required>

                <label for='stil_artistic'>Stil Artistic:</label>
                <input type='text' id='stil_artistic' name='StilArtistic' value='{sculptor['StilArtistic']}' required>
                 <div class="container">
                <button type='submit'>Salvează</button>
                <a href='/sculptors'>Înapoi la lista sculptorilor</a>
            </div>
            </form>
            
        </body>
        </html>
        """
        return render_template_string(html)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()
        
    
# RUTE SCULPTURI
@app.route('/sculptures', methods=['GET'])
def get_sculptures():
    connection = connect_to_database()
    if not connection:
        return jsonify({"error": "Nu s-a putut conecta la baza de date"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Sculptures")
        sculptures = cursor.fetchall()
        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Lista Sculpturilor</title>
            {styles}
        </head>
        <body>
            <h1>Lista Sculpturilor</h1>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Titlu</th>
                    <th>Material</th>
                    <th>Înălțime</th>
                    <th>Greutate</th>
                    <th>An Creație</th>
                    <th>Locație Muzeu</th>
                    <th>Acțiuni</th>
                </tr>
        """.format(styles=css_styles)
        for sculpture in sculptures:
            html += f"""
                <tr>
                    <td>{sculpture['SculptureID']}</td>
                    <td>{sculpture['Titlu']}</td>
                    <td>{sculpture['Material']}</td>
                    <td>{sculpture['Inaltime']}</td>
                    <td>{sculpture['Greutate']}</td>
                    <td>{sculpture['AnCreatie']}</td>
                    <td>{sculpture['LocatieMuzeu']}</td>
                    <td>
                        <form action='/edit_sculpture/{sculpture['SculptureID']}' method='GET' style='display:inline;'>
                            <button class="edit-button">Modifică</button>
                        </form>
                        <form action='/delete_sculpture/{sculpture['SculptureID']}' method='POST' style='display:inline;'>
                            <button class="delete-button">Șterge</button>
                        </form>
                    </td>
                </tr>
            """
        html += """
            </table>
            <div class="container">
                <button class="add-button" onclick="window.location.href='/add_sculpture';">Adaugă Sculptură</button>
                <a href='/'>Înapoi la Home</a>
            </div>
        </body>
        </html>
        """
        return render_template_string(html)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()
        
           
@app.route('/add_sculpture', methods=['GET', 'POST'])
def add_sculpture():
    """Adaugă o nouă sculptură."""
    if request.method == 'POST':
        data = request.form
        connection = connect_to_database()
        if not connection:
            return jsonify({"error": "Nu s-a putut conecta la baza de date"}), 500

        try:
            cursor = connection.cursor()
            sql = """
            INSERT INTO Sculptures (Titlu, Material, Inaltime, Greutate, AnCreatie, LocatieMuzeu) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                data['Titlu'], data['Material'], data['Inaltime'], 
                data['Greutate'], data['AnCreatie'], data['LocatieMuzeu']
            ))
            connection.commit()
            return """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Sculptură Adăugată</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        text-align: center;
                        margin-top: 50px;
                    }
                    .success-message {
                        font-size: 1.5em;
                        font-weight: bold;
                        color: #28a745;
                    }
                    .back-button {
                        display: inline-block;
                        text-decoration: none;
                        background-color: #007bff;
                        color: white;
                        padding: 12px 20px;
                        font-size: 1.2em;
                        border-radius: 5px;
                        transition: background-color 0.3s;
                        margin-top: 20px;
                    }
                    .back-button:hover {
                        background-color: #0056b3;
                    }
                </style>
            </head>
            <body>
                <div class="success-message">Sculptură adăugată cu succes!</div>
                <a href="/sculptures" class="back-button">Înapoi la lista sculpturilor</a>
            </body>
            </html>
            """, 201
        except Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            connection.close()

    # Pagina de adăugare
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Adaugă Sculptură</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                margin-top: 20px;
            }
            form {
                display: inline-block;
                text-align: left;
                background: #f9f9f9;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            label {
                display: block;
                margin: 10px 0 5px;
                font-size: 1.1em;
            }
            input {
                width: 100%;
                padding: 8px;
                font-size: 1em;
                margin-bottom: 20px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            button {
                padding: 12px 20px;
                font-size: 1.2em;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            button.add-button {
                background-color: #28a745;
                color: white;
            }
            button.add-button:hover {
                background-color: #218838;
            }
            button.back-button {
                background-color: #007bff;
                color: white;
                margin-left: 10px;
            }
            button.back-button:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <h1>Adaugă Sculptură</h1>
        <form method="POST">
            <label for="titlu">Titlu:</label>
            <input type="text" id="titlu" name="Titlu" required>

            <label for="material">Material:</label>
            <input type="text" id="material" name="Material" required>

            <label for="inaltime">Înălțime:</label>
            <input type="text" id="inaltime" name="Inaltime" required>

            <label for="greutate">Greutate:</label>
            <input type="text" id="greutate" name="Greutate" required>

            <label for="an_creatie">An Creație:</label>
            <input type="text" id="an_creatie" name="AnCreatie" required>

            <label for="locatie_muzeu">Locație Muzeu:</label>
            <input type="text" id="locatie_muzeu" name="LocatieMuzeu" required>

            <button type="submit" class="add-button">Adaugă</button>
            <button type="button" class="back-button" onclick="window.location.href='/sculptures'">Înapoi</button>
        </form>
    </body>
    </html>
    """
    return render_template_string(html)


@app.route('/delete_sculpture/<int:id>', methods=['POST'])
def delete_sculpture(id):
    """Șterge o sculptură și reindexează ID-urile."""
    connection = connect_to_database()
    if not connection:
        return jsonify({"error": "Nu s-a putut conecta la baza de date"}), 500

    try:
        cursor = connection.cursor()

        # Șterge sculptura
        sql = "DELETE FROM Sculptures WHERE SculptureID = %s"
        cursor.execute(sql, (id,))
        connection.commit()

        # Reindexează ID-urile
        cursor.execute("SET @new_id = 0;")
        cursor.execute("UPDATE Sculptures SET SculptureID = (@new_id := @new_id + 1);")
        cursor.execute("ALTER TABLE Sculptures AUTO_INCREMENT = 1;")
        connection.commit()

        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Sculptură Ștearsă</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    text-align: center;
                    margin-top: 50px;
                }
                .success-message {
                    font-size: 1.5em;
                    font-weight: bold;
                    color: #28a745;
                }
                .back-button {
                    display: inline-block;
                    text-decoration: none;
                    background-color: #007bff;
                    color: white;
                    padding: 12px 20px;
                    font-size: 1.2em;
                    border-radius: 5px;
                    transition: background-color 0.3s;
                    margin-top: 20px;
                }
                .back-button:hover {
                    background-color: #0056b3;
                }
            </style>
        </head>
        <body>
            <div class="success-message">Sculptură ștearsă!</div>
            <a href="/sculptures" class="back-button">Înapoi la lista sculpturilor</a>
        </body>
        </html>
        """, 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()



@app.route('/edit_sculpture/<int:id>', methods=['GET', 'POST'])
def edit_sculpture(id):
    """Editează o sculptură."""
    connection = connect_to_database()
    if not connection:
        return jsonify({"error": "Nu s-a putut conecta la baza de date"}), 500

    if request.method == 'POST':
        data = request.form
        try:
            cursor = connection.cursor()
            sql = """
            UPDATE Sculptures 
            SET Titlu = %s, Material = %s, Inaltime = %s, Greutate = %s, AnCreatie = %s, LocatieMuzeu = %s 
            WHERE SculptureID = %s
            """
            cursor.execute(sql, (
                data['Titlu'], data['Material'], data['Inaltime'], 
                data['Greutate'], data['AnCreatie'], data['LocatieMuzeu'], id
            ))
            connection.commit()
            return """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Sculptură Editată</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        text-align: center;
                        margin-top: 50px;
                    }
                    .success-message {
                        font-size: 1.5em;
                        font-weight: bold;
                        color: #28a745;
                    }
                    .back-button {
                        display: inline-block;
                        text-decoration: none;
                        background-color: #007bff;
                        color: white;
                        padding: 12px 20px;
                        font-size: 1.2em;
                        border-radius: 5px;
                        transition: background-color 0.3s;
                        margin-top: 20px;
                    }
                    .back-button:hover {
                        background-color: #0056b3;
                    }
                </style>
            </head>
            <body>
                <div class="success-message">Sculptură actualizată cu succes!</div>
                <a href="/sculptures" class="back-button">Înapoi la lista sculpturilor</a>
            </body>
            </html>
            """, 200
        except Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            connection.close()

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Sculptures WHERE SculptureID = %s", (id,))
        sculpture = cursor.fetchone()
        if not sculpture:
            return "<h1>Sculptura nu a fost găsită!</h1><a href='/sculptures'>Înapoi la lista sculpturilor</a>", 404

        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Editează Sculptură</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    text-align: center;
                    margin-top: 20px;
                }}
                form {{
                    display: inline-block;
                    text-align: left;
                    background: #f9f9f9;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                }}
                label {{
                    display: block;
                    margin: 10px 0 5px;
                    font-size: 1.1em;
                }}
                input {{
                    width: 100%;
                    padding: 8px;
                    font-size: 1em;
                    margin-bottom: 20px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                }}
                button {{
                    padding: 12px 20px;
                    font-size: 1.2em;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    transition: background-color 0.3s;
                }}
                button.save-button {{
                    background-color: #28a745;
                    color: white;
                }}
                button.save-button:hover {{
                    background-color: #218838;
                }}
                button.back-button {{
                    background-color: #007bff;
                    color: white;
                    margin-left: 10px;
                }}
                button.back-button:hover {{
                    background-color: #0056b3;
                }}
            </style>
        </head>
        <body>
            <h1>Editează Sculptură</h1>
            <form method="POST">
                <label for="titlu">Titlu:</label>
                <input type="text" id="titlu" name="Titlu" value="{sculpture['Titlu']}" required>

                <label for="material">Material:</label>
                <input type="text" id="material" name="Material" value="{sculpture['Material']}" required>

                <label for="inaltime">Înălțime:</label>
                <input type="text" id="inaltime" name="Inaltime" value="{sculpture['Inaltime']}" required>

                <label for="greutate">Greutate:</label>
                <input type="text" id="greutate" name="Greutate" value="{sculpture['Greutate']}" required>

                <label for="an_creatie">An Creație:</label>
                <input type="text" id="an_creatie" name="AnCreatie" value="{sculpture['AnCreatie']}" required>

                <label for="locatie_muzeu">Locație Muzeu:</label>
                <input type="text" id="locatie_muzeu" name="LocatieMuzeu" value="{sculpture['LocatieMuzeu']}" required>

                <button type="submit" class="save-button">Salvează</button>
                <button type="button" class="back-button" onclick="window.location.href='/sculptures'">Înapoi</button>
            </form>
        </body>
        </html>
        """
        return render_template_string(html)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()


css_styles = """
<style>
    body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 20px;
        text-align: center;
    }
    table {
        width: 80%;
        margin: 20px auto;
        border-collapse: collapse; /* Elimină spațiile dintre celule */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    th, td {
        border: 1px solid #ddd;
        padding: 10px;
        text-align: center;
    }
    th {
        background-color: #f4f4f4;
        font-weight: bold;
    }
    tr:nth-child(even) {
        background-color: #f9f9f9;
        margin: 0;
        border: none;
    }
    tr:hover {
        background-color: #f1f1f1;
    }
   
    .add-button {
        background-color: #28a745;
        color: white;
        padding: 12px 20px;
        font-size: 1.2em;
        border-radius: 15px;
        border: none;
    }
    .add-button:hover {
        background-color: #218838;
    }
    .delete-button {
        background-color: #dc3545;
        color: white;
        padding: 15px 20px;
        font-size: 1.2em;
        border: none;
        margin: none;
        border-radius: 15px;
    }
    .delete-button:hover {
        background-color: #c82333;
    }
    .edit-button {
        background-color: #ffc107;
        color: black;
        padding: 15px 20px;
        font-size: 1.2em;
        border-radius: 15px;
        border: none;
    }
    .edit-button:hover {
        background-color: #e0a800;
    }
    .container {
        margin-top: 20px;
    }
    .container button {
        display: inline-block;
        margin: 50px;
    }
    .container a {
        display: inline-block;
        text-decoration: none;
        background-color: #007bff;
        color: white;
        padding: 12px 20px;
        font-size: 1.2em;
        border-radius: 15px;
        transition: background-color 0.3s;
    }
    .container a:hover {
        background-color: #0056b3;
    }
    form {
        width: 50%; /* Lățime redusă pentru form */
        margin: 20px auto;
        padding: 0px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border-radius: 15px;
        background-color: #f9f9f9;
    }
    label {
        font-size: 1.2em;
        display: block;
        margin: 10px 0 5px;
    }
    input, select {
        width: 70%; /* Dimensiune redusă pentru casetele de input */
        padding: 8px;
        font-size: 1em;
        margin-bottom: 20px;
        border: 1px solid #ddd;
        border-radius: 5px;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    .form-button {
        background-color: #007bff;
        color: white;
        padding: 15px 30px; /* Dimensiuni mai mari pentru buton */
        font-size: 1.2em;
        border: none;
        border-radius: 15px;
        cursor: pointer;
        margin-top: 10px;
    }
    .form-button:hover {
        background-color: #0056b3;
    }
    
    button, input[type="submit"] {
        background-color: #556B2F;
        color: white;
        padding: 12px 20px; /* Dimensiuni mai mari pentru buton */
        font-size: 1.2em;
        border: none;
        border-radius: 15px;
        cursor: pointer;
        margin-top: 10px;
    }
    button:hover, input[type="submit"]:hover {
        background-color: #556B2F;
    }
</style>
"""

@app.route('/associations', methods=['GET'])
def get_associations():
    connection = connect_to_database()
    if not connection:
        return jsonify({"error": "Nu s-a putut conecta la baza de date"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                ss.SculptureID,
                s.Titlu AS TitluSculptura,
                ss.SculptorID,
                sc.Nume AS NumeSculptor,
                sc.Prenume AS PrenumeSculptor
            FROM 
                Sculpture_Sculptor ss
            JOIN 
                Sculptures s ON ss.SculptureID = s.SculptureID
            JOIN 
                Sculptors sc ON ss.SculptorID = sc.SculptorID;
        """)
        associations = cursor.fetchall()
        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Lista Asocierilor</title>
            {styles}
        </head>
        <body>
            <h1>Lista Asocierilor Sculpturi-Sculptori</h1>
            <table>
                <tr>
                    <th>ID Sculptură</th>
                    <th>Titlu Sculptură</th>
                    <th>ID Sculptor</th>
                    <th>Nume Sculptor</th>
                    <th>Prenume Sculptor</th>
                    <th>Acțiuni</th>
                </tr>
        """.format(styles=css_styles)
        for association in associations:
            html += f"""
                <tr>
                    <td>{association['SculptureID']}</td>
                    <td>{association['TitluSculptura']}</td>
                    <td>{association['SculptorID']}</td>
                    <td>{association['NumeSculptor']}</td>
                    <td>{association['PrenumeSculptor']}</td>
                    <td>
                        <form action='/edit_association/{association['SculptureID']}/{association['SculptorID']}' method='GET' style='display:inline;'>
                            <button class="edit-button">Modifică</button>
                        </form>
                        <form action='/delete_association/{association['SculptureID']}/{association['SculptorID']}' method='POST' style='display:inline;'>
                            <button class="delete-button">Șterge</button>
                        </form>
                    </td>
                </tr>
            """
        html += """
            </table>
            <div class="container">
                <button class="add-button" onclick="window.location.href='/add_association';">Adaugă Asociere</button>
                <a href='/'>Înapoi la Home</a>
            </div>
        </body>
        </html>
        """
        return render_template_string(html)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()


@app.route('/add_association', methods=['GET', 'POST'])
def add_association():
    """Adaugă o asociere între o sculptură și un sculptor."""
    connection = connect_to_database()
    if not connection:
        return jsonify({"error": "Nu s-a putut conecta la baza de date"}), 500

    if request.method == 'POST':
        data = request.form
        try:
            cursor = connection.cursor()
            sql = "INSERT INTO Sculpture_Sculptor (SculptureID, SculptorID) VALUES (%s, %s)"
            cursor.execute(sql, (data['SculptureID'], data['SculptorID']))
            connection.commit()
            return """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Asociere Adăugată</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        text-align: center;
                        margin-top: 50px;
                    }
                    .success-message {
                        font-size: 1.5em;
                        font-weight: bold;
                        color: #28a745;
                    }
                    .back-button {
                        display: inline-block;
                        text-decoration: none;
                        background-color: #007bff;
                        color: white;
                        padding: 12px 20px;
                        font-size: 1.2em;
                        border-radius: 5px;
                        transition: background-color 0.3s;
                        margin-top: 20px;
                    }
                    .back-button:hover {
                        background-color: #0056b3;
                    }
                </style>
            </head>
            <body>
                <div class="success-message">Asociere adăugată cu succes!</div>
                <a href="/associations" class="back-button">Înapoi la lista asocierilor</a>
            </body>
            </html>
            """, 201
        except Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            connection.close()

    # Obține lista sculpturilor și sculptorilor
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT SculptureID, Titlu FROM Sculptures")
        sculptures = cursor.fetchall()
        cursor.execute("SELECT SculptorID, Nume, Prenume FROM Sculptors")
        sculptors = cursor.fetchall()
    except Error as e:
        return jsonify({"error": str(e)}), 500

    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Adaugă Asociere</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                margin-top: 20px;
            }
            form {
                display: inline-block;
                text-align: left;
                background: #f9f9f9;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            label {
                display: block;
                margin: 10px 0 5px;
                font-size: 1.1em;
            }
            select {
                width: 100%;
                padding: 8px;
                font-size: 1em;
                margin-bottom: 20px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            button.add-button {
                background-color: #28a745;
                color: white;
                padding: 12px 20px;
                font-size: 1.2em;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            button.add-button:hover {
                background-color: #218838;
            }
            button.back-button {
                background-color: #007bff;
                color: white;
                padding: 12px 20px;
                font-size: 1.2em;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s;
                margin-left: 10px;
            }
            button.back-button:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <h1>Adaugă Asociere</h1>
        <form method="POST">
            <label for="sculpture_id">Selectează Sculptura:</label>
            <select id="sculpture_id" name="SculptureID" required>
    """
    for sculpture in sculptures: #Completează lista cu toate sculpturile disponibile
        html += f"<option value='{sculpture['SculptureID']}'>{sculpture['Titlu']}</option>"

    html += """
            </select>
            <label for="sculptor_id">Selectează Sculptorul:</label>
            <select id="sculptor_id" name="SculptorID" required>
    """
    for sculptor in sculptors: #Adăugarea opțiunilor pentru sculptori
        html += f"<option value='{sculptor['SculptorID']}'>{sculptor['Nume']} {sculptor['Prenume']}</option>"

    html += """
            </select>
            <button type="submit" class="add-button">Adaugă</button>
            <button type="button" class="back-button" onclick="window.location.href='/associations'">Înapoi la lista de asocieri </button>
        </form>
    </body>
    </html>
    """
    return render_template_string(html)


@app.route('/edit_association/<int:sculpture_id>/<int:sculptor_id>', methods=['GET', 'POST'])
def edit_association(sculpture_id, sculptor_id):
    """Editează o asociere existentă între sculptură și sculptor."""
    connection = connect_to_database()
    if not connection:
        return jsonify({"error": "Nu s-a putut conecta la baza de date"}), 500

    if request.method == 'POST':
        data = request.form
        try:
            cursor = connection.cursor()
            sql = """
            UPDATE Sculpture_Sculptor
            SET SculptureID = %s, SculptorID = %s
            WHERE SculptureID = %s AND SculptorID = %s
            """
            cursor.execute(sql, (data['SculptureID'], data['SculptorID'], sculpture_id, sculptor_id))
            connection.commit()
            return """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Asociere Editată</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        text-align: center;
                        margin-top: 50px;
                    }
                    .success-message {
                        font-size: 1.5em;
                        font-weight: bold;
                        color: #28a745;
                    }
                    .back-button {
                        display: inline-block;
                        text-decoration: none;
                        background-color: #007bff;
                        color: white;
                        padding: 12px 20px;
                        font-size: 1.2em;
                        border-radius: 5px;
                        transition: background-color 0.3s;
                        margin-top: 20px;
                    }
                    .back-button:hover {
                        background-color: #0056b3;
                    }
                </style>
            </head>
            <body>
                <div class="success-message">Asociere actualizată cu succes!</div>
                <a href="/associations" class="back-button">Înapoi la lista asocierilor</a>
            </body>
            </html>
            """, 200
        except Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            connection.close()

    # Obține lista sculpturilor și sculptorilor
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT SculptureID, Titlu FROM Sculptures")
        sculptures = cursor.fetchall()
        cursor.execute("SELECT SculptorID, Nume, Prenume FROM Sculptors")
        sculptors = cursor.fetchall()
    except Error as e:
        return jsonify({"error": str(e)}), 500

    # Formatează pagina HTML
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Editează Asociere</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                text-align: center;
                margin-top: 20px;
            }}
            form {{
                display: inline-block;
                text-align: left;
                background: #f9f9f9;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }}
            label {{
                display: block;
                margin: 10px 0 5px;
                font-size: 1.1em;
            }}
            select {{
                width: 100%;
                padding: 8px;
                font-size: 1em;
                margin-bottom: 20px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }}
            button.save-button {{
                background-color: #28a745;
                color: white;
                padding: 12px 20px;
                font-size: 1.2em;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s;
            }}
            button.save-button:hover {{
                background-color: #218838;
            }}
            button.back-button {{
                background-color: #007bff;
                color: white;
                padding: 12px 20px;
                font-size: 1.2em;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s;
                margin-left: 10px;
            }}
            button.back-button:hover {{
                background-color: #0056b3;
            }}
        </style>
    </head>
    <body>
        <h1>Editează Asociere</h1>
        <form method="POST">
            <label for="sculpture_id">Selectează Sculptura:</label>
            <select id="sculpture_id" name="SculptureID" required>
    """
    for sculpture in sculptures:
        selected = "selected" if sculpture['SculptureID'] == sculpture_id else ""
        html += f"<option value='{sculpture['SculptureID']}' {selected}>{sculpture['Titlu']}</option>"

    html += """
            </select>
            <label for="sculptor_id">Selectează Sculptorul:</label>
            <select id="sculptor_id" name="SculptorID" required>
    """
    for sculptor in sculptors:
        selected = "selected" if sculptor['SculptorID'] == sculptor_id else ""
        html += f"<option value='{sculptor['SculptorID']}' {selected}>{sculptor['Nume']} {sculptor['Prenume']}</option>"

    html += """
            </select>
            <button type="submit" class="save-button">Salvează</button>
            <button type="button" class="back-button" onclick="window.location.href='/associations'">Înapoi la lista de asocieri </button>
        </form>
    </body>
    </html>
    """
    return render_template_string(html)


@app.route('/delete_association/<int:sculpture_id>/<int:sculptor_id>', methods=['POST'])
def delete_association(sculpture_id, sculptor_id):
    """Șterge o asociere."""
    connection = connect_to_database()
    if not connection:
        return jsonify({"error": "Nu s-a putut conecta la baza de date"}), 500

    try:
        cursor = connection.cursor()
        sql = "DELETE FROM Sculpture_Sculptor WHERE SculptureID = %s AND SculptorID = %s"
        cursor.execute(sql, (sculpture_id, sculptor_id))
        connection.commit()
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Asociere Ștearsă</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    text-align: center;
                    margin-top: 50px;
                }
                .success-message {
                    font-size: 1.5em;
                    font-weight: bold;
                    color: #28a745;
                }
                .back-button {
                    display: inline-block;
                    text-decoration: none;
                    background-color: #007bff;
                    color: white;
                    padding: 12px 20px;
                    font-size: 1.2em;
                    border-radius: 5px;
                    transition: background-color 0.3s;
                    margin-top: 20px;
                }
                .back-button:hover {
                    background-color: #0056b3;
                }
            </style>
        </head>
        <body>
            <div class="success-message">Asociere ștearsă cu succes!</div>
            <a href="/associations" class="back-button">Înapoi la lista asocierilor</a>
        </body>
        </html>
        """, 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)