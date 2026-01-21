# CSS Best Practices Skill (netiCRM 專用版)

這是一個專門協助撰寫高品質 CSS 程式碼的 Claude Skill,特別針對 **netiCRM/CiviCRM 專案**優化,強制要求選擇器加上 `.crm-container` 前綴以實現樣式隔離。

## 設計目標

解決 AI 撰寫 CSS 的核心問題,並針對 netiCRM 專案特性優化:

1. **視覺渲染與文本預測的衝突** - 透過明確的空間推理檢查清單
2. **上下文缺失與全域特性** - 強調權重管理和 @layer 使用
3. **訓練資料的新舊混雜** - 明確列出現代/過時特性對照
4. **缺乏語意與抽象化** - 提供命名規範和樣式提取指引
5. **🆕 netiCRM 樣式隔離** - 自動檢查 `.crm-container` 前綴,防止全域污染

## Skill 結構

```
css-best-practices/
├── SKILL.md                           # 核心技能指引
├── references/                        # 參考文件
│   ├── neticrm-guidelines.md          # 🆕 netiCRM/CiviCRM 專用指引
│   ├── tailwind-guidelines.md         # Tailwind CSS 詳細指引
│   ├── css-modules-guidelines.md      # CSS Modules 使用規範
│   └── modern-css-features.md         # 現代 CSS 特性支援表
└── scripts/                           # 工具腳本
    └── check_css_quality.py           # CSS 品質檢查工具 (支援 CRM 檢查)
```

## 安裝方式

### 在 claude.ai 使用

1. 將整個 `css-best-practices` 資料夾壓縮成 ZIP 檔
2. 到 claude.ai > Settings > Features
3. 上傳 ZIP 檔案

### 在 Claude Code 使用

```bash
# 複製到個人 skills 資料夾 (全專案可用)
cp -r css-best-practices ~/.claude/skills/

# 或複製到專案 skills 資料夾 (僅該專案)
cp -r css-best-practices /path/to/project/.claude/skills/
```

### 透過 API 使用

參考 Anthropic 官方文件的 Skills API 章節。

## 使用範例

安裝後,Claude 會在以下情境自動啟用此 skill:

### 範例 1: netiCRM 專案開發 (🆕 主要使用情境)

```
User: 幫我寫一個 CiviCRM 的操作按鈕列 CSS

Claude 會:
1. 啟動 css-best-practices skill
2. 自動加上 .crm-container 前綴
3. 使用現代 Flexbox 佈局
4. 遵循 netiCRM 命名規範
5. 提供響應式設計

輸出範例:
.crm-container .crm-actions-ribbon {
  display: flex;
  gap: 0.5rem;
  padding: 1rem;
}

.crm-container .crm-button-primary {
  background: var(--crm-color-primary);
  padding: 0.5rem 1rem;
}
```

### 範例 2: 檢查現有 netiCRM CSS

```
User: 幫我檢查這段 netiCRM CSS 有沒有問題
[貼上 CSS 程式碼]

Claude 會:
1. 使用 check_css_quality.py --civicrm 分析
2. 檢查是否缺少 .crm-container 前綴
3. 指出使用過時特性 (如 float)
4. 建議改用現代方法
5. 提供重構後的程式碼
```

### 範例 3: 撰寫新的 CSS (一般專案)

```
User: 幫我寫一個卡片元件的 CSS,要有圓角、陰影,hover 時有動畫效果

Claude 會:
1. 啟動 css-best-practices skill
2. 使用現代 CSS (Grid/Flexbox)
3. 避免過度限定選擇器
4. 使用 CSS Variables
5. 提供語意化的 class 命名
```

### 範例 4: Tailwind 開發

```
User: 用 Tailwind 做一個響應式導覽列

Claude 會:
1. 讀取 tailwind-guidelines.md
2. 使用正確的 class 名稱 (避免幻覺)
3. 實作 mobile-first 響應式設計
4. 不會發明不存在的 class
```

## 核心特性

### 🆕 1. netiCRM/CiviCRM 專案優化

- ✅ 自動加上 `.crm-container` 前綴
- ✅ 檢測缺少前綴的選擇器
- ✅ 識別允許的例外情況
- ✅ 自動偵測 CiviCRM 相關檔案

### 2. 現代 CSS 優先

- ✅ 使用 Grid/Flexbox 取代 float
- ✅ 使用 clamp() 取代固定值
- ✅ 使用 Logical Properties
- ❌ 禁止過時的 clearfix hack

### 3. 架構優先

