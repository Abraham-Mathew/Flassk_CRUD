#!/usr/bin/env python
# coding: utf-8

# In[6]:


from flask import Flask,render_template,request,redirect,url_for,flash
import sqlite3 as sql


# In[7]:


app=Flask(__name__)


# In[8]:


@app.route("/")
@app.route("/index")
def index():
    con=sql.connect("student.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from student")
    data=cur.fetchall()
    return render_template("index.html",datas=data)


# In[9]:


@app.route("/add_user",methods=['POST','GET'])
def add_user():
    if request.method=='POST':
        first_name=request.form['first_name']
        last_name=request.form['last_name']
        dob=request.form['dob']
        amount_due=request.form['amount_due']
        con=sql.connect("student.db")
        cur=con.cursor()
        cur.execute("insert into student(first_name,last_name,dob,amount_due) values (?,?,?,?)",(first_name,last_name,dob,amount_due))
        con.commit()
        flash('Student Added','success')
        return redirect(url_for("index"))
    return render_template("add_user.html")


# In[10]:


@app.route("/edit_user/<string:student_id>",methods=['POST','GET'])
def edit_user(student_id):
    if request.method=='POST':
        first_name=request.form['first_name']
        last_name=request.form['last_name']
        dob=request.form['dob']
        amount_due=request.form['amount_due']
        con=sql.connect("student.db")
        cur=con.cursor()
        cur.execute("update student set first_name=?,last_name=?,dob=?,amount_due=? where student_id=?",(first_name,last_name,dob,amount_due,student_id))
        con.commit()
        flash('Student Updated','success')
        return redirect(url_for("index"))
    con=sql.connect("student.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from student where student_id=?",(student_id,))
    data=cur.fetchone()
    return render_template("edit_user.html",datas=data)


# In[11]:


@app.route("/delete_user/<string:student_id>",methods=['GET'])
def delete_user(student_id):
    con=sql.connect("student.db")
    cur=con.cursor()
    cur.execute("delete from student where student_id=?",(student_id,))
    con.commit()
    flash('User Deleted','warning')
    return redirect(url_for("index"))


# In[ ]:


if __name__=='__main__':
    app.run()

