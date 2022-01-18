from flask import Flask, render_template, request, jsonify
from werkzeug import secure_filename
import os
import shutil
import re
from unzip_and_return import aia_to_xml
from flask_cors import CORS
from combine import combine
import json
import datetime
import random
import time

app = Flask(__name__)
CORS(app)


@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['files']
    team_number = request.form['data']
    f.save(secure_filename(f.filename))
    result = aia_to_xml(secure_filename(f.filename)[0:-4],team_number)
    os.remove(secure_filename(f.filename))
    return result

@app.route('/battle',methods=['POST'])
def battle():
   req_time = str(time.time()).replace('.','')
   getdata=request.form['pythonCodeData']
   getdata=re.split('"',getdata)
   #print(getdata)
   codea=getdata[3].replace('\\n','\n')
   codeb=getdata[7].replace('\\n','\n')
   file_write = open('pythoncodeandb/{}codea.txt'.format(req_time),'w',encoding="utf-8")
   file_write2 = open('pythoncodeandb/{}codeb.txt'.format(req_time),'w',encoding="utf-8")
   for i in codea[0:-1]:
       file_write.write(i)
       if i=='\\':
           file_write.write('\n')
   file_write.close()

   for i in codeb[0:-1]:
       file_write2.write(i)
       if i=='\\':
           file_write2.write('\n')
   file_write2.close()


   file = open('pythoncodeandb/{}codea.txt'.format(req_time),'r', encoding="utf-8")
   file2 = open('pythoncodeandb/{}codeb.txt'.format(req_time),'r', encoding ="utf-8")
   filehead = open('strategy_battle_head.txt',encoding="utf-8")
   filemiddle = open('strategy_battle_middle.txt',encoding="utf-8")
   filebottom=open('strategy_battle_bottom.txt',encoding="utf-8")
   file_write = open('combine_code/'+'{}battle.py'.format(req_time),'w',encoding="utf-8")
   file_write.write("req_time_two = \"{}\"\n".format(req_time))
   contents = file.readlines()
   contents2 = file2.readlines()
   contentshead=filehead.readlines()
   contentsmiddle = filemiddle.readlines()
   contentsbottom = filebottom.readlines()
   for line in contentshead:
       file_write.write(line)
   filehead.close()
   file_write.write('    '+str(line))

   for line in contents:
       file_write.write('    '+str(line))
   file.close()

   for line in contentsmiddle:
       file_write.write(line)
   filemiddle.close()

   for line in contents2:
       file_write.write('    '+str(line))
   file2.close()

   for line in contentsbottom:
       file_write.write(line)
   filebottom.close()
   file_write.close()

   exec(open('combine_code/'+'{}battle.py'.format(req_time),encoding="utf-8").read(),{})
   with open('BattleReport/{}Report.json'.format(req_time), 'r', encoding="utf-8") as json_file:
       data = json.load(json_file)
   print(req_time)
   if os.path.exists('combine_code/' + '{}battle.py'.format(req_time)):
     print('delete battle')
     #os.remove('combine_code/' + '{}battle.py'.format(req_time))
   if os.path.exists('BattleReport/{}Report.json'.format(req_time)):
     print('delete report')
     os.remove('BattleReport/{}Report.json'.format(req_time))
   if os.path.exists('pythoncodeandb/{}codea.txt'.format(req_time)):
     os.remove('pythoncodeandb/{}codea.txt'.format(req_time))
   if os.path.exists('pythoncodeandb/{}codeb.txt'.format(req_time)):
     os.remove('pythoncodeandb/{}codeb.txt'.format(req_time))
   
   return jsonify(data)
app.run(host='0.0.0.0',port=5000)





    
        
