import tkinter as tk
from tkinter import filedialog, messagebox
import os
import ttkbootstrap as tb
from ttkbootstrap import Style
from pdf_converter import convert_pdf_to_images, merge_images_to_pdf, delete_temp_images
from PyPDF2 import PdfReader
import json
import webbrowser


# 设置支持的语言和语言文件目录
LANGUAGES = ['en_US', 'zh_CN']
LOCALE_DIR = os.path.join(os.path.dirname(__file__), 'locales')


def load_translations(language):
    """加载语言翻译文件"""
    file_path = os.path.join(LOCALE_DIR, f'{language}.json')
    if not os.path.isfile(file_path):
        file_path = os.path.join(LOCALE_DIR, 'zh_CN.json')  # 默认语言
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


# 默认语言
translations = load_translations('zh_CN')


def _(key):
    """获取翻译文本"""
    return translations.get(key, key)


def set_language(language_code):
    """设置语言"""
    global translations
    translations = load_translations(language_code)



class PDFConverterGUI:
    def __init__(self, master):
        self.master = master
        self.master.title(_("title"))
        self.author_frame = self.create_author_link(master)

        # 使用系统默认主题
        self.style = Style(theme='darkly')
        self.master.tk_setPalette(background=self.style.colors.bg)

        # 主题和语言选择行
        self.theme_language_frame = self.create_theme_language_frame()
        self.theme_label = self.create_theme_label(self.theme_language_frame)
        self.theme_menu = self.create_theme_menu(self.theme_language_frame)

        self.language_var = tk.StringVar(value='zh_CN')
        self.language_menu = self.create_language_menu(self.theme_language_frame)

        # 选择 PDF 文件
        self.file_frame = self.create_file_frame(master)
        self.file_label = self.create_file_label(self.file_frame)
        self.file_entry = self.create_file_entry(self.file_frame)
        self.browse_button = self.create_browse_button(self.file_frame)

        # DPI 单选框
        self.dpi_frame = self.create_dpi_frame(master)
        self.dpi_var = self.create_dpi_var()
        self.low_dpi_radio = self.create_dpi_radio(self.dpi_frame, _("low_dpi"), 150)
        self.medium_dpi_radio = self.create_dpi_radio(self.dpi_frame, _("medium_dpi"), 300)
        self.high_dpi_radio = self.create_dpi_radio(self.dpi_frame, _("high_dpi"), 450)
        self.very_high_dpi_radio = self.create_dpi_radio(self.dpi_frame, _("very_high_dpi"), 750)

        # 自定义 DPI 输入框
        self.custom_dpi_frame = self.create_custom_dpi_frame(master)
        self.custom_dpi_label = self.create_custom_dpi_label(self.custom_dpi_frame)
        self.custom_dpi_entry = self.create_custom_dpi_entry(self.custom_dpi_frame)

        # 是否删除图片的单选框
        self.delete_images_frame = self.create_delete_images_frame(master)
        self.delete_images_var = tk.BooleanVar(value=False)
        self.delete_images_checkbox = self.create_delete_images_checkbox(self.delete_images_frame)

        # 转换按钮
        self.convert_button = self.create_convert_button(master)

        # 进度条及百分比显示
        self.progress_frame = self.create_progress_frame(master)
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = self.create_progress_bar(self.progress_frame)
        self.progress_percentage = self.create_progress_percentage(self.progress_frame)

    # 在 PDFConverterGUI 类中添加一个新方法来创建作者链接
    def create_author_link(self, master):
        frame = tk.Frame(master)
        frame.pack(pady=10, padx=10, fill=tk.X, side=tk.BOTTOM)
        link = tk.Label(frame, text="作者博客", fg="red", font=("Arial", 12, "bold"), cursor="hand2")
        link.pack(side=tk.RIGHT, padx=5)
        link.bind("<Button-1>", lambda e: webbrowser.open("https://www.xiaoyu.ac.cn"))
        return frame

    def create_theme_language_frame(self):
        frame = tk.Frame(self.master)
        frame.pack(pady=10, padx=10, fill=tk.X)
        return frame

    def create_theme_label(self, parent):
        label = tk.Label(parent, text=_("select_theme"))
        label.pack(side=tk.LEFT, padx=5)
        return label

    def create_theme_menu(self, parent):
        theme_var = tk.StringVar(value='darkly')
        menu = tk.OptionMenu(parent, theme_var, 'darkly', 'flatly', 'solar', 'cosmo', 'default', command=self.change_theme)
        menu.pack(side=tk.LEFT, padx=5)
        return menu

    def create_language_menu(self, parent):
        menu = tk.OptionMenu(parent, self.language_var, 'en_US', 'zh_CN', command=self.change_language)
        menu.pack(side=tk.RIGHT, padx=5)
        return menu

    def create_file_frame(self, master):
        frame = tk.Frame(master)
        frame.pack(pady=10, padx=10, fill=tk.X)
        return frame

    def create_file_label(self, parent):
        label = tk.Label(parent, text=_("select_pdf_file"))
        label.pack(side=tk.LEFT, padx=5)
        return label

    def create_file_entry(self, parent):
        entry = tk.Entry(parent, width=50)
        entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        return entry

    def create_browse_button(self, parent):
        button = tk.Button(parent, text=_("browse_file"), command=self.browse_file)
        button.pack(side=tk.RIGHT, padx=5)
        return button

    def create_dpi_frame(self, master):
        frame = tk.Frame(master)
        frame.pack(pady=10, padx=10, fill=tk.X)
        return frame

    def create_dpi_var(self):
        return tk.IntVar(value=300)

    def create_dpi_radio(self, parent, text, value):
        radio = tk.Radiobutton(parent, text=text, variable=self.dpi_var, value=value)
        radio.pack(side=tk.LEFT, padx=5)
        return radio

    def create_custom_dpi_frame(self, master):
        frame = tk.Frame(master)
        frame.pack(pady=10, padx=10, fill=tk.X)
        return frame

    def create_custom_dpi_label(self, parent):
        label = tk.Label(parent, text=_("custom_dpi"))
        label.pack(side=tk.TOP, padx=5, pady=(0, 5))
        return label

    def create_custom_dpi_entry(self, parent):
        entry = tk.Entry(parent, width=20)
        entry.pack(side=tk.TOP, padx=5)
        return entry

    def create_delete_images_frame(self, master):
        frame = tk.Frame(master)
        frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        return frame

    def create_delete_images_checkbox(self, parent):
        checkbox = tk.Checkbutton(parent, text=_("delete_images"), variable=self.delete_images_var)
        checkbox.pack(side=tk.TOP, padx=5)
        return checkbox

    def create_convert_button(self, master):
        button = tk.Button(master, text=_("convert_button"), command=self.start_conversion)
        button.pack(pady=20, padx=10)
        return button

    def create_progress_frame(self, master):
        frame = tk.Frame(master)
        frame.pack(pady=10, padx=10, fill=tk.X)
        return frame

    def create_progress_bar(self, parent):
        progress_bar = tk.ttk.Progressbar(parent, variable=self.progress_var, maximum=100,
                                          style='info.Horizontal.TProgressbar')
        progress_bar.pack(side=tk.TOP, padx=10, pady=(0, 5), fill=tk.X, expand=True)
        return progress_bar

    def create_progress_percentage(self, parent):
        percentage_label = tk.Label(parent, text="0%", font=("Arial", 10))
        percentage_label.pack(side=tk.TOP, pady=(0, 10))
        return percentage_label

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)

    def change_theme(self, theme_name):
        self.style.theme_use(theme_name)
        self.master.tk_setPalette(background=self.style.colors.bg)
        print(_("theme_changed").format(theme_name))

    def change_language(self, language_code):
        set_language(language_code)
        self.update_texts()
        print(_("language_changed").format(language_code))

    def update_texts(self):
        self.master.title(_("title"))
        self.theme_label.config(text=_("select_theme"))
        self.file_label.config(text=_("select_pdf_file"))
        self.browse_button.config(text=_("browse_file"))
        self.low_dpi_radio.config(text=_("low_dpi"))
        self.medium_dpi_radio.config(text=_("medium_dpi"))
        self.high_dpi_radio.config(text=_("high_dpi"))
        self.very_high_dpi_radio.config(text=_("very_high_dpi"))
        self.custom_dpi_label.config(text=_("custom_dpi"))
        self.delete_images_checkbox.config(text=_("delete_images"))
        self.convert_button.config(text=_("convert_button"))
        self.progress_label.config(text=_("progress_label"))

    def update_progress(self, progress):
        self.progress_var.set(progress)
        self.progress_percentage.config(text=f"{int(progress)}%")
        self.master.update_idletasks()

    def start_conversion(self):
        file_path = self.file_entry.get()
        dpi = self.dpi_var.get()

        # 处理自定义 DPI 输入
        custom_dpi = self.custom_dpi_entry.get()
        if self.validate_custom_dpi(custom_dpi):
            dpi = int(custom_dpi)
        else:
            dpi = 300

        if not file_path:
            messagebox.showerror(_("error_no_file"), _("error_no_file"))
            return

        img_dir = os.path.join(os.path.dirname(file_path), 'page_img')
        output_pdf_path = os.path.join(os.path.dirname(file_path), f'{os.path.basename(file_path)[:-4]}_converted.pdf')

        try:
            pdf = PdfReader(file_path)
            total_pages = len(pdf.pages)

            print(_("starting_conversion").format(file_path, dpi))
            # 执行 PDF 到图片的转换
            convert_pdf_to_images(file_path, img_dir, os.path.basename(file_path), dpi, self.update_progress, total_pages)
            # 合并图片为 PDF
            merge_images_to_pdf(img_dir, output_pdf_path, os.path.basename(file_path), dpi)

            # 根据用户选择是否删除临时图片
            if self.delete_images_var.get():
                delete_temp_images(img_dir)

            messagebox.showinfo(_("success"), _("success") + f" {output_pdf_path}")

        except Exception as e:
            messagebox.showerror(_("error_conversion"), _("error_conversion") + f" {e}")

    def validate_custom_dpi(self, custom_dpi):
        """验证自定义 DPI 输入"""
        if custom_dpi.isdigit():
            custom_dpi_value = int(custom_dpi)
            if 150 <= custom_dpi_value <= 750:
                return True
            else:
                messagebox.showwarning(_("warning_custom_dpi"), _("warning_custom_dpi"))
        return False


if __name__ == "__main__":
    root = tb.Window()  # 使用 ttkbootstrap 的窗口
    app = PDFConverterGUI(root)
    root.mainloop()
