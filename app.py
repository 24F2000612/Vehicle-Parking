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
    return render_template('user_registration.html')



def intialize_admin():
    with app.app_context():
        if not User.query.filter_by(role='admin').first():
            admin = User(username='UDGHOSH',email=)


 


with app.app_context():
    db.create_all()

if __name__=='__main__':
    app.run(debug=True)
