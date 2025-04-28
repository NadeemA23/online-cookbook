from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



# Define the Recipe model
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    steps = db.Column(db.Text, nullable=False)
    cuisine = db.Column(db.String(50), nullable=False)
    tools = db.Column(db.String(100), nullable=False)

# Home Page - Show All Recipes
@app.route('/')
def home():
    recipes = Recipe.query.all()
    return render_template('index.html', recipes=recipes)

# Add Recipe
@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        new_recipe = Recipe(
            name=request.form['name'],
            ingredients=request.form['ingredients'],
            steps=request.form['steps'],
            cuisine=request.form['cuisine'],
            tools=request.form['tools']
        )
        db.session.add(new_recipe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_recipe.html')

# Edit Recipe
@app.route('/edit/<int:recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)

    if request.method == 'POST':
        recipe.name = request.form['name']
        recipe.ingredients = request.form['ingredients']
        recipe.steps = request.form['steps']
        recipe.cuisine = request.form['cuisine']
        recipe.tools = request.form['tools']

        db.session.commit()
        return redirect(url_for('home'))

    return render_template('edit_recipe.html', recipe=recipe)

# Delete Recipe
@app.route('/delete/<int:recipe_id>')
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for('home'))

# Initialize DB when app starts
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)