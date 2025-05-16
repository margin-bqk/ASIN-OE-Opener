import tkinter as tk
from tkinter import messagebox, ttk
import webbrowser
import threading
import time

# 全局变量，用于控制是否停止打开网页
stop_opening = False

def open_links():
    global stop_opening
    stop_opening = False
    
    # 获取输入文本
    input_text = asin_input.get("1.0", tk.END).strip()
    
    # 判断分隔符是换行符还是逗号
    if '\n' in input_text:
        items = input_text.split('\n')
    else:
        items = input_text.split(',')
    
    # 去除空白项并去除前后空白字符
    items = [item.strip() for item in items if item.strip()]

    print(f'items: {items}')
    
    if len(items) > 10:
        messagebox.showwarning("注意", "输入的 ASIN/OE 数量超过 10 个！可能造成卡顿")
    
    # 获取选择的站点
    default_site = site_var.get()
    site_prefix = {
        "英国": "https://www.amazon.co.uk",
        "德国": "https://www.amazon.de",
        "意大利": "https://www.amazon.it",
        "法国": "https://www.amazon.fr",
        "西班牙": "https://www.amazon.es"
    }
    
    ebay_prefix = {
        "英国": {
            "base": "https://www.ebay.co.uk",
            "search": "/sch/i.html?_from=R40&_nkw={query}&_sacat=0&_stpos=MK402RB&_fcid=3"
        },
        "德国": {
            "base": "https://www.ebay.de", 
            "search": "/sch/i.html?_from=R40&_nkw={query}&_sacat=0&_stpos=20095&_fcid=77"
        }
    }
    
    for item in items:
        if stop_opening:
            break
        if item:
            time.sleep(0.6)
            # 检查是否有国家前缀
            if item.startswith('[') and ']' in item:
                country_code = item[1:item.index(']')]
                item = item[item.index(']') + 1:].strip()
                if country_code == 'UK':
                    selected_site = '英国'
                elif country_code == 'DE':
                    selected_site = '德国'
                elif country_code == 'IT':
                    selected_site = '意大利'
                elif country_code == 'FR':
                    selected_site = '法国'
                elif country_code == 'ES':
                    selected_site = '西班牙'
            else:
                selected_site = default_site

            print(selected_site, item)  
            
            # 获取选择的平台
            platform = platform_var.get()
            
            # 严格判断是否为 ASIN
            if item.startswith('B0') and len(item) == 10:
                # 如果是 ASIN
                url = f'{site_prefix[selected_site]}/dp/{item}'
            elif item.isdigit() and len(item) == 12 and selected_site in ebay_prefix and platform == "Ebay":
                # 如果是 eBay itemid
                url = f'{ebay_prefix[selected_site]["base"]}/itm/{item}'
            else:
                # 如果是 OE
                if platform == "亚马逊":
                    url = f'{site_prefix[selected_site]}/s?k={item}&i=automotive'
                else:
                    if selected_site in ebay_prefix:
                        url = f'{ebay_prefix[selected_site]["base"]}{ebay_prefix[selected_site]["search"].format(query=item)}'
                    else:
                        url = f'{site_prefix[selected_site]}/s?k={item}&i=automotive'
            webbrowser.open(url)
            root.update()  # 更新 GUI

def stop_opening_links(event=None):
    global stop_opening
    stop_opening = True
    messagebox.showinfo("停止", "已停止打开网页。")

