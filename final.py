# 书本220页
# GUI库，创建窗口和控件
import tkinter
# 消息对话框
import tkinter.messagebox
# 文件选择对话框
import tkinter.filedialog
# 时间控制，用于滚动延迟
import time
# 随机数生成，打乱名单顺序
import random
# 多线程，防止界面卡顿
import threading
# 迭代工具，创建循环迭代器
import itertools
# 操作系统接口，获取文件名
import os

# 主窗口设置
root = tkinter.Tk()
root.title('随机提问')
root.geometry('280x280+400+300')
root.resizable(False, False)


# 关闭程序时执行的函数代码，停止滚动显示学生名单
def closeWindow():
    root.flag = False
    time.sleep(0.1)
    root.destroy()


# 销毁窗口
root.protocol('WM_DELETE_WINDOW', closeWindow)

# 默认学生名单
default_students = ['张三', '李四', '王五', '赵六', '周七', '钱八']

# 当前使用的学生名单
students = default_students.copy()


# 用于控制是否滚动显示学生名单
root.flag = False
# 用于记录当前使用的名单来源
current_list_source = "默认名单"


# 上传自定义名单的函数
def upload_custom_list():
    # 打开文件选择对话框
    filepath = tkinter.filedialog.askopenfilename(
        title='选择名单文件',
        filetypes=[
            ('文本文件', '*.txt'),
            ('所有文件', '*.*')
        ]
    )

    if not filepath:  # 用户取消了选择
        return

    # 检查用户是否取消了文件选择
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # 处理文件内容，提取名单
        new_students = []
        for line in lines:
            # 去除空白字符，并按逗号、空格、制表符等分割
            line = line.strip()
            if not line:  # 跳过空行
                continue

            # 尝试多种分隔符
            for separator in [',', '，', ';', '；', ' ', '\t']:
                if separator in line:
                    names = [name.strip() for name in line.split(separator) if name.strip()]
                    new_students.extend(names)
                    break
            else:
                # 如果没有分隔符，整行作为一个名字
                new_students.append(line)

        if not new_students:
            tkinter.messagebox.showwarning('警告', '文件中没有找到有效的名字！')
            return

        # 更新学生名单
        global students, current_list_source
        students = new_students
        current_list_source = os.path.basename(filepath)

        # 更新状态标签
        lbl_status['text'] = f'已加载: {current_list_source}'
        lbl_status['fg'] = 'blue'

        # 显示加载结果
        message = f'成功加载 {len(students)} 个名字:\n' + ', '.join(students[:10])
        if len(students) > 10:
            message += f'...等共{len(students)}人'
        tkinter.messagebox.showinfo('名单加载成功', message)

    except Exception as e:
        tkinter.messagebox.showerror('错误', f'读取文件时出错:\n{str(e)}')


# 恢复默认名单
def restore_default_list():
    global students, current_list_source
    students = default_students.copy()
    current_list_source = "默认名单"
    lbl_status['text'] = '使用默认名单'
    lbl_status['fg'] = 'black'
    tkinter.messagebox.showinfo('恢复默认', '已恢复为默认名单')


# 显示当前名单
def show_current_list():
    message = f'当前名单来源: {current_list_source}\n\n'
    message += f'名单中共有 {len(students)} 人:\n\n'

    # 每行显示5个名字
    for i in range(0, len(students), 5):
        message += '  '.join(students[i:i + 5]) + '\n'

    tkinter.messagebox.showinfo('当前名单', message)


def switch():
    root.flag = True
    # 随机打乱学生名单
    t = students.copy()
    random.shuffle(t)
    t = itertools.cycle(t)
    while root.flag:
        # 滚动显示
        lb1['text'] = lb2['text']
        lb2['text'] = lb3['text']
        lb3['text'] = next(t)
        # 数字可以修改，控制滚动速度
        time.sleep(0.1)


def btnStartClick():
    # 检查是否有名单
    if not students:
        tkinter.messagebox.showwarning('警告', '当前名单为空，请先上传名单！')
        return

    # 每次单击"开始"按钮启动新线程，并禁用"开始"按钮,启用"停止"按钮
    t = threading.Thread(target=switch)
    t.start()
    btnStart['state'] = 'disabled'
    btnStop['state'] = 'normal'
    btnUpload['state'] = 'disabled'
    btnRestore['state'] = 'disabled'


def btnStopClick():
    # 单击"停止"按钮结束滚动显示,弹窗提示中奖名单,修改按钮状态
    root.flag = False
    time.sleep(0.3)
    if students:  # 确保名单不为空
        tkinter.messagebox.showinfo('恭喜', f'本次中奖: {lb2["text"]}\n\n(来自: {current_list_source})')
    btnStart['state'] = 'normal'
    btnStop['state'] = 'disabled'
    btnUpload['state'] = 'normal'
    btnRestore['state'] = 'normal'


# 创建按钮
btnUpload = tkinter.Button(root, text='上传名单', command=upload_custom_list)
btnUpload.place(x=20, y=10, width=80, height=25)

btnStart = tkinter.Button(root, text='开始', command=btnStartClick)
btnStart.place(x=110, y=10, width=60, height=25)

btnStop = tkinter.Button(root, text='停止', command=btnStopClick)
btnStop['state'] = 'disabled'
btnStop.place(x=180, y=10, width=60, height=25)

# 恢复默认名单按钮
btnRestore = tkinter.Button(root, text='恢复默认', command=restore_default_list)
btnRestore.place(x=20, y=40, width=80, height=25)

# 查看当前名单按钮
btnShow = tkinter.Button(root, text='查看名单', command=show_current_list)
btnShow.place(x=110, y=40, width=130, height=25)

# 状态标签
lbl_status = tkinter.Label(root, text='使用默认名单')
lbl_status.place(x=20, y=70, width=240, height=20)

# 用于滚动显示学生名单的3个Label组件
# 可以根据需要添加Label组件的数量,但要修改上面的线程函数代码
lb1 = tkinter.Label(root, text='')
lb1.place(x=80, y=100, width=120, height=25)

# 红色Label组件，表示中奖名单
lb2 = tkinter.Label(root, text='')
lb2['fg'] = 'red'
lb2['font'] = ('Arial', 12, 'bold')
lb2.place(x=80, y=130, width=120, height=30)

lb3 = tkinter.Label(root, text='')
lb3.place(x=80, y=165, width=120, height=25)

# 添加说明标签
lbl_help = tkinter.Label(root, text='文件格式: 每行一个名字，或用逗号分隔')
lbl_help.place(x=20, y=200, width=240, height=20)
lbl_help2 = tkinter.Label(root, text='支持: 张三\\n李四,王五\\n赵六;周七')
lbl_help2.place(x=20, y=220, width=240, height=20)
lbl_help3 = tkinter.Label(root, text='中奖者会显示在红色框中')
lbl_help3.place(x=20, y=240, width=240, height=20)
lbl_help3['fg'] = 'red'

# 启动tkinter主程序
root.mainloop()