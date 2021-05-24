from flask import Flask, render_template, request,jsonify
from werkzeug import secure_filename
import os
import re
from unzip_and_return import aia_to_xml
from flask_cors import CORS, cross_origin
from combine import combine
import json


app = Flask(__name__)
CORS(app)
# app.config['UPLOAD_FOLDER']=r'C:\Users\pierc\Desktop\BebrasCampServer\upload'
# def function(file_name):
#     pass

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['files']
    team_number = request.form['data']
    f.save(secure_filename(f.filename))
    result = aia_to_xml(secure_filename(f.filename)[0:-4],team_number)
    #os.remove(secure_filename(f.filename))
    return result

@app.route('/save',methods=['POST'])
def save():
    if request.method == 'POST':
        code = request.form['code']
        team_name = request.form['team_name']
        with open('./xmltopython/'+team_name+'.txt', 'w') as f:
            f.write(code)
            combine()
            return 'ok'

@app.route('/battle',methods=['POST'])
def battle():
    getdata=request.form['pythonCodeData']
    getdata=re.split(': |,', getdata)
    codea=getdata[1].replace('\\n','\n')
    codeb=getdata[3].replace('\\n','\n')
    file_write = open('codea.txt', 'w', encoding="utf-8")
    file_write2 = open('codeb.txt', 'w', encoding="utf-8")
    for i in codea[2:-2]:
        file_write.write(i)
        if i =='\\':
            file_write.write('\n')
    file_write.close()
    for i in codeb[2:-2]:
        file_write2.write(i)
        if i =='\\':
            file_write2.write('\n')
    file_write2.close()

    file = open('codea.txt', 'r', encoding="utf-8")
    file2 = open('codeb.txt', 'r', encoding="utf-8")
    filehead = open('strategy_battle_head.txt', encoding="utf-8")
    filemiddle = open('strategy_battle_middle.txt', encoding="utf-8")
    filebottom = open('strategy_battle_bottom.txt', encoding="utf-8")
    file_write = open('combine_code/' + 'battle.py', 'w', encoding="utf-8")
    contents = file.readlines()
    contents2 = file2.readlines()
    contentshead = filehead.readlines()
    contentsmiddle = filemiddle.readlines()
    contentsbottom = filebottom.readlines()
    for line in contentshead:
        file_write.write(line)
    filehead.close()
    file_write.write('    ' + str(line))

    for line in contents:
        file_write.write('    ' + str(line))
    file.close()

    for line in contentsmiddle:
        file_write.write(line)
    filemiddle.close()

    for line in contents2:
        file_write.write('    ' + str(line))
    file.close()


    for line in contentsbottom:
        file_write.write(line)
    filebottom.close()
    file_write.close()


    exec(open('./combine_code/'+'battle.py', encoding="utf-8").read(),globals())
    with open('./combine_code/BattleReport/Report.json', 'r', encoding="utf-8") as json_file:
        data = json.load(json_file)
        return jsonify(data)


app.run(host='0.0.0.0', port=5000)

# from flask import Flask
# from flask_uploads import UploadSet, IMAGES, configure_uploads
# from flask import request
#
# app = Flask(__name__)
#
# app.config['SECRET_KEY'] = 'development'
# app.config['UPLOADED_DEF_DEST'] = r'D:\Desktop\BebrasCampServer\upload'
# app.config['UPLOADED_DEF_URL'] = '\\static\\upload\\'
#
# abc = UploadSet(name='def', extensions=IMAGES)
# configure_uploads(app, abc)
#
# html = '''
# <html>
#    <body>
#       <div action = "http://localhost:5000/uploader" method = "POST"
#          enctype = "multipart/form-data">
#          <input  type="file"
#                                 name="upload"
#                                 id="upload"
#                                 class="upload-box"
#                                 accept=".aia"
#                                 placeholder="選擇檔案"/>
#
#          <button onclick="uploadTeamFile()"/>
#       </div>
#    </body>
#
#
# <script>
# const uploadTeamFile = () => {
#
#     const teamId = 'teamid123';
#
#     const input = document.querySelector('input[type="file"]');
#
#
#         const data = {
#             teamId,
#         };
#         const formData = new FormData();
#         for (file of input.files) {
#             formData.append('files', file, file.name);
#         }
#         formData.append('data', JSON.stringify(data));
#
#         fetch('/api/uploadFile', {
#             method: 'post',
#             body: formData,
#         })
#             .then((response) => {
#                 console.log('uploadFile response', response);
#                 return response;
#             })
#             .then((response) => {
#                 if (response.status == 200) {
#                     console.log('Success:', response);
#                     alert(`完成提交！`);
#                 }
#             })
#             .catch((error) => {
#                 console.error('Error:', error);
#                 alert(`上傳失敗`);
#             });
#     } else {
#         alert('請登入');
#         window.location.href = './main';
#     }
# };
# </script>
# </html>
# '''
#
#
# @app.route('/uploads/', methods=['GET', 'POST'])
# def uploads():
#     if request.method == 'POST' and 'in_abc' in request.files:
#         filename = abc.save(request.files['in_abc'])
#         print(filename)
#         file_url = abc.url(filename)
#         print(file_url)
#     return html
#
#
# if __name__ == '__main__':
#     app.run(host='localhost', port=5000)