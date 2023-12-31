from flask import Flask, render_template, request, redirect, url_for, session, flash
from database_runner import *
import datetime
from datetime import timedelta


app = Flask(__name__)
app.secret_key = 'hello'
app.permanent_session_lifetime = timedelta(minutes=1)

@app.route('/main', methods=['GET', 'POST'])
def main():
    return render_template('index.html')

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
    # print(login, password)


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
            return redirect(url_for('messages_pagination', page_num=1))
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

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    login = ''
    password = ''
    repeat_password = ''
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        repeat_password = request.form.get('repeat_password')
    else:
        if 'login' in session:
            return redirect(url_for('messages_pagination', page_num=1))
        return render_template('registration.html')


    exist_login = db.query(Users).filter(Users.name == login).all()
    if exist_login != []:
        flash('This login has been taken already!')
        return render_template('registration.html')

    if password != repeat_password:
        flash('Passwords are not the same!')
        return render_template('registration.html')

    user_add = Users(login)
    db.add(user_add)
    db.commit()

    user_id = db.query(Users).filter_by(name=login).all()[0].get_id()

    pass_add = Passwords(user_id, password)
    db.add(pass_add)
    db.commit()  # не опасна ли такая схема добавления, если одновременных регистраций будет много? превратится в кашу или нет?

    flash('Your registration is successful')
    return redirect(url_for('messages_pagination', page_num=1))


@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if 'login' in session:
        login = session['login']
        session.permanent = True

        all_messages = db.query(Messages).all()

        message = ''
        if request.method == 'POST' and message != None:

            message = request.form.get('message')

            di = db.query(Users).filter_by(name=login).all() # получение списка с содержанием Users(login)
            d = di[0] # получение самого Users(login)

            add_message = Messages(d.get_id(), message, datetime.datetime.utcnow())
            db.add(add_message)
            db.commit()

            return redirect(url_for('messages_pagination'))

        return render_template('messages.html',
                               login=login,
                               all_messages=all_messages)

    else:
        return redirect(url_for('login'))

    page_num = 1
@app.route('/messages/page/<int:page_num>', methods=['GET', 'POST'])
def messages_pagination(page_num):

    if 'login' in session:
        login = session['login']
        session.permanent = True

        all_msg_count = db.query(Messages).count()
        if  all_msg_count == 0:
            return render_template('messages.html')
        messages_per_page = 10  # сколько сообщений на одной странице
        max_pages_count = all_msg_count // messages_per_page
        if all_msg_count % messages_per_page != 0:
            max_pages_count += 1

        if page_num > max_pages_count: #обработка случая, когда пользователь вводит в адерсную строку страницу,
                                       #превышающую максимальное количество страниц
            return redirect(url_for('messages_pagination', page_num=max_pages_count)) # В РЕДИРЕКТ НАДО ПИСАТЬ НАЗВАНИЕ ФУНКЦИИ, А НЕ ЕНДПОИНТ!!
        if page_num < 1: #обработка случая "0" в адресной строке
            return redirect(url_for('messages_pagination', page_num=1))

        all_msg = db.query(Messages).all()[::-1]
        msg_left = messages_per_page - (all_msg_count % messages_per_page)


        if page_num == max_pages_count: # берем массив сообщений нужного диапазона
            all_messages = all_msg[
                           page_num * messages_per_page - messages_per_page: page_num * messages_per_page - msg_left]
        else:
            all_messages = all_msg[page_num * messages_per_page - messages_per_page: page_num * messages_per_page]

        url = '/messages/page/'
        if page_num == 1:  # создание ссылки на страницу назад
            previuos = url + str(1)
        else:
            previuos = url + str(page_num - 1)

        if page_num == max_pages_count:  # создание ссылки на страницу вперед
            next = url + str(max_pages_count)
        else:
            next = url + str(page_num + 1)


        message = ''
        if request.method == 'POST' and message != None:
            message = request.form.get('message')

            user_id = db.query(Users).filter_by(name=login).all()[0].get_id()  # получение списка с содержанием Users(login)
                                                                               # получение самого Users(login) + получение user_id

            add_message = Messages(user_id, message, datetime.datetime.utcnow())

            db.add(add_message)
            db.commit()
            return redirect(url_for('messages_pagination', page_num=1))

        return render_template('messages.html', all_messages=all_messages,
                               previuos=previuos,
                               next=next,
                               page_num=page_num)

    else:
        return redirect(url_for('login'))




if __name__ == '__main__':
    app.run(debug=True)
