from flask import Flask,request,redirect,url_for,render_template,flash,session,send_file
from flask_session import Session
from otp import genotp
from cmail import sendmail
from stoken import endata,dndata
import mysql.connector
import flask_excel as excel
from io import BytesIO
import re
mydb=mysql.connector.connect(user='root',password='Bindu@123',host='localhost',db='snm')
app=Flask(__name__)
excel.init_excel(app)     #initialization method
app.config['SESSION_TYPE']='filesystem'  # Session data stored in local files.
Session(app)
app.secret_key='stephen'   # flash message security
@app.route('/')
def home():
    return render_template('welcome.html')
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=request.form['name']
        useremail=request.form['email']
        userpassword=request.form['password']
        try:
            cursor=mydb.cursor()
            cursor.execute('select count(useremail) from userdata where useremail=%s',[useremail])
            count_email=cursor.fetchone()
            cursor.close()
        except Exception as e:
            print(e)
            flash('Could not verify email')
            return redirect(url_for('register'))
        else:
            if count_email[0]==0:            # new user means new email
                gotp=genotp()
                userdata={'username':username,'useremail':useremail,'userpassword':userpassword,'server_otp':gotp}
                subject=f"SNM APP VERIFICATION"
                body=f"Use this OTP for verification:{gotp}"
                sendmail(to=useremail,subject=subject,body=body)
                flash('The OTP has been send to given mail')
                return redirect(url_for('otpverification',serverdata=endata(userdata)))
            elif count_email[0]==1:
                flash('Email already exists')           
    return render_template('register.html')
@app.route('/otpverification/<serverdata>',methods=['GET','POST'])
def otpverification(serverdata):
    try:
        de_data=dndata(serverdata)
    except Exception as e:
        print(e)
        flash('Could not verify otp')
        return redirect(url_for('register'))
    else:
        if request.method=='POST':
            user_otp=request.form['otp']
            if user_otp==de_data['server_otp']:
                cursor=mydb.cursor()#it is mysql cursor created using mysqldb connection object
                cursor.execute('insert into userdata(username,useremail,userpassword) values(%s,%s,%s)',[de_data['username'],de_data['useremail'],de_data['userpassword']])
                mydb.commit()
                cursor.close()
                flash('Details registered successfully')
                return redirect(url_for('login'))
            else:
                flash('Invalid OTP')
                return redirect(url_for('otpverification',serverdata=serverdata))
        return render_template('otp.html')
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        login_useremail=request.form['email']
        login_password=request.form['password']
        try:
            cursor=mydb.cursor()
            cursor.execute('select count(useremail) from userdata where useremail=%s',[login_useremail])
            count_email=cursor.fetchone()
        except Exception as e:
            print(e)
            flash('could not verify your mail')
            return redirect(url_for('login'))
        else:
            if count_email[0]==1:
                cursor.execute('select userpassword from userdata where useremail=%s',[login_useremail])
                stored_password=cursor.fetchone()
                if stored_password[0]==login_password:
                    session['user']=login_useremail
                    flash('user logged in successfully')
                    return redirect(url_for('dashboard'))
                else:
                    flash('Password was wrong')
                    return redirect(url_for('login'))
            else:
                flash('Enter valid email for login')
                return redirect(url_for('login'))
    return render_template('login.html')
@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    return render_template('dashboard.html')
@app.route('/logout')
def logout():
    if session.get('user'):
        session.pop('user')
        return redirect(url_for('login'))
    else:
        flash('pls login to logout')
        return redirect(url_for('login'))
@app.route('/addnotes',methods=['GET','POST'])
def addnotes():
    if not session.get('user'):
        flash('pls login to addnotes')
        return redirect(url_for('login'))
    if request.method=='POST':
        title=request.form['title']
        description=request.form['description']
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
            user_id=cursor.fetchone()
            if user_id[0]:
                cursor.execute('insert into notesdata(notes_title,notes_description,userid) values(%s,%s,%s)',[title,description,user_id[0]])
                mydb.commit()
                cursor.close()
            else:
                flash('could not fetch user details')
                return redirect(url_for('addnotes'))
        except Exception as e:
            print(e)
            flash('Could not stored notes details')
            return redirect(url_for('addnotes'))
        else:
            flash('Notes added successfully')
            return redirect(url_for('addnotes'))
    return render_template('addnotes.html')
@app.route('/viewallnotes')
def viewallnotes():
    if not session.get('user'):
        flash('pls login to view all notes')
        return redirect(url_for('login'))
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
        user_id=cursor.fetchone()[0]
        cursor.execute('select notesid,notes_title,created_at from notesdata where userid=%s',[user_id])
        stored_allnotesdata=cursor.fetchall()
        print(stored_allnotesdata)
        cursor.close()
    except Exception as e:
        print(e)
        flash('Could not fetch notes details')
        return redirect(url_for('dashboard'))
    else:
        return render_template('viewallnotes.html',stored_allnotesdata=stored_allnotesdata)
