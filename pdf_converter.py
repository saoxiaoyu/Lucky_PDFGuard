import fitz
import os
from PyPDF2 import PdfMerger, PdfReader
from reportlab.pdfgen import canvas



def convert_pdf_to_images(pdf_path, img_dir, pdf_fn, dpi, update_progress=None, total_pages=None):
    if not os.path.isdir(img_dir):
        os.mkdir(img_dir)
    with fitz.open(pdf_path) as pdf:
        for pg in range(pdf.page_count):
            page = pdf[pg]
            # 获取页面实际尺寸
            page_rect = page.rect
            # 转换为 DPI 单位
            zoom_x = dpi / 72
            zoom_y = dpi / 72
            mat = fitz.Matrix(zoom_x, zoom_y)
            pm = page.get_pixmap(matrix=mat, alpha=False)
            # 保存图片时应用页面实际尺寸
            pm.save(f'{img_dir}/{pg + 1}.png')
            print(f'PDF文件||{pdf_fn}||第{pg + 1}页已转为图片')

            if update_progress and total_pages:
                progress = (pg + 1) / total_pages * 100
                update_progress(progress)


def merge_images_to_pdf(img_dir, output_pdf_path, pdf_fn, dpi):
    # 获取文件夹中的所有图片
    image_files = [os.path.join(img_dir, fn) for fn in os.listdir(img_dir) if fn.endswith('.png')]
    image_files.sort(key=lambda fn: int(os.path.splitext(os.path.basename(fn))[0]))

    # 创建 PDF 文件
    result_pdf = PdfMerger()
    for img_path in image_files:
        img = fitz.open(img_path)
        img_rect = img[0].rect  # 获取图像的实际尺寸
        temp_pdf = f'{img_dir}/{os.path.basename(img_path).replace(".png", "_temp.pdf")}'

        c = canvas.Canvas(temp_pdf, pagesize=(img_rect.width, img_rect.height))
        c.drawImage(img_path, 0, 0, width=img_rect.width, height=img_rect.height)
        c.save()

        with open(temp_pdf, 'rb') as fp:
            pdf_reader = PdfReader(fp)
            result_pdf.append(pdf_reader)

        os.remove(temp_pdf)  # 删除临时 PDF 文件

    if not os.path.isdir(os.path.dirname(output_pdf_path)):
        os.mkdir(os.path.dirname(output_pdf_path))

    result_pdf.write(output_pdf_path)
    print(f'PDF文件||{pdf_fn}||转换已成纯图像PDF文件：{os.path.basename(output_pdf_path)}')
    result_pdf.close()


def delete_temp_images(img_dir):
    for file in os.listdir(img_dir):
        if file.endswith('.png'):
            os.remove(os.path.join(img_dir, file))
    print('临时图片已删除')
