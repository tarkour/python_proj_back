from flask import Flask, render_template, request, redirect, url_for, session
from database_runner import *
import datetime
from datetime import timedelta

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
        if request.method == 'POST':

            message = request.form.get('message')
            # print(datetime.datetime.utcnow())
            di = db.query(Users).filter_by(name=login).all() # получение списка с содержанием Users(login)
            d = di[0] # получение самого Users(login)
            # print(d.get_id())
            # print(message)
            # print(datetime.datetime.utcnow())
            add_message = Messages(d.get_id(), message, datetime.datetime.utcnow())
            db.add(add_message)
            db.commit()


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
        print('login correct')

        if db.query(Passwords).filter(Passwords.password == password).all() != [] \
                and db.query(Users, Passwords).filter(Users.id == Passwords.user_id).filter(Users.name == login).filter(Passwords.password == password).all() != []:
            print('password correct')
            print('You are in!')

            session['login'] = login
            return redirect(url_for('messages'))

        else:
            print('wrong password')
    else:
        print('wrong login')




@app.route('/logout')
def logout():
    session.pop('login', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
