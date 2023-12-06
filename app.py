from flask import Flask, render_template, request, redirect, url_for, session, flash
from database_runner import *
import datetime
from datetime import timedelta
import requests

app = Flask(__name__)
app.secret_key = 'hello'
app.permanent_session_lifetime = timedelta(minutes=1)

@app.route('/main', methods=['GET', 'POST'])
def main():
    return render_template('index.html')

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     return 'hello, world??'


@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if 'login' in session:
        login = session['login']
        session.permanent = True
        all_messages = db.query(Messages).all()

        message = ''
        print('request.method = ', request.method)
        if request.method == 'POST' and message != None:

            message = request.form.get('message')

            di = db.query(Users).filter_by(name=login).all() # получение списка с содержанием Users(login)
            d = di[0] # получение самого Users(login)

            add_message = Messages(d.get_id(), message, datetime.datetime.utcnow())
            db.add(add_message)
            db.commit()
            # message = ''

            # response = requests.get('http://127.0.0.1:5000/messages')

            return redirect(url_for('messages'))

        return render_template('messages.html',
                               login=login,
                               all_messages=all_messages)

    else:
        return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    login = ''
    password = ''
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
    else:
        if 'login' in session:
            return redirect(url_for('messages'))
        return render_template('login.html')
    print(login, password)


    if db.query(Users).filter(Users.name == login).all() != []:
        login_user_id = db.query(Users).filter(Users.name == login).all()[0]
        login_user_id = login_user_id.get_id()
        passwords_user_id = db.query(Passwords).filter(Passwords.password == password).all() # получение всех списков, где пароль такой же, как мы ввели
                                                                                            # проверка делается на случай одинковых паролей в базе данных
        flag = False
        temp_pass = ''
        for p in passwords_user_id:

            if login_user_id == p.get_user_id(): # сравнение id у логина и user_id у пароля
                flag = True # если совпадает - флаг становится True
                temp_pass = p.get_pass()


        if flag == True and temp_pass == password:
            flash(f'You are in, {login}!')
            session['login'] = login
            return redirect(url_for('messages'))
        else:
            flash('wrong pass')
            return redirect(url_for('login'))

    else:
        flash('wrong login')
        return redirect(url_for('login'))





@app.route('/logout')
def logout():
    session.pop('login', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
