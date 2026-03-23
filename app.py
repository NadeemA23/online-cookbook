import os
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'sqlite:///database.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback_secret')

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    recipes = db.relationship('Recipe', backref='owner', lazy=True)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    steps = db.Column(db.Text, nullable=False)
    cuisine = db.Column(db.String(50), nullable=False)
    tools = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
@login_required
def home():
    recipes = Recipe.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', recipes=recipes)


@app.route("/register", methods=["GET", "POST"])
def register():
    message = None
    if request.method == "POST":
        existing_user = User.query.filter_by(username=request.form['username']).first()
        if existing_user:
            message = "Username already exists"
            return render_template("register.html", message=message)

        hashed_password = generate_password_hash(request.form['password'])
        new_user = User(username=request.form['username'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))

    return render_template("register.html", message=message)


@app.route("/login", methods=["GET", "POST"])
def login():
    message = None
    if request.method == "POST":
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('home'))
        else:
            message = "Invalid username or password"
    return render_template("login.html", message=message)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


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
            user_id=current_user.id
        )
        db.session.add(new_recipe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add_recipe.html")


@app.route("/edit/<int:recipe_id>", methods=["GET", "POST"])
@login_required
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)

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


@app.route("/delete/<int:recipe_id>")
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)

    if recipe.user_id != current_user.id:
        abort(403)

    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for('home'))


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=False)