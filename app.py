from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price_per_unit REAL NOT NULL,
            category TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/items', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_items():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        data = request.json
        cursor.execute('INSERT INTO inventory_items (name, quantity, price_per_unit, category) VALUES (?, ?, ?, ?)',
                       (data['name'], data['quantity'], data['price_per_unit'], data['category']))
        conn.commit()
        return jsonify({"message": "Item added successfully!"})

    elif request.method == 'GET':
        cursor.execute('SELECT * FROM inventory_items')
        items = cursor.fetchall()
        return jsonify(items)

    elif request.method == 'PUT':
        data = request.json
        cursor.execute('UPDATE inventory_items SET name = ?, quantity = ?, price_per_unit = ?, category = ? WHERE id = ?',
                       (data['name'], data['quantity'], data['price_per_unit'], data['category'], data['id']))
        conn.commit()
        return jsonify({"message": "Item updated successfully!"})

    elif request.method == 'DELETE':
        item_id = request.args.get('id')
        cursor.execute('DELETE FROM inventory_items WHERE id = ?', (item_id,))
        conn.commit()
        return jsonify({"message": "Item deleted successfully!"})

    conn.close()

if __name__ == '__main__':
    app.run(debug=True)
