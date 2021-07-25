from flask_app.models.recipe import Recipes
from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/users/register", methods=['POST'])
def register_user():
    # validate the form data
    if User.validate_registration(request.form):

        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': bcrypt.generate_password_hash(request.form['password'])

        }


        User.create_user(data)
    # create user if data is valid


    return redirect('/')


@app.route('/users/login', methods=['POST'])
def login_user():

    users = User.get_users_with_email(request.form)

    if len(users) != 1:
        flash("User with given email dosen't exist")
        return redirect('/')

    user = users[0]

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Password for the given user is incorrect")
        return redirect('/')

    session['user_id'] = user.id
    session['user_first_name'] = user.first_name
    session['user_last_name'] = user.last_name
    
    return redirect('/success')

@app.route('/success')
def success():
    if 'user_id' not in session:
        flash('Please log in to view this page.')
        return redirect('/')
    recipe = Recipes.get_all_recipes()
    return render_template('success.html', recipe=recipe)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/recipes/form')
def recipe_form():
    if 'user_id' not in session:
        flash('Please log in to view this page.')
        return redirect('/')

    return render_template('new_recipe.html')

@app.route('/recipes/new', methods=['POST'])
def new_recipe():

    if Recipes.validate_recipe(request.form) == False:
        return redirect('/recipes/form')
        
    data = {
        'name': request.form['name'],
        'under30': request.form['under30'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'made_on': request.form['made_on'],
        'user_id': session['user_id']
        }

    Recipes.create_recipe(data)
    return redirect('/success')


@app.route('/edit/<int:id>')
def show_edit(id):
    data = {'id': id}

    single_recipe = Recipes.show_recipe(data)
    
    return render_template('edit.html', x=single_recipe)

@app.route('/recipes/edit/<int:id>', methods=['POST'])
def make_edit(id):

    if Recipes.validate_recipe(request.form) == False:
        return redirect(f'/edit/{id}')

    data = {
        'id': id,
        'name': request.form['name'],
        'under30': request.form['under30'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'made_on': request.form['made_on'],
        'user_id': session['user_id']}

    Recipes.edit_recipe(data)

    return redirect('/success')

@app.route('/view/<int:id>')
def show_recipe(id):
    data = {'id': id}

    single_recipe = Recipes.show_recipe(data)

    return render_template('show.html', x=single_recipe)

@app.route('/delete/<int:id>')
def delete_recipe(id):
    data = {'id': id}
    Recipes.delete_recipe(data)

    return redirect('/success')