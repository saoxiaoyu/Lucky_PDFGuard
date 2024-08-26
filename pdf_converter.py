import fitz as fz
import os as o
from PyPDF2 import PdfWriter, PdfReader as PR
from reportlab.pdfgen import canvas as cns


def ensure_directory_exists(directory):
    if not o.path.isdir(directory):
        o.mkdir(directory)
    print(f'Directory ensured: {directory}')


def open_pdf_document(pdf_file):
    try:
        document = fz.open(pdf_file)
        return document
    except Exception as e:
        print(f"Error opening PDF document {pdf_file}: {e}")
        raise


def save_pixmap_as_image(pixmap, image_path):
    try:
        pixmap.save(image_path)
        print(f'Saved image: {image_path}')
    except Exception as e:
        print(f"Error saving image {image_path}: {e}")
        raise


def convert_page_to_image(page, dpi, image_path):
    try:
        # 获取页面尺寸
        page_size = page.rect

        # 计算缩放因子
        zoom_factor = dpi / 72
        matrix = fz.Matrix(zoom_factor, zoom_factor)

        # 渲染页面为图片
        pixmap = page.get_pixmap(matrix=matrix, alpha=False)
        save_pixmap_as_image(pixmap, image_path)
    except Exception as e:
        print(f"Error converting page to image: {e}")
        raise


def convert_pdf_to_images(pdf_path, img_dir, pdf_fn, dpi, update_progress=None, total_pages=None):
    ensure_directory_exists(img_dir)

    document = open_pdf_document(pdf_path)
    try:
        for pg in range(document.page_count):
            page = document[pg]
            image_path = f'{img_dir}/{pg + 1}.png'
            print(f'Processing page {pg + 1} of {pdf_fn}')
            convert_page_to_image(page, dpi, image_path)

            # 更新进度
            if update_progress and total_pages:
                progress = (pg + 1) / total_pages * 100
                update_progress(progress)
    finally:
        document.close()
        print(f'Finished processing PDF: {pdf_fn}')


def sort_image_files(img_dir):
    image_files = [o.path.join(img_dir, fn) for fn in o.listdir(img_dir) if fn.endswith('.png')]
    image_files.sort(key=lambda fn: int(o.path.splitext(o.path.basename(fn))[0]))
    return image_files


def create_temp_pdf(image_path, temp_pdf_path):
    try:
        img_doc = fz.open(image_path)
        img_rect = img_doc[0].rect
        temp_canvas = cns.Canvas(temp_pdf_path, pagesize=(img_rect.width, img_rect.height))
        temp_canvas.drawImage(image_path, 0, 0, width=img_rect.width, height=img_rect.height)
        temp_canvas.save()
        print(f'Temporary PDF created: {temp_pdf_path}')
    except Exception as e:
        print(f"Error creating temporary PDF {temp_pdf_path}: {e}")
        raise


def merge_images_to_pdf(img_dir, output_pdf_path, pdf_fn, dpi):
    image_files = sort_image_files(img_dir)
    merger = PdfWriter()

    try:
        for img_path in image_files:
            temp_pdf = f'{img_dir}/{o.path.basename(img_path).replace(".png", "_temp.pdf")}'
            create_temp_pdf(img_path, temp_pdf)

            # 合并临时 PDF 文件
            with open(temp_pdf, 'rb') as fp:
                pdf_reader = PR(fp)
                merger.add_page(pdf_reader.pages[0])

            # 删除临时 PDF 文件
            o.remove(temp_pdf)
    except Exception as e:
        print(f"Error merging images to PDF: {e}")
        raise
    finally:
        if not o.path.isdir(o.path.dirname(output_pdf_path)):
            o.mkdir(o.path.dirname(output_pdf_path))

        # 设置 PDF 元数据
        merger.add_metadata({
            '/Author': 'WY'
        })

        # 写入最终的 PDF 文件
        with open(output_pdf_path, 'wb') as output_pdf:
            merger.write(output_pdf)
        print(f'PDF merged and saved as: {output_pdf_path}')


def delete_temp_images(img_dir):
    for file in o.listdir(img_dir):
        if file.endswith('.png'):
            file_path = o.path.join(img_dir, file)
            try:
                o.remove(file_path)
                print(f'Deleted temporary image: {file_path}')
            except Exception as e:
                print(f"Error deleting temporary image {file_path}: {e}")
                raise
    print('All temporary images deleted.')
