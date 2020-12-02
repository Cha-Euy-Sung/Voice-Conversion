from flask import Flask, render_template
from flask import url_for, redirect
from flask import request, session
import time
from datetime import datetime
from werkzeug.utils import secure_filename
import text_to_speech as ts
import voice_conversion.test as vc


# flask 초기화, 이름을 포함함
app = Flask(__name__)
# error 보기위한 용도, debug 용도
app.debug = True




'''
수정사항
1. txt 파일 생성 이름 수정 - line 39
'''


@app.route('/', host='index.html')
def index():
    return render_template('index.html')


@app.route('/tts', methods=['GET','POST'])
def tts():
    if request.method == 'GET':
        singer = request.args.get('singer', 'iu')
        return render_template('text-to-speech.html', singer=singer)


@app.route('/create', methods=['POST','GET'])
def gettext(display=None):
    if request.method == 'POST':
        # tts 텍스트가 넘어간 부분
        text = request.form['tts-text']
        # 현재 날짜로 저장
        # TODO - 다른 사용자가 동시에 접근한다면?
        datestring = str(datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f'))
        # print(datestring)
        # 파일 저장

        with open('tts_storage/text/tts_script.txt', 'w', encoding='utf-8') as file:
            # 개행문자 제거, 공백 처리 , 마침표 기준 분할, 공백 줄 제거, 공백제거
            newline_removed_string = text.replace('\n', "").strip()
            period_separated_lines = [line.strip() for line in newline_removed_string.split('.') if line]
            # print(period_separated_lines)
            # 마침표 및 개행 추가하여 저장
            for line in period_separated_lines:
                file.write(line + '.\n')
            file.close()
        print("## Creating Voice file...")
        ts.generate_voice()
        print("## Voice Created.")
        # 로딩부분을 보여주기 위한 sleep
        # print(text)
        # query
        # time.sleep(2)
        print("## Voice Conversion Start...")
        vc.test('A2B')
        print("## Conversion Done")

        return render_template("done.html", display=text)


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        # 경로 + 파일 명 - 미완성
        file.save('c:/' + secure_filename(file.filename))
        return 'file upload 성공!'


# 안쓰고 참고 하는 부분
@app.route('/generic')
def generic():
    return render_template('generic.html')


@app.route('/elements.html')
def elements():
    return render_template('elements.html')


if __name__ == '__main__':
    app.run()
