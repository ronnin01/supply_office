from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import ItemSetup, UserTable
from . import db
from werkzeug.utils import secure_filename
import os
import random

auth = Blueprint('auth', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = UserTable.query.filter_by(UT_Username=username).first()

        if(user):
            if(user.UT_Password == password):
                return redirect(url_for('auth.student_index_page'))
            else:
                flash("Incorrect Password", category='error')
        else:
            flash('Incorrect Username', category='error')

        return redirect(url_for('auth.admin_item_entry'))
    else:
        return render_template('signin.html')

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":

        ut_idno = request.form['ut_idno']
        ut_pic = request.files.get('ut_pic')
        ut_firstname = request.form['ut_firstname']
        ut_lastname = request.form['ut_lastname']
        ut_mi = request.form['ut_mi']
        ut_email = request.form['ut_email']
        ut_contact = request.form['ut_contact']
        ut_username = request.form['ut_username']
        ut_password = request.form['ut_password']
        ut_confirm_password = request.form['ut_confirm_password']

        if len(ut_password) < 6:
            flash('Password must be 6 above length', category='error')
        elif ut_password != ut_confirm_password:
            flash('Password is not match', category='error')
        elif ut_pic and allowed_file(ut_pic.filename):
            
            filename = secure_filename(ut_pic.filename)
            # ut_pic.save(os.path.join(url_for('static', filename='uploads'), filename))

            new_user = UserTable(
                UT_UserID = "12350982341",
                UT_IDNo = ut_idno,
                UT_FirstName = ut_firstname,
                UT_LastName = ut_lastname,
                UT_MI = ut_mi,
                UT_Contact = ut_contact,
                UT_Email = ut_email,
                UT_Pic = "Profile.png",
                UT_Username = ut_username,
                UT_Password = ut_password,
                UT_UserType = "Student",
                UT_Designation = "Student",
                UT_Department = "COT",
            )
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('auth.signin'))

        else:
            flash("Image must be png or jpg.", category='error')

    return render_template('signup.html')

@auth.route('/', methods=['GET', 'POST'])
def student_index_page():
    return render_template('student_index_page.html')

@auth.route('/admin/item-entry', methods=['GET', 'POST'])
def admin_item_entry():
    if request.method == 'POST':
        id_number = request.form['is_itemno']

        new_item = ItemSetup(IS_ItemNo = id_number)
        db.session.add(new_item)
        db.session.commit()

        return 'hello'
    else:
        return render_template('index.html')