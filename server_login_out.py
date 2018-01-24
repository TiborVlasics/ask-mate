from flask import Blueprint, render_template, request, redirect, url_for, session
import data_manager, utility, user_handling
from datetime import datetime

login = Blueprint('login', __name__, template_folder='templates')


@login.route('/register', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        return render_template('registration.html')
    else:
        new_user_data={'user_name': request.form['user_name'],
                       'password': user_handling.hash_password(request.form['password']),
                       'registration_date': datetime.fromtimestamp(utility.display_unix_time()),
                       'email': request.form['email']}
        user_handling.new_user_to_db(new_user_data)
        return redirect('/')

@login.route('/', methods=['GET','POST'])
@login.route('/<error>', methods=['GET','POST'])
def login_check(error=None):
    if request.method == 'GET':
        if error:
            message = "Please log in to access this feature!"
        else:
            message = ""
        questions = data_manager.list_all_questions_ordered_by_submission_time()
        return render_template('register_login.html', questions=questions, message=message)
    else:
        hash = user_handling.get_password_hash_from_db(request.form['user_name'])
        verify = user_handling.verify_password(request.form['password'], hash['password'])
        if verify:
            session['user_id'] = hash['id']
            return redirect('/')
        else:
            message = 'Wrong user name or password'
            questions = data_manager.list_all_questions_ordered_by_submission_time()
            return render_template('register_login.html', questions=questions, message=message)


@login.route('/out')
def logout():
    session.pop('user_id')
    return redirect('/')