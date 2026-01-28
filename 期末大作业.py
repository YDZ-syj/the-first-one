
# 导入GUI库tkinter，用于创建图形用户界面（窗口和各类控件）
import tkinter
# 导入tkinter的messagebox模块，用于弹出消息对话框（提示、警告、确认等）
import tkinter.messagebox
# 导入tkinter的filedialog模块，用于打开文件选择对话框（让用户选择本地文件）
import tkinter.filedialog
# 导入time模块，用于控制程序休眠时间（实现名单滚动延迟效果）
import time
# 导入random模块，用于生成随机数（打乱学生名单顺序，实现随机抽取）
import random
# 导入threading模块，用于创建多线程（避免名单滚动时界面卡顿）
import threading
# 导入itertools模块，用于创建迭代工具（这里用cycle实现名单循环迭代）
import itertools
# 导入os模块，用于操作系统相关操作（这里获取上传文件的文件名）
import os

# 创建主窗口对象，tkinter程序的核心容器
root = tkinter.Tk()
# 设置主窗口标题
root.title('随机提问')
# 设置主窗口大小和初始位置：宽280px×高280px，屏幕左上角偏移400px（x轴）、300px（y轴）
root.geometry('280x280+400+300')
# 禁止调整主窗口大小（宽、高均不可变）
root.resizable(False, False)


# 定义关闭窗口时执行的函数：停止名单滚动并销毁窗口
def closeWindow():
    # 设置控制滚动的标志为False，终止滚动循环
    root.flag = False
    # 休眠0.1秒，确保滚动线程有时间响应停止信号
    time.sleep(0.1)
    # 彻底销毁主窗口，结束程序运行
    root.destroy()


# 绑定窗口关闭事件（用户点击右上角×时），触发closeWindow函数
root.protocol('WM_DELETE_WINDOW', closeWindow)

# 定义默认学生名单（程序初始自带的名单数据）
default_students = ['张三', '李四', '王五', '赵六', '周七', '钱八']
# 当前使用的学生名单（初始复制默认名单，后续可通过上传替换）
students = default_students.copy()
# 定义滚动控制标志（True=滚动中，False=停止滚动），绑定在root对象上方便全局访问
root.flag = False
# 记录当前名单的来源（默认名单/上传的文件名），用于状态显示
current_list_source = "默认名单"


# 定义上传自定义名单的函数（让用户选择本地txt文件作为名单）
def upload_custom_list():
    # 打开文件选择对话框，让用户选择名单文件
    filepath = tkinter.filedialog.askopenfilename(
        title='选择名单文件',  # 对话框标题
        filetypes=[  # 允许选择的文件类型
            ('文本文件', '*.txt'),  # 优先显示txt文件
            ('所有文件', '*.*')  # 可选所有类型文件
        ]
    )
    # 如果用户取消了文件选择（filepath为空），直接返回不执行后续操作
    if not filepath:
        return

    # 尝试读取并解析选中的文件（捕获可能出现的错误，如文件损坏、编码问题）
    try:
        # 以只读模式打开文件，指定编码为utf-8（避免中文乱码）
        with open(filepath, 'r', encoding='utf-8') as file:
            # 读取文件所有行，存入lines列表
            lines = file.readlines()

        # 初始化新名单列表，用于存储解析后的学生姓名
        new_students = []
        # 遍历文件的每一行，提取姓名
        for line in lines:
            # 去除行首尾的空白字符（空格、换行符、制表符等）
            line = line.strip()
            # 如果处理后是空行，跳过不处理
            if not line:
                continue

            # 尝试用多种分隔符分割行内容（适配不同用户的输入习惯）
            for separator in [',', '，', ';', '；', ' ', '\t']:
                # 如果当前行包含该分隔符
                if separator in line:
                    # 按分隔符分割行，去除每个姓名的空白字符，过滤空字符串
                    names = [name.strip() for name in line.split(separator) if name.strip()]
                    # 将分割后的姓名添加到新名单
                    new_students.extend(names)
                    # 跳出分隔符循环，处理下一行
                    break
            else:
                # 如果该行没有任何分隔符，整行作为一个姓名添加到新名单
                new_students.append(line)

        # 如果解析后新名单为空，弹出警告提示
        if not new_students:
            tkinter.messagebox.showwarning('警告', '文件中没有找到有效的名字！')
            return

        # 全局变量声明（修改函数外部的students和current_list_source）
        global students, current_list_source
        # 更新当前使用的学生名单为解析后的新名单
        students = new_students
        # 更新名单来源为选中文件的文件名（仅保留文件名，去掉路径）
        current_list_source = os.path.basename(filepath)

        # 更新状态标签的显示内容（告知用户已加载的名单）
        lbl_status['text'] = f'已加载: {current_list_source}'
        # 设置状态标签文字颜色为蓝色
        lbl_status['fg'] = 'blue'

        # 构建加载成功的提示信息
        message = f'成功加载 {len(students)} 个名字:\n' + ', '.join(students[:10])
        # 如果名单超过10人，省略后续名字并显示总人数
        if len(students) > 10:
            message += f'...等共{len(students)}人'
        # 弹出信息对话框，展示加载结果
        tkinter.messagebox.showinfo('名单加载成功', message)

    # 捕获读取文件时的所有异常（如文件不存在、权限不足、编码错误等）
    except Exception as e:
        # 弹出错误对话框，显示具体错误信息
        tkinter.messagebox.showerror('错误', f'读取文件时出错:\n{str(e)}')


