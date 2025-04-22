from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# DB connection
def get_db_connection():
    conn = sqlite3.connect('recipes.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create table if it doesn't exist
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            steps TEXT NOT NULL,
            cuisine TEXT NOT NULL,
            tools TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Home Page – Show All Recipes
@app.route('/')
def home():
    conn = get_db_connection()
    recipes = conn.execute('SELECT * FROM recipes').fetchall()
    conn.close()
    return render_template('index.html', recipes=recipes)

# Add Recipe
@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        name = request.form['name']
        ingredients = request.form['ingredients']
        steps = request.form['steps']
        cuisine = request.form['cuisine']
        tools = request.form['tools']

        conn = get_db_connection()
        conn.execute('INSERT INTO recipes (name, ingredients, steps, cuisine, tools) VALUES (?, ?, ?, ?, ?)',
                     (name, ingredients, steps, cuisine, tools))
        conn.commit()
        conn.close()

        return redirect(url_for('home'))
    return render_template('add_recipe.html')

# Delete Recipe
@app.route('/delete/<int:recipe_id>')
def delete_recipe(recipe_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

    # Edit Recipe
@app.route('/edit/<int:recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    conn = get_db_connection()
    recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        ingredients = request.form['ingredients']
        steps = request.form['steps']
        cuisine = request.form['cuisine']
        tools = request.form['tools']

        conn.execute('''
            UPDATE recipes
            SET name = ?, ingredients = ?, steps = ?, cuisine = ?, tools = ?
            WHERE id = ?
        ''', (name, ingredients, steps, cuisine, tools, recipe_id))

        conn.commit()
        conn.close()
        return redirect(url_for('home'))

    conn.close()
    return render_template('edit_recipe.html', recipe=recipe)

# Initialize DB when app starts
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
    