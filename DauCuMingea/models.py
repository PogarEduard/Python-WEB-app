from DauCuMingea import db, login_manager
from DauCuMingea import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30),  unique=True, nullable=False)
    email_address = db.Column(db.String(), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    admin = db.Column(db.Boolean())
    ligh_mode = db.Column(db.Boolean())
    items = db.relationship('Item', backref='owned_user',lazy=True)


    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String())
    photo = db.Column(db.String())
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def delete_item(self, item):
        db.session.delete(item)
        db.session.commit()


class Tennis_Field(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(),nullable=False)
    location = db.Column(db.String(),nullable=False)
    description = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer())
    photo = db.Column(db.String())


    def __repr__(self):
        return f'Tennis_field{self.id}'

    def delete_tennis(self, tennis_field):
        db.session.delete(tennis_field)
        db.session.commit()


class RentingRepository(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    location_name = db.Column(db.String(), nullable=False)
    location = db.Column(db.String(), nullable=False)
    renter = db.Column(db.String(),nullable=False)
    rent_start_time = db.Column(db.Integer(), nullable=False)
    rent_end_time = db.Column(db.Integer(),nullable=False)
    when_was_rented = db.Column(db.String(),nullable=False)
    price = db.Column(db.Integer(),nullable=False)


class ADS(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    src = db.Column(db.String(),nullable = False)
    href = db.Column(db.String(),nullable = False)
    description = db.Column(db.String,nullable=False)