@app.route('/viewnotes/<nid>')
def viewnotes(nid):
    if not session.get('user'):
        flash('pls login to view all notes')
        return redirect(url_for('login'))
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
        user_id=cursor.fetchone()[0]
        cursor.execute('select notesid,notes_title,notes_description,created_at from notesdata where userid=%s and notesid=%s',[user_id,nid])
        stored_notesdata=cursor.fetchone()
        print(stored_notesdata)
        cursor.close()
    except Exception as e:
        print(e)
        flash('Could not fetch notes details')
        return redirect(url_for('dashboard'))
    else:
        return render_template('viewnotes.html',stored_notesdata=stored_notesdata)
@app.route('/deletenotes/<nid>')
def deletenotes(nid):
    if not session.get('user'):
        flash('pls login to access to delete notes')
        return redirect(url_for('login'))
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
        user_id=cursor.fetchone()[0]
        cursor.execute('delete from notesdata where userid=%s and notesid=%s',[user_id,nid])
        mydb.commit()
        cursor.close()
    except Exception as e:
        print(e)
        flash('Could not delete notes')
        return redirect(url_for('dashboard'))
    else:
        flash('Notes successfully deleted')
        return redirect(url_for('viewallnotes'))
@app.route('/updatenotes/<nid>',methods=['GET','POST'])

def updatenotes(nid):
    if not session.get('user'):
        flash('pls login to access to update notes')
        return redirect(url_for('login'))
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
        user_id=cursor.fetchone()[0]
        cursor.execute('select notesid,notes_title,notes_description,created_at from notesdata where userid=%s and notesid=%s',[user_id,nid])
        stored_notesdata=cursor.fetchone()
        print(stored_notesdata)
        cursor.close()
    except Exception as e:
        print(e)
        flash('Could not fetch notes details')
        return redirect(url_for('viewallnotes'))
    else:
        if request.method=='POST':
            updated_title=request.form['title']
            updated_description=request.form['description']
            try:
                cursor=mydb.cursor(buffered=True)
                cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
                user_id=cursor.fetchone()
                if user_id[0]:
                    cursor.execute('update notesdata set notes_title=%s,notes_description=%s where userid=%s and notesid=%s',[updated_title,updated_description,user_id[0],nid])
                    mydb.commit()
                    cursor.close()
                else:
                    flash('could not fetch user details')
                    return redirect(url_for('updatednotes',nid=nid))
            except Exception as e:
                print(e)
                flash('Could not update notes details')
                return redirect(url_for('updatenotes',nid=nid))
            else:
                flash('Notes updates successfully')
                return redirect(url_for('updatenotes',nid=nid))   
        return render_template('updatenotes.html',stored_notesdata=stored_notesdata)
@app.route('/getexceldata')
def getexceldata():
    if not session.get('user'):
        flash('pls login to view all notes')
        return redirect(url_for('login'))
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
        user_id=cursor.fetchone()[0]
        cursor.execute('select notesid,notes_title,notes_description,created_at from notesdata where userid=%s',[user_id])
        stored_allnotesdata=cursor.fetchall()
        # print(stored_allnotesdata)
        cursor.close()
    except Exception as e:
        print(e)
        flash('Could not fetch notes details')
        return redirect(url_for('dashboard'))
    else:
        array_data=[list(i) for i in stored_allnotesdata]      #list of list we get data
        columns=['Notesid','NotesTitle','NotesDescription','Created_at']
        array_data.insert(0,columns)
        return excel.make_response_from_array(array_data,'xlsx',file_name='Allnotesdata')
        # return render_template('viewallnotes.html',stored_allnotesdata=stored_allnotesdata)
@app.route('/fileupload',methods=['GET','POST'])
def fileupload():
    if not session.get('user'):
        flash('pls login to access dashboard features')
        return redirect(url_for('userlogin'))
    if request.method=='POST':
        user_filedata=request.files['filedata']
        # print(user_filedata)
        fname=user_filedata.filename
        fdata=user_filedata.read()
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
            user_id=cursor.fetchone()[0]
            cursor.execute('insert into filesdata(filename,filedata,userid) values(%s,%s,%s)',[fname,fdata,user_id])
            mydb.commit()
            cursor.close()
        except Exception as e:
            print(e)
            flash('Could not store file details')
            return redirect(url_for('fileupload'))
        else:
            flash('File uploaded successfully')
    return render_template('fileupload.html')
@app.route('/viewallfiles')
def viewallfiles():
    if not session.get('user'):
        flash('pls login to view all files')
        return redirect(url_for('login'))
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
        user_id=cursor.fetchone()[0]
        cursor.execute('select filesid,filename,created_at from filesdata where userid=%s',[user_id])
        stored_allfilesdata=cursor.fetchall()
        #print(stored_allfilesdata)
        cursor.close()
    except Exception as e:
        print(e)
        flash('Could not fetch files details')
        return redirect(url_for('dashboard'))
    else:
        return render_template('viewallfiles.html',stored_allfilesdata=stored_allfilesdata)
