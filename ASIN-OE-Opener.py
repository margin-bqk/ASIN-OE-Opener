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
    
    # 获取OE prefix
    oe_prefix = prefix_var.get().strip()
    
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
                # 如果有OE prefix，则拼接
                search_item = f"{oe_prefix} {item}" if oe_prefix else item
                if platform == "亚马逊":
                    url = f'{site_prefix[selected_site]}/s?k={search_item}&i=automotive'
                else:
                    if selected_site in ebay_prefix:
                        url = f'{ebay_prefix[selected_site]["base"]}{ebay_prefix[selected_site]["search"].format(query=search_item)}'
                    else:
                        url = f'{site_prefix[selected_site]}/s?k={search_item}&i=automotive'
            webbrowser.open(url)
            root.update()  # 更新 GUI

def stop_opening_links(event=None):
    global stop_opening
    stop_opening = True
    messagebox.showinfo("停止", "已停止打开网页。")

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

# 创建OE prefix输入框
prefix_var = tk.StringVar()
prefix_label = tk.Label(root, text="OE前缀(可选):")
prefix_label.pack()
prefix_entry = tk.Entry(root, textvariable=prefix_var, width=20)
prefix_entry.pack(pady=5)

# 创建按钮
open_button = tk.Button(root, text="打开链接", command=lambda: threading.Thread(target=open_links).start())
open_button.pack(pady=5)

# 绑定 ESC 键
root.bind('<Escape>', stop_opening_links)

# 运行主循环
root.mainloop()
