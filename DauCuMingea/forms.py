from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField , IntegerField , BooleanField, DateField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from DauCuMingea.models import User



class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Exista deja un cont cu acest nume! Va rog folositi alt nume.')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Exista deja un cont cu acest Email! Va rog folositi alt email.')

    username = StringField(label='Nume utilizator:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email address:', validators=[Email(),DataRequired()])
    password1 = PasswordField(label='Parola:', validators=[Length(min=6),DataRequired()])
    password2 = PasswordField(label='Confirma parola:',validators=[EqualTo('password1'),DataRequired()])
    admin = BooleanField()
    submit = SubmitField(label='Creaza cont')

class AddItemForm(FlaskForm):
    name = StringField(label='Numele obiectului:',validators=[DataRequired()])
    price = IntegerField(label='Pretul obiectului:',validators=[DataRequired()])
    description = StringField(label='Descrierea obiectului:',validators=[DataRequired()])
    photo = StringField(label='Adaugare link fotografie')
    submit = SubmitField(label='Adauga')

class AddTennisFieldForm(FlaskForm):
    name = StringField(label='Numele terenului de tenis:',validators=[DataRequired()])
    price = IntegerField(label='Pretul de inchiriere:',validators=[DataRequired()])
    location = StringField(label='Locatia terenului de tenis:',validators=[DataRequired()])
    description = StringField(label='Spune ceva despre acest teren:',validators=[DataRequired()])
    photo = StringField(label='Adaugare link fotografie')
    submit = SubmitField(label='Adauga')

class LoginForm(FlaskForm):
    username = StringField(label='Nume utilizator:', validators=[DataRequired()])
    password = PasswordField(label='Parola:', validators=[DataRequired()])
    submit = SubmitField(label='Logare')

class RentingForm(FlaskForm):

    when_was_rented = DateField()
    start_date = DateField(validators=[DataRequired()])
    end_date = DateField(validators=[DataRequired()])
    submit = SubmitField(label='Inchiriere')

class DeleteItemForm(FlaskForm):
    submit = SubmitField(label='Stergere')

class DeleteTennisField(FlaskForm):
    submit = SubmitField(label='Stergere')

class SearchForm(FlaskForm):
    submit = SubmitField(label='Cautare')

class AdsForm(FlaskForm):
    src = StringField(label='Poza pentru reclama:',validators=[DataRequired()])
    href = StringField(label='Adreza de redirectionare:',validators=[DataRequired()])
    description = StringField(label='O scurta descriere:',validators=[DataRequired()])
    submit = SubmitField(label='Postare')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Cumpara')