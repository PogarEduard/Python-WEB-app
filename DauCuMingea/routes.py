import random
import datetime as dt
from DauCuMingea import app
from flask import render_template, flash,url_for , redirect , request
from DauCuMingea.models import User , Item , Tennis_Field , RentingRepository, ADS
from DauCuMingea.forms import RegisterForm, LoginForm , AddItemForm , AddTennisFieldForm , DeleteTennisField , DeleteItemForm,RentingForm , SearchForm , AdsForm, PurchaseItemForm
from DauCuMingea import db
from flask_login import login_user, logout_user, current_user
from flask_mail import Message
from DauCuMingea import mail

from werkzeug.utils import secure_filename

@app.route('/')
@app.route('/home')
def home_page():
    if request.method == 'GET':
        ads = ADS.query.all()

        ads1 = ads[random.randint(0,len(ads) - 1)]
        ads2 = ads[random.randint(0,len(ads) - 1)]
        ads3 = ads[random.randint(0,len(ads) - 1)]
        ads4 = ads[random.randint(0,len(ads) - 1)]
        ads5 = ads[random.randint(0,len(ads) - 1)]
        ads6 = ads[random.randint(0,len(ads) - 1)]
        ads7 = ads[random.randint(0,len(ads) - 1)]
        ads8 = ads[random.randint(0,len(ads) - 1)]



        tennis_fields = Tennis_Field.query.all()

        n = tennis_fields[random.randint(0, len(tennis_fields) - 1)].id
        y = tennis_fields[random.randint(0, len(tennis_fields) - 1)].id
        t = tennis_fields[random.randint(0, len(tennis_fields) - 1)].id

        while n == t or n == y or t == y or t == y == n:
            n = tennis_fields[random.randint(0, len(tennis_fields) - 1)].id
            y = tennis_fields[random.randint(0, len(tennis_fields) - 1)].id
            t = tennis_fields[random.randint(0, len(tennis_fields) - 1)].id


        tennis_fields1 = Tennis_Field.query.get(n)
        tennis_fields2 = Tennis_Field.query.get(y)
        tennis_fields3 = Tennis_Field.query.get(t)

        return render_template('home.html', tennis_fields1=tennis_fields1, tennis_fields2=tennis_fields2, tennis_fields3=tennis_fields3, tennis_fields=tennis_fields, ads1=ads1, ads2=ads2, ads3=ads3, ads4=ads4, ads5=ads5, ads6=ads6, ads7=ads7, ads8=ads8)


@app.route('/TennisFields', methods=['GET', 'POST'])
def fields_page():
    renting = RentingRepository()
    tennis_field_delete_form = DeleteTennisField()
    renting_form = RentingForm()
    search_form = SearchForm()

    search_name = request.args.get('search_name')

    if search_form.validate_on_submit():
        search_name = request.form.get('search_name')
    if search_name:
        tennis_fields = Tennis_Field.query.filter_by(location=search_name.capitalize())
    else:
        tennis_fields = Tennis_Field.query.all()



    if renting_form.validate_on_submit():
        renting_field_name = request.form.get('rent_tennis_field_name')
        renting_field_price = request.form.get('rent_tennis_field_price')
        renting_field_location = request.form.get('rent_tennis_field_location')
        username = User.query.filter_by(id=current_user.id).first()

        prima_zi = renting_form.start_date.data
        ultima_zi = renting_form.end_date.data

        prima_zi = str(prima_zi)
        ultima_zi = str(ultima_zi)

        date = dt.datetime.now()

        if int(prima_zi[8:]) <= int(date.strftime('%d')) or int(prima_zi[5:7]) < int(date.strftime('%m')) or int(prima_zi[2:4]) < int(date.strftime('%y')):
            flash(f'Data pe care ati introdus-o nu este corecta , va rog alegeti o data!', category='danger')
        else:
            if prima_zi[5:7] == ultima_zi[5:7]:
                pret_final = ((int(ultima_zi[8:])-int(prima_zi[8:]) + 1) * int(renting_field_price))
            elif prima_zi[5:7] == '01' \
                    or prima_zi[5:7] == '03'\
                    or prima_zi[5:7] == '05' \
                    or prima_zi[5:7] == '07' \
                    or prima_zi[5:7] == '08' \
                    or prima_zi[5:7] == '10' \
                    or prima_zi[5:7] == '12':
                pret_final = (31 - int(prima_zi[8:]) + int(ultima_zi[8:]) + 1) * int(renting_field_price)
            elif prima_zi[5:7] == '02':
                pret_final = (28 - int(prima_zi[8:]) + int(ultima_zi[8:]) + 1) * int(renting_field_price)
            elif prima_zi[5:7] == '04' \
                    or prima_zi[5:7] == '06'\
                    or prima_zi[5:7] == '09' \
                    or prima_zi[5:7] == '11':
                pret_final = (30 - int(prima_zi[8:]) + int(ultima_zi[8:]) + 1) * int(renting_field_price)

            add_renting = RentingRepository(
                    location_name = renting_field_name,
                    location =  renting_field_location,
                    renter = username.username,
                    rent_start_time = renting_form.start_date.data,
                    rent_end_time = renting_form.end_date.data,
                    when_was_rented = dt.datetime.now(),
                    price = pret_final,
            )
            db.session.add(add_renting)
            db.session.commit()
            msg = Message(f'Va multumim ca ati apelat la noi {current_user.username}', sender=current_user.email_address, recipients=['pogareduard@yahoo.com'])
            msg.body = f'Ati inchiriat terenul {renting_field_name} incepand cu data de {renting_form.start_date.data} pana la {renting_form.end_date.data} pentru suma de {pret_final} Ron'
            mail.send(msg)
            flash(f'Terenul {renting_field_name} a fost inchiriat de la data de {add_renting.rent_start_time} pana la data de {add_renting.rent_end_time} pentru suma de {pret_final} Ron',category='success')
        return redirect(url_for('fields_page'))

    if tennis_field_delete_form.validate_on_submit():
        tennis_field = request.form.get('delete_tennis_field')
        tennis_field_delete = Tennis_Field.query.filter_by(id=tennis_field).first()
        db.session.delete(tennis_field_delete)
        db.session.commit()
        flash(f'Terenul de tenis a fost sters!',category='success')
        return redirect(url_for('fields_page'))

    return render_template('fields.html', tennis_fields=tennis_fields, tennis_field_delete_form=tennis_field_delete_form, renting_form=renting_form, renting=renting, search_form=search_form)