- 使用 @layer 管理權重
- 避免 !important 濫用
- 單一 class 選擇器 (CRM 的 .crm-container 除外)
- 提取共用樣式

### 4. 框架專門指引

- **netiCRM**: 完整的 .crm-container 規範和檢查
- **Tailwind**: 正確 class 名稱、避免幻覺
- **CSS Modules**: composition、命名規範
- **現代特性**: 瀏覽器支援度參考

### 5. 品質檢查工具

Python 腳本自動檢測:
- 🆕 **CiviCRM 前綴檢查** (--civicrm 模式)
- !important 濫用
- float 佈局
- clearfix hack
- vendor prefixes
- 過度限定選擇器
- 魔術數字

## 測試 Skill

### 測試一般 CSS (不良範例)

建立測試檔案:

```css
/* test-bad.css */
.container::after {
  content: "";
  display: table;
  clear: both;
}

div.box {
  float: left;
  width: 200px !important;
}
```

執行檢查:

```bash
python scripts/check_css_quality.py test-bad.css
```

預期輸出會指出:
- ❌ 使用了 clearfix hack
- ❌ 使用了 float 佈局
- ⚠️ 使用了 !important
- ⚠️ 過度限定的選擇器 (div.box)

### 🆕 測試 CiviCRM CSS (不良範例)

建立測試檔案:

```css
/* test-civicrm-bad.css */
/* ❌ 缺少 .crm-container 前綴 */
.crm-actions-ribbon {
  background: #f5f5f5;
}

.crm-submit-buttons {
  display: flex;
}
```

執行檢查:

```bash
# 方法 1: 自動偵測 (檔名包含 'crm')
python scripts/check_css_quality.py test-civicrm-bad.css

# 方法 2: 明確指定 CiviCRM 模式
python scripts/check_css_quality.py test-bad.css --civicrm
```

預期輸出會指出:
- ❌ **CiviCRM 選擇器缺少 .crm-container 前綴**
- 建議改為: `.crm-container .crm-actions-ribbon`

### 🆕 測試 CiviCRM CSS (良好範例)

```css
/* test-civicrm-good.css */
/* ✅ 正確加上 .crm-container 前綴 */
.crm-container .crm-actions-ribbon {
  background: #f5f5f5;
  display: flex;
  gap: 0.5rem;
}

/* ✅ 允許的例外 */
#civicrm-menu {
  z-index: 9999;
}
```

執行檢查應該通過,只有少量或零錯誤。

## 客製化

### 調整 SKILL.md

根據團隊需求修改核心原則,例如:

```markdown
## 團隊特定規範

- 使用 BEM 命名規範
- 間距使用 8px 基準網格
- 顏色使用 Design Token
```

### 新增 references

建立團隊專屬的參考文件:

```
references/
├── company-design-system.md
├── accessibility-checklist.md
└── performance-guidelines.md
```

### 擴充檢查腳本

編輯 `check_css_quality.py` 新增客製化檢查:

```python
def check_design_tokens(self):
    """檢查是否使用 Design Tokens"""
    # 實作邏輯...
```

## 效能考量

此 skill 使用漸進式揭露:

- **Metadata** (~100 tokens): 總是載入
- **SKILL.md** (~5000 tokens): 觸發時載入
- **References** (~15000 tokens): 按需載入
- **Scripts**: 執行時不佔用 context

## 已知限制

1. **無法執行視覺驗證**: AI 無法真正「看到」渲染結果
2. **框架更新**: Tailwind 等框架更新時需手動更新 references
3. **腳本執行環境**: 需要 Python 3.6+ 環境

## 維護建議

### 定期更新

1. **每季更新** `modern-css-features.md` 的瀏覽器支援度
2. **框架升級時更新** Tailwind/框架相關文件
3. **收集團隊回饋** 持續改進規範

### 版本控制

```bash
# 建議使用 Git 追蹤變更
cd css-best-practices
git init
git add .
git commit -m "Initial CSS skill setup"
```

## 貢獻與回饋

發現問題或有改進建議:

1. 測試並記錄問題情境
2. 提出具體的改進方案
3. 更新相關文件

## 授權

本 skill 採用 MIT License,可自由使用和修改。

## 參考資源

- [Agent Skills 官方文件](https://docs.anthropic.com/en/docs/build-with-claude/agent-skills)
- [CSS 現代特性 - MDN](https://developer.mozilla.org/zh-TW/docs/Web/CSS)
- [Tailwind CSS 官方文件](https://tailwindcss.com/docs)
- [Can I Use - 瀏覽器支援查詢](https://caniuse.com/)
