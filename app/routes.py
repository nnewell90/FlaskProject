from app import app
from flask import render_template, flash, redirect
from app.forms import LoginForm
from flask import request
from flask import url_for
from flask import jsonify
import requests


# routes - URLs where a flask app accepts requests
@app.route('/')
@app.route('/index')
# a view function - route handler
def index():
    user = {'username': 'nnewell'}
    classes = [{'classInfo': {'code': 'CSC324', 'title': 'DevOps'}, 'instructor': 'Baoqiang Yan'},
               {'classInfo': {'code': 'CSC184', 'title': 'Python Programming'}, 'instructor': 'Evan Noynaert'}]
    return render_template('index.html', title='Home', user=user, classes=classes)
# changed index.html to nnewell.html

# new route for Exam 1
@app.route('/success')
def success():
    return render_template('nnewell.html', title='Success')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            credentials = {"username": form.username.data, "password": form.password.data}
            response = requests.post(url_for('loginAPI', _external=True), json=credentials)
            dict = response.json()
            if dict['Success']:
                #flash('Welcome user {}({})! You opted for remember_me={}'.format(form.username.data, dict['uid'], form.remember_me.data))
                return redirect(url_for('success'))
            else:
                flash('Invalid credentials')
    else:
        if request.args:
            flash('GET method not allowed for login!')
        # else:
        #     flash('No data in request!')

    return render_template('login.html', title='Sign In', form=form)


@app.route('/restlogin', methods=['GET', 'POST'])
@app.route('/loginAPI', methods=['GET', 'POST'])
def loginAPI():
    json_data = request.get_json(force=True)
    if json_data:
        username = json_data["username"]
        password = json_data["password"]
    else:
        return jsonify(Success=False)
    if username == 'nnewell' and password == '123':
        return jsonify(Success=True, uid=11)
    return jsonify(Success=False)


@app.route('/json')
def jsonTest():
    # return jsonify(list(range(5)))
    instructor = {"username": "byan",
                  "role": "instructor",
                  "uid": 11,
                  "name": {
                      "firstname": "Baoqiang",
                      "lastname": "Yan"
                  }
                  }

    return jsonify(instructor)




