for i in range(1, 13):
    for j in range(1, 13):
        # if j>i:
            # 注意一定要加encoding="utf-8"，要不然會error
            file = open('xmltopython/Team' + str(i) + '.txt', 'r', encoding="utf-8")
            file2 = open('xmltopython/Team' + str(j) + '.txt', 'r', encoding="utf-8")
            filehead = open('strategy_battle_head.txt', encoding="utf-8")
            filemiddle = open('strategy_battle_middle.txt', encoding="utf-8")
            filebottom = open('strategy_battle_bottom.txt', encoding="utf-8")
            file_write = open('combine_code/Team' + str(i) + ' vs Team' + str(j) + '.py', 'w', encoding="utf-8")
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
