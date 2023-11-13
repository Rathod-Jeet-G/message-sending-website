from flask import Flask, render_template, request, redirect, session
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

from flask_mysqldb import MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'singup'
mysql = MySQL(app)


@app.route("/")
def index():
    return render_template('signup.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/home")
def home():
    if((session["email"])!=False):
        return render_template('index.html')
    else:
        return render_template('login.html')

@app.route("/incoming_view")
def incoming_view():
    if((session["email"])!=False):
        with app.app_context():
            val = session['email']
            cursor = mysql.connection.cursor()
            cursor.execute('''SELECT * FROM message WHERE todata = %s ''',(val,))
            result = cursor.fetchall()
            cursor.close()
            print("ans",result)
            return render_template('view.html',data=result)
    else:
        return render_template('login.html')

@app.route("/sent-view")
def sent_view():
    if((session["email"])!=False):
        with app.app_context():
            val = session['email']
            cursor = mysql.connection.cursor()
            cursor.execute('''SELECT * FROM message WHERE fromdata = %s ''',(val,))
            result = cursor.fetchall()
            cursor.close()
            print("ans",result)
            return render_template('sent.html',data=result)
    else:
        return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    gender = request.form.get('gender')
    mo_no = request.form.get('mno')
    email = request.form.get('email')
    passw = request.form.get('pass')
    with app.app_context():
        cursor = mysql.connection.cursor()
       
        cursor.execute(
            '''INSERT INTO info(First_name,Last_name,gender,mobile_NO,email,pass) VALUES (%s,%s,%s,%s,%s,%s)''',
            (
                fname,lname,gender,mo_no,email,passw))
        mysql.connection.commit()
    return redirect('/login')


@app.route('/login-data', methods=['POST'])
def logindata():
    if request.method == 'POST':
        name = request.form.get('email')
        passw = request.form.get('pass')

        with app.app_context():
            cursor = mysql.connection.cursor()
            cursor.execute('''select count(*) from info where email = %s  and pass=%s''',(name,passw))
            if cursor.fetchall()[0][0]>=1:
                session['email'] = name
                return render_template("index.html")    
            
            return render_template('login.html')
            
                
      

@app.route("/msg",methods=['POST'])
def msg():
    from_m = request.form.get('from')
    to_m = request.form.get('to')
    msg_m = request.form.get('message')

    if(from_m!=session['email']):
        print("please enter your email id")
        return render_template('login.html')
    else:
        with app.app_context():
            cursor = mysql.connection.cursor()
        
            cursor.execute(
                '''INSERT INTO message(fromdata,todata,msg) VALUES (%s,%s,%s)''',
                (
                    from_m,to_m,msg_m))
            mysql.connection.commit()
    return redirect('/home')
        
    
@app.route("/logout")
def logout():
    session["email"] = False
    return redirect("/login")


if __name__ == '__main__':
    app.run(debug=True)
