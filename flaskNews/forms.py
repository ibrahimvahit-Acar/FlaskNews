from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from flaskNews.models import User
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user

#Uygulamada kullanılacak olan formların kodları burada tanımlanmıştır.


#Kaydolma formu
class RegistrationForm(FlaskForm):
    username = StringField('Kullanıcı Adı',
                           validators=[DataRequired(), Length(min=2, max=20)])

    password = PasswordField('Şifre', validators=[DataRequired()])
    confirm_password = PasswordField('Şifreyi Doğrula',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Kayıt Ol')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'Bu kullanıcı adı alınmış lütfen farklı bir kullanıcı adı giriniz.')

#Giriş formu
class LoginForm(FlaskForm):
    username = StringField('Kullanıcı Adı',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Şifre', validators=[DataRequired()])
    remember = BooleanField('Beni Hatırla')
    submit = SubmitField('Giriş')

#Arama Formu
class SearchForm(FlaskForm):
    searchField = StringField('Aramınızı giriniz')
    search = SubmitField('Ara')

#Güncelleme Formu
class UpdateAccountForm(FlaskForm):
    picture = FileField('Profil resmini güncelle', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Güncelle')
