# 第一次作业10.11
# name='胡岩松'
# number=202510008942
# print(f'名字：{name} 学号：{number}')
#
# num=input('请输入一个三位数以上的整数：')
# b=num[:-2]
# print(f'百位数以上的数字是：{b}')
#
# import math
# radius=float(input('请输入圆的半径：'))
# area=math.pi*radius**2
# perimeter=2*math.pi*radius
# print(f'圆的面积是：{area:.2f},圆的周长是：{perimeter:.2f}')

# # 第二次作业10.22
# nums = [1,3,5,7]
# nums.insert(2,10)
# nums.pop()
# nums.append(9)
# print(nums)
#
# # a = input('请输入5哥整数，用空格分隔：')
# # b = [int(x) for x in a .split()]
# # b.sort(reverse=True)
# # print('降序排序后得到的列表为：',b)
# #
# # print('请输入5位学生的姓名和成绩（如Tom:85 Jerry:92 ...)')
# # c = input('请用空格分隔每个学生的信息：')
# # student = []
# # for d in c.split():
# #     zheyikuai = d.split(':')
# #     name = zheyikuai[0]
# #     score = int(zheyikuai[1])
# #     student.append([name,score])
# # print('\n解析后的学生列表：',student)
# # # 按成绩从高到低排序
# # student.sort(key=lambda x: x[1],reverse=True)
# # print('按成绩高到低排序：',student)
# # # 找出成绩最高和最低的学生
# # best_student = student[0]
# # low_student =  student[-1]
# # print('成绩最高的学生：',best_student)
# # print('成绩最低的学生：',low_student)
# # # 计算全班平均分
# # total_score = sum(score for name,score in student)
# # average_score = total_score / len(student)
# # print('全班平均分',average_score)

# 第三次作业10.28
# 1，登录口令强度提示
# a = input('请输入一行口令：')
# if len(a) < 6:
#     result = '口令过短'
# elif len(a) >=6<=10 and a.isdigit():
#     result = '强度：中'
# elif len(a) >10 :
#     has_digit = any(char.isdigit() for char in a)
#     has_alpha = any(char.isalpha() for char in a)
#     has_special = any(not char.isalnum() for char in a)
#     result = '强度：高'
# else:
#     result = '强度：低'
# print(result)

# 2，成绩分级问题
# score = int(input('请输入成绩（0~100）：'))
# if score >= 90:
#     print('A')
# elif score <=89 >=80:
#     print('B')
# elif score <=79 >=70:
#     print('C')
# elif score <=69 >=60:
#     print('D')
# elif score <60:
#     print('E')
# else:
#     print()

# 3，最大值求解
# b = int(input('请输入第一个整数:'))
# c = int(input('请输入第二个整数:'))
# d = int(input('请输入第三个整数:'))
# if b >= c:
#     if b >= d:
#         max_value = b
#     else:
#         max_value = d
# else:
#     if c >=b:
#         max_value = c
#     else:
#         max_value = b
# print(f'这三个整数中的最大值是：{max_value}')

# 4.三角形判定与分类
# first_side = float(input('请输入第一条边的长度：'))
# second_side = float(input('请输入第二条边的长度：'))
# third_side = float(input('请输入第三条边的长度：'))
# if first_side + second_side >third_side and first_side + third_side >second_side and second_side + third_side >first_side:
#     if first_side == second_side == third_side:
#         print('这是一个等边三角形')
#     elif first_side == second_side or first_side == third_side or second_side == third_side:
#         print('这是一个等腰三角形')
#     else:
#         print('这是一个普通三角形')

# 5.阶梯水费计算
# use_water = float(input('请输入使用的水量(吨)：'))
# if use_water <= 50:
#     cost_total = use_water * 2
# elif use_water <= 100:
#     cost_total = 50 * 2 + (use_water-50)*3
# else:
#     cost_total = 50*2 + 50*3 +(use_water-100)*4
# print(f'使用的水量：{use_water},总费用：{cost_total}元')

# 12.22
# 1.
# with open('lab.txt', 'w', encoding='utf-8') as f:
#     for i in range(1, 10):
#         for j in range(1, i + 1):
#             f.write(f"{j}×{i}={i*j}\t")
#         f.write("\n")
#
#
# #2.
# def process_grades():
#     try:
#         with open('grades.txt', 'r', encoding='utf-8') as e:
#             scores = []
#             for line in e:
#                 line = line.strip()
#                 if line:
#                     try:
#                         scores.append(float(line))
#                     except ValueError:
#                         print(f"警告：无法将 '{line}' 转换为数字，已跳过")
#
#         if not scores:
#             print("错误：grades.txt中没有有效的成绩数据")
#             return
#
#         average_score = sum(scores) / len(scores)
#         max_score = max(scores)
#         min_score = min(scores)
#
#
#         with open('average_scores.txt', 'w', encoding='utf-8') as e:
#             e.write(f"全班平均分：{average_score:.2f} 分\n")
#             e.write(f"最高分：{max_score:.2f} 分\n")
#             e.write(f"最低分：{min_score:.2f} 分\n")
#
#         print("成绩统计信息已成功写入 average_scores.txt 文件。")
#         print(f"处理了 {len(scores)} 个成绩数据")
#
#     except FileNotFoundError:
#         print("错误：未找到 grades.txt 文件")
#
#
#
# process_grades()
#
# # 3.
# import os
#
#
# def create_and_rename_files():
#     filenames = ['a.txt', 'b.txt', 'c.txt']
#
#     for filename in filenames:
#         with open(filename, 'w', encoding='utf-8') as g:
#             g.write(f"这是文件 {filename} 的内容\n")
#         print(f"已创建文件: {filename}")
#
#     print("\n原始文件：", ", ".join(filenames))
#
#     txt_files = [f for g in os.listdir('.') if g.endswith('.txt') and f in filenames]
#
#     print("\n正在修改文件扩展名...")
#     for txt_file in txt_files:
#         name_without_ext = os.path.splitext(txt_file)[0]
#         new_name = f"{name_without_ext}.bak"
#
#         os.rename(txt_file, new_name)
#         print(f"已重命名: {txt_file} -> {new_name}")
#
#     print("\n运行程序后：", ", ".join([f"{name.split('.')[0]}.bak" for name in filenames]))
#
#
# create_and_rename_files()