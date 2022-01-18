import zipfile
import re
import glob
import shutil
import os
from xml.dom import minidom

def format_xml(input_str):
    str = minidom.parseString(input_str)
    output_str = str.toprettyxml(indent="    ")
    return output_str

# 這裡預設希望上傳檔案時自動將.aia檔改名成WatermelonChess_TeamX.aia
# 執行解壓縮
def aia_to_xml(file_name,team_number):
    if os.path.exists('WaTErmelonChess/Screen2.bky'):
        os.remove('WaTErmelonChess/Screen2.bky')

    aia_file_name = file_name
    unzip = zipfile.ZipFile(aia_file_name+'.aia', 'r') #主要解壓縮的Function
    for names in unzip.namelist():
        # 所要的block在Screen2的部分，這裡只把Screen2.bky抓出來
        if re.search("Screen2.bky", names):
            unzip.extract(names, aia_file_name + '/')
            break
    unzip.close()
    target = glob.glob(aia_file_name + "/*/*/*/*/Screen2.bky")[0]
    # 把Screen2.bky移到統一資料夾裡，並改名成TeamX.bky
    shutil.move(target, 'WaTErmelonChess/')
    shutil.rmtree(aia_file_name + '/')
    file = open('WaTErmelonChess/Screen2.bky','r',encoding="utf-8")
    contents=file.readlines()
    if len(contents)<20:
        ostr=''
        for line in contents:
            ostr=ostr+line
        output=format_xml(ostr)
        file_write=open('WaTErmelonChess/Screen2.bky','w',encoding="utf-8")
        file_write.write(output)
        file_write.close()
    file.close()
    os.rename('WaTErmelonChess/Screen2.bky', 'WaTErmelonChess/' + team_number + '.bky')

    chinese_to_var = []
    return_word='<xml xmlns="https://developers.google.com/blockly/xml">'
    # 注意一定要加encoding="utf-8"，要不然會error
    file = open('WaTErmelonChess/' + team_number + '.bky', 'r', encoding="utf-8",errors='ignore')

    file_write = open('CodeTransfer/' + team_number[11:16]+ '.txt', 'w',errors='ignore')
    contents = file.readlines()
    # 把盤面評分函式的部分，開頭和結束分別是第幾行找到，存在line_id_start和line_id_end
    line_id = 0
    line_id_start = -1
    find_start = False
    line_id_end = -1
    for line in contents:
        # 先確認該行有沒有出現盤面評分四個字，然後回推前四行是不是procedures_defreturn類別
        if line.find('盤面評分') != -1 and contents[line_id - 4].find('procedures_defreturn') != -1:
            line_id_start = line_id - 4
            find_start = True
        # 找到開頭後找到結尾處
        elif find_start == True and contents[line_id].find('分數') != -1 and contents[line_id - 1].find('lexical_variable_get') != -1and contents[line_id - 2].find('VALUE') != -1:
            line_id_end = line_id - 4
            break
        line_id = line_id + 1
    file.close()
    # 把盤面評分函式的blocks複製到新文件，並且加上開頭結尾以利之後轉換用
    file_write.write(repr('<xml xmlns="https://developers.google.com/blockly/xml">')[1:-1] + '\n')
    for i in range(line_id_start+20, line_id_end+1):
        contents[i] = contents[i].replace("global 棋子位置", "temp_board")
        contents[i] = contents[i].replace("分數", "score")
        contents[i] = contents[i].replace("_生存", "fun_Alive")
        contents[i] = contents[i].replace("_群組", "fun_Group")
        contents[i] = contents[i].replace("global 電腦", "global_yellow_side")
        contents[i] = contents[i].replace("global 玩家", "global_red_side")
        contents[i] = contents[i].replace("_是否有棋", "Exist_Chess")
        contents[i] = contents[i].replace("盤面", "board")
        contents[i] = contents[i].replace("_鄰居", "Neighbor")
        contents[i] = contents[i].replace("當前下棋者","current_player")
        contents[i] = contents[i].replace("下位下棋者", "next_player")
        print('test')

        for ch in contents[i]:
            if (u'\u4e00' <= ch and ch <= u'\u9fff') and ch not in chinese_to_var:
                chinese_to_var.append(ch)
            if ch in chinese_to_var:
                file_write.write('C' + str(chinese_to_var.index(ch)))
                return_word = return_word + 'C'+ str(chinese_to_var.index(ch))
            else:
                file_write.write(ch)
                return_word = return_word + ch

    file_write.write(repr('<yacodeblocks ya-version="208" language-version="33"></yacodeblocks>')[1:-1] + '\n')
    file_write.write(repr('</xml>')[1:-1] + '\n')
    #contents = file.readlines()
    return_word=return_word+'<yacodeblocks ya-version="208" language-version="33"></yacodeblocks></xml>'
    print(return_word)
    file_write.close()
    os.remove('WaTErmelonChess/' + team_number + '.bky')
    return return_word






