import fitz
import os
from PyPDF2 import PdfMerger, PdfReader
from reportlab.lib.pagesizes import A4, portrait
from reportlab.pdfgen import canvas


def convert_pdf_to_images(pdf_path, img_dir, pdf_fn, dpi, update_progress=None, total_pages=None):
    if not os.path.isdir(img_dir):
        os.mkdir(img_dir)
    with fitz.open(pdf_path) as pdf:
        for pg in range(pdf.page_count):
            page = pdf[pg]
            mat = fitz.Matrix(2, 2)
            pm = page.get_pixmap(matrix=mat, dpi=dpi, alpha=False)
            page_num = pg + 1
            pm.save(f'{img_dir}/{page_num}.png')
            print(f'PDF文件||{pdf_fn}||第{page_num}页已转为图片')

            if update_progress and total_pages:
                progress = (pg + 1) / total_pages * 100
                update_progress(progress)


def merge_images_to_pdf(img_dir, output_pdf_path, pdf_fn, dpi):
    jpg_files = [os.path.join(img_dir, fn) for fn in os.listdir(img_dir) if fn.endswith('.png')]
    jpg_files.sort(key=lambda fn: int(os.path.splitext(os.path.basename(fn))[0]))
    result_pdf = PdfMerger()
    temp_pdf = f'{img_dir}/{pdf_fn[:-4]}_dpi{dpi}_temp.pdf'

    for fn in jpg_files:
        c = canvas.Canvas(temp_pdf, pagesize=portrait(A4))
        c.drawImage(fn, 0, 0, *portrait(A4))
        c.save()
        with open(temp_pdf, 'rb') as fp:
            pdf_reader = PdfReader(fp)
            result_pdf.append(pdf_reader)

    if not os.path.isdir(os.path.dirname(output_pdf_path)):
        os.mkdir(os.path.dirname(output_pdf_path))

    result_pdf.write(output_pdf_path)
    print(f'PDF文件||{pdf_fn}||转换已成纯图像PDF文件：{os.path.basename(output_pdf_path)}')
    result_pdf.close()
    os.remove(temp_pdf)


def delete_temp_images(img_dir):
    for file in os.listdir(img_dir):
        if file.endswith('.png'):
            os.remove(os.path.join(img_dir, file))
    print('临时图片已删除')