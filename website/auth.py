from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
#from .models import Itemsetup, Usertable, Category, Brand, Location, Department
#from . import db, app, photos
#from . import db
from .__init__ import connection
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os.path
import random
import json

auth = Blueprint('auth', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        #cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        conn = connection()
        cur = conn.cursor()
        cur.execute("Select UT_UserID, UT_Email, UT_Password, UT_UserType, UT_Pic From usertable where UT_email = '" + email + "'")
        user = cur.fetchone()
        #user = Usertable.query.filter_by(UT_Email=email).first()
        cur.close()
        if(user):
            #if(user.UT_Password == password):
            if check_password_hash(user.UT_Password, password):
                session['email'] = user.UT_Email
                session['userno'] = user.UT_UserID
                session['user_image'] = user.UT_Pic
                session['user_type'] = user.UT_UserType
                if user.UT_UserType == "Student":
                    return redirect(url_for('auth.student_index_page'))
                else:
                    return redirect(url_for('auth.admin_dashboard'))
            else:
                flash("Incorrect Password", category='error')
        else:
            flash('Email Add does not exist', category='error')

    return render_template('signin.html')

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@auth.route('/signout')
def signout():
    session.clear()
    return redirect(url_for('auth.signin'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    conn = connection()
    cur = conn.cursor()
    #item = Itemsetup.query.all()
    #cur = db.connection.cursor(MySQLdb.cursors.DictCursor)


    cur.execute("Select Des_Title, Des_ID from Designation order by Des_Title")
    designation = cur.fetchall()

    cur.execute("Select Dept_No, Dept_Name from Department order by Dept_Name")
    department = cur.fetchall()
    ut_usertype = request.form.get('ut_usertype')
    if request.method == "POST":

        ut_idno = request.form.get('ut_idno')
        ut_pic = request.files.get('ut_pic')
        ut_firstname = request.form.get('ut_firstname')
        ut_lastname = request.form.get('ut_lastname')
        ut_mi = request.form.get('ut_mi')
        ut_designation = request.form.get('ut_designation')
        ut_department = request.form.get('ut_department')
        ut_email = request.form.get('ut_email')
        ut_contact = request.form.get('ut_contact')
        ut_username = request.form.get('ut_username')
        ut_password = request.form.get('ut_password')
        ut_confirm_password = request.form.get('ut_confirm_password')
        
        
        if len(ut_password) < 6:
            flash('Password must be 6 above length', category='error')
        elif ut_password != ut_confirm_password:
            flash('Password is not match', category='error')
        elif not(ut_pic):
            conn = connection()
            cur = conn.cursor()
            cur.execute("Select UT_Email from usertable where UT_email = '" + ut_email + "'")
            data = cur.fetchone()
            #cur.close()
            if data:
                flash('Email already exist.', category='error')
            else:

                filename = secure_filename("defaultProf.png")
                ut_pic.save(os.path.join('D:/Private/CIT Masteral files/Capstone 1 and 2 References/Capstone 2 files/requisition/website/static/uploads', filename))
            #ut_pic.save(os.path.join('C:/Users/Aaron Fulgar/Desktop/requisition/website/static/uploads', filename))
                
               
                #conn = connection()
                #cur = conn.cursor()
                cur.execute("INSERT INTO UserTable (UT_IDno, UT_LastName, UT_FirstName, UT_MI, UT_Contact, UT_Email,UT_Username, UT_Designation, UT_Password, UT_Pic, UT_Department, UT_Usertype) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",ut_idno, ut_lastname,ut_firstname, 
                ut_mi, ut_contact, ut_email,ut_username, ut_designation, generate_password_hash(ut_password, method='sha256'),filename,ut_department,ut_usertype)
                #db.connection.commit()
                conn.commit()
                conn.close()
                flash("You have been registered." ,category='success')

                return redirect(url_for('auth.signin'))
        elif ut_pic and allowed_file(ut_pic.filename):
        #else:
            #cur = db.connection.cursor()
            conn = connection()
            cur = conn.cursor()
            cur.execute("Select UT_Email from usertable where UT_email = '" + ut_email + "'")
            data = cur.fetchone()
            #cur.close()
            if data:
                flash('Email already exist.', category='error')
            else:

                filename = secure_filename(ut_pic.filename)
                ut_pic.save(os.path.join('D:/Private/CIT Masteral files/Capstone 1 and 2 References/Capstone 2 files/requisition/website/static/uploads', filename))
            #ut_pic.save(os.path.join('C:/Users/Aaron Fulgar/Desktop/requisition/website/static/uploads', filename))
                
               
                #conn = connection()
                #cur = conn.cursor()
                cur.execute("INSERT INTO UserTable (UT_IDno, UT_LastName, UT_FirstName, UT_MI, UT_Contact, UT_Email,UT_Username, UT_Designation, UT_Password, UT_Pic, UT_Department, UT_Usertype) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",ut_idno, ut_lastname,ut_firstname, 
                ut_mi, ut_contact, ut_email,ut_username, ut_designation, generate_password_hash(ut_password, method='sha256'),filename,ut_department,ut_usertype)
                #db.connection.commit()
                conn.commit()
                conn.close()
                flash("You have been registered.",category='success')

                return redirect(url_for('auth.signin'))
        else:
            flash("Image must be png or jpg.", category='error')
    if ut_usertype == 'Owner':
        return render_template('adminowneruser.html', departments=department, designations = designation)
    else:
        return render_template('signup.html', departments=department, designations = designation)

@auth.route('/', methods=['GET', 'POST'])
def student_index_page():
    if 'email' not in session:
        flash('Please login first', category='error')
        return redirect(url_for('auth.signin'))
    conn = connection()
    cur = conn.cursor()
    #item = Itemsetup.query.all()
    #cur = db.connection.cursor(MySQLdb.cursors.DictCursor)


    cur.execute("Select Cat_Name, Cat_Id from Category")
    cat = cur.fetchall()

    cur.execute("Select IS_ItemNo, IS_ItemName, IS_ItemDesc, IS_BegStock, Br_BrandName, IS_Condition, Loc_Name, IS_Model, IS_Pic, (UT_LastName + ', ' + UT_FirstName) as Name, \
    (Select ISNULL(sum(St_qty), 0) from Stocks where St_ItemNo = IS_ItemNo AND St_Mode = 'Add') as AddStock, \
    (Select ISNULL(sum(St_qty), 0) from Stocks where St_ItemNo = IS_ItemNo AND St_Mode = 'Del')  as DelStock, \
    (Select ISNULL(sum(TD_qty), 0) from TransDetail where TD_ItemNo = IS_ItemNo AND TD_Status IN(0,1,2,3))  as BorStock, \
    (Select ISNULL(sum(TD_qty), 0) from TransDetail where TD_ItemNo = IS_ItemNo AND TD_Status IN(4,5,6))  as RetStock \
    from ItemSetup left join Brand on ItemSetup.IS_Brand = Brand.Br_BrandId \
    left join Location on ItemSetup.IS_Location = Location.Loc_No \
    left join Department on ItemSetup.IS_Department = Department.Dept_No \
    left join Usertable on ItemSetup.IS_Owner = Usertable.UT_UserID \
    order by IS_DateAdded desc")
    item = cur.fetchall()

    
    cur.close()

        # return redirect(url_for('auth.signin'))
        #return render_template('index.html', data=0)
    return render_template('student_index_page.html', items=item, cat=cat)




@auth.route('/admin/item/add/cat', methods=['GET', 'POST'])
def addcat():
    if 'email' not in session:
        flash('Please login first', category='error')
        return redirect(url_for('auth.signin'))

    conn = connection()
    cur = conn.cursor()
    
    
    cur.execute("Select * from Brand order by Br_BrandName")
    brand = cur.fetchall()
        
    
    cur.execute("Select * from Category order by Cat_Name")
    category = cur.fetchall()

    cur.execute("Select Distinct UT_LastName, UT_FirstName, UT_UserID from UserTable where UT_UserType <> 'Student' order by UT_LastName")
    user = cur.fetchall()

    cur.execute("Select * from Location order by Loc_Name")
    location = cur.fetchall()

    cur.execute("Select Dept_No, Dept_Name from Department order by Dept_Name")
    department = cur.fetchall()

    if request.method == 'POST':
        catname = str(request.form.get('txtAddCat'))
        cur.execute("INSERT INTO Category (Cat_Name) VALUES (?)",(catname))
        conn.commit()
        conn.close()
        flash("New Category Added to database", category="success")
        return redirect(url_for('auth.admin_item_entry'))
    flash("POST was not excuted", category="error")    
    return render_template('additem.html', brands = brand, categories = category, users = user, locations=location, departments=department)
    


@auth.route('/admin/item/add', methods=['GET', 'POST'])
def admin_item_entry():
    if 'email' not in session:
        flash('Please login first', category='error')
        return redirect(url_for('auth.signin'))
    conn = connection()
    cur = conn.cursor()
    #if session['item'] == 'add':
        #brands = Brand.query.all()
        #cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        #cur = db.connection.cursor()
        
    cur.execute("Select * from Brand order by Br_BrandName")
    brand = cur.fetchall()
        
        #categories = Category.query.all()
        #cur = db.connection.cursor()
    cur.execute("Select * from Category order by Cat_Name")
    category = cur.fetchall()

        #user = Usertable.query.all()
        #cur = db.connection.cursor()
    if session['user_type'] == 'Admin':
        cur.execute("Select Distinct UT_LastName, UT_FirstName, UT_UserID from UserTable where UT_UserType = 'Owner' order by UT_LastName")
    else:
        cur.execute("Select Distinct UT_LastName, UT_FirstName, UT_UserID from UserTable where UT_UserID = ? order by UT_LastName",(session['userno']))
    
    user = cur.fetchall()

        #location = Location.query.all()
        #cur = db.connection.cursor()
    cur.execute("Select * from Location order by Loc_Name")
    location = cur.fetchall()

        #department = Department.query.all()
        #cur = db.connection.cursor()
    cur.execute("Select Dept_No, Dept_Name from Department order by Dept_Name")
    department = cur.fetchall()

    if request.method == 'POST':
        IS_ItemName = request.form.get('txtItemName')
        IS_SerialNo = request.form.get('txtSerial')
        IS_ItemDesc = request.form.get('txtItemDesc')
        IS_CategoryNo = request.form.get('txtCategory')
        IS_Brand = request.form.get('txtBrand')
        IS_Model = request.form.get('txtModel')
        IS_Location = request.form.get('txtLocation')
        IS_Department = request.form.get('txtDepartment')
        IS_Owner = request.form.get('txtOwner')
        IS_BegStock = request.form.get('txtStocks')
        IS_Unit = request.form.get('txtUnit')
        IS_Pic = request.files.get('imgItem')
        IS_Condition = request.form.get('txtCondition')
        #IS_UserNo = request.form.get('txtUserNo')
        if IS_Pic and allowed_file(IS_Pic.filename):
        #else:
            filename = secure_filename(IS_Pic.filename)

            IS_Pic.save(os.path.join('D:/Private/CIT Masteral files/Capstone 1 and 2 References/Capstone 2 files/requisition/website/static/uploads', filename))
           
            conn = connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO ItemSetup (IS_ItemName, IS_SerialNo, IS_ItemDesc, IS_CategoryNo, IS_Brand, IS_Model,IS_Location, IS_Department, IS_Owner, IS_BegStock, IS_Unit,IS_Pic,IS_Condition, IS_DateAdded, IS_UserNo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,GETDATE(),?)",(IS_ItemName, IS_SerialNo,IS_ItemDesc, 
            IS_CategoryNo, IS_Brand, IS_Model, IS_Location, IS_Department, IS_Owner, IS_BegStock,IS_Unit,filename,IS_Condition,session['userno']))
            conn.commit()
            conn.close()
                #db.connection.commit()
            flash("New Item Added to database", category="success")
            return redirect(url_for('auth.admin_item_all'))
        else:
            flash("Image must be png or jpg.", category='error')
    return render_template('additem.html', brands = brand, categories = category, users = user, locations=location, departments=department)
    
@auth.route('/admin/items/update/<string:id_data>', methods=['GET', 'POST'])
def admin_item_update(id_data):
    if 'email' not in session:
        flash('Please login first', category='error')
        return redirect(url_for('auth.signin'))
    conn = connection()
    cur = conn.cursor()

    cur.execute("Select * from Brand order by Br_BrandName")
    brand = cur.fetchall()

    cur.execute("Select * from Category order by Cat_Name")
    category = cur.fetchall()

    if session['user_type'] == 'Admin':
        cur.execute("Select Distinct UT_LastName, UT_FirstName, UT_UserID from UserTable where UT_UserType = 'Owner' order by UT_LastName")
    else:
        cur.execute("Select Distinct UT_LastName, UT_FirstName, UT_UserID from UserTable where UT_UserID = ? order by UT_LastName",(session['userno']))
    
    user = cur.fetchall()


    cur.execute("Select * from Location order by Loc_Name")
    location = cur.fetchall()

    cur.execute("Select Dept_No, Dept_Name from Department order by Dept_Name")
    department = cur.fetchall()
    cur.execute("Select * from ItemSetup left join Brand on ItemSetup.IS_Brand = Brand.Br_BrandId \
        left join Category on ItemSetup.IS_CategoryNo = Category.Cat_ID \
        left join Location on ItemSetup.IS_Location = Location.Loc_No \
        left join Department on ItemSetup.IS_Department = Department.Dept_No \
        left join Usertable on ItemSetup.IS_Owner = Usertable.UT_UserID \
        where IS_ItemNo = " + id_data )
    item = cur.fetchone()
    cur.close()
    if request.method == 'POST':
        

        IS_ItemNo = request.form.get('txtItemNo')
        IS_ItemName = request.form.get('txtItemName')
        IS_SerialNo = request.form.get('txtSerial')
        IS_ItemDesc = request.form.get('txtItemDesc')
        IS_CategoryNo = request.form.get('txtCategory')
        IS_Brand = request.form.get('txtBrand')
        IS_Model = request.form.get('txtModel')
        IS_Location = request.form.get('txtLocation')
        IS_Department = request.form.get('txtDepartment')
        IS_Owner = request.form.get('txtOwner')
        IS_BegStock = request.form.get('txtStocks')
        IS_Unit = request.form.get('txtUnit')
        IS_Pic = request.files.get('imgItem')
        IS_Condition = request.form.get('txtCondition')
     
        #IS_UserNo = request.form.get('txtUserNo')
        if IS_Pic and allowed_file(IS_Pic.filename):
        #else:
            filename = secure_filename(IS_Pic.filename)

            IS_Pic.save(os.path.join('D:/Private/CIT Masteral files/Capstone 1 and 2 References/Capstone 2 files/requisition/website/static/uploads', filename))
            #photos.save(request.files.get('imgItem'))

            
            conn = connection()
            cur = conn.cursor()
            
            
            cur.execute("Update ItemSetup set IS_ItemName = ?, IS_SerialNo = ?, IS_ItemDesc = ?, IS_CategoryNo = ?, IS_Brand  = ?, IS_Model = ?, IS_Location = ?, IS_Department = ?, IS_Owner = ?, IS_Unit = ?, IS_Pic = ?, IS_Condition = ?, IS_DateAdded = GETDATE(), IS_UserNo = ? where IS_ItemNo = " + id_data,(IS_ItemName, IS_SerialNo,IS_ItemDesc, 
            IS_CategoryNo, IS_Brand, IS_Model, IS_Location, IS_Department, IS_Owner,IS_Unit,filename,IS_Condition, session['userno']))
            conn.commit()
            conn.close()
                #db.connection.commit()
            flash("Item Details Updated", category="success")
            return redirect(url_for('auth.admin_item_all'))

        else:
            flash("Image must be png or jpg.", category='error')
    return render_template('updateitem.html', brands = brand, categories = category, users = user, locations=location, departments=department, item = item)
    
@auth.route('/admin/items/all', methods=['GET', 'POST'])
def admin_item_all():
    if 'email' not in session:
        flash('Please login first', category='error')
        return redirect(url_for('auth.signin'))
    conn = connection()
    cur = conn.cursor()
    #item = Itemsetup.query.all()
    #cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    if session['user_type'] == 'Admin':
        cur.execute("Select *, (Select ISNULL(sum(St_qty), 0) from Stocks where St_ItemNo = IS_ItemNo AND St_Mode = 'Add') as AddStock, \
        (Select ISNULL(sum(St_qty), 0) from Stocks where St_ItemNo = IS_ItemNo AND St_Mode = 'Del')  as DelStock, \
        (Select ISNULL(sum(TD_qty), 0) from TransDetail where TD_ItemNo = IS_ItemNo AND TD_Status IN(0,1,2,3))  as BorStock, \
        (Select ISNULL(sum(TD_qty), 0) from TransDetail where TD_ItemNo = IS_ItemNo AND TD_Status IN(4,5,6))  as RetStock \
        from ItemSetup left join Brand on ItemSetup.IS_Brand = Brand.Br_BrandId \
        left join Category on ItemSetup.IS_CategoryNo = Category.Cat_ID \
        left join Location on ItemSetup.IS_Location = Location.Loc_No \
        left join Department on ItemSetup.IS_Department = Department.Dept_No \
        left join Usertable on ItemSetup.IS_Owner = Usertable.UT_UserID \
        order by IS_DateAdded desc")
    else:
        cur.execute("Select *, (Select ISNULL(sum(St_qty), 0) from Stocks where St_ItemNo = IS_ItemNo AND St_Mode = 'Add') as AddStock, \
        (Select ISNULL(sum(St_qty), 0) from Stocks where St_ItemNo = IS_ItemNo AND St_Mode = 'Del')  as DelStock, \
        (Select ISNULL(sum(TD_qty), 0) from TransDetail where TD_ItemNo = IS_ItemNo AND TD_Status IN(0,1,2,3))  as BorStock, \
        (Select ISNULL(sum(TD_qty), 0) from TransDetail where TD_ItemNo = IS_ItemNo AND TD_Status IN(4,5,6))  as RetStock \
        from ItemSetup left join Brand on ItemSetup.IS_Brand = Brand.Br_BrandId \
        left join Category on ItemSetup.IS_CategoryNo = Category.Cat_ID \
        left join Location on ItemSetup.IS_Location = Location.Loc_No \
        left join Department on ItemSetup.IS_Department = Department.Dept_No \
        left join Usertable on ItemSetup.IS_Owner = Usertable.UT_UserID \
        where UT_UserID = ? order by IS_DateAdded desc",(session['userno']))
        
    item = cur.fetchall()

    cur.execute("Select TD_TransN, (UT_FirstName + ' ' + UT_LastName) as Name, UT_Pic, IS_ItemName from TransDetail left join TransHeader on TransDetail.TD_THNO = TransHeader.TH_ID left join ItemSetup on TransDetail.TD_ItemNo = ItemSetup.IS_ItemNo left Join UserTable on TransHeader.TH_UserNo = UserTable.UT_UserID where TD_Status = '0' AND IS_Owner = ?",(session['userno']))
    Notification = cur.fetchall()
    
    cur.execute("Select (count(IS_ItemNo)) as cntItem from TransDetail left join TransHeader on TransDetail.TD_THNO = TransHeader.TH_ID left join ItemSetup on TransDetail.TD_ItemNo = ItemSetup.IS_ItemNo left Join UserTable on TransHeader.TH_UserNo = UserTable.UT_UserID where TD_Status = '0' AND IS_Owner = ?",(session['userno']))
    cntNotify = cur.fetchone()
    cur.close()

        # return redirect(url_for('auth.signin'))
        #return render_template('index.html', data=0)
    return render_template('index.html', items=item,ListNotify = Notification, cntItem=cntNotify)
    

@auth.route('/admin/item/borrow', methods=['GET', 'POST'])
def admin_item_borrow():
    if 'email' not in session:
        flash('Please login first', category='error')
        return redirect(url_for('auth.signin'))
    conn = connection()
    cur = conn.cursor()
    
    #item = Itemsetup.query.all()
    #cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("Select * from ItemSetup left join Brand on ItemSetup.IS_Brand = Brand.Br_BrandId \
    left join Category on ItemSetup.IS_CategoryNo = Category.Cat_ID \
    left join Location on ItemSetup.IS_Location = Location.Loc_No \
    left join Department on ItemSetup.IS_Department = Department.Dept_No \
    left join Usertable on ItemSetup.IS_Owner = Usertable.UT_UserID \
    where BR_Brandname = 'Canon' order by IS_DateAdded desc")
    item = cur.fetchall()
    conn.close()

        # return redirect(url_for('auth.signin'))
        #return render_template('index.html', data=0)
    return render_template('index.html', items=item)

@auth.route('/admin/items/delete/<string:id_data>', methods=['GET'])
def admin_item_delete(id_data):
    if 'email' not in session:
        flash('Please login first', category='error')
        return redirect(url_for('auth.signin'))
    conn = connection()
    conn = connection()
    cur = conn.cursor()
    
    cur.execute("Delete from ItemSetup where IS_ItemNo = " + id_data)
    conn.commit()
    conn.close()

    return redirect(url_for('auth.admin_item_all'))

@auth.route('/categoryadd', methods=['POST'])
def categoryadd():
    if request.method == "POST":
        conn = connection()
        cur = conn.cursor()

        cur.execute("INSERT INTO Category(Cat_Name, Cat_Desc) VALUES(?,?)", (request.form.get('txtAddCat'),request.form.get('txtCatDesc')))

        conn.commit()
        conn.close()

        flash("New Category Added to database", category="success")
        return redirect(url_for('auth.admin_item_entry'))
@auth.route('/brandadd', methods=['POST'])
def brandadd():
    if request.method == "POST":
        conn = connection()
        cur = conn.cursor()

        cur.execute("INSERT INTO Brand(Br_BrandName) VALUES(?)", request.form.get('txtAddBrand'))

        conn.commit()
        conn.close()

        flash("New Brand Added to database", category="success")
        return redirect(url_for('auth.admin_item_entry'))

@auth.route('/departmentadd', methods=['POST'])
def departmentadd():
    if request.method == "POST":
        conn = connection()
        cur = conn.cursor()

        cur.execute("INSERT INTO Department(Dept_Name, Dep_Desc) VALUES(?,?)", (request.form.get('txtAddDeptName'),request.form.get('txtDeptDesc')))

        conn.commit()
        conn.close()

        flash("New Department Added to database", category="success")
        return redirect(url_for('auth.admin_item_entry'))
    
@auth.route('/locationadd', methods=['POST'])
def locationadd():
    if request.method == "POST":
        conn = connection()
        cur = conn.cursor()

        cur.execute("INSERT INTO Location(Loc_Name, Loc_Desc) VALUES(?,?)", (request.form.get('txtAddLocName'),request.form.get('txtLocDesc')))

        conn.commit()
        conn.close()

        flash("New Location Added to database", category="success")
        return redirect(url_for('auth.admin_item_entry'))

@auth.route('/editstock', methods=['POST'])
def editstock():
    if request.method == "POST":
        conn = connection()
        cur = conn.cursor()
        itemno = request.form.get('txtNo')
        Stat = request.form.get('txtStat')
        Qty = request.form.get('txtstock') 
        userno = session['userno']
        if (Stat == 'Add'):
            cur.execute("INSERT INTO STOCKS(St_ItemNo, St_Mode, St_Qty, St_UserNo,St_Date) VALUES(?,?,?,?,GETDATE())", (itemno,Stat,Qty,userno))
        else:
            cur.execute("INSERT INTO STOCKS(St_ItemNo, St_Mode, St_Qty, St_UserNo,St_Date) VALUES(?,?,?,?,GETDATE())", (itemno,Stat,Qty,userno))
        conn.commit()
        conn.close()

        flash("New Stocks Added to database", category="success")
        return redirect(url_for('auth.admin_item_all'))
@auth.route('/delstock', methods=['POST'])
def delstock():
    if request.method == "POST":
        conn = connection()
        cur = conn.cursor()

        cur.execute("INSERT INTO Location(Loc_Name, Loc_Desc) VALUES(?,?)", (request.form.get('txtAddLocName'),request.form.get('txtLocDesc')))

        conn.commit()
        conn.close()

        flash("New Location Added to database", category="success")
        return redirect(url_for('auth.admin_item_entry'))
    

@auth.route('/singleitem', methods=['GET', 'POST'])
def singleitem():
    if 'email' not in session:
        flash('Please login first', category='error')
        return redirect(url_for('auth.signin'))
    conn = connection()
    cur = conn.cursor()

    cur.execute("Select IS_ItemNo, IS_ItemName, IS_ItemDesc, IS_BegStock, Br_BrandName, IS_Condition, Loc_Name, IS_Model, IS_Pic, (UT_LastName + ', ' + UT_FirstName) as Name, \
    (Select ISNULL(sum(St_qty), 0) from Stocks where St_ItemNo = IS_ItemNo AND St_Mode = 'Add') as AddStock, \
    (Select ISNULL(sum(St_qty), 0) from Stocks where St_ItemNo = IS_ItemNo AND St_Mode = 'Del')  as DelStock, \
    (Select ISNULL(sum(TD_qty), 0) from TransDetail where TD_ItemNo = IS_ItemNo AND TD_Status IN(0,1,2,3))  as BorStock, \
    (Select ISNULL(sum(TD_qty), 0) from TransDetail where TD_ItemNo = IS_ItemNo AND TD_Status IN(4,5,6))  as RetStock \
    from ItemSetup left join Brand on ItemSetup.IS_Brand = Brand.Br_BrandId \
    left join Location on ItemSetup.IS_Location = Location.Loc_No \
    left join Department on ItemSetup.IS_Department = Department.Dept_No \
    left join Usertable on ItemSetup.IS_Owner = Usertable.UT_UserID \
    where IS_ItemNo = " + request.form.get('item_id') )
    item = cur.fetchone()
    
    if request.method == 'POST':
        cur.execute("Select TH_No from LastTH")
        th = cur.fetchone()
        if th:
            THNo = int(th.TH_No) + 1
        else:
            THNo = 1
        userno = session['userno']
        cur.execute("INSERT INTO TransHeader(TH_UserNo, TH_TransDate) VALUES(?,GETDATE())", (userno))
        conn.commit()
        ItemNo = request.form.get('txtBItemNo')
        Qty = request.form.get('txtBQty')
        cur.execute("INSERT INTO TransDetail(TD_THNo, TD_ItemNo, TD_Qty, TD_DateBorrowed, TD_Status, TD_Receivedby) VALUES(?,?,?,GETDATE(),0,1)", (THNo, request.form.get('item_id'), request.form.get('item_quantity') ))
        conn.commit()
        if th:
            cur.execute("Update LastTH set TH_No = ?", THNo)
            conn.commit()
        else:
            cur.execute("INSERT INTO LastTH(TH_No) VALUES(?)", (THNo))
            conn.commit()
        conn.close()
            #db.connection.commit()
        
        return jsonify({
            "message": "Item Borrowed Successfully."
        })  

    
    return render_template('single_item.html', item = item)


@auth.route('/admin/owner/user', methods=['GET'])
def add_user_owner():
    conn = connection()
    cur = conn.cursor()
    #item = Itemsetup.query.all()
    #cur = db.connection.cursor(MySQLdb.cursors.DictCursor)


    cur.execute("Select Des_Title, Des_ID from Designation order by Des_Title")
    designation = cur.fetchall()

    cur.execute("Select Dept_No, Dept_Name from Department order by Dept_Name")
    department = cur.fetchall()
    return render_template('adminowneruser.html', designations = designation, departments = department)

@auth.route('/admin/dashboard')
def admin_dashboard():

    return render_template('dashboard.html')

# GET BRAND AJAX
@auth.route('/get/brand/ajax', methods=['GET', 'POST'])
def get_brand_ajax():
    conn = connection()
    cur = conn.cursor()

    if request.method == "POST":
        cur.execute("INSERT INTO Brand(Br_BrandName) VALUES(?)", request.form.get('brand_data'))

    cur.execute("Select * from Brand order by Br_BrandName")
    brands= cur.fetchall()

    data = []

    for brands_data in brands:
        brand_data = {
            "brand_id": brands_data.Br_BrandID,
            "brand_name": brands_data.Br_BrandName
        }
        data.append(brand_data)

    conn.commit();
    return jsonify(data)
    
# GET CATEGORY AJAX
@auth.route('/get/category/ajax', methods=['GET', 'POST'])
def get_category_ajax():
    conn = connection()
    cur = conn.cursor()

    if request.method == "POST":
        cur.execute("INSERT INTO Category(Cat_Name, Cat_Desc) VALUES(?,?)", (request.form.get('cat'),request.form.get('txtCatDesc')))

    cur.execute("Select * from Category order by Cat_Name")
    category = cur.fetchall()

    data = []

    for cat_data in category:
        datas = {
            "cat_id": cat_data.Cat_ID,
            "cat_name": cat_data.Cat_Name
        }
        data.append(datas)

    conn.commit()
    return jsonify(data)
# GET LOCATION AJAX
@auth.route('/get/location/ajax', methods=['GET', 'POST'])
def get_location_ajax():
    conn = connection()
    cur = conn.cursor()

    if request.method == "POST":
       cur.execute("INSERT INTO Location(Loc_Name, Loc_Desc) VALUES(?,?)", (request.form.get('loc'),request.form.get('txtLocDesc')))

    cur.execute("Select * from Location order by Loc_Name")
    location = cur.fetchall()

    data = []

    for loc_data in location:
        datas = {
            "loc_num": loc_data.Loc_No,
            "loc_name": loc_data.Loc_Name
        }
        data.append(datas)

    conn.commit()
    return jsonify(data)

# GET DEPARTMENT AJAX
@auth.route('/get/department/ajax', methods=['GET', 'POST'])
def get_department_ajax():
    conn = connection()
    cur = conn.cursor()

    if request.method == "POST":
        dept_add = cur.execute("INSERT INTO Department(Dept_Name, Dep_Desc) VALUES(?,?)", (request.form.get('dept'),request.form.get('txtDeptDesc')))


    cur.execute("Select Dept_No, Dept_Name from Department order by Dept_Name")
    department = cur.fetchall()

    data = []

    for dept_data in department:
        datas = {
            "dept_no": dept_data.Dept_No,
            "dept_name": dept_data.Dept_Name
        }
        data.append(datas)

    conn.commit()
    return jsonify(data)

# RETRIEVE DETAIL ITEM
@auth.route('/get/item/detail/borrow', methods=['POST'])
def get_item_detail_borrow():
    if request.method == "POST":

        conn = connection()
        cur = conn.cursor()

        cur.execute("Select IS_ItemNo, IS_ItemName, IS_ItemDesc, IS_BegStock, Br_BrandName, IS_Condition, Loc_Name, IS_Model, IS_Pic, (UT_LastName + ', ' + UT_FirstName) as Name, \
        (Select ISNULL(sum(St_qty), 0) from Stocks where St_ItemNo = IS_ItemNo AND St_Mode = 'Add') as AddStock, \
        (Select ISNULL(sum(St_qty), 0) from Stocks where St_ItemNo = IS_ItemNo AND St_Mode = 'Del')  as DelStock, \
        (Select ISNULL(sum(TD_qty), 0) from TransDetail where TD_ItemNo = IS_ItemNo AND TD_Status IN(0,1,2,3))  as BorStock, \
        (Select ISNULL(sum(TD_qty), 0) from TransDetail where TD_ItemNo = IS_ItemNo AND TD_Status IN(4,5,6))  as RetStock \
        from ItemSetup left join Brand on ItemSetup.IS_Brand = Brand.Br_BrandId \
        left join Location on ItemSetup.IS_Location = Location.Loc_No \
        left join Department on ItemSetup.IS_Department = Department.Dept_No \
        left join Usertable on ItemSetup.IS_Owner = Usertable.UT_UserID \
        where IS_ItemNo = " + request.form.get('item_id') )
        item = cur.fetchone()

        data = []

        datas = {
            "is_itemno": request.form.get('item_id'),
            "is_itemname": item.IS_ItemName,
            "is_itemdesc": item.IS_ItemDesc,
            "is_begstock": item.IS_BegStock,
            "br_brandname": item.Br_BrandName,
            "is_condition": item.IS_Condition,
            "loc_name": item.Loc_Name,
            "is_model": item.IS_Model,
            "is_pic": item.IS_Pic,
            "name": item.Name
        }
        data.append(datas)
            

        conn.commit()
        return jsonify(data)

# ON SEARCH AJAX CALL DATA
@auth.route('/get/on/search/data/items', methods=['POST'])
def get_on_search_data_items():
    if request.method == "POST":

        conn = connection()
        cur = conn.cursor()

        cur.execute("Select IS_ItemNo, IS_ItemName, IS_ItemDesc, IS_BegStock, Br_BrandName, IS_Condition, Loc_Name, IS_Model, IS_Pic, (UT_LastName + ', ' + UT_FirstName) as Name, \
        (Select ISNULL(sum(St_qty), 0) from Stocks where St_ItemNo = IS_ItemNo AND St_Mode = 'Add') as AddStock, \
        (Select ISNULL(sum(St_qty), 0) from Stocks where St_ItemNo = IS_ItemNo AND St_Mode = 'Del')  as DelStock, \
        (Select ISNULL(sum(TD_qty), 0) from TransDetail where TD_ItemNo = IS_ItemNo AND TD_Status IN(0,1,2,3))  as BorStock, \
        (Select ISNULL(sum(TD_qty), 0) from TransDetail where TD_ItemNo = IS_ItemNo AND TD_Status IN(4,5,6))  as RetStock \
        from ItemSetup left join Brand on ItemSetup.IS_Brand = Brand.Br_BrandId \
        left join Location on ItemSetup.IS_Location = Location.Loc_No \
        left join Department on ItemSetup.IS_Department = Department.Dept_No \
        left join Usertable on ItemSetup.IS_Owner = Usertable.UT_UserID \
        where IS_ItemName like '%"+request.form.get('input_search_data')+"%'")
        items = cur.fetchall()

        data = []

        for item in items:
            datas = {
                "is_itemno": item.IS_ItemNo,
                "is_itemname": item.IS_ItemName,
                "is_itemdesc": item.IS_ItemDesc,
                "is_begstock": item.IS_BegStock,
                "br_brandname": item.Br_BrandName,
                "is_condition": item.IS_Condition,
                "loc_name": item.Loc_Name,
                "is_model": item.IS_Model,
                "is_pic": item.IS_Pic,
                "name": item.Name
            }
            data.append(datas)
            

        conn.commit()
        return jsonify(data)

@auth.route('/get/borrows/notifications', methods=['GET'])
def get_borrows_notifications():
    conn = connection()
    cur = conn.cursor()

    cur.execute("Select TD_TransN, (UT_FirstName + ' ' + UT_LastName) as Name, UT_Pic, IS_ItemName from TransDetail left join TransHeader on TransDetail.TD_THNO = TransHeader.TH_ID left join ItemSetup on TransDetail.TD_ItemNo = ItemSetup.IS_ItemNo left Join UserTable on TransHeader.TH_UserNo = UserTable.UT_UserID where TD_Status = '0' AND IS_Owner = ?",(session['userno']))
    Notification = cur.fetchall()

    data = []

    for notif in Notification:
        datas = {
            "td_transn": notif.TD_TransN,
            "name": notif.Name,
            "ut_pic": notif.UT_Pic,
            "is_itemname": notif.IS_ItemName
        }
        data.append(datas)

    return jsonify(data)

@auth.route('/approve/borrow', methods=['POST'])
def approved_borrow():
    if request.method == "POST":
        conn = connection()
        cur = conn.cursor()

        cur.execute("UPDATE TransDetail set TD_Status = 6 WHERE TD_TransN = ?", (request.form.get('trans_id')))

        conn.commit()

        return jsonify({"message": "You approved the borrow."})

@auth.route("/decline/borrow", methods=['POST'])
def declined_borrow():
    if request.method == "POST":
        conn = connection()
        cur = conn.cursor()

        cur.execute("UPDATE TransDetail set TD_Status = 7 WHERE TD_TransN = ?", (request.form.get('trans_id')))

        conn.commit()

        return jsonify({"message": "You declined the borrow."})

# TOTAL USERS HEADER AJAX()
@auth.route('/total/users/header/ajax', methods=['GET'])
def total_users_header_ajax():
    conn = connection()
    cur = conn.cursor()
    
    cur.execute("SELECT (COUNT(UT_UserID)) as counted_user FROM UserTable")
    total_users = cur.fetchone()

    return jsonify({
        "total_user": total_users.counted_user
    })

# TOTAL UNRETURNED ITEMS HEADER AJAX
@auth.route('/total/unreturned/items/header/ajax', methods=['GET'])
def total_unreturned_items_ajax():
    conn = connection()
    cur = conn.cursor()
    
    cur.execute("Select (count(TD_TransN)) as counted_items from TransDetail left join TransHeader on TransDetail.TD_THNO = TransHeader.TH_ID left join ItemSetup on TransDetail.TD_ItemNo = ItemSetup.IS_ItemNo left Join UserTable on TransHeader.TH_UserNo = UserTable.UT_UserID where TD_Status = '6'")
    total_unreturned_items = cur.fetchone()

    return jsonify({
        "total_unreturned_item": total_unreturned_items.counted_items
    })

# TOTAL PENDING ITEMS HEADER AJAX
@auth.route('/total/pending/items/header/ajax', methods=['GET'])
def total_pending_items_header_ajax():
    conn = connection()
    cur = conn.cursor()
    
    cur.execute("Select (count(TD_TransN)) as counted_items from TransDetail left join TransHeader on TransDetail.TD_THNO = TransHeader.TH_ID left join ItemSetup on TransDetail.TD_ItemNo = ItemSetup.IS_ItemNo left Join UserTable on TransHeader.TH_UserNo = UserTable.UT_UserID where TD_Status = '0'")
    total_pending_items = cur.fetchone()

    return jsonify({
        "total_pending_item": total_pending_items.counted_items
    })

# TOTAL DECLINED ITEMS
@auth.route("/total/declined/items/header/ajax", methods=['GET'])
def total_declined_items_header_ajax():
    conn = connection()
    cur = conn.cursor()
    
    cur.execute("Select (count(TD_TransN)) as counted_items from TransDetail left join TransHeader on TransDetail.TD_THNO = TransHeader.TH_ID left join ItemSetup on TransDetail.TD_ItemNo = ItemSetup.IS_ItemNo left Join UserTable on TransHeader.TH_UserNo = UserTable.UT_UserID where TD_Status = '7'")
    total_declined_items = cur.fetchone()

    return jsonify({
        "total_declined_item": total_declined_items.counted_items
    })
