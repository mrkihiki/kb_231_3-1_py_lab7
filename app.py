import os
import random
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask, url_for, render_template, json, abort, redirect, request
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import StringField, SelectField, TextAreaField, BooleanField, FileField ,SubmitField
from wtforms.validators import DataRequired, Email
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['SECRET_KEY'] = 'my_secret_key'
bootstrap = Bootstrap5(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_navbar():
    return '''
    <nav class="navbar navbar-dark bg-dark mb-4">
        <div class="container">
            <a class="navbar-brand" href="/">Марс</a>
            <div>
                <a href="/" class="text-white me-3">Главная</a>
                <a href="/list_prof/ul" class="text-white me-3">Профессии</a>
                <a href="/distribution" class="text-white me-3">Каюты</a>
                <a href="/astronaut_selection" class="text-white me-3">Запись</a>
                <a href="/galery" class="text-white">Галерея</a>
            </div>
        </div>
    </nav>
    '''


def get_footer():
    return '''
    <footer class="bg-dark text-white text-center py-3 mt-4">
        <div class="container">
            <p>© 2025 Миссия Колонизация Марса</p>
        </div>
    </footer>
    '''


def send_email(to_email, subject, body, photo=None):
    # === НАСТРОЙКИ SMTP (ИЗМЕНИТЕ ЭТИ ДАННЫЕ!) ===
    SMTP_SERVER = "smtp.yandex.ru"  # для Gmail
    SMTP_PORT = 587
    SMTP_USERNAME = "mrkihiki@yandex.ru"  # ваш email
    SMTP_PASSWORD = "eqikzfvrvqwdtnnh"  # пароль приложения (не обычный пароль!)
    FROM_EMAIL = "mrkihiki@yandex.ru"
    # ============================================

    try:
        # Создаем сообщение
        msg = MIMEMultipart()
        msg['From'] = FROM_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject

        # Добавляем текст письма
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        # Если есть фото, прикрепляем его
        if photo and hasattr(photo, 'filename') and photo.filename:
            # Создаем временный файл
            temp_filename = f"temp_photo_{photo.filename}"
            photo.save(temp_filename)

            # Прикрепляем файл
            with open(temp_filename, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename="{photo.filename}"'
                )
                msg.attach(part)

            # Удаляем временный файл
            os.remove(temp_filename)

        # Устанавливаем соединение с SMTP сервером
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Шифрование
        server.login(SMTP_USERNAME, SMTP_PASSWORD)

        # Отправляем письмо
        server.send_message(msg)
        server.quit()

        print(f"✅ Email успешно отправлен на {to_email}")
        return True

    except Exception as e:
        print(f"❌ Ошибка отправки email: {e}")
        return False


@app.route('/')
@app.route('/index')
def index():
    param = {}
    param['get_navbar'] = get_navbar()
    param['get_footer'] = get_footer()
    param['title'] = 'Добро пожаловать!'
    return render_template('index.html', **param)


@app.route('/list_prof/<list_type>')
def list_prof(list_type):
    param = {}
    param['get_navbar'] = get_navbar()
    param['get_footer'] = get_footer()
    param['title'] = 'Список профессий!'
    param['professions'] = [
        'Инженер-исследователь',
        'Пилот',
        'Строитель',
        'Экзобиолог',
        'Врач',
        'Инженер по терраформированию',
        'Климатолог',
        'Специалист по радиационной защите',
        'Астрогеолог',
        'Гляциолог',
        'Инженер жизнеобеспечения',
        'Метеоролог',
        'Оператор марсохода',
        'Киберинженер',
        'Штурман',
        'Пилот дронов'
    ]
    param['list_type'] = list_type
    return render_template('list_prof.html',**param)


@app.route('/distribution')
def distribution():
    param = {}
    param['get_navbar'] = get_navbar()
    param['get_footer'] = get_footer()
    param['title'] = 'Размещение'
    with open("static/members/crew.json", "rt", encoding="utf8") as f:
        crew = json.loads(f.read())
    param['crew'] = crew
    return render_template('distribution.html', **param)


@app.route('/member/<int:number>')
def member_by_number(number):
    param = {}
    param['get_navbar'] = get_navbar()
    param['get_footer'] = get_footer()
    param['title'] = 'Член экипажа'
    with open("static/members/crew.json", "rt", encoding="utf8") as f:
        crew = json.loads(f.read())

    if number < 1 or number > len(crew):
        abort(404, description="Член экипажа не найден")

    param['member'] = crew[number - 1]
    param['is_random'] = False
    return render_template('member.html',**param)


@app.route('/member/random')
def member_random():
    param = {}
    param['get_navbar'] = get_navbar()
    param['get_footer'] = get_footer()
    param['title'] = 'Член экипажа'
    with open("static/members/crew.json", "rt", encoding="utf8") as f:
        crew = json.loads(f.read())
    param['crew'] = crew
    param['is_random'] = True
    return render_template('member.html',**param)

@app.route('/room/<sex>/<int:age>')
def room(sex, age):
    param = {}
    param['get_navbar'] = get_navbar()
    param['get_footer'] = get_footer()
    param['title'] = 'Оформление каюты'
    param['sex'] = sex
    param['age'] = age
    return render_template('room.html',**param)


@app.route('/astronaut_selection', methods=['GET', 'POST'])
def astronaut_selection():
    param = {}
    param['get_navbar'] = get_navbar()
    param['get_footer'] = get_footer()
    param['title'] = 'Запись добровольцем'
    class AstronautForm(FlaskForm):
        last_name = StringField('Фамилия', validators=[DataRequired()])
        first_name = StringField('Имя', validators=[DataRequired()])
        email = StringField('Email', validators=[DataRequired(), Email()])
        education = SelectField('Образование', choices=[
            ('school', 'Среднее'),
            ('college', 'Среднее специальное'),
            ('bachelor', 'Бакалавриат'),
            ('master', 'Магистратура'),
            ('phd', 'Докторантура')
        ], validators=[DataRequired()])
        profession = SelectField('Профессия', choices=[
            ('engineer', 'Инженер-исследователь'),
            ('pilot', 'Пилот'),
            ('builder', 'Строитель'),
            ('exobiologist', 'Экзобиолог'),
            ('doctor', 'Врач'),
            ('terraformer', 'Инженер по терраформированию'),
            ('climatologist', 'Климатолог'),
            ('radiation', 'Специалист по радиационной защите'),
            ('astrogeologist', 'Астрогеолог'),
            ('glaciologist', 'Гляциолог'),
            ('life_support', 'Инженер жизнеобеспечения'),
            ('meteorologist', 'Метеоролог'),
            ('rover_operator', 'Оператор марсохода'),
            ('cyber_engineer', 'Киберинженер'),
            ('navigator', 'Штурман'),
            ('drone_pilot', 'Пилот дронов')
        ], validators=[DataRequired()])
        gender = SelectField('Пол', choices=[
            ('male', 'Мужской'),
            ('female', 'Женский')
        ], validators=[DataRequired()])
        motivation = TextAreaField('Мотивация', validators=[DataRequired()])
        stay_on_mars = BooleanField('Готовы ли остаться на Марсе?')
        photo = FileField('Фото')
        submit = SubmitField('Отправить заявку')

    form = AstronautForm()
    param['form'] = form
    if form.validate_on_submit():
        # Сохраняем фото
        photo = None
        if form.photo.data:
            file = form.photo.data
            if allowed_file(file.filename):
                photo = file

        # Формируем тело письма
        body = f"""Новая заявка на участие в миссии!

        Данные кандидата:
        Фамилия: {form.last_name.data}
        Имя: {form.first_name.data}
        Email: {form.email.data}
        Образование: {dict(form.education.choices).get(form.education.data)}
        Профессия: {dict(form.profession.choices).get(form.profession.data)}
        Пол: {dict(form.gender.choices).get(form.gender.data)}
        Мотивация: {form.motivation.data}
        Готов остаться на Марсе: {'Да' if form.stay_on_mars.data else 'Нет'}
        """
        if send_email(form.email.data, 'Заявка на участие в миссии', body, photo):
            render_template('success.html',**param)
    return render_template('astronaut_selection.html',**param)


@app.route('/galery', methods=['GET', 'POST'])
def galery():
    param = {}
    param['get_navbar'] = get_navbar()
    param['get_footer'] = get_footer()
    param['title'] = 'Галерея'
    #Список изображений
    images = [
            'https://avatars.mds.yandex.net/i?id=c84810f4f463b7e04ed81b95a812d4f8_l-5014030-images-thumbs&n=13',
            'https://i.pinimg.com/originals/dc/18/a1/dc18a128be9c6708a16f76c4fdf29e03.jpg',
            'https://s0.rbk.ru/v6_top_pics/media/img/0/55/347256249103550.jpeg'
        ]
    gallery_folder = os.path.join('static', 'img', 'gallery')
    os.makedirs(gallery_folder, exist_ok=True)

    for filename in os.listdir(gallery_folder):
        if allowed_file(filename):
            images.append(f'img/gallery/{filename}')

    if request.method == 'POST':
        # Обработка загрузки файла
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(gallery_folder, filename))
            return redirect(url_for('galery'))

    param['images'] = images
    return render_template('galery.html',**param)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')