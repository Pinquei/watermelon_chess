```markdown
# 西瓜棋 AI 對戰平台系統

本專案提供一個基於 Web 的平台，用於運行「西瓜棋」(Watermelon Chess) 的 AI 對戰。學生或使用者可以上傳他們使用 App Inventor 設計的 AI 程式（`.aia` 檔案），系統會自動處理這些程式碼，並讓不同的 AI 進行對戰，最後回傳對戰結果。

## 系統架構

主要流程如下：

1.  **上傳 (Upload)**: 使用者透過 Web 介面上傳 `.aia` 檔案。
2.  **處理 (Process)**: 伺服器解壓縮 `.aia` 檔案，提取 Blockly 程式碼 (`.bky`)，並進行初步處理（例如變數名稱替換）。
3.  **組合 (Combine)**: 伺服器將兩個參賽者的 AI 評分函數程式碼，與預設的遊戲引擎模板組合，生成一個完整的 Python 對戰腳本。
4.  **對戰 (Battle)**: 伺服器執行生成的對戰腳本，模擬完整的遊戲過程。
5.  **結果 (Result)**: 伺服器將包含詳細步驟和勝負結果的對戰報告 (JSON 格式) 回傳給使用者。

## 檔案說明

以下是專案中各個檔案的功能說明：

* **`api.py`**
    * **用途**: 系統的主要進入點，是一個 Flask Web 應用程式。
    * **功能**:
        * 提供 `/upload` API 接口，接收使用者上傳的 `.aia` 檔案和隊伍資訊。
        * 呼叫 `unzip_and_return.py` 來處理上傳的檔案。
        * 提供 `/battle` API 接口，接收兩個 AI 的 Python 程式碼。
        * 動態組合對戰腳本（使用 `.txt` 模板和 AI 程式碼）。
        * 使用 `exec()` 執行對戰腳本 (**注意：存在安全風險，建議改進**)。
        * 讀取並回傳 JSON 格式的對戰結果。
        * 管理和清理執行過程中產生的暫存檔案。

* **`unzip_and_return.py`**
    * **用途**: 處理從 App Inventor 導出的 `.aia` 檔案。
    * **功能**:
        * 解壓縮 `.aia` 檔案，找到並提取 Blockly 程式碼 (`Screen2.bky`)。
        * 從 Blockly XML 中提取核心的「盤面評分」函數部分。
        * 進行必要的變數名稱替換（例如，將 App Inventor 中的中文變數名，如 "棋子位置"、"分數"、"玩家"、"電腦" 等，替換為 Python 腳本中使用的變數名，如 `temp_board`, `score`, `my_player_id`, `opponent_player_id` 等）。
        * 將處理後的 Blockly XML 區塊返回給 `api.py`。

* **`strategy_battle.py`**
    * **用途**: 包含了完整的西瓜棋遊戲核心邏輯和 AI 對戰框架的原始版本。
    * **功能**:
        * 定義遊戲規則、棋盤結構、棋子移動、吃子判斷 (`Neighbor`, `Exist_Chess`, `Group`, `Alive`, `Move_Chess`, `Chess_Eliminate`)。
        * 定義勝負判斷邏輯 (`Winner`) 和遊戲狀態更新 (`Update_Condition`)。
        * 包含 AI 決策的基本框架 (`AI_Play`)，使用評分函數來選擇最佳移動。
        * 提供了 AI 評分函數的範例。
        * 包含遊戲主迴圈 (`main`)，用於驅動對戰進行。
    * **注意**: 實際運行時，遊戲邏輯主要由 `.txt` 模板文件提供，但此檔案是理解遊戲規則和 AI 運作方式的重要參考。

* **`strategy_battle_head.txt`**[cite: 21], **`strategy_battle_middle.txt`**[cite: 43], **`strategy_battle_bottom.txt`** [cite: 1]
    * **用途**: 這三個是文字模板檔案，用於動態生成最終執行的對戰腳本。
    * **功能**:
        * `head.txt`: 包含對戰腳本開頭的 import、全域變數、核心遊戲函數定義，以及紅方 AI 評分函數 (`AI_Score_Red_Side`) 的開頭。
        * `middle.txt`: 包含紅方 AI 評分函數的結尾，以及黃方 AI 評分函數 (`AI_Score_Yellow_Side`) 的開頭。
        * `bottom.txt`: 包含黃方 AI 評分函數的結尾、AI 輔助函數、`AI_Play` 函數和 `main` 函數的完整定義。
    * `api.py` 會將參賽者的 AI 程式碼插入這些模板的適當位置，組合成完整的可執行 Python 檔案。

* **`combine.py`**
    * **用途**: 一個獨立的（或較早版本的）腳本，用於將 `xmltopython` 文件夾中的 Python AI 程式碼兩兩組合，並使用 `.txt` 模板生成對戰腳本。
    * **注意**: 目前 `api.py` 中的 `/battle` 接口是自己實現了組合邏輯，可能並未直接使用此腳本。此文件或可作為參考或用於離線批量生成對戰腳本。

* **`code_transfer.py`**
    * **用途**: 一個獨立的（或較早版本的）腳本，用於將特定文件夾中的 Blockly 程式碼（`.txt` 格式）裡的中文字元替換為 `C` 開頭的代碼。
    * **注意**: 其部分功能與 `unzip_and_return.py` 重疊，目前可能未在主流程 (`api.py`) 中直接使用。

## 目錄結構 (推測)

```
.
├── api.py                     # 主要 Flask 應用程式
├── unzip_and_return.py        # AIA 處理工具
├── combine.py                 # (輔助/舊版) 程式碼組合工具
├── code_transfer.py           # (輔助/舊版) 變數名稱轉換工具
├── strategy_battle.py         # 核心遊戲邏輯參考
├── strategy_battle_head.txt   # 對戰腳本模板 (頭部)
├── strategy_battle_middle.txt # 對戰腳本模板 (中部)
├── strategy_battle_bottom.txt # 對戰腳本模板 (底部)
├── WaTErmelonChess/           # 存放解壓後的 .bky 檔案 (臨時)
├── CodeTransfer/              # 存放處理後的 Blockly XML 或 Python 程式碼片段 (臨時)
├── pythoncodeandb/            # 存放從前端接收的 AI 程式碼 (臨時)
├── combine_code/              # 存放組合生成的完整對戰腳本 (臨時)
├── BattleReport/              # 存放生成的對戰報告 JSON 檔案 (臨時/永久?)
├── venv/                      # (建議) Python 虛擬環境
└── requirements.txt           # (建議) 專案依賴列表
```

## 如何運行 (基本步驟)

1.  **設定環境**:
    * 確保已安裝 Python。
    * (建議) 建立並啟用 Python 虛擬環境。
    * 安裝所需的函式庫 (主要為 Flask, Flask-CORS, func-timeout)。建議創建 `requirements.txt` 文件。
        ```bash
        pip install Flask Flask-CORS func-timeout
        ```
2.  **創建所需目錄**: 確保 `WaTErmelonChess`, `CodeTransfer`, `pythoncodeandb`, `combine_code`, `BattleReport` 這些目錄存在。
3.  **運行伺服器**:
    ```bash
    python api.py
    ```
    伺服器將在 `0.0.0.0:5000` 上運行。
4.  **客戶端**: 需要一個前端應用程式來與 `/upload` 和 `/battle` API 進行互動。

## 注意事項與尚須改進部分

* **安全**: 使用 `exec()` 執行來自使用者輸入（間接來自 `.aia` 檔案）的程式碼**非常危險**。強烈建議使用沙箱 (Sandbox) 環境或 `subprocess` 來隔離執行對戰腳本，限制其權限。
* **錯誤處理**: 增加更詳細的錯誤處理和日誌記錄。
* **暫存檔案**: 使用 `tempfile` 模組管理臨時檔案可能更佳。
* **程式碼一致性**: 整合 `api.py` 和 `combine.py` 中的程式碼組合邏輯。確認 `code_transfer.py` 是否仍需保留。
* **設定**: 將硬編碼的路徑和設定（如超時時間）移到設定檔或環境變數中。
```