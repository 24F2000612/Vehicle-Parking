from flask import Flask , render_template , request , flash ,redirect , url_for , session 
from models import db, VehicleUser, ParkingLot, ParkingSpot, ParkingReservation
from datetime import datetime
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehicle_park.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db.init_app(app)

#define route
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        Login_name = request.form.get('Login_name')
        Full_Name = request.form.get('Full_Name')
        Email_Address = request.form.get('Email_Address')
        User_Password = request.form.get('User_Password')
        Phone_Number = request.form.get('Phone_Number')
        Address = request.form.get('Address')
        Pin_Code = request.form.get('Pin_Code')
        new_user = VehicleUser(
            Login_name=Login_name,
            Full_Name=Full_Name,
            Email_Address=Email_Address,
            User_Password=User_Password,
            Phone_Number=Phone_Number,
            Address=Address,
            Pin_Code=Pin_Code,
            Role='user'
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Registration failed: {str(e)}', 'danger')
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
            # Redirect admin to admin dashboard, regular users to user dashboard
            if user.Role == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
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
    lots = ParkingLot.query.all()
    return render_template('dashboard.html', user=user ,lots=lots)

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect(url_for('home'))

@app.route('/admin_dashboard')
def admin_dashboard():
     # Check if user is logged in
    if 'user_id' not in session:
        flash('Please log in first', 'warning')
        return redirect(url_for('login'))
    
    # Check if user is admin
    current_user = VehicleUser.query.get(session['user_id'])
    if not current_user or current_user.Role != 'admin':
        flash('Admin access required', 'danger')
        return redirect(url_for('login'))
    users = VehicleUser.query.all()
    lots = ParkingLot.query.all()
    spots = ParkingSpot.query.all()
    reservations = ParkingReservation.query.all()
    
    return render_template('admin_dashboard.html', 
                         users=users, 
                         lots=lots, 
                         spots=spots, 
                         reservations=reservations)

@app.route('/vehicle_edit_lot/<int:lot_id>', methods=['GET', 'POST'])
def edit_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    if request.method == 'POST':
        lot.Location_Name = request.form['Location_Name']
        lot.Address_name = request.form['Address_name']
        lot.PRICE = request.form['PRICE']
        lot.Maximum_Number_Spots = request.form['Maximum_Number_Spots']
        db.session.commit()
        flash('Parking lot updated!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('vehicle_edit_lot.html', lot=lot)

@app.route('/add_lot', methods=['GET', 'POST'])
def add_lot():
    user_id = session.get('user_id')
    user = VehicleUser.query.get(user_id)
    if not user or user.Role != 'admin':
        flash("Only admin can add parking lots.", "danger")
        return redirect(url_for('home'))

    if request.method == 'POST':
        print("Form submitted!")  # Debug
        Location_Name = request.form['Location_Name']
        Address_name = request.form['Address_name']
        PRICE = request.form['PRICE']
        Maximum_Number_Spots = request.form['Maximum_Number_Spots']
        print("Form data:", Location_Name, Address_name, PRICE, Maximum_Number_Spots)  # Debug
        new_lot = ParkingLot(
            Location_Name=Location_Name,
            Address_name=Address_name,
            PRICE=PRICE,
            Maximum_Number_Spots=Maximum_Number_Spots
        )
        db.session.add(new_lot)
        db.session.commit()
        print("Lot added to DB!")  # Debug
        flash('Parking lot added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('add_lot.html')

@app.route('/delete_lot/<int:lot_id>', methods=['POST'])
def delete_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    
    user_id = session.get('user_id')
    user = VehicleUser.query.get(user_id)
    if not user or user.Role != 'admin':
        flash("You don't have permission to delete this lot.", "danger")
        return redirect(url_for('home'))

    # Check if lot has any spots before deleting
    if lot.availabe_spots and len(lot.availabe_spots) > 0:
        flash("Cannot delete lot. It has parking spots.", "warning")
        return redirect(url_for('admin_dashboard'))

    db.session.delete(lot)
    db.session.commit()
    flash("Parking lot deleted successfully.", "success")
    return redirect(url_for('admin_dashboard'))

@app.route('/reserve_spot/<int:spot_id>', methods=['POST'])
def reserve_spot(spot_id):
    if 'user_id' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    spot = ParkingSpot.query.get_or_404(spot_id)
    if spot.Current_Status != 'Available':
        flash('Spot not available!', 'danger')
        return redirect(url_for('dashboard'))
    vehicle_number = request.form['Vehicle_Number']
    reservation = ParkingReservation(
        User_id=session['user_id'],
        Spot_Id=spot.Spot_Id,
        Vehicle_Number=vehicle_number,
        Entry_Time=datetime.now(),  # Save as datetime object, not string
        Exit_Time=None,
        Total_Cost=None
    )
    spot.Current_Status = 'O'
    db.session.add(reservation)
    db.session.commit()
    flash('Spot booked successfully!', 'success')
    return redirect(url_for('dashboard'))


@app.route('/add_spot', methods=['GET', 'POST'])
def add_spot():
    user_id = session.get('user_id')
    user = VehicleUser.query.get(user_id)
    if not user or user.Role != 'admin':
        flash("Only admin can add parking spots.", "danger")
        return redirect(url_for('home'))
    lots = ParkingLot.query.all()
    if request.method == 'POST':
        Lot_Id = request.form['Lot_Id']
        Current_Status = 'A'
        new_spot = ParkingSpot(Lot_Id=Lot_Id, Current_Status=Current_Status)
        db.session.add(new_spot)
        db.session.commit()
        flash('Parking spot added!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('add_spot.html', lots=lots)

@app.route('/delete_spot/<int:spot_id>', methods=['POST'])
def delete_spot(spot_id):
    spot = ParkingSpot.query.get_or_404(spot_id)
    user_id = session.get('user_id')
    user = VehicleUser.query.get(user_id)
    if not user or user.Role != 'admin':
        flash("You don't have permission to delete this spot.", "danger")
        return redirect(url_for('home'))
    db.session.delete(spot)
    db.session.commit()
    flash("Parking spot deleted successfully.", "success")
    return redirect(url_for('admin_dashboard'))

from datetime import datetime

@app.route('/release_spot/<int:reservation_id>', methods=['POST'])
def release_spot(reservation_id):
    reservation = ParkingReservation.query.get_or_404(reservation_id)
    spot = ParkingSpot.query.get(reservation.Spot_Id)
    reservation.Exit_Time = datetime.now()  # <-- Add this

    # Calculate duration and cost
    # Calculate duration and cost
    entry = reservation.Entry_Time  # Already a datetime object
    exit = reservation.Exit_Time    # Already a datetime object
    duration_hours = max(1, int((exit - entry).total_seconds() // 3600))

    lot = ParkingLot.query.get(spot.Lot_Id)
    reservation.Total_Cost = duration_hours * lot.PRICE  # <-- Add this
    spot.Current_Status = 'A'
    db.session.commit()
    flash('Spot released!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/search_parking', methods=['GET', 'POST'])
def search_parking():
    if request.method == 'POST':
        search_location = request.form.get('search_location')
        lots = ParkingLot.query.filter(ParkingLot.Location_Name.contains(search_location)).all()
    else:
        lots = ParkingLot.query.all()
    return render_template('search_parking.html', lots=lots)

@app.route('/occupied_spot_details/<int:spot_id>')
def occupied_spot_details(spot_id):
    spot = ParkingSpot.query.get_or_404(spot_id)
    if spot.Current_Status == 'O':
        reservation = ParkingReservation.query.filter_by(Spot_Id=spot_id, Exit_Time=None).first()
        return render_template('occupied_spot_details.html', spot=spot, reservation=reservation)
    else:
        flash('Spot is not occupied', 'info')
        return redirect(url_for('admin_dashboard'))
    
@app.route('/book_spot/<int:lot_id>')
def book_spot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    available_spots = [spot for spot in lot.available_spots if spot.Current_Status == 'A']
    return render_template('book_spot.html', lot=lot, spots=available_spots)















def intialize_admin():
    with app.app_context():
        if not VehicleUser.query.filter_by(Login_name='admin').first():
            admin = VehicleUser(Login_name='admin',Full_Name="udghosh rao",Email_Address="133@gmail.com",User_Password='123f', Phone_Number='1234567890',Role='admin',Address=" Kolkata",Pin_Code="123456")
            db.session.add(admin)
            db.session.commit()
            print("Admin created successfully!")


with app.app_context():
    db.create_all()
    # intialize_admin()

if __name__=='__main__':
    intialize_admin()
    app.run(debug=True)
