#!/usr/bin/env python
# coding: utf-8

# In[7]:


# 這裡先將有中文的部分一律轉成英文，因為Transfer時有的中文可以順利直接轉有的卻會變亂碼
# 由於無法解決Transfer的問題，雖然python支援中文變數命名，還是都轉成英文
chinese_to_var = []
for i in range (10, 11):
    file = open('ScoringFuncBlock/Team' + str(i) + '.txt', 'r', encoding="utf-8")
    file_write = open('CodeTransfer/Team' + str(i) + '.txt', 'w')
    contents = file.readlines()
    for line in contents:
        contents.line = line.replace('global 棋子位置','global_chess_position')

    for line in contents:
        for ch in line:
            if (u'\u4e00' <= ch and ch <= u'\u9fff') and ch not in chinese_to_var:
                chinese_to_var.append(ch)
            if ch in chinese_to_var:
                file_write.write('C' + str(chinese_to_var.index(ch)))
            else:
                file_write.write(ch)

    file.close()
    file_write.close()


# In[ ]:


# 處理如何呼叫blockly的transfer code system(JavaScript...)，將block轉成python code

