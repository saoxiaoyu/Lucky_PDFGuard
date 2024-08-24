import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import fitz
from PyPDF2 import PdfMerger, PdfReader
from pdf_converter import convert_pdf_to_images, merge_images_to_pdf, delete_temp_images


class TestPDFConverter(unittest.TestCase):

    @patch('pdf_converter.fitz.open')
    def test_convert_pdf_to_images(self, mock_fitz_open):
        """测试 PDF 转换为图片"""
        mock_pdf = MagicMock()
        mock_page = MagicMock()
        mock_pixmap = MagicMock()

        mock_fitz_open.return_value = mock_pdf
        mock_pdf.__enter__.return_value = mock_pdf
        mock_pdf.page_count = 2
        mock_pdf.__getitem__.return_value = mock_page
        mock_page.get_pixmap.return_value = mock_pixmap

        with patch('pdf_converter.os.path.isdir', return_value=False), \
                patch('pdf_converter.os.mkdir'), \
                patch('pdf_converter.os.path.join', side_effect=lambda a, b: f'{a}/{b}'), \
                patch('pdf_converter.print') as mock_print:
            mock_pixmap.save = MagicMock()

            def mock_update_progress(progress):
                pass

            convert_pdf_to_images('test.pdf', 'img_dir', 'test', 300, mock_update_progress, 2)

            mock_fitz_open.assert_called_once_with('test.pdf')
            mock_page.get_pixmap.assert_called_once_with(matrix=fitz.Matrix(300 / 72, 300 / 72), alpha=False)
            mock_pixmap.save.assert_called()
            mock_print.assert_any_call('PDF文件||test||第1页已转为图片')
            mock_print.assert_any_call('PDF文件||test||第2页已转为图片')

    @patch('pdf_converter.PdfMerger')
    @patch('pdf_converter.fitz.open')
    @patch('pdf_converter.canvas.Canvas')
    def test_merge_images_to_pdf(self, mock_canvas, mock_fitz_open, mock_PdfMerger):
        """测试图片合并为 PDF"""
        mock_merger = MagicMock()
        mock_PdfMerger.return_value = mock_merger

        mock_image = MagicMock()
        mock_fitz_open.return_value = mock_image
        mock_image[0].rect = fitz.Rect(0, 0, 100, 100)
        mock_canvas.return_value = MagicMock()

        with patch('pdf_converter.os.path.join', side_effect=lambda a, b: f'{a}/{b}'), \
                patch('pdf_converter.os.listdir', return_value=['1.png']), \
                patch('pdf_converter.open', mock_open(read_data='data')), \
                patch('pdf_converter.print') as mock_print:
            merge_images_to_pdf('img_dir', 'output.pdf', 'test', 300)

            mock_fitz_open.assert_called_once_with('img_dir/1.png')
            mock_canvas.assert_called_once()
            mock_merger.append.assert_called()
            mock_print.assert_called_once_with('PDF文件||test||转换已成纯图像PDF文件：output.pdf')

    @patch('pdf_converter.os.listdir')
    @patch('pdf_converter.os.remove')
    def test_delete_temp_images(self, mock_os_remove, mock_os_listdir):
        """测试删除临时图片"""
        mock_os_listdir.return_value = ['1.png', '2.png']
        delete_temp_images('img_dir')

        mock_os_remove.assert_any_call('img_dir/1.png')
        mock_os_remove.assert_any_call('img_dir/2.png')
        mock_os_remove.assert_called()
        print("临时图片已删除")  # This is to confirm the output of the function.


if __name__ == '__main__':
    unittest.main()
