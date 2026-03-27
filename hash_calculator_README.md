# 文件/文件夹 Hash 计算器

一个使用 Python + Tkinter 开发的桌面应用程序，可计算文件或文件夹的 Hash 值。

## 功能特点

- 支持选择文件或文件夹进行 Hash 计算
- 支持四种哈希算法：MD5、SHA-1、SHA-256、SHA-512
- 显示文件大小、文件数量等信息
- 一键复制 Hash 值到剪贴板
- 支持文件夹内所有文件合并计算 Hash

## 运行方式

```bash
# 直接运行
python hash_calculator.py
```

## 使用说明

1. 运行程序后，选择"文件"或"文件夹"模式
2. 点击"选择文件"或"选择文件夹"按钮
3. 选择要计算的 Hash 算法（默认 SHA-256）
4. 点击"开始计算"按钮
5. 等待计算完成后，可点击"复制Hash值"按钮复制结果

## 打包为 EXE（可选）

如果需要打包为 Windows 可执行文件：

```bash
# 安装 pyinstaller
pip install pyinstaller

# 打包
pyinstaller --onefile --noconsole --icon=favicon.ico hash_calculator.py
```

打包后的 exe 文件位于 `dist` 文件夹中。
