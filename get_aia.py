from flask import Flask, render_template, request
from werkzeug import secure_filename
import os
from unzip_and_return import aia_to_xml

app = Flask(__name__)
# app.config['UPLOAD_FOLDER']=r'C:\Users\pierc\Desktop\BebrasCampServer\upload'
# def function(file_name):
#     pass

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['upload']
    f.save(secure_filename(f.filename))
    result = aia_to_xml(secure_filename(f.filename)[0:-4])
    os.remove(secure_filename(f.filename))
    return result

@app.route('/save',methods=['POST'])
def save():
    if request.method == 'POST':
        code = request.form['code']
        team_name = request.form['team_name']
        with open(team_name, 'w') as f:
            f.write(code)

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
