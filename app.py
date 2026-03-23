import os
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'sqlite:///database.db')  # Local DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback_secret')  # Use env var if available

# Initialize database
db = SQLAlchemy(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    recipes = db.relationship('Recipe', backref='owner', lazy=True)

# Recipe model
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    steps = db.Column(db.Text, nullable=False)
    cuisine = db.Column(db.String(50), nullable=False)
    tools = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Load user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home page - only show the logged-in user’s recipes
@app.route('/')
@login_required  # force login to see recipes
def home():
    recipes = Recipe.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', recipes=recipes)

# Registration
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        existing_user = User.query.filter_by(username=request.form['username']).first()
        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(request.form['password'])
        new_user = User(username=request.form['username'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('home'))

    return render_template("register.html")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password")
    return render_template("login.html")

# Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# Add a recipe
@app.route("/add", methods=["GET", "POST"])
@login_required
def add_recipe():
    if request.method == "POST":
        new_recipe = Recipe(
            name=request.form['name'],
            ingredients=request.form['ingredients'],
            steps=request.form['steps'],
            cuisine=request.form['cuisine'],
            tools=request.form['tools'],
            user_id=current_user.id  # assign recipe to current user
        )
        db.session.add(new_recipe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add_recipe.html")

# Edit a recipe
@app.route("/edit/<int:recipe_id>", methods=["GET", "POST"])
@login_required
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)

    # Prevent editing someone else’s recipe
    if recipe.user_id != current_user.id:
        abort(403)

    if request.method == "POST":
        recipe.name = request.form['name']
        recipe.ingredients = request.form['ingredients']
        recipe.steps = request.form['steps']
        recipe.cuisine = request.form['cuisine']
        recipe.tools = request.form['tools']
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("edit_recipe.html", recipe=recipe)

# Delete a recipe
@app.route("/delete/<int:recipe_id>")
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)

    # Prevent deleting someone else’s recipe
    if recipe.user_id != current_user.id:
        abort(403)

    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for('home'))

# Initialize the database
with app.app_context():
    db.create_all()

# unRun the app
if __name__ == '__main__':
    app.run(debug=False)