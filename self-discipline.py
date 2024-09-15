import tkinter as tk
from tkinter import messagebox
import threading
import time
import pygetwindow as gw

# 初始化全局变量
timer_running = False
start_time = 0  # 开始时间
elapsed_time = 0  # 累计的计时时间
startup_flag = True  # 启动标志，用于区分启动初期状态

# 检测 Edge 浏览器是否打开了抖音
def monitor_douyin():
    global timer_running, start_time, elapsed_time, startup_flag
    notified = False  # 用于跟踪是否已经提示过用户
    
    while True:
        douyin_open = False  # 标记是否打开了抖音
        # 获取所有打开的窗口
        windows = gw.getAllTitles()
        # 检查所有窗口标题是否包含抖音
        for title in windows:
            if 'douyin.com' in title.lower() or '抖音' in title:
                douyin_open = True
                break  # 找到抖音页面就停止搜索

        if douyin_open:
            if timer_running:
                # 停止计时
                stop_timer()
            # 持续提示用户
            if not notified and not startup_flag:
                messagebox.showinfo("提醒", "你已经打开了抖音！请专注工作。")
                notified = True  # 设置为已提示
        else:
            if notified:  # 如果之前提示过用户，且现在抖音关闭
                notified = False  # 重置通知状态

        # 如果程序刚启动，跳过检查
        if startup_flag:
            startup_flag = False
        
        time.sleep(5)  # 每5秒检查一次

# 番茄钟计时器函数 (正向计时)
def start_timer(label):
    global timer_running, start_time, elapsed_time
    timer_running = True
    start_time = time.time() - elapsed_time  # 继续从暂停时的时间计时

    def count_up():
        global timer_running, elapsed_time
        if timer_running:
            elapsed_time = time.time() - start_time
            mins, secs = divmod(int(elapsed_time), 60)
            time_format = f'{mins:02}:{secs:02}'
            label.config(text=time_format)
            label.after(1000, count_up)  # 每秒更新一次

    count_up()

# 停止计时器
def stop_timer():
    global timer_running
    timer_running = False
    # 可以在这里添加更多的停止逻辑，比如更新 UI 状态
    timer_label.config(fg="#dc143c")  # 改变计时器标签的颜色表示暂停状态

# 重置计时器显示
def reset_timer(label):
    stop_timer()  # 确保计时器停止
    label.config(text="00:00")  # 重置显示
    global elapsed_time
    elapsed_time = 0  # 重置累计时间
    # 更新按钮状态
    start_button.config(text="开始/继续")  # 更新按钮文本为“开始/继续”
    timer_label.config(fg="#007acc")  # 恢复计时器标签颜色

# 在新线程中启动番茄钟
def start_pomodoro(label):
    label.config(fg="#007acc")  # 恢复计时器标签颜色为蓝色
    threading.Thread(target=start_timer, args=(label,)).start()

# 主UI设置
def main_ui():
    global timer_label, start_button  # 声明为全局变量，以便其他函数访问

    # 创建主窗口
    root = tk.Tk()
    root.title("番茄钟")

    # 设置窗口大小
    root.geometry("300x325")

    # 设置背景颜色
    root.configure(bg="#f0f8ff")  # 浅蓝色背景

    # 创建标题标签
    title_label = tk.Label(root, text="专注时间", font=('Helvetica', 18, 'bold'), bg="#f0f8ff", fg="#333333")
    title_label.pack(pady=10)

    # 创建计时器标签
    timer_label = tk.Label(root, text="00:00", font=('Helvetica', 36), bg="#f0f8ff", fg="#007acc")
    timer_label.pack(pady=20)

    # 创建开始/继续按钮
    start_button = tk.Button(root, text="开始/继续", font=('SimSun', 12), command=lambda: start_pomodoro(timer_label), bg="#32cd32", fg="white", relief='raised', bd=3)
    start_button.pack(pady=10)

    # 创建暂停按钮
    stop_button = tk.Button(root, text="暂停", font=('SimSun', 12), command=stop_timer, bg="#dc143c", fg="white", relief='raised', bd=3)
    stop_button.pack(pady=10)

    # 创建归零按钮
    reset_button = tk.Button(root, text="归零", font=('SimSun', 12), command=lambda: reset_timer(timer_label), bg="#1e90ff", fg="white", relief='raised', bd=3)
    reset_button.pack(pady=10)

    # 在单独线程中开始监控抖音
    threading.Thread(target=monitor_douyin, daemon=True).start()

    # 运行主循环
    root.mainloop()

if __name__ == "__main__":
    main_ui()