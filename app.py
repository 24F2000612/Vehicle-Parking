from flask import Flask , render_template , request , flash ,redirect , url_for , session 
from models import db , VehicleUser
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehicle_park.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db.init_app(app)

#define route
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register' ,methods =['GET','POST'])
def register():
    if request.method=='POST':
        Login_name = request.form['Login_name']
        Email_Address = request.form['Email_Address']
        Full_Name = request.form['Full_Name']
        User_Password = request.form['User_Password']
        Phone_Number = request.form['Phone_number']
        new_user = VehicleUser(Login_name=Login_name,User_Password=password,Email_Address=Email_Address,Phone_Number=Phone_Number,Full_Name=Full_Name,Role='user')

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! conglaturation','success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Registration failed : {str(e)}','danger')
            return redirect(url_for('register'))
    return render_template('user_registration.html')

@app.route('/login' ,methods=['GET','POST'])
def login():
    if request.method=='POST':
        Email_Address = request.form['Email_Address']
        User_Password = request.form['User_Password']
        user = VehicleUser.query.filter_by(Email_Address=Email_Address,User_Password=User_Password).first()
        if user:
            session['user_id'] = user.User_id
            session['user_name'] = user.Full_Name
            flash("Login Successful","success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials" , "Danger")
            return redirect(url_for('login'))
    return render_template('user_login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    
    user = VehicleUser.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect(url_for('home'))


def intialize_admin():
    with app.app_context():
        if not VehicleUser.query.filter_by(Login_name='admin').first():
            admin = VehicleUser(Login_name='admin',Email_Address="133@gmail.com",User_Password='123f', Phone_Number='1234567890',Role='admin')
            db.session.add(admin)
            db.session.commit()
            print("Admin created successfully!")


with app.app_context():
    db.create_all()
    intialize_admin()

if __name__=='__main__':
    app.run(debug=True)
