import tkinter as tk
from tkinter import ttk, messagebox as msg
import pymouse, pykeyboard, pyperclip,time
from pynput.mouse import Button,Controller as mouse_cl
from pynput.keyboard import Key,Controller as key_cl

# 创建用户窗口
mainForm = tk.Tk()
mainForm.title('自动发送程序')
mainForm.resizable(0, 0)
mainForm.iconbitmap(".\\ico.ico")

# 输入框，用于输入要群发的用户名
nameText = tk.Text(mainForm, height=10, width=40)
nameText.insert(0.0, "发送名单")
nameText.grid(row=0, padx=5, pady=5)

msgText = tk.Text(mainForm, height=10, width=40)
msgText.insert(0.0, "发送内容")
msgText.grid(row=1, padx=5, pady=5)

numText = tk.Text(mainForm, height=2,width=40)
numText.insert(0.0, "发送次数（默认 1 次）")
numText.grid(row=2, padx=5, pady=5)



mouseSearchXY = (-1, -1)
mouseInputXY = (-1, -1)


def send(string,num):
    mouse = mouse_cl()
    mouse.press(Button.left)
    mouse.release(Button.left)
    for i in range(num):  #消息发送次数
        key = key_cl()
        key.type(string)
        key.press(Key.enter)
        key.release(Key.enter)


def onClickMouseButton():
    global mouseSearchXY, mouseInputXY
    m = pymouse.PyMouse()
    msg.showinfo('提示', '请在点击确认后2秒内将鼠标移动到搜索框，2秒后自动获取搜索框鼠标位置。')
    time.sleep(2)
    mouseSearchXY = m.position()
    msg.showinfo('提示', '请在点击确认后2秒内将鼠标移动到输入框，2秒后自动获取输入框鼠标位置。')
    time.sleep(2)
    mouseInputXY = m.position()
    msg.showinfo('提示', '任务完成')


mouseButton = ttk.Button(mainForm, text='点击获取鼠标位置', width=40, command=onClickMouseButton)
mouseButton.grid(row=3, padx=5, pady=5)


def onClickStartButton():
    # 判断是否已经读取鼠标位置
    if mouseSearchXY == (-1, -1) or mouseInputXY == (-1, -1):
        msg.showerror('错误', '请先获取鼠标位置')
        return
    # 判断输入框有没有内容
    nameContent = nameText.get(0.0, tk.END).rstrip()
    if nameContent == '发送名单' or nameContent == '':
        msg.showerror('错误', '请先输入发送名单')
        return
    msgContent = msgText.get(0.0, tk.END).rstrip()
    if msgContent == '发送内容' or msgContent == '':
        msg.showerror('错误', '请先输入发送内容')
        return
    numContent = numText.get(0.0, tk.END).rstrip()
    if numContent == '发送次数（默认 1 次）':
        num = 1
    elif type(eval(numContent)) == int:
        num = int(numContent)
    else:
        msg.showerror('错误', '请先输入合理的发送次数，应为一个整数')
        return
    # 开始群发
    if not msg.askokcancel('提示', '提示完成之前别动鼠标哦'):
        return
    m = pymouse.PyMouse()  # 获取鼠标对象
    k = pykeyboard.PyKeyboard()  # 获取键盘对象
    lst = nameContent.split()
    for i in lst:
        m.click(mouseSearchXY[0], mouseSearchXY[1]) #模拟点击第一个获取的位置
        
        pyperclip.copy(i)
        k.press_key(k.control_key)
        k.tap_key('v')
        k.release_key(k.control_key)   #搜索框粘贴第一个名字     
        time.sleep(1)
        k.tap_key(k.enter_key)
        time.sleep(1)             #搜索
        ls = msgContent.split()
        for j in ls:
            m.click(mouseInputXY[0], mouseInputXY[1])   #点击输入框位置
            time.sleep(0.5)
            send(j,num)
            time.sleep(0.5)
    msg.showinfo('提示', '任务完成')


startButton = ttk.Button(mainForm, text='启动', width=40, command=onClickStartButton)
startButton.grid(row=4, padx=5, pady=5)

mainForm.mainloop()