# 定义恢复默认名单的函数（将当前名单重置为初始默认名单）
def restore_default_list():
    # 全局变量声明（修改函数外部的students和current_list_source）
    global students, current_list_source
    # 重新复制默认名单到当前名单（避免直接赋值导致关联修改）
    students = default_students.copy()
    # 更新名单来源为"默认名单"
    current_list_source = "默认名单"
    # 更新状态标签显示
    lbl_status['text'] = '使用默认名单'
    # 恢复状态标签文字颜色为黑色
    lbl_status['fg'] = 'black'
    # 弹出提示，告知用户已恢复默认名单
    tkinter.messagebox.showinfo('恢复默认', '已恢复为默认名单')


# 定义显示当前名单的函数（展示当前使用的名单详情）
def show_current_list():
    # 构建当前名单信息：先显示名单来源
    message = f'当前名单来源: {current_list_source}\n\n'
    # 显示名单中的总人数
    message += f'名单中共有 {len(students)} 人:\n\n'
    # 格式化名单显示，每行最多显示5个名字
    for i in range(0, len(students), 5):
        # 截取当前行的5个名字，用两个空格分隔，添加换行符
        message += '  '.join(students[i:i + 5]) + '\n'
    # 弹出信息对话框，展示完整名单
    tkinter.messagebox.showinfo('当前名单', message)


# 定义名单滚动显示的核心函数（在子线程中运行，避免阻塞界面）
def switch():
    # 设置滚动标志为True，启动滚动
    root.flag = True
    # 复制当前学生名单（避免打乱原始名单）
    t = students.copy()
    # 随机打乱复制后的名单顺序
    random.shuffle(t)
    # 创建循环迭代器（名单滚动到末尾后自动从头开始）
    t = itertools.cycle(t)

    # 循环滚动：只要滚动标志为True，就持续更新显示
    while root.flag:
        # 滚动动画逻辑：将下一个名字依次传递给三个Label
        lb1['text'] = lb2['text']  # 第一个Label显示第二个Label之前的内容
        lb2['text'] = lb3['text']  # 第二个Label显示第三个Label之前的内容
        lb3['text'] = next(t)  # 第三个Label显示迭代器的下一个名字
        # 控制滚动速度：休眠0.1秒（数值越小滚动越快，越大越慢）
        time.sleep(0.1)


# 定义"开始"按钮的点击事件处理函数
def btnStartClick():
    # 检查当前名单是否为空，如果为空弹出警告
    if not students:
        tkinter.messagebox.showwarning('警告', '当前名单为空，请先上传名单！')
        return

    # 创建子线程，执行switch函数（名单滚动）
    t = threading.Thread(target=switch)
    # 启动子线程
    t.start()

    # 更新按钮状态：禁用"开始"、启用"停止"、禁用"上传名单"和"恢复默认"
    btnStart['state'] = 'disabled'
    btnStop['state'] = 'normal'
    btnUpload['state'] = 'disabled'
    btnRestore['state'] = 'disabled'


