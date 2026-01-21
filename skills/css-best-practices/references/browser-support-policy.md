# 瀏覽器支援政策與 CSS 技術評估指引

本文件整合公司的瀏覽器支援規格，提供 CSS 技術可行性評估的完整指引。

---

## 公司瀏覽器支援政策

### 基本原則

**關於 iOS/iPadOS 版本定義**

本規格採用滾動式版本支援，**N** 代表目前 Apple 官方發布之最新主要版本。

確認最新版本號 (N) 請參考：
- [iOS version history - Wikipedia](https://en.wikipedia.org/wiki/IOS_version_history)
- 使用 WebSearch 查詢：`"iOS version history" site:wikipedia.org`

### 支援範圍

#### 電腦版
- 支援主流瀏覽器 Chrome、Firefox、Edge、Safari 之 **最新正式發布版本 (Latest Stable Release)**
- **不支援** Internet Explorer (IE) 所有版本

#### 平板與手機

**Android**
- Chrome、Firefox 之最新正式發布版本

**iOS / iPadOS**（採用 N-2 滾動式支援策略）
- **完整支援**：最新主要版本 (N) 及 前一個主要版本 (N-1)
- **僅確保基本瀏覽**：再前一個主要版本 (N-2)
- **停止支援**：低於 N-2 之所有舊版本（因資安考量與技術限制，建議使用者自行升級）

**「僅確保基本瀏覽」定義**
- ✅ 可正常使用：網站基本版面配置、文字內容閱讀、連結點擊
- ⚠️ 可能無法使用：動態效果、進階互動功能、部分視覺樣式

---

## iOS 版本滾動式支援機制

Apple 發布新版 iOS 通常會於每年 9 月，本規範之支援版本將隨 Apple 官方發布時程自動與時俱進。

### 滾動更新示意（以 2026.01 為例）

由於 Apple 於 2025 年統一調整版本策略，直接由 iOS 18 跨越至 iOS 26，支援列表會自動適應如下：

- **完整支援**：
  - **目前最新版本 (N)**：iOS 26 / iPadOS 26
  - **前一版本 (N-1)**：iOS 18 / iPadOS 18（*註：中間跳過 19-25*）
- **基本瀏覽**：**再前一個主要版本 (N-2)**：iOS 17 / iPadOS 17
- **停止支援**：iOS 16 / iPadOS 16（含）以下

**重要提醒**：每年 9 月 Apple 發布新版本後，支援列表會自動更新。評估 CSS 技術時，務必先確認當前的 N 值。

---

## iOS 瀏覽器限制說明

### 技術限制

因為 Apple 的 App Store 政策規定，iOS 所有第三方瀏覽器（含 Chrome、Firefox）**強制使用 WebKit 引擎**。

具體限制包括：
1. Chrome 無法使用其原生的 Blink 引擎，Firefox 也無法使用其 Gecko 引擎
2. 瀏覽器的 JavaScript 效能受到限制，因為他們無法使用自己的 JavaScript 引擎
3. 某些網頁功能可能無法正常運作，因為必須遵循 WebKit 的實作方式

### 歐盟特例（iOS 17.4+）
- 僅歐盟經濟區可使用非 WebKit 引擎
- 需符合 Apple 安全規範、審核要求及商業協議

### 技術影響

**JavaScript 限制**
- JavaScript 引擎效能取決於 WebKit
- 部分網頁功能可能無法完整支援

**CSS 限制**
- 在 iOS 中所有瀏覽器 CSS 支援度與 iOS Safari (WebKit) 一致
- 新功能支援進度會依賴 WebKit 實作時程
- **評估 CSS 技術時，只需查看 iOS Safari 的支援度即可**

---

## CSS 技術可行性評估流程

### 核心概念：核心功能 vs 加分特效

**核心功能**（影響網站主要架構排版或內容顯示）
- 必須支援到「僅確保基本瀏覽」版本（N-2）
- 建議達到 [Baseline Widely available](https://developer.mozilla.org/en-US/docs/Glossary/Baseline/Compatibility#baseline_badges) 標準
- 範例：CSS Grid、Flexbox、基本選擇器

**加分特效**（提升體驗的裝飾性質）
- 只需支援「完整支援」版本（N 和 N-1）
- 建議達到 [Baseline Newly available](https://developer.mozilla.org/en-US/docs/Glossary/Baseline/Compatibility#baseline_badges) 標準
- 範例：Scroll-driven Animations、text-autospace

### 評估步驟

**步驟 1: 確認當前支援政策**

使用 WebSearch 查詢最新 iOS 版本：
```
查詢語句範例：
"iOS version history" site:wikipedia.org
"latest iOS version 2026"
```

確認當前的 N、N-1、N-2 值（例如：2026.01 時為 26、18、17）

**步驟 2: 技術支援度檢查**

在 [MDN](https://developer.mozilla.org/) 或 [caniuse.com](https://caniuse.com/) 確認該技術標註狀態：

使用 WebFetch 查詢：
```
URL: https://caniuse.com/?search=[CSS技術名稱]
Prompt: "請提取這個 CSS 技術的瀏覽器支援資訊，特別是 iOS Safari 的最低支援版本"
```

或使用 WebSearch：
```
查詢語句範例：
"CSS Grid browser support iOS Safari"
"CSS Nesting caniuse iOS"
```

**步驟 3: 判斷技術類型**

- 這個技術是「核心功能」還是「加分特效」？
- 核心功能：若不支援會導致版面崩壞或內容無法顯示
- 加分特效：若不支援僅缺少額外效果，但不影響基本閱讀

**步驟 4: 對照決策樹**

根據技術類型和支援度做出決策（見下方決策樹）

---

## 決策樹

```
需要使用某個 CSS 技術？
│
├─ 步驟 1: 確認當前支援政策 (N, N-1, N-2)
│  └─ 查詢 iOS version history
│
├─ 步驟 2: 查詢技術支援度
│  ├─ 查詢 caniuse.com / MDN
│  └─ 確認 iOS Safari 最低支援版本
│
├─ 步驟 3: 判斷技術類型
│  ├─ 核心功能？
│  │  ├─ iOS 最低支援版本 <= N-2？
│  │  │  ├─ 是 → ✅ 可直接使用
│  │  │  └─ 否 → ❌ 不建議使用，需等到支援度提升或使用降級方案
│  │  └─ 達到 Baseline Widely available？
│  │     ├─ 是 → ✅ 優先使用
│  │     └─ 否 → ⚠️ 謹慎使用，需提供 fallback
│  │
│  └─ 加分特效？
│     ├─ iOS 最低支援版本 <= N-1？
│     │  ├─ 是 → ✅ 可使用（漸進增強）
│     │  └─ 否 → ⚠️ 僅在 N 版本使用，舊版自然降級
│     └─ 達到 Baseline Newly available？
│        ├─ 是 → ✅ 可使用
│        └─ 否 → ⚠️ 實驗性質，謹慎使用
```

---

## 實際評估案例

### 案例一：CSS Grid

**查詢結果**（範例）
- Baseline 狀態：Widely available
- iOS Safari 最低支援版本：iOS 10.3+

**評估結果**（2026.01 時間點）
- 公司支援範圍：完整支援 26、18；基本瀏覽 17
- 技術類型：**核心功能**（影響版面佈局）
- **結論**：✅ 可直接使用，無需降級方案
- **原因**：支援度已達 Baseline Widely available，且支援版本遠低於公司最低支援版本

### 案例二：CSS Nesting

**查詢結果**（範例）
- Baseline 狀態：2023 Newly available
- iOS Safari 最低支援版本：iOS 16.5 (部分支援) / iOS 17.2 (完整支援)

**評估結果**（2026.01 時間點）
- 公司支援範圍：完整支援 26、18；基本瀏覽 17
- 技術類型：**核心功能**（影響 CSS 架構處理）
- **結論**：❌ 不建議直接使用（若要使用需設定轉譯）
- **原因**：
  - 未達到 Baseline Widely available 標準
  - 雖然「基本瀏覽」版本已推進至 iOS 17，但 iOS 17.0 - 17.1 僅為部分支援（不支援 Type Selectors 巢狀寫法），若直接使用原生語法，在 iOS 17.0/17.1 設備上可能導致版面崩壞，未完全符合「確保基本瀏覽」之定義
- **建議作法**：
  - 先維持使用傳統的 CSS 寫法，直到該技術與公司當時的支援政策的最低版本相容
  - 若需要先用該技術，可以在本機進行，要部署時則使用 SCSS/SASS 進行轉譯後的傳統 CSS

### 案例三：CSS text-autospace

**查詢結果**（範例）
- Baseline 狀態：2025 Newly available
- iOS Safari 最低支援版本：iOS 18.4+

**評估結果**（2026.01 時間點）
- 公司支援範圍：完整支援 26、18；基本瀏覽 17
- 技術類型：**加分特效**（改善閱讀體驗，非必要）
- **結論**：✅ 建議直接使用（作為漸進增強）
- **原因**：
  - **屬於加分特效**：此屬性用於改善閱讀體驗（中英文間距），若瀏覽器不支援，文字仍可正常閱讀，僅缺少額外間距，不影響版面功能，符合「僅確保基本瀏覽」之定義
  - **替代方案優勢**：相較於傳統使用的 JavaScript 解決方案（如 `pangu.js`），原生 CSS 效能更佳且無載入延遲導致的版面跳動 (Layout Shift)
- **建議作法**：
  - 設定 `text-autospace: normal` 以啟用預設的中英數自動間距
  - 無需針對舊版瀏覽器製作 Polyfill，讓其自然降級（Graceful Degradation）即可

### 案例四：WebP 圖檔格式

**查詢結果**（範例）
- Baseline 狀態：Widely available
- iOS Safari 最低支援版本：iOS 14.0+

**評估結果**（2026.01 時間點）
- 公司支援範圍：完整支援 26、18；基本瀏覽 17
- 技術類型：**核心功能**（影響內容顯示）
- **結論**：✅ 可直接使用
- **原因**：
  - **技術成熟度**：已達到 Baseline Widely available 標準，且支援版本 (iOS 14) 遠低於公司目前最低支援的 iOS 17
- **建議作法**：
  - 可將 WebP 作為專案預設圖檔格式，無需額外提供降級圖檔，除非有極特殊的舊版系統需求

### 案例五：CSS `:has()` 選擇器

**查詢結果**（範例）
- Baseline 狀態：2023 Newly available
- iOS Safari 最低支援版本：iOS 15.4+

**評估結果**（2026.01 時間點）
- 公司支援範圍：完整支援 26、18；基本瀏覽 17
- 技術類型：**核心功能**（影響版面結構控制）
- **結論**：✅ 可直接使用
- **原因**：
  - 雖然是 Newly available，但其最低支援版本 (iOS 15.4) 已完整覆蓋公司「基本瀏覽」定義要求的 iOS 17
- **建議作法**：
  - 可全面取代過去需要透過 JavaScript 切換 Class 來控制父層樣式的作法，提升開發效率與效能

### 案例六：滾動驅動動畫 (Scroll-driven Animations)

**查詢結果**（範例）
- Baseline 狀態：尚未達到 Baseline 穩定支援（WebKit 仍於實驗階段或新版導入）
- iOS Safari 最低支援版本：iOS 18+ (預期)

**評估結果**（2026.01 時間點）
- 公司支援範圍：完整支援 26、18；基本瀏覽 17
- 技術類型：**加分特效**（視覺動畫，非必要）
- **結論**：✅ 建議作為漸進增強（加分特效）使用
- **原因**：
  - **屬於加分特效**：捲動視覺動畫屬於提升體驗的裝飾性質，若不支援，使用者仍能正常閱讀內容與操作連結，符合「基本瀏覽」定義
  - **版本限制**：此技術在 iOS 17 (N-2) 上無法運作，不符合核心功能需支援到 N-2 的原則
- **建議作法**：
  - 針對支援的裝置提供流暢的原生 CSS 動畫
  - 在 iOS 17 等舊版裝置上讓其自然降級，不需為了實現動畫效果而載入額外的 Polyfill

---

## 快速檢查清單

在使用新的 CSS 技術前，請確認：

- [ ] 已查詢當前的 iOS 版本支援政策（N, N-1, N-2）
- [ ] 已在 caniuse.com 或 MDN 查詢該技術的支援度
- [ ] 已確認該技術在 iOS Safari 的最低支援版本
- [ ] 已判斷該技術是「核心功能」還是「加分特效」
- [ ] 核心功能：確認最低支援版本 <= N-2
- [ ] 加分特效：確認可在舊版自然降級，不影響基本瀏覽
- [ ] 如需使用新技術但支援度不足，已準備降級方案或轉譯工具

---

## 參考資源

- **iOS 版本歷史**：https://en.wikipedia.org/wiki/IOS_version_history
- **Can I Use**：https://caniuse.com/ - 瀏覽器支援查詢
- **MDN Web Docs**：https://developer.mozilla.org/zh-TW/ - 完整文件與 Baseline 標註
- **Baseline**：https://web.dev/baseline/ - 跨瀏覽器支援狀態說明