@app.route('/echipamente', methods=['GET','POST'])
def item_page():
    item_purchase_form = PurchaseItemForm()
    item_delete_form = DeleteItemForm()
    items = Item.query.all()

    if item_delete_form.validate_on_submit():
        item_delete = request.form.get('item_to_delete')
        item_to_delete = Item.query.filter_by(id=item_delete).first()
        db.session.delete(item_to_delete)
        db.session.commit()
        flash(f'Obiectul a fost sters!', category='success')
        return redirect(url_for('item_page'))

    if item_purchase_form.validate_on_submit():
        item_name = request.form.get('item_name')
        msg = Message(f'Felicitari ati cumparat obiectul {item_name}')
        msg.body = f'Va multumim!'
        flash(f'Merge {item_name}')
        return redirect(url_for('item_page'))

    return render_template('items.html', items=items, item_delete_form=item_delete_form, item_purchase_form=item_purchase_form)



@app.route('/dsadas!@3!$#SD--562',methods=['GET','POST'])
def add_item():
    item_form = AddItemForm()
    if item_form.validate_on_submit():
        item_to_add = Item(
            name=item_form.name.data,
            price=item_form.price.data,
            description=item_form.description.data,
            photo = item_form.photo.data)
        db.session.add(item_to_add)
        db.session.commit()
        flash(f'Felicitari , obiectul {item_to_add.name} a fost adaugat!',category='success')
        return redirect(url_for('add_item'))

    if item_form.errors != {}:
        for err_msg in item_form.errors.values():
            flash(f'A aparut o eroare in adaugarea obiectului: {err_msg}', category='danger')

    return render_template('itemadmin.html',item_form=item_form)

@app.route('/ASDWQDfdgfd@#!$#14564-',methods=['GET','POST'])
def add_tennis_field():
    field_form = AddTennisFieldForm()
    if field_form.validate_on_submit():
        field_to_add = Tennis_Field(name = field_form.name.data,
                                  price = field_form.price.data,
                                  location = field_form.location.data,
                                  description = field_form.description.data,
                                  photo = field_form.photo.data)
        db.session.add(field_to_add)
        db.session.commit()
        flash(f'Felicitari , Terenul {field_to_add.name} a fost adaugat!', category='success')
        return redirect(url_for('fields_page'))

    if field_form.errors != {}:
        for err_msg in field_form.errors.values():
            flash(f'A aparut o eroare in adaugarea terenului de tenis: {err_msg}', category='danger')

    return render_template('fieldsadmin.html', field_form=field_form)

@app.route('/sakhjdgaskdgkasjhdh',methods=['POST', 'GET'])
def add_ads():
    ads_form = AdsForm()
    if request.method == 'POST':
        if ads_form.validate_on_submit():
            ads_to_add = ADS(
                src = ads_form.src.data,
                href = ads_form.href.data,
                description = ads_form.description.data,
            )
        db.session.add(ads_to_add)
        db.session.commit()
        flash(f'Reclama a fost adaugata!', category='success')
        return redirect(url_for('add_ads'))

    if ads_form.errors != {}:
            for err_msg in ads_form.errors.values():
                flash(f'A aparut o eroare in adaugarea reclamei: {err_msg}', category='danger')
    return render_template('adsadmin.html', ads_form=ads_form)

@app.route('/dqwipj3p2131310-23$#%#$%!')
def transaction():
    if request.method == 'GET':
        renting = RentingRepository.query.all()
        return render_template('renting.html' ,renting=renting)

@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data,
                              admin=False
                              )
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Cont creat cu succes! Bine ai venit {user_to_create.username}', category='success')
        return redirect(url_for('home_page'))
    if form.errors != {}: #if there are not errors from valitation
        for err_msg in form.errors.values():
            flash(f'A aparut o eroare in crearea contului: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login',methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Te-ai logat cu succes: {attempted_user.username}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash(f'Contul nu exista sau ai gresit numele sau parola.',category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash('Te-ai delogat cu succes!',category='info')
    return redirect(url_for('home_page'))