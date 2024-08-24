import os
from os.path import isdir, join, exists
import logging

# 配置日志记录
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def create_directory(directory_path):
    if not isdir(directory_path):
        try:
            os.mkdir(directory_path)
            logging.info(f"目录已创建: {directory_path}")
        except Exception as e:
            logging.error(f"创建目录失败: {directory_path}，错误: {e}")
            raise


def get_pdf_files_in_directory(directory_path):
    if not isdir(directory_path):
        logging.warning(f"目录不存在: {directory_path}")
        return []

    pdf_files = []
    try:
        files = os.listdir(directory_path)
        for file in files:
            if file.endswith('.pdf'):
                pdf_file_path = join(directory_path, file)
                pdf_files.append(pdf_file_path)
                logging.debug(f"找到 PDF 文件: {pdf_file_path}")
    except Exception as e:
        logging.error(f"读取目录失败: {directory_path}，错误: {e}")
        raise

    return pdf_files


def remove_file(file_path):
    if exists(file_path):
        try:
            os.remove(file_path)
            logging.info(f"文件已删除: {file_path}")
        except Exception as e:
            logging.error(f"删除文件失败: {file_path}，错误: {e}")
            raise
    else:
        logging.warning(f"文件不存在: {file_path}")


def verify_and_remove(file_path):
    if exists(file_path):
        try:
            remove_file(file_path)
            return True
        except Exception:
            return False
    return False


def process_directory(directory_path):
    create_directory(directory_path)
    pdf_files = get_pdf_files_in_directory(directory_path)

    for pdf_file in pdf_files:
        success = verify_and_remove(pdf_file)
        if success:
            logging.info(f"处理完成文件: {pdf_file}")
        else:
            logging.error(f"处理失败文件: {pdf_file}")


# 示例代码（可选）：仅在直接运行此脚本时执行
if __name__ == "__main__":
    test_directory = "test_pdfs"
    process_directory(test_directory)
