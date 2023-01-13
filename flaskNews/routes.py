from flask import render_template, url_for, flash, redirect, request
from flaskNews.forms import RegistrationForm, LoginForm, SearchForm, UpdateAccountForm
from flaskNews.models import User
from flaskNews import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from flaskNews.webscraping import sozcuData, search
from PIL import Image
import secrets  
import os

#Ana sayfa
@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    image_file = url_for(
        'static', filename='profile_pics/' + 'TrakyaNews.png')
    return render_template('home.html', image_file=image_file)

#Ekonomi sayfası
@app.route("/ekonomi", methods=['GET', 'POST'])
@login_required
def ekonomi():
    try:
        value = request.form['operator']
    except:
        value = 1
    myNews = sozcuData(
        "https://www.sozcu.com.tr/ekonomi/", "news-item", value)
    form = SearchForm()
    if form.validate_on_submit():
        myNews = search(myNews, form.searchField.data)
    return render_template('ekonomi.html', myNews=myNews, title="Ekonomi Haberleri", form=form, value=value)

#Güncel haberler sayfası
@app.route("/guncel", methods=['GET', 'POST'])
@login_required
def guncel():
    try:
        value = request.form['operator']
    except:
        value = 1
    myNews = sozcuData(
        "https://www.sozcu.com.tr/son-dakika/", "timeline-card", value)

    form = SearchForm()
    if form.validate_on_submit():
        myNews = search(myNews, form.searchField.data)
    return render_template('guncel.html', myNews=myNews, title="Güncel Haberler", form=form, value=value)

#Spor Sayfası
@app.route("/spor", methods=['GET', 'POST'])
@login_required
def spor():
    try:
        value = request.form['operator']
    except:
        value = 1
    myNews = sozcuData(
        "https://www.sozcu.com.tr/spor/", "news-item", value)
    form = SearchForm()
    if form.validate_on_submit():
        myNews = search(myNews, form.searchField.data)

    return render_template('spor.html', myNews=myNews, title="Spor Haberleri", form=form, value=value)

#Dünya haberleri sayfası
@app.route("/dunya", methods=['GET', 'POST'])
@login_required
def dunya():
    try:
        value = request.form['operator']
    except:
        value = 1
    myNews = sozcuData(
        "https://www.sozcu.com.tr/dunya/", "news-item", value)

    form = SearchForm()
    if form.validate_on_submit():
        myNews = search(myNews, form.searchField.data)
    return render_template('dunya.html', myNews=myNews, title="Dünyadan Haberler", form=form, value=value)

#Hayat haberleri sayfası
@app.route("/hayat", methods=['GET', 'POST'])
@login_required
def hayat():
    try:
        value = request.form['operator']
    except:
        value = 1
    myNews = sozcuData(
        "https://www.sozcu.com.tr/hayatim/", "news-item", value)

    form = SearchForm()
    if form.validate_on_submit():
        myNews = search(myNews, form.searchField.data)

    return render_template('hayat.html', myNews=myNews, title="Dünyadan Haberler", form=form, value=value)

#Giriş Sayfası
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Lütfen emailinizi veya şifrenizi kontrol edin', 'danger')
    return render_template('login.html', title='Giriş', form=form)

#Hesap oluşturma sayfası
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Hesabınız oluşturulmuştur.Lütfen giriş yapınız', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Kayıt ol', form=form)

#Bilgisayardan resim seçme fonksiyonu
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

#Hesap sayfası
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        db.session.commit()
        flash('Resmin güncellendi', 'success')
        return redirect(url_for('account'))
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

#Çıkış yapar
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
