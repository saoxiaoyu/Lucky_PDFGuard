import tkinter as tk
from tkinter import filedialog, messagebox
import os
import ttkbootstrap as tb
from ttkbootstrap import Style
from pdf_converter import convert_pdf_to_images, merge_images_to_pdf, delete_temp_images  # 从 pdf_converter.py 导入需要的函数


class PDFConverterGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("PDF 转换器")

        # 使用系统默认主题
        self.style = Style(theme='darkly')
        self.master.tk_setPalette(background=self.style.colors.bg)

        # 主题选择下拉菜单
        self.theme_frame = tk.Frame(master)
        self.theme_frame.pack(pady=10, padx=10, fill=tk.X)

        self.theme_label = tk.Label(self.theme_frame, text="选择主题:")
        self.theme_label.pack(side=tk.LEFT, padx=5)

        self.theme_var = tk.StringVar(value='darkly')
        self.theme_menu = tk.OptionMenu(self.theme_frame, self.theme_var, 'darkly', 'flatly', 'solar', 'cosmo', 'default', command=self.change_theme)
        self.theme_menu.pack(side=tk.LEFT, padx=5)

        # 选择 PDF 文件
        self.file_frame = tk.Frame(master)
        self.file_frame.pack(pady=10, padx=10, fill=tk.X)

        self.file_label = tk.Label(self.file_frame, text="选择 PDF 文件:")
        self.file_label.pack(side=tk.LEFT, padx=5)

        self.file_entry = tk.Entry(self.file_frame, width=50)
        self.file_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        self.browse_button = tk.Button(self.file_frame, text="选择文件", command=self.browse_file)
        self.browse_button.pack(side=tk.RIGHT, padx=5)

        # DPI 单选框
        self.dpi_frame = tk.Frame(master)
        self.dpi_frame.pack(pady=10, padx=10, fill=tk.X)

        self.dpi_var = tk.IntVar(value=300)

        self.low_dpi_radio = tk.Radiobutton(self.dpi_frame, text="150 DPI (低质量)", variable=self.dpi_var, value=150)
        self.low_dpi_radio.pack(side=tk.LEFT, padx=5)

        self.medium_dpi_radio = tk.Radiobutton(self.dpi_frame, text="300 DPI (一般质量)", variable=self.dpi_var, value=300)
        self.medium_dpi_radio.pack(side=tk.LEFT, padx=5)

        self.high_dpi_radio = tk.Radiobutton(self.dpi_frame, text="450 DPI (高质量)", variable=self.dpi_var, value=450)
        self.high_dpi_radio.pack(side=tk.LEFT, padx=5)

        self.very_high_dpi_radio = tk.Radiobutton(self.dpi_frame, text="750 DPI (超高质量，可能会有严重性能问题)", variable=self.dpi_var, value=750)
        self.very_high_dpi_radio.pack(side=tk.LEFT, padx=5)

        # 自定义 DPI 输入框
        self.custom_dpi_frame = tk.Frame(master)
        self.custom_dpi_frame.pack(pady=10, padx=10, fill=tk.X)

        self.custom_dpi_label = tk.Label(self.custom_dpi_frame, text="或输入自定义 DPI:")
        self.custom_dpi_label.pack(side=tk.TOP, padx=5, pady=(0, 5))

        self.custom_dpi_entry = tk.Entry(self.custom_dpi_frame, width=10)
        self.custom_dpi_entry.pack(side=tk.TOP, padx=5)

        # 是否删除图片的单选框
        self.delete_images_frame = tk.Frame(master)
        self.delete_images_frame.pack(pady=10, padx=10, fill=tk.X)

        self.delete_images_var = tk.BooleanVar(value=False)
        self.delete_images_checkbox = tk.Checkbutton(self.delete_images_frame, text="转换完成后删除临时图片", variable=self.delete_images_var)
        self.delete_images_checkbox.pack(side=tk.TOP, padx=5)

        # 转换按钮
        self.convert_button = tk.Button(master, text="开始转换", command=self.start_conversion)
        self.convert_button.pack(pady=20, padx=10)

        # 进度条及百分比显示
        self.progress_frame = tk.Frame(master)
        self.progress_frame.pack(pady=10, padx=10, fill=tk.X)

        self.progress_label = tk.Label(self.progress_frame, text="转换进度:")
        self.progress_label.pack(side=tk.LEFT, padx=5)

        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = tk.ttk.Progressbar(self.progress_frame, variable=self.progress_var, maximum=100, length=350, style='info.Horizontal.TProgressbar')
        self.progress_bar.pack(side=tk.LEFT, padx=5)

        self.progress_percentage = tk.Label(self.progress_frame, text="0%")
        self.progress_percentage.pack(side=tk.LEFT, padx=5)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)

    def change_theme(self, theme_name):
        self.style.theme_use(theme_name)
        self.master.tk_setPalette(background=self.style.colors.bg)
        print(f"主题已更改为: {theme_name}")

    def update_progress(self, progress):
        self.progress_var.set(progress)
        self.progress_percentage.config(text=f"{int(progress)}%")
        self.master.update_idletasks()

    def start_conversion(self):
        file_path = self.file_entry.get()
        dpi = self.dpi_var.get()

        custom_dpi = self.custom_dpi_entry.get()
        if custom_dpi.isdigit():
            custom_dpi = int(custom_dpi)
            if 150 <= custom_dpi <= 750:
                dpi = custom_dpi
            else:
                messagebox.showwarning("警告", "自定义 DPI 超出范围。使用默认 DPI 300。")
                dpi = 300

        if not file_path:
            messagebox.showerror("错误", "请先选择 PDF 文件")
            return

        img_dir = os.path.join(os.path.dirname(file_path), 'page_img')
        output_pdf_path = os.path.join(os.path.dirname(file_path), f'{os.path.basename(file_path)[:-4]}_converted.pdf')

        try:
            from PyPDF2 import PdfReader
            pdf = PdfReader(file_path)
            total_pages = len(pdf.pages)

            print(f"开始转换 PDF 文件: {file_path} 使用 DPI: {dpi}")
            convert_pdf_to_images(file_path, img_dir, os.path.basename(file_path), dpi, self.update_progress,
                                  total_pages)
            merge_images_to_pdf(img_dir, output_pdf_path, os.path.basename(file_path), dpi)

            if self.delete_images_var.get():
                delete_temp_images(img_dir)

            messagebox.showinfo("成功", f"PDF 转换完成：{output_pdf_path}")

        except Exception as e:
            messagebox.showerror("转换错误", f"转换过程中发生错误: {e}")


if __name__ == "__main__":
    root = tb.Window()  # 使用 ttkbootstrap 的窗口
    app = PDFConverterGUI(root)
    root.mainloop()