def show_instructions():
    instructions = """
    # ASIN/OE 链接打开工具

    ## 功能概述

    该工具用于批量打开 ASIN 或 OE 链接，支持多个国家的 Amazon 和 eBay 网站。用户可以在输入框中输入多个 ASIN 或 OE 编号，并选择目标平台和站点，工具会自动打开相应的链接。

    ## 主要功能

    ### 1. 输入 ASIN/OE 编号

    用户可以在输入框中输入多个 ASIN 或 OE 编号，编号之间可以用换行符或逗号分隔。

    ### 2. 选择目标站点

    用户可以从下拉菜单中选择目标站点，支持以下站点：
    - 英国
    - 德国
    - 意大利
    - 法国
    - 西班牙

    ### 3. 打开链接

    点击“打开链接”按钮后，工具会逐个打开输入的 ASIN 或 OE 编号对应的链接。支持以下情况：
    - 如果编号以 `B0` 开头且长度为 10，则认为是 ASIN，打开 Amazon 链接。
    - 如果编号是 12 位数字且目标站点为英国或德国，则认为是 eBay itemid，打开 eBay 链接。
    - 其他情况则认为是 OE 编号，打开 Amazon 搜索链接。

    ### 4. 停止打开链接

    用户可以按下 `ESC` 键来停止打开链接，工具会弹出提示框告知用户已停止操作。

    ## 详细说明

    ### 输入处理

    - 获取输入框中的文本，按换行符或逗号分隔成多个编号。
    - 去除空白项并去除前后空白字符。
    - 如果输入的编号超过 10 个，弹出警告提示框。

    ### 站点选择

    - 用户可以从下拉菜单中选择默认站点。
    - 支持的站点包括英国、德国、意大利、法国和西班牙。

    ### 链接生成

    - 根据用户选择的站点和编号类型，生成相应的链接并打开。
    - 支持按下 `ESC` 键停止打开链接。

    ### 国家前缀处理

    - 检查编号是否有国家前缀（例如 `[UK]`）。
    - 根据国家前缀选择相应的站点。

    ### 链接类型判断

    - 如果编号以 `B0` 开头且长度为 10，则认为是 ASIN，生成 Amazon 链接。
    - 如果编号是 12 位数字且目标站点为英国或德国，则认为是 eBay itemid，生成 eBay 链接。
    - 其他情况则认为是 OE 编号，生成 Amazon 搜索链接。

    ## 界面元素

    - 主窗口：用于显示工具界面。
    - 输入框：用于输入多个 ASIN 或 OE 编号。
    - 站点选择下拉菜单：用于选择目标站点。
    - 打开链接按钮：用于开始批量打开链接。
    - 停止操作：按下 `ESC` 键停止打开链接。

    ## 使用方法

    1. 在输入框中输入多个 ASIN 或 OE 编号，编号之间用换行符或逗号分隔。
    2. 从下拉菜单中选择目标站点。
    3. 点击“打开链接”按钮，工具会逐个打开输入的编号对应的链接。
    4. 如果需要停止操作，按下 `ESC` 键。
    """
    instruction_window = tk.Toplevel(root)
    instruction_window.title("使用说明")
    instruction_text = tk.Text(instruction_window, wrap=tk.WORD)
    instruction_text.insert(tk.END, instructions)
    instruction_text.config(state=tk.DISABLED)
    instruction_text.pack(expand=True, fill=tk.BOTH)

# 创建主窗口
root = tk.Tk()
root.title("ASIN/OE 链接打开工具")

# 创建输入框
asin_input = tk.Text(root, height=10, width=50)
asin_input.pack(pady=10)

# 创建平台选择下拉菜单
platform_var = tk.StringVar(value="亚马逊")
platform_label = tk.Label(root, text="选择平台:")
platform_label.pack()
platform_menu = ttk.Combobox(root, textvariable=platform_var, values=["亚马逊", "Ebay"])
platform_menu.pack(pady=5)

# 创建站点选择下拉菜单
site_var = tk.StringVar(value="德国")
site_label = tk.Label(root, text="选择站点:")
site_label.pack()
site_menu = ttk.Combobox(root, textvariable=site_var, values=["英国", "德国", "意大利", "法国", "西班牙"])
site_menu.pack(pady=5)

# 创建按钮
open_button = tk.Button(root, text="打开链接", command=lambda: threading.Thread(target=open_links).start())
open_button.pack(pady=5)

# 添加显示说明按钮
instruction_button = tk.Button(root, text="显示说明", command=show_instructions)
instruction_button.pack(pady=5)

# 绑定 ESC 键
root.bind('<Escape>', stop_opening_links)

# 运行主循环
root.mainloop()
