from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Папка для загрузки видео
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Путь к файлам данных
USERS_FILE = 'users.txt'
VIDEOS_FILE = 'videos.txt'

# Проверка существования файлов
if not os.path.exists(USERS_FILE):
    open(USERS_FILE, 'w').close()

if not os.path.exists(VIDEOS_FILE):
    open(VIDEOS_FILE, 'w').close()


# Главная страница
@app.route('/')
def index():
    videos = []
    with open(VIDEOS_FILE, 'r') as f:
        for line in f:
            username, video_name = line.strip().split(',')
            videos.append({'username': username, 'video_name': video_name})
    return render_template('index.html', videos=videos)


# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with open(USERS_FILE, 'a') as f:
            f.write(f'{username},{password},0\n')  # 0 подписчиков изначально
        return redirect(url_for('login'))
    return render_template('register.html')

# Проверка существования файлов
if not os.path.exists(USERS_FILE):
    open(USERS_FILE, 'w').close()

if not os.path.exists(VIDEOS_FILE):
    open(VIDEOS_FILE, 'w').close()



# Авторизация
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with open(USERS_FILE, 'r') as f:
            for line in f:
                saved_username, saved_password, _ = line.strip().split(',')
                if username == saved_username and password == saved_password:
                    session['username'] = username
                    return redirect(url_for('profile'))
        return "Неверное имя пользователя или пароль!"
    return render_template('login.html')

# Проверка существования файлов
if not os.path.exists(USERS_FILE):
    open(USERS_FILE, 'w').close()

if not os.path.exists(VIDEOS_FILE):
    open(VIDEOS_FILE, 'w').close()



# Профиль пользователя
@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    with open(USERS_FILE, 'r') as f:
        for line in f:
            saved_username, _, subscribers = line.strip().split(',')
            if username == saved_username:
                return render_template('profile.html', username=username, subscribers=subscribers)
    return "Пользователь не найден!"


# Загрузка видео
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            with open(VIDEOS_FILE, 'a') as f:
                f.write(f"{session['username']},{filename}\n")
            return redirect(url_for('index'))
    return render_template('upload.html')


# Выход из аккаунта
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
