import tkinter as tk
from tkinter import messagebox, ttk
import webbrowser
import threading
import time

# 全局变量，用于控制是否停止打开网页
stop_opening = False

# 全局变量，分隔符映射
splitter_dic = {"换行符": "\n", "制表符": "\t", ",": ",", "@": "@", ";": ";"}


def open_links():
    global stop_opening
    stop_opening = False

    # 获取输入文本
    input_text = asin_input.get("1.0", tk.END).strip()

    # 获取OE prefix
    oe_prefix = prefix_var.get().strip()

    # 获取和判断分隔符
    splitter = splitter_var.get()
    if splitter == "自动":
        for k in splitter_dic.keys():
            if splitter_dic[k] in input_text:
                items = input_text.split(splitter_dic[k])
                break
    else:
        items = input_text.split(splitter_dic[splitter])

    # 去除空白项并去除前后空白字符
    items = [item.strip() for item in items if item.strip()]

    print(f"items: {items}")

    if len(items) > 15:
        messagebox.showwarning("注意", "输入的 ASIN/OE 数量超过 15 个！可能造成卡顿")

    # 获取选择的站点
    default_site = site_var.get()
    site_prefix = {
        "英国": "https://www.amazon.co.uk",
        "德国": "https://www.amazon.de",
        "意大利": "https://www.amazon.it",
        "法国": "https://www.amazon.fr",
        "西班牙": "https://www.amazon.es",
    }

    ebay_prefix = {
        "英国": {
            "base": "https://www.ebay.co.uk",
            "search": "/sch/i.html?_from=R40&_nkw={query}&_sacat=0&_stpos=MK402RB&_fcid=3",
        },
        "德国": {
            "base": "https://www.ebay.de",
            "search": "/sch/i.html?_from=R40&_nkw={query}&_sacat=0&_stpos=20095&_fcid=77",
        },
    }

    for item in items:
        if stop_opening:
            break
        if item:
            time.sleep(0.6)
            print(f"\n处理item: {item}")

            # 初始化变量
            selected_site = default_site
            platform = None

            # 1. 先处理平台前缀
            lower_item = item.lower()
            if lower_item.startswith("[amazon]"):
                item = item[8:].strip()
                platform = "亚马逊"
                print(f"检测到Amazon前缀，设置平台为: {platform}")
            elif lower_item.startswith("[ebay]"):
                item = item[6:].strip()
                platform = "Ebay"
                print(f"检测到Ebay前缀，设置平台为: {platform}")

            # 2. 处理国家前缀
            if item.startswith("[") and "]" in item:
                country_code = item[1 : item.index("]")]
                item = item[item.index("]") + 1 :].strip()
                if country_code == "UK":
                    selected_site = "英国"
                elif country_code == "DE":
                    selected_site = "德国"
                elif country_code == "IT":
                    selected_site = "意大利"
                elif country_code == "FR":
                    selected_site = "法国"
                elif country_code == "ES":
                    selected_site = "西班牙"
                print(f"检测到国家前缀，设置站点为: {selected_site}")

            # 3. 如果没有平台前缀，使用下拉框选择
            if platform is None:
                platform = platform_var.get()
                print(f"无平台前缀，使用下拉框选择平台: {platform}")

            print(
                f"最终平台: {platform}, 最终站点: {selected_site}, 处理后的item: {item}"
            )

            # 生成URL
            if item.startswith("B0") and len(item) == 10:
                url = f"{site_prefix[selected_site]}/dp/{item}"
            elif (
                item.isdigit()
                and len(item) == 12
                and selected_site in ebay_prefix
                and platform == "Ebay"
            ):
                if desc_only_var.get():
                    url = f"https://itm.ebaydesc.com/itmdesc/{item}"
                else:
                    url = f'{ebay_prefix[selected_site]["base"]}/itm/{item}'
            else:
                search_item = f"{oe_prefix} {item}" if oe_prefix else item
                if platform == "亚马逊":
                    url = f"{site_prefix[selected_site]}/s?k={search_item}&i=automotive"
                else:
                    if selected_site in ebay_prefix:
                        url = f'{ebay_prefix[selected_site]["base"]}{ebay_prefix[selected_site]["search"].format(query=search_item)}'
                    else:
                        url = f"{site_prefix[selected_site]}/s?k={search_item}&i=automotive"

            print(f"生成的URL: {url}")
            webbrowser.open(url)
            root.update()


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
site_menu = ttk.Combobox(
    root, textvariable=site_var, values=["英国", "德国", "意大利", "法国", "西班牙"]
)
site_menu.pack(pady=5)

# 创建分隔符下拉菜单
splitter_var = tk.StringVar(value="自动")
splitter_label = tk.Label(root, text="选择分隔符:")
splitter_label.pack()
splitter_menu = ttk.Combobox(
    root, textvariable=splitter_var, values=["换行符", "制表符", ",", "@", ";"]
)
splitter_menu.pack(pady=5)

# 创建OE prefix输入框
prefix_var = tk.StringVar()
prefix_label = tk.Label(root, text="OE前缀(可选):")
prefix_label.pack()
prefix_entry = tk.Entry(root, textvariable=prefix_var, width=20)
prefix_entry.pack(pady=5)

# 创建只打开描述页勾选框
desc_only_var = tk.BooleanVar()
desc_only_check = tk.Checkbutton(root, text="只打开描述页", variable=desc_only_var)
desc_only_check.pack(pady=5)

# 创建按钮
open_button = tk.Button(
    root, text="打开链接", command=lambda: threading.Thread(target=open_links).start()
)
open_button.pack(pady=5)

# 绑定 ESC 键
root.bind("<Escape>", stop_opening_links)

# 运行主循环
root.mainloop()
