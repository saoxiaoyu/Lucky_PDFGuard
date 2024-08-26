# Lucky_PDFGuardV1.0使用方法

离线pdf转纯图pdf
1.安装和运行
①　源代码安装
- 安装：下载最新版本的发布包，解压缩到本地目录。确保已安装Python 3.11或以上版本。使用命令行进入解压目录，执行以下命令安装所需的依赖库：
```bash
pip install -r requirements.txt
```
- 运行：在命令行中进入解压目录，并运行以下命令启动应用程序：
```bash
python pdf_gui.py
```
②　直接使用打包好的单文件
2. 使用界面说明
- 主题和语言选择：界面顶部有主题和语言选择框，允许用户选择不同的界面主题和语言。
- 文件选择区：包括一个文本框和一个“浏览”按钮，用户可以通过点击“浏览”按钮选择要转换的PDF文件。
- DPI 设置区：包含几个DPI选项的单选按钮（低、中、高、超高），以及一个自定义DPI输入框，用户可以选择合适的DPI或输入自定义值。
- 转换按钮：点击“转换”按钮开始PDF转换任务。
- 进度条：显示当前转换进度的进度条和百分比。
3. 文件选择
- 点击“浏览”按钮，弹出文件选择对话框，选择要转换的PDF文件。选定文件后，文件路径会显示在文本框中。
4. DPI 设置
- 选择预设的DPI选项（150、300、450、750），或者在自定义DPI输入框中输入一个介于150到750之间的数值。DPI设置影响转换后图像的清晰度和文件大小。
5. 转换按钮
- 确认文件选择和DPI设置后，点击“开始转换”按钮开始转换过程。转换期间，进度条会显示转换的实时进度，转换完成后，系统会弹出提示框通知用户结果。
6. 错误处理和常见问题解答
- 文件选择错误：确保选择的文件是有效的PDF文件。如果出现错误，请检查文件路径是否正确，文件是否损坏。
- DPI 设置错误：如果输入的自定义DPI不在有效范围内（150到750），系统会默认使用300DPI值。
- 删除临时文件问题：如果在转换完成后临时图像文件未能删除，请检查文件夹权限或手动删除这些文件以节省存储空间。
