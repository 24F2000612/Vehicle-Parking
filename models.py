from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class VehicleUser(db.Model):
    __tablename__ = "VehicleUser"
    User_id = db.Column(db.Integer , primary_key = True)
    Login_name = db.Column(db.String , unique = True , nullable = False)
    Full_Name = db.Column(db.String ,nullable =False )
    Email_Address = db.Column(db.String , unique = True , nullable = False)
    User_Password = db.Column(db.String ,nullable = False)
    Phone_Number = db.Column(db.String , nullable = True)
    ParkingReservation = db.relationship("ParkingReservation" , backref ='customer_booking' , cascade ="all , delete")

class ParkingLot(db.Model):
    __tablename__ = "ParkingLot"
    id = db.Column(db.Integer , primary_key=True)
    Location_Name = db.Column(db.String , nullable = False)
    Address_name = db.Column(db.String , nullable = False)
    PRICE = db.Column(db.Integer , nullable = False)
    Maximum_Number_Spots = db.Column(db.Integer , nullable = False)
    availabe_spot = db.relationship("ParkingSpot" , backref = "belong_to_lot" , cascade = "all, delete")

class ParkingSpot(db.Model):
    __tablename__ = "ParkingSpot"
    Spot_Id = db.Column(db.Integer, primary_key=True)
    Current_Status = db.Column(db.String , nullable = False)
    Lot_Id = db.Column(db.Integer , db.ForeignKey("ParkingLot.id") , nullable = False, )
    spot_booking = db.relationship("ParkingReservation", backref = "allocated_spot" , cascade="all , delete")

class ParkingReservation(db.Model):
    __tablename__ = "ParkingReservation"
    Reservation_Id = db.Column(db.Integer ,primary_key=True )
    User_id = db.Column(db.Integer,db.ForeignKey("VehicleUser.User_id"),nullable = False)
    spot_id_id = db.Column(db.Integer , db.ForeignKey(ParkingSpot.Spot_Id) , nullable = False)
    Booked_Spot = db.relationship("ParkingSpot" , backref ="Spot_reservation")
    