# 定义"停止"按钮的点击事件处理函数
def btnStopClick():
    # 设置滚动标志为False，停止滚动
    root.flag = False
    # 休眠0.3秒，确保滚动线程完全停止，避免显示异常
    time.sleep(0.3)

    # 确保名单不为空时，弹出中奖提示
    if students:
        tkinter.messagebox.showinfo('恭喜', f'本次中奖: {lb2["text"]}\n\n(来自: {current_list_source})')

    # 恢复按钮状态：启用"开始"、禁用"停止"、启用"上传名单"和"恢复默认"
    btnStart['state'] = 'normal'
    btnStop['state'] = 'disabled'
    btnUpload['state'] = 'normal'
    btnRestore['state'] = 'normal'


# 创建"上传名单"按钮：绑定upload_custom_list函数，设置位置和大小
btnUpload = tkinter.Button(root, text='上传名单', command=upload_custom_list)
btnUpload.place(x=20, y=10, width=80, height=25)

# 创建"开始"按钮：绑定btnStartClick函数，设置位置和大小
btnStart = tkinter.Button(root, text='开始', command=btnStartClick)
btnStart.place(x=110, y=10, width=60, height=25)

# 创建"停止"按钮：绑定btnStopClick函数，初始状态为禁用，设置位置和大小
btnStop = tkinter.Button(root, text='停止', command=btnStopClick)
btnStop['state'] = 'disabled'
btnStop.place(x=180, y=10, width=60, height=25)

# 创建"恢复默认"按钮：绑定restore_default_list函数，设置位置和大小
btnRestore = tkinter.Button(root, text='恢复默认', command=restore_default_list)
btnRestore.place(x=20, y=40, width=80, height=25)

# 创建"查看名单"按钮：绑定show_current_list函数，设置位置和大小
btnShow = tkinter.Button(root, text='查看名单', command=show_current_list)
btnShow.place(x=110, y=40, width=130, height=25)

# 创建状态标签：显示当前名单来源，设置位置和大小
lbl_status = tkinter.Label(root, text='使用默认名单')
lbl_status.place(x=20, y=70, width=240, height=20)

# 创建3个Label组件，用于滚动显示学生名单（形成滚动动画效果）
# 第一个Label：显示上方滚动内容，设置位置和大小
lb1 = tkinter.Label(root, text='')
lb1.place(x=80, y=100, width=120, height=25)

# 第二个Label：显示中奖名单（核心显示区），设置红色、加粗字体，位置和大小
lb2 = tkinter.Label(root, text='')
lb2['fg'] = 'red'  # 文字颜色为红色
lb2['font'] = ('Arial', 12, 'bold')  # 字体：Arial、12号、加粗
lb2.place(x=80, y=130, width=120, height=30)

# 第三个Label：显示下方滚动内容，设置位置和大小
lb3 = tkinter.Label(root, text='')
lb3.place(x=80, y=165, width=120, height=25)

# 创建说明标签1：提示文件格式要求，设置位置和大小
lbl_help = tkinter.Label(root, text='文件格式: 每行一个名字，或用逗号分隔')
lbl_help.place(x=20, y=200, width=240, height=20)

# 创建说明标签2：展示格式示例，设置位置和大小
lbl_help2 = tkinter.Label(root, text='支持: 张三\\n李四,王五\\n赵六;周七')
lbl_help2.place(x=20, y=220, width=240, height=20)

# 创建说明标签3：提示中奖者显示位置，设置红色文字，位置和大小
lbl_help3 = tkinter.Label(root, text='中奖者会显示在红色框中')
lbl_help3.place(x=20, y=240, width=240, height=20)
lbl_help3['fg'] = 'red'  # 文字颜色为红色

# 启动tkinter主事件循环（让窗口保持显示，监听用户操作，程序入口）
root.mainloop()