import unittest
from unittest.mock import patch
import tkinter as tk
import json
import os

from pdf_gui import PDFConverterGUI, load_translations, set_language, _

# 测试数据目录
LOCALE_DIR = os.path.join(os.path.dirname(__file__), 'locales')


class TestPDFConverterGUI(unittest.TestCase):

    def setUp(self):
        """在每个测试之前运行，设置测试环境"""
        self.root = tk.Tk()
        self.root.withdraw()  # 隐藏主窗口
        self.app = PDFConverterGUI(self.root)

    def test_load_translations(self):
        """测试加载语言文件"""
        # 创建一个测试语言文件
        test_language = 'test'
        test_file_path = os.path.join(LOCALE_DIR, f'{test_language}.json')
        with open(test_file_path, 'w', encoding='utf-8') as f:
            json.dump({'greeting': 'Hello'}, f)

        translations = load_translations(test_language)
        self.assertEqual(translations['greeting'], 'Hello')

        # 清理测试文件
        os.remove(test_file_path)

    def test_set_language(self):
        """测试设置语言"""
        test_language = 'test'
        test_file_path = os.path.join(LOCALE_DIR, f'{test_language}.json')
        with open(test_file_path, 'w', encoding='utf-8') as f:
            json.dump({'greeting': 'Hello'}, f)

        set_language(test_language)
        self.assertEqual(_('greeting'), 'Hello')

        # 清理测试文件
        os.remove(test_file_path)

    @patch('pdf_gui.filedialog.askopenfilename')
    def test_browse_file(self, mock_askopenfilename):
        """测试文件选择对话框"""
        mock_askopenfilename.return_value = 'test.pdf'
        self.app.browse_file()
        self.assertEqual(self.app.file_entry.get(), 'test.pdf')

    def test_change_theme(self):
        """测试主题切换"""
        self.app.change_theme('flatly')
        self.assertEqual(self.app.style.theme_use(), 'flatly')

    @patch('pdf_gui.json.load')
    def test_change_language(self, mock_json_load):
        """测试语言切换"""
        mock_json_load.return_value = {'greeting': 'Hola'}
        self.app.change_language('es_ES')
        self.assertEqual(_('greeting'), 'Hola')

    def test_update_texts(self):
        """测试界面文本更新"""
        self.app.change_language('en_US')  # 确保使用默认语言
        self.app.update_texts()
        self.assertEqual(self.app.theme_label.cget('text'), 'Select Theme:')
        self.assertEqual(self.app.file_label.cget('text'), 'Select PDF File:')
        self.assertEqual(self.app.browse_button.cget('text'), 'Browse File')

    def tearDown(self):
        """在每个测试之后运行，清理测试环境"""
        self.root.destroy()


if __name__ == '__main__':
    unittest.main()
