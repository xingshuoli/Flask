from functools import wraps

from flask import Flask, request, jsonify, render_template, redirect, flash, url_for, session
from mysql_util import MysqlUtil
from forms import RegisterForm
from passlib.hash import sha256_crypt

# from flask_bootstrap import Bootstrap
app = Flask(__name__)
app.secret_key = '123456'


# bootstrap = Bootstrap(app)


@app.route('/')
def index():  # put application's code here
    return redirect('/login')


@app.route('/about')
def about():
    return 'About Page'


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        db = MysqlUtil()
        sql = 'select username from users where username = %s' % username
        result = db.cursor.execute(sql)
        if result != 0:
            flash('User already exists', 'danger')
            return redirect('/register', form=form)
        sql = 'insert into users(username, password) values(%s, %s)' % (username, password)
        db.insert(sql)
        flash('Register success', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():  # put application's code here
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        sql = 'select * from users where username = %s' % username
        db = MysqlUtil()
        result = db.fetch_one(sql)
        if result:
            password = result["password"]
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username
                flash('Login success', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Password not match', 'danger')
                return render_template('login.html',error='Password not match')
        else:
            flash('User not found', 'danger')
            return render_template('register.html',error='User not found')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    db = MysqlUtil()
    sql = 'select * from users where username = %s' % session['username']
    result = db.fetch_all(sql)
    if result:
        return render_template('dashboard.html', users=result)
    else:
        return render_template('dashboard.html')
@app.route('/admin')
def admin():
    return 'Admin Page'

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 3306
    debug = True
    app.run(host=host, port=port, debug=debug)
