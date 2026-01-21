#!/usr/bin/env python3
"""
CSS 品質檢查腳本
檢查常見的 CSS 反模式和最佳實踐違規
"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple

class CSSQualityChecker:
    def __init__(self, css_content: str):
        self.css_content = css_content
        self.issues: List[Dict] = []
        
    def check_all(self, is_civicrm_project: bool = False) -> List[Dict]:
        """執行所有檢查"""
        self.check_important_usage()
        self.check_float_layout()
        self.check_clearfix()
        self.check_vendor_prefixes()
        self.check_over_qualified_selectors()
        self.check_magic_numbers()
        self.check_inline_styles()
        
        # CiviCRM 專案特殊檢查
        if is_civicrm_project:
            self.check_crm_container_prefix()
        
        return self.issues
    
    def check_important_usage(self):
        """檢查 !important 濫用"""
        pattern = r'!important'
        matches = re.finditer(pattern, self.css_content)
        count = sum(1 for _ in matches)
        
        if count > 0:
            self.issues.append({
                'type': 'warning',
                'category': 'specificity',
                'message': f'發現 {count} 處使用 !important',
                'suggestion': '除非覆蓋第三方樣式或 utility class,應避免使用 !important'
            })
    
    def check_float_layout(self):
        """檢查使用 float 做佈局"""
        pattern = r'float:\s*(left|right)'
        matches = re.finditer(pattern, self.css_content, re.IGNORECASE)
        
        for match in matches:
            self.issues.append({
                'type': 'error',
                'category': 'layout',
                'message': f'使用了過時的 float 佈局: {match.group(0)}',
                'suggestion': '使用 Flexbox 或 Grid 取代 float 佈局'
            })
    
    def check_clearfix(self):
        """檢查 clearfix hack"""
        patterns = [
            r'clear:\s*both',
            r'::after.*clear:\s*both',
            r'content:\s*["\']\\s*["\'].*clear'
        ]
        
        for pattern in patterns:
            if re.search(pattern, self.css_content, re.IGNORECASE):
                self.issues.append({
                    'type': 'error',
                    'category': 'layout',
                    'message': '使用了 clearfix hack',
                    'suggestion': '現代瀏覽器不需要 clearfix,使用 Flexbox 或 Grid'
                })
                break
    
    def check_vendor_prefixes(self):
        """檢查手寫的 vendor prefixes"""
        pattern = r'-(webkit|moz|ms|o)-'
        matches = re.finditer(pattern, self.css_content)
        
        for match in matches:
            self.issues.append({
                'type': 'warning',
                'category': 'compatibility',
                'message': f'手寫的 vendor prefix: {match.group(0)}',
                'suggestion': '使用 Autoprefixer 自動處理 vendor prefixes'
            })
    
    def check_over_qualified_selectors(self):
        """檢查過度限定的選擇器"""
        # 匹配像 div.class 或 ul > li > a 這樣的選擇器
        patterns = [
            r'\b(div|span|ul|ol|li|p|a|h[1-6])\.[a-zA-Z]',  # 元素+class
            r'[>\s]+\w+[>\s]+\w+[>\s]+\w+',  # 三層以上嵌套
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, self.css_content)
            for match in matches:
                # 跳過註解
                if not self._is_in_comment(match.start()):
                    self.issues.append({
                        'type': 'warning',
                        'category': 'specificity',
                        'message': f'過度限定的選擇器: {match.group(0)}',
                        'suggestion': '使用單一 class 選擇器,避免元素+class 組合'
                    })
    
    def check_magic_numbers(self):
        """檢查魔術數字 (硬編碼的像素值)"""
        # 檢查大量的絕對像素值
        pattern = r':\s*(\d{2,})px'
        matches = re.finditer(pattern, self.css_content)
        magic_numbers = [m.group(1) for m in matches if int(m.group(1)) > 16]
        
        if len(magic_numbers) > 5:
            self.issues.append({
                'type': 'info',
                'category': 'maintainability',
                'message': f'發現大量硬編碼像素值: {len(magic_numbers)} 處',
                'suggestion': '考慮使用 CSS Variables 或 rem 單位提高可維護性'
            })
    
    def check_inline_styles(self):
        """檢查內聯樣式定義 (簡化版,主要檢查 style 屬性模式)"""
        # 這個檢查適用於包含 HTML 的檔案
        pattern = r'style\s*=\s*["\'][^"\']+["\']'
        matches = re.finditer(pattern, self.css_content, re.IGNORECASE)
        count = sum(1 for _ in matches)
        
        if count > 0:
            self.issues.append({
                'type': 'warning',
                'category': 'maintainability',
                'message': f'發現 {count} 處內聯樣式',
                'suggestion': '將樣式提取到 CSS class 中'
            })
    
    def _is_in_comment(self, position: int) -> bool:
        """檢查位置是否在註解中"""
        # 簡化版,檢查前面是否有 /* 且後面有 */
        before = self.css_content[:position]
        comment_start = before.rfind('/*')
        comment_end = before.rfind('*/')
        return comment_start > comment_end
    
    def check_crm_container_prefix(self):
        """檢查 CiviCRM 專案是否使用 .crm-container 前綴"""
        # 允許的例外情況 (這些選擇器不需要 .crm-container 前綴)
        allowed_without_prefix = [
            r'^body:has\(\.crm-container\)',  # body:has(.crm-container) 是正確的
            r'^html:has\(\.crm-container\)',  # html:has(.crm-container) 是正確的
            r'^#civicrm-menu',                # CiviCRM 頂部選單
            r'^\.crm-notify-container',       # 通知容器
            r'^\.crm-container\s',            # .crm-container 本身
            r'^\*\s',                         # 通用選擇器 *
            r'^\*,',                          # 通用選擇器組合
            r'^\*::',                         # 偽元素
            r'^@',                            # @media, @keyframes 等
        ]
        
        # 檢查不正確的 body/html 使用
        self._check_body_html_usage()
        
        # 檢查不正確的 :root 使用
        self._check_root_usage()
        
        # 匹配所有選擇器區塊
        # 簡化版: 匹配 .crm- 開頭的 class (排除 .crm-container 本身)
        pattern = r'\.crm-(?!container\s)([a-zA-Z0-9_-]+)\s*\{'
        
        for match in re.finditer(pattern, self.css_content):
            selector_start = match.start()
            
            # 檢查是否在註解中
            if self._is_in_comment(selector_start):
                continue
            
            # 獲取這個選擇器的完整行
            line_start = self.css_content.rfind('\n', 0, selector_start) + 1
            line_end = self.css_content.find('{', selector_start)
            full_selector = self.css_content[line_start:line_end].strip()
            
            # 檢查是否是允許的例外
            is_allowed = any(re.match(pattern, full_selector) for pattern in allowed_without_prefix)
            if is_allowed:
                continue
            
            # 檢查前面是否已經有 .crm-container
            if '.crm-container' not in full_selector:
                self.issues.append({
                    'type': 'error',
                    'category': 'civicrm',
                    'message': f'CiviCRM 選擇器缺少 .crm-container 前綴: {full_selector}',
                    'suggestion': f'應改為: .crm-container {full_selector}'
                })
    
    def _check_body_html_usage(self):
        """檢查 body/html 是否正確使用 :has() 選擇器"""
        # 匹配 body 或 html (不含 :has)
        patterns = [
            (r'^body\s*\{', 'body', 'body:has(.crm-container)'),
            (r'^html\s*\{', 'html', 'html:has(.crm-container)'),
            (r'^body\s*[,\{]', 'body', 'body:has(.crm-container)'),
        ]
        
        for pattern, element, suggestion in patterns:
            matches = re.finditer(pattern, self.css_content, re.MULTILINE)
            for match in matches:
                if self._is_in_comment(match.start()):
                    continue
                
                # 獲取完整選擇器
                line_start = self.css_content.rfind('\n', 0, match.start()) + 1
                line_end = self.css_content.find('{', match.start())
                full_selector = self.css_content[line_start:line_end].strip()
                
                self.issues.append({
                    'type': 'error',
                    'category': 'civicrm',
                    'message': f'在 CiviCRM 專案中，{element} 選擇器應使用 :has() 確保只影響有 CRM 的頁面: {full_selector}',
                    'suggestion': f'應改為: {suggestion} {{ ... }} 或在 .crm-container 內設定樣式'
                })
    
    def _check_root_usage(self):
        """檢查 :root 中是否定義了 --crm- 開頭的變數"""
        # 匹配 :root { 區塊
        root_pattern = r':root\s*\{([^}]+)\}'
        matches = re.finditer(root_pattern, self.css_content, re.DOTALL)
        
        for match in matches:
            if self._is_in_comment(match.start()):
                continue
            
            content = match.group(1)
            # 檢查是否有 --crm- 開頭的變數
            if re.search(r'--crm-', content):
                self.issues.append({
                    'type': 'warning',
                    'category': 'civicrm',
                    'message': '在 CiviCRM 專案中，CSS Variables 應定義在 .crm-container 內而非 :root',
                    'suggestion': '將 --crm-* 變數移到 .crm-container { } 區塊中，避免污染全域命名空間'
                })


def analyze_css_file(filepath: str, is_civicrm_project: bool = False) -> List[Dict]:
    """分析 CSS 檔案"""
    try:
        content = Path(filepath).read_text(encoding='utf-8')
        checker = CSSQualityChecker(content)
        return checker.check_all(is_civicrm_project=is_civicrm_project)
    except FileNotFoundError:
        return [{
            'type': 'error',
            'category': 'file',
            'message': f'找不到檔案: {filepath}',
            'suggestion': '確認檔案路徑是否正確'
        }]
    except Exception as e:
        return [{
            'type': 'error',
            'category': 'unknown',
            'message': f'分析時發生錯誤: {str(e)}',
            'suggestion': '檢查檔案格式是否正確'
        }]

def analyze_css_string(css_string: str, is_civicrm_project: bool = False) -> List[Dict]:
    """分析 CSS 字串"""
    checker = CSSQualityChecker(css_string)
    return checker.check_all(is_civicrm_project=is_civicrm_project)

def format_report(issues: List[Dict]) -> str:
    """格式化報告輸出"""
    if not issues:
        return "✅ 沒有發現問題!CSS 程式碼品質良好。"
    
    report = []
    report.append(f"\n發現 {len(issues)} 個問題:\n")
    report.append("=" * 80)
    
    # 按類型分組
    errors = [i for i in issues if i['type'] == 'error']
    warnings = [i for i in issues if i['type'] == 'warning']
    infos = [i for i in issues if i['type'] == 'info']
    
    for category, items in [('❌ 錯誤', errors), ('⚠️  警告', warnings), ('ℹ️  資訊', infos)]:
        if items:
            report.append(f"\n{category} ({len(items)}):")
            report.append("-" * 80)
            for item in items:
                report.append(f"\n[{item['category'].upper()}]")
                report.append(f"問題: {item['message']}")
                report.append(f"建議: {item['suggestion']}\n")
    
    report.append("=" * 80)
    return "\n".join(report)

def main():
    """主程式"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='CSS 品質檢查工具',
        epilog='範例: python check_css_quality.py style.css --civicrm'
    )
    parser.add_argument('filepath', help='CSS 檔案路徑')
    parser.add_argument(
        '--civicrm', 
        action='store_true',
        help='啟用 CiviCRM/netiCRM 專案檢查 (檢查 .crm-container 前綴)'
    )
    
    args = parser.parse_args()
    
    # 自動偵測: 如果檔案名稱包含 'crm' 或 'civi',預設啟用 CiviCRM 模式
    auto_detect_civicrm = 'crm' in args.filepath.lower() or 'civi' in args.filepath.lower()
    is_civicrm = args.civicrm or auto_detect_civicrm
    
    if auto_detect_civicrm and not args.civicrm:
        print(f"📋 自動偵測到 CiviCRM 相關檔案,啟用 CiviCRM 檢查模式")
        print(f"   (使用 --no-civicrm 可停用自動偵測)\n")
    
    issues = analyze_css_file(args.filepath, is_civicrm_project=is_civicrm)
    report = format_report(issues)
    print(report)
    
    # 如果有錯誤,回傳非零 exit code
    has_errors = any(i['type'] == 'error' for i in issues)
    sys.exit(1 if has_errors else 0)

if __name__ == '__main__':
    main()
