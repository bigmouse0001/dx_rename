import os
import re
import sqlite3
import tkinter as tk
from tkinter import filedialog

# 连接SQLite数据库(路径不带双引号)
conn = sqlite3.connect(r'C:\Users\Administrator\Desktop\批量重命名\duxiu511_pls40k.db')
c = conn.cursor()

# 定义GUI窗口
root = tk.Tk()
root.title("文件重命名工具")
root.geometry("400x400")

# 定义文件夹选择框
folder_path = tk.StringVar()
def select_folder_path():
    folder_selected = filedialog.askdirectory()
    folder_path.set(folder_selected)

label_folder_path = tk.Label(root, text="请选择要重命名文件所在的文件夹：")
label_folder_path.pack()

entry_folder_path = tk.Entry(root, textvariable=folder_path)
entry_folder_path.pack()

button_select_folder = tk.Button(root, text="选择文件夹", command=select_folder_path)
button_select_folder.pack()

# 定义文件名规则选择框
label_rule_order = tk.Label(root, text="请选择新文件名规则：")
label_rule_order.pack()

rule_order = tk.StringVar()
rule_order.set("title,author,publisher,ssid")

radio_button_1 = tk.Radiobutton(root, text="书名,作者,出版社_ssid", variable=rule_order, value="title,author,publisher,ssid")
radio_button_1.pack()

radio_button_2 = tk.Radiobutton(root, text="书名,作者,年份_ssid", variable=rule_order, value="title,author,publish_date,ssid")
radio_button_2.pack()

radio_button_3 = tk.Radiobutton(root, text="作者,书名,年份_ssid", variable=rule_order, value="author,title,publish_date,ssid")
radio_button_3.pack()

radio_button_3 = tk.Radiobutton(root, text="作者,书名,出版社_ssid", variable=rule_order, value="author,title,publisher,ssid")
radio_button_3.pack()

radio_button_4 = tk.Radiobutton(root, text="书名,作者,出版社,年份_ssid", variable=rule_order, value="title,author,publisher,publish_date,ssid")
radio_button_4.pack()

radio_button_5 = tk.Radiobutton(root, text="作者,书名,出版社,年份_ssid", variable=rule_order, value="author,title,publisher,publish_date,ssid")
radio_button_5.pack()

radio_button_4 = tk.Radiobutton(root, text="书名,作者,出版社,年份,isbn_ssid", variable=rule_order, value="title,author,publisher,publish_date,isbn,ssid")
radio_button_4.pack()

radio_button_6 = tk.Radiobutton(root, text="ssid", variable=rule_order, value="ssid")
radio_button_6.pack()


# 定义重命名按钮
def rename_files_in_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isdir(file_path):
            rename_files_in_folder(file_path)
        elif os.path.isfile(file_path):
            # 从文件名中识别出连续8位数字
            # match = re.search(r'\d{8}', filename)
            match = re.search(r'(?<!\d)\d{8}(?!\d)', filename)
            if match:
                ssid = match.group(0)
                # 执行SQL查询
                c.execute("SELECT ssid,title,author,publisher,publish_date,isbn FROM book_infos WHERE ssid = ?", (ssid,))
                result = c.fetchone()
                if result:
                    # 构造新的文件名
                    if rule_order.get() == "ssid":
                        new_filename = ssid + os.path.splitext(filename)[1]
                    else:
                        rule = rule_order.get().split(",")
                        new_filename = ""
                        for i, r in enumerate(rule):
                            if r == "title":
                                new_filename += result[1]
                            elif r == "author":
                                new_filename += result[2]
                            elif r == "publisher":
                                new_filename += result[3]
                            elif r == "publish_date":
                                new_filename += result[4]
                            elif r == "isbn":
                                new_filename += result[5]
                            if i < 3:
                                new_filename += ", "
                        new_filename += ", " + ssid + os.path.splitext(filename)[1]
                    # 将文件名中的非法字符替换为下划线
                    new_filename = re.sub(r'[\\/:*?"<>|]', '_', new_filename)
                    # 如果新文件名中有两个连续的分隔符", "，则只保留一个
                    # new_filename = re.sub(r',\s*,', ',', new_filename)
                    # 重命名文件
                    os.rename(os.path.join(folder, filename), os.path.join(folder, new_filename))

def rename_files():
    folder = folder_path.get()
    rename_files_in_folder(folder)

button_rename = tk.Button(root, text="重命名文件", command=rename_files)
button_rename.pack()

root.mainloop()
