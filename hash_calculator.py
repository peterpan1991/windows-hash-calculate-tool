# -*- coding: utf-8 -*-
"""
文件/文件夹 Hash 计算器
支持 MD5, SHA-1, SHA-256, SHA-512 四种哈希算法
"""

import hashlib
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import threading

class HashCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DJY 文件/文件夹 Hash 计算器")
        self.root.geometry("700x550")
        self.root.resizable(False, False)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_dir, "favicon.ico")
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)


        # 设置中文字体
        self.font_title = ("Microsoft YaHei", 14, "bold")  # pyright: ignore[reportUnannotatedClassAttribute]
        self.font_normal = ("Microsoft YaHei", 10)  # pyright: ignore[reportUnannotatedClassAttribute]

        # 初始化标志
        self.calculation_stopped = False
        self.last_result_text = ""

        self.setup_ui()
        
    def setup_ui(self):
        """设置UI界面"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(
            main_frame, 
            text="DJY 文件/文件夹 Hash 计算器",
            font=self.font_title
        )
        title_label.pack(pady=(0, 10))

        # 选择模式和算法（同一行）
        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill=tk.X, pady=(0, 10))

        # 选择模式
        mode_frame = ttk.LabelFrame(options_frame, text="选择模式", padding="5")
        mode_frame.pack(side=tk.LEFT, fill=tk.X, padx=(0, 10), expand=True)

        self.mode_var = tk.StringVar(value="file")
        ttk.Radiobutton(
            mode_frame,
            text="文件",
            variable=self.mode_var,
            value="file",
            command=self.update_select_button
        ).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(
            mode_frame,
            text="文件夹",
            variable=self.mode_var,
            value="folder",
            command=self.update_select_button
        ).pack(side=tk.LEFT, padx=10)

        # 算法选择
        algo_frame = ttk.LabelFrame(options_frame, text="哈希算法", padding="5")
        algo_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.algo_var = tk.StringVar(value="sha256")
        algorithms = [
            ("MD5", "md5"),
            ("SHA-1", "sha1"),
            ("SHA-256", "sha256"),
            ("SHA-512", "sha512")
        ]

        for text, value in algorithms:
            ttk.Radiobutton(
                algo_frame,
                text=text,
                variable=self.algo_var,
                value=value
            ).pack(side=tk.LEFT, padx=5)

        # 文件/文件夹选择
        select_frame = ttk.Frame(main_frame)
        select_frame.pack(fill=tk.X, pady=(0, 10))

        self.path_entry = ttk.Entry(select_frame, width=50, font=self.font_normal)
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        self.select_btn = ttk.Button(
            select_frame,
            text="选择文件",
            command=self.select_path
        )
        self.select_btn.pack(side=tk.LEFT)

        # 计算按钮
        self.calc_btn = ttk.Button(
            main_frame,
            text="开始计算",
            command=self.start_calculation
        )
        self.calc_btn.pack(pady=(0, 10))

        # 进度条和按钮区域
        progress_btn_frame = ttk.Frame(main_frame)
        progress_btn_frame.pack(fill=tk.X, pady=(0, 10))

        # 进度条
        self.progress = ttk.Progressbar(
            progress_btn_frame,
            mode='determinate',
            length=400
        )
        self.progress.pack(side=tk.LEFT, padx=(0, 10))

        # 停止按钮
        self.stop_btn = ttk.Button(
            progress_btn_frame,
            text="停止",
            state=tk.DISABLED,
            command=self.stop_calculation
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        # 清除按钮
        self.clear_btn = ttk.Button(
            progress_btn_frame,
            text="清除",
            state=tk.DISABLED,
            command=self.clear_result
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)

        # 保存按钮
        self.save_btn = ttk.Button(
            progress_btn_frame,
            text="保存",
            state=tk.DISABLED,
            command=self.save_result
        )
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        # 结果显示
        result_frame = ttk.LabelFrame(main_frame, text="计算结果", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True)

        # 创建滚动框架
        scroll_frame = ttk.Frame(result_frame)
        scroll_frame.pack(fill=tk.BOTH, expand=True)

        scroll_y = ttk.Scrollbar(scroll_frame, orient=tk.VERTICAL)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.result_text = tk.Text(
            scroll_frame,
            height=25,
            font=("Microsoft YaHei", 10),
            wrap=tk.WORD,
            bg="#f5f5f5",
            yscrollcommand=scroll_y.set
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)
        scroll_y.config(command=self.result_text.yview)
        
    def update_select_button(self):
        """更新选择按钮文本"""
        mode = self.mode_var.get()
        if mode == "file":
            self.select_btn.config(text="选择文件")
        else:
            self.select_btn.config(text="选择文件夹")
            
    def select_path(self):
        """选择文件或文件夹"""
        mode = self.mode_var.get()
        
        if mode == "file":
            path = filedialog.askopenfilename(
                title="选择文件",
                filetypes=[("所有文件", "*.*")]
            )
        else:
            path = filedialog.askdirectory(title="选择文件夹")
        
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)
            self.clear_result()

    def clear_result(self):
        """清除结果"""
        self.result_text.delete(1.0, tk.END)
        self.progress['value'] = 0
        self.clear_btn.config(state=tk.DISABLED)
        self.save_btn.config(state=tk.DISABLED)

    def stop_calculation(self):
        """停止计算"""
        self.calculation_stopped = True
        
    def format_size(self, size):
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"
        
    def calculate_hash(self, file_path, algorithm, progress_callback=None, file_size=None):
        """计算单个文件的hash"""
        hash_obj = hashlib.new(algorithm)
        read_size = 0

        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hash_obj.update(chunk)
                if progress_callback and file_size:
                    read_size += len(chunk)
                    progress_callback(min(read_size / file_size * 100, 100))

        return hash_obj.hexdigest()
        
    def calculate_folder_hash(self, folder_path, algorithm, progress_callback=None):
        """计算文件夹中每个文件的hash"""
        files_info = []
        total_size = 0

        # 先收集所有文件路径
        all_files = []
        for root, dirs, filenames in os.walk(folder_path):
            for filename in sorted(filenames):
                file_path = os.path.join(root, filename)
                all_files.append(file_path)

        total_files = len(all_files)
        for idx, file_path in enumerate(all_files):
            try:
                file_size = os.path.getsize(file_path)
                file_mtime = os.path.getmtime(file_path)

                # 单文件内的进度回调
                def file_progress(pct):
                    overall = (idx + pct / 100) / total_files * 100
                    if progress_callback:
                        progress_callback(min(overall, 100))

                file_hash = self.calculate_hash(file_path, algorithm, file_progress, file_size)
                files_info.append({
                    'path': file_path,
                    'size': file_size,
                    'mtime': file_mtime,
                    'hash': file_hash
                })
                total_size += file_size

                # 更新整体进度
                if progress_callback:
                    progress_callback(min((idx + 1) / total_files * 100, 100))

                # 检查是否停止
                if self.calculation_stopped:
                    return files_info, total_size
            except Exception:
                continue

        return files_info, total_size

    def format_time(self, timestamp):
        """格式化时间戳"""
        import datetime
        return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        
    def start_calculation(self):
        """开始计算"""
        path = self.path_entry.get().strip()
        
        if not path:
            messagebox.showwarning("警告", "请先选择文件或文件夹！")
            return

        if not os.path.exists(path):
            messagebox.showerror("错误", "路径不存在！")
            return

        # 重置停止标志
        self.calculation_stopped = False

        # 禁用按钮
        self.calc_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.clear_btn.config(state=tk.DISABLED)
        self.save_btn.config(state=tk.DISABLED)
        self.progress['value'] = 0
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "计算中，请稍候...\n")
        
        # 在新线程中计算
        thread = threading.Thread(target=self.calculate_in_thread)
        thread.start()
        
    def calculate_in_thread(self):
        """在线程中执行计算"""
        try:
            path = self.path_entry.get().strip()
            algorithm = self.algo_var.get()
            is_folder = self.mode_var.get() == "folder"

            def update_progress(value):
                self.root.after(0, lambda v=value: self.progress.configure(value=v))

            if is_folder:
                files_info, total_size = self.calculate_folder_hash(path, algorithm, update_progress)
                self.root.after(0, self.update_folder_result, path, files_info, total_size)
            else:
                file_size = os.path.getsize(path)
                file_mtime = os.path.getmtime(path)
                result = self.calculate_hash(path, algorithm, update_progress, file_size)
                self.root.after(0, self.update_file_result, path, file_size, file_mtime, result)

        except Exception as e:
            self.root.after(0, self.show_error, str(e))
            
    def update_file_result(self, path, size, mtime, hash_value):
        """更新文件计算结果"""
        self.progress['value'] = 100
        self.calc_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.clear_btn.config(state=tk.NORMAL)
        self.save_btn.config(state=tk.NORMAL)

        self.result_text.delete(1.0, tk.END)
        normalized_path = path.replace('/', '\\')
        self.result_text.insert(tk.END, f"路径: {normalized_path}\n")
        self.result_text.insert(tk.END, f"大小: {self.format_size(size)}\n")
        self.result_text.insert(tk.END, f"文件数: 1 个文件\n")
        self.result_text.insert(tk.END, f"修改时间: {self.format_time(mtime)}\n")
        self.result_text.insert(tk.END, f"Hash值:\n{hash_value}\n")
        self.result_text.see(tk.END)

    def update_folder_result(self, path, files_info, total_size):
        """更新文件夹计算结果"""
        self.progress['value'] = 100
        self.calc_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.clear_btn.config(state=tk.NORMAL)
        self.save_btn.config(state=tk.NORMAL)

        self.result_text.delete(1.0, tk.END)
        normalized_path = path.replace('/', '\\')
        self.result_text.insert(tk.END, f"路径: {normalized_path}\n")
        self.result_text.insert(tk.END, f"大小: {self.format_size(total_size)}\n")
        self.result_text.insert(tk.END, f"文件数: {len(files_info)} 个文件\n")
        self.result_text.insert(tk.END, f"修改时间: -\n")
        self.result_text.insert(tk.END, "-" * 60 + "\n")

        for info in files_info:
            normalized_file_path = info['path'].replace('/', '\\')
            result_line = f"路径: {normalized_file_path}\n"
            result_line += f"大小: {self.format_size(info['size'])}\n"
            result_line += f"修改时间: {self.format_time(info['mtime'])}\n"
            result_line += f"Hash值:\n{info['hash']}\n"
            result_line += "-" * 60 + "\n"
            self.result_text.insert(tk.END, result_line)
        self.result_text.see(tk.END)
        
    def show_error(self, error_msg):
        """显示错误"""
        self.progress['value'] = 0
        self.calc_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.result_text.delete(1.0, tk.END)
        messagebox.showerror("计算错误", f"计算过程中出现错误:\n{error_msg}")

    def copy_hash(self):
        """复制hash值"""
        hash_value = self.result_text.get(1.0, tk.END).strip()

        if hash_value and hash_value != "计算中，请稍候...":
            self.root.clipboard_clear()
            self.root.clipboard_append(hash_value)
            messagebox.showinfo("提示", "Hash值已复制到剪贴板！")
        else:
            messagebox.showwarning("警告", "没有可复制的Hash值！")

    def save_result(self):
        """保存结果到文件"""
        result_text = self.result_text.get(1.0, tk.END).strip()

        if not result_text or result_text == "计算中，请稍候...":
            messagebox.showwarning("警告", "没有可保存的结果！")
            return

        # 获取默认文件名
        default_name = f"hash_result_{self.algo_var.get()}.txt"

        save_path = filedialog.asksaveasfilename(
            title="保存结果",
            defaultextension=".txt",
            initialfile=default_name,
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )

        if save_path:
            try:
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write(result_text)
                messagebox.showinfo("提示", "结果已保存成功！")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败:\n{str(e)}")


def main():
    """主函数"""
    root = tk.Tk()
    app = HashCalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
