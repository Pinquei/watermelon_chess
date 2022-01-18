import os

def combine():
    entries = os.listdir('xmltopython')
    #print(entries)

    for i in entries:
        for j in entries:
            # if j>i:
                # 注意一定要加encoding="utf-8"，要不然會error
                file = open('xmltopython/' + str(i), 'r', encoding="utf-8")
                file2 = open('xmltopython/' + str(j), 'r', encoding="utf-8")
                filehead = open('strategy_battle_head.txt', encoding="utf-8")
                filemiddle = open('strategy_battle_middle.txt', encoding="utf-8")
                filebottom = open('strategy_battle_bottom.txt', encoding="utf-8")
                file_write = open('combine_code/' + str(i)[0:-4] + ' vs ' + str(j)[0:-4] + '.py', 'w', encoding="utf-8")
                contents = file.readlines()
                contents2 = file2.readlines()
                contentshead = filehead.readlines()
                contentsmiddle = filemiddle.readlines()
                contentsbottom = filebottom.readlines()
                # 把盤面評分函式的部分，開頭和結束分別是第幾行找到，存在line_id_start和line_id_end
                for line in contentshead:
                    file_write.write(line)
                filehead.close()

                for line in contents:
                    file_write.write('    ' + str(line))
                file.close()

                for line in contentsmiddle:
                    file_write.write(line)
                filemiddle.close()

                for line in contents2:
                    file_write.write('    ' + str(line))
                file2.close()

                for line in contentsbottom:
                    file_write.write(line)
                filebottom.close()
                file_write.close()

