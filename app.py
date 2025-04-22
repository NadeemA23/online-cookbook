from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for recipes
recipes = []

# Home route to show all recipes
@app.route('/')
def home():
    return render_template('index.html', recipes=recipes)

# Add recipe route (form + submit)
@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        recipe = {
            'name': request.form['name'],
            'ingredients': request.form['ingredients'],
            'steps': request.form['steps'],
            'cuisine': request.form['cuisine'],
            'tools': request.form['tools']
        }
        recipes.append(recipe)
        return redirect(url_for('home'))
    return render_template('add_recipe.html')

# Optional: Delete a recipe by index
@app.route('/delete/<int:index>')
def delete_recipe(index):
    if 0 <= index < len(recipes):
        recipes.pop(index)
    return redirect(url_for('home'))

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)