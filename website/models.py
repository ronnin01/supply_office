from . import db
from sqlalchemy.sql import func

class ItemSetup(db.Model):
    IS_ItemNo = db.Column(db.Integer, primary_key=True)
    IS_SerialNo = db.Column(db.Integer)
    IS_ItemName = db.Column(db.String)
    IS_ItemDesc = db.Column(db.String)
    IS_CategoryNo = db.Column(db.Integer)
    IS_Brand = db.Column(db.String)
    IS_Model = db.Column(db.String)
    IS_Location = db.Column(db.Integer)
    IS_Department = db.Column(db.Integer)
    IS_Owner = db.Column(db.Integer)
    IS_Pic = db.Column(db.String)
    IS_DateAdded = db.Column(db.DateTime(timezone=True), default=func.now())
    IS_BegStock = db.Column(db.Integer)
    IS_Unit = db.Column(db.String)
    IS_UserNo = db.Column(db.Integer)

class UserTable(db.Model):
    UT_UserID = db.Column(db.Integer, primary_key=True)
    UT_IDNo = db.Column(db.Integer)
    UT_FirstName = db.Column(db.String)
    UT_LastName = db.Column(db.String)
    UT_MI = db.Column(db.String)
    UT_Contact = db.Column(db.Integer)
    UT_Email = db.Column(db.String)
    UT_Pic = db.Column(db.String)
    UT_Username = db.Column(db.String, unique=True)
    UT_Password = db.Column(db.String)
    UT_UserType = db.Column(db.String)
    UT_Designation = db.Column(db.String)
    UT_Department = db.Column(db.String)