@app.route('/deletefiles/<fid>')
def deletefiles(fid):
    if not session.get('user'):
        flash('pls login to access to delete files')
        return redirect(url_for('login'))
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
        user_id=cursor.fetchone()[0]
        cursor.execute('delete from filesdata where userid=%s and filesid=%s',[user_id,fid])
        mydb.commit()
        cursor.close()
    except Exception as e:
        print(e)
        flash('Could not delete files')
        return redirect(url_for('dashboard'))
    else:
        flash('File successfully deleted')
        return redirect(url_for('viewallfiles'))
@app.route('/viewfile/<fid>')
def viewfile(fid):
    if not session.get('user'):
        flash('pls login to view all files')
        return redirect(url_for('login'))
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
        user_id=cursor.fetchone()[0]
        cursor.execute('select filesid,filename,filedata,created_at from filesdata where userid=%s and filesid=%s',[user_id,fid])
        stored_filedata=cursor.fetchone()
        #print(stored_filedata)
        cursor.close()
    except Exception as e:
        print(e)
        flash('Could not fetch files details')
        return redirect(url_for('dashboard'))
    else:
        bytes_array=BytesIO(stored_filedata[2])
        return send_file(bytes_array,as_attachment=False,download_name=stored_filedata[1])
@app.route('/downloadfile/<fid>')
def downloadfile(fid):
    if not session.get('user'):
        flash('pls login to view all files')
        return redirect(url_for('login'))
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
        user_id=cursor.fetchone()[0]
        cursor.execute('select filesid,filename,filedata,created_at from filesdata where userid=%s and filesid=%s',[user_id,fid])
        stored_filedata=cursor.fetchone()
        #print(stored_filedata)
        cursor.close()
    except Exception as e:
        print(e)
        flash('Could not fetch files details')
        return redirect(url_for('dashboard'))
    else:
        bytes_array=BytesIO(stored_filedata[2])
        return send_file(bytes_array,as_attachment=True,download_name=stored_filedata[1])
@app.route('/searchdata',methods=['POST'])
def searchdata():
    if not session.get('user'):
        flash('pls login to asscess dashboard')
        return redirect(url_for('login'))
    try:
        user_search=request.form['search'] #'' or '      dssfef'
        strg=['A-Za-z0-9']
        pattern=re.compile(f'^{strg}',re.IGNORECASE)
        if pattern.match(user_search):
            try:
                cursor=mydb.cursor(buffered=True)
                cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
                user_id=cursor.fetchone()[0]
                cursor.execute('select notesid,notes_title,created_at from notesdata where (notesid like %s or notes_title like %s or created_at like %s or notes_description like %s) and userid=%s',[user_search+'%',user_search+'%',user_search+'%',user_search+'%',user_id])
                search_result=cursor.fetchall() 
                cursor.close()
            except Exception as e:
                print(e)
                flash('could not fetch search data pls check')
                return redirect(url_for('dashboard')) 
            else:
                return render_template('viewallnotes.html',stored_allnotesdata=search_result)            
        else:
            flash('Invalid search data pls check')
            return redirect(url_for('dashboard'))
    except Exception as e:
        print(e)
        flash('could check search data pls check')
        return redirect(url_for('dashboard'))
@app.route('/forgotpassword',methods=['GET','POST'])
def forgotpassword():
    if request.method=='POST':
        user_email=request.form['email']
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select count(*) from userdata where useremail=%s',[user_email])
            email_count=cursor.fetchone()
            cursor.close()
        except Exception as e:
            print(e)
            flash('Could not verify user')
            return redirect(url_for('login'))
        else:
            if email_count[0]==1:
                subject=f'Reset link for SNM forgotpassword'
                body=f"Use the given link for new password update{url_for('newpassword',useremail=endata(user_email),_external=True)}"
                sendmail(to=user_email,subject=subject,body=body)
                flash('Reset link has been sent to given email')
                return redirect(url_for('forgotpassword'))
            elif email_count[0]==0:
                flash('Email not registered pls check')
                return redirect(url_for('login'))
    return render_template('forgot.html')
@app.route('/newpassword/<useremail>',methods=['GET','PUT'])
def newpassword(useremail):
    try:
        forgot_email=dndata(useremail)
    except Exception as e:
        flash('Could not verify the email')
        return redirect(url_for('newpassword',useremail=useremail))
    else:
        if request.method=='PUT'
            new_password=request.get_json()['password']
            try:
                cursor=mydb.cursor(buffered=True)
                cursor.execute('update userdata set userpassword=%s where useremail=%s',[new_password,forgot_email])
                mydb.commit()
                cursor.clone()
            except Exception as e:
                print(e)
                flash('Could not update password')
                return redirect(url_for('newpassword',useremail=useremail))
            else:
                flash('password updated successfully')
                return jsonify({"message":"passwword updated successfully"})
        return render_template('newpassword.html')
app.run(use_reloader=True,debug=True)