from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import pandas as pd
import pickle
from flask import Flask, render_template, Response
import matplotlib.pyplot as plt
import numpy as np
import io
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 데이터베이스 연결 함수
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# 데이터베이스 초기화 함수
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            user_id TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# 시작 페이지 
@app.route('/')
def start():
    return render_template('시작.html')

# 홈 페이지
@app.route('/home')
def home():
    return render_template('home.html')


# 소개페이지
@app.route('/introduce')
def introduce():
    return render_template('소개.html')    

#서비스페이지
@app.route('/service')
def service():
    return render_template('서비스.html')

# 회원가입
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        user_id = request.form['user_id']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if password != confirm_password:
            flash('비밀번호가 일치하지 않습니다.')
            return render_template('회원가입.html')

        hashed_password = generate_password_hash(password)
        print(f"해싱된 비밀번호: {hashed_password}")  # 디버깅 출력

        try:
            with get_db_connection() as conn:
                conn.execute('INSERT INTO users (username, user_id, email, password) VALUES (?, ?, ?, ?)',
                             (username, user_id, email, hashed_password))
            flash('회원가입이 완료되었습니다. 로그인 해주세요.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('이미 사용 중인 아이디입니다.')
            return render_template('회원가입.html')

    return render_template('회원가입.html')

# 로그인
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('로그인.html')
    elif request.method == 'POST':
        # data = request.get_json()
        # print(f"로그인 요청 데이터: {data}")  # 디버깅용 출력
        user_id = request.form.get('username')
        password = request.form.get('password')
        print(user_id,password)
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()
        conn.close()

        if user:
            print(f"사용자 찾음: {user['user_id']}")  # 사용자 정보 확인
        else:
            print("사용자를 찾을 수 없습니다.")
        
        if user and check_password_hash(user['password'], password):
            print("비밀번호 일치")
            return redirect(url_for('login_next'))
        else:
            print("비밀번호 불일치 또는 사용자 없음")
            return Response({"success": False}), 401
            
# 로그인 성공 후 페이지
@app.route('/login_next')
def login_next():
    return render_template('login2.html')

# 프로필 페이지    

@app.route('/profile')
def profile():
    return render_template('프로필.html')

# 테스트용 막대그래프 페이지
@app.route('/barchart')
def barchart():
    data = {
        'labels': ['둔산2동', '탄방동', '둔산1동', '관저2동', '괴정동'],
        'values': [1614.7, 1115.8, 572.7, 445.1, 375.8]
    }
    return render_template('barchart.html', data=data)

# 메인 실행
if __name__ == '__main__':
    init_db()
    app.run(debug=True)