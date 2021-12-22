# 导库
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#获取总数据
datas_student = pd.read_csv('./conf/学生成绩表.csv',encoding ='ansi')
studentsNum = len(datas_student)-1 #学生人数

class ASAS:
    #各科平均分柱状图
    def __init__(self):
        # 各科平均分means ， 综合成绩list overall
        datas_studentDe = datas_student.iloc[1:61, -6:]
        datas_studentDe = np.array(datas_studentDe)
        datas_studentDe = datas_studentDe.astype(np.float64)
        means = np.round(datas_studentDe.mean(axis=0), 2)
        plt.rcParams['font.sans-serif'] = ['SimHei']
        x = [i for i in range(0, 6)]
        y = means
        subject = ['语文', '数学', '英语', '物理', '化学', '生物']
        plt.bar(x, y, color='b', tick_label=subject, width=0.3)
        y_max = max(y)
        for x, y in enumerate(y):
            plt.text(x, y + y_max / 40, str(means[x]), ha='center')
        plt.xlabel('科目')
        plt.ylabel('分数')
        plt.title('各科平均分数')

    def show(self):
        plt.show()
        


class AAS:
    #六次月考平均分折线图
    def __init__(self):
        y = []
        for i in range(6):
            datas_studentDe = datas_student.iloc[1:61, i + 1::6]
            datas_studentDe = np.array(datas_studentDe)
            datas_studentDe = datas_studentDe.astype(np.float64)
            means = np.round(datas_studentDe.mean(axis=0), 2)
            y.append(means)
        x = ['第一次', '第二次', '第三次', '第四次', '第五次', '第六次']
        plt.title('6次月考各科平均分')  # 折线图标题
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示汉字
        plt.xlabel('月考')  # x轴标题
        plt.ylabel('分数')  # y轴标题
        for i in range(len(y)):
            plt.plot(x, y[i], marker='o', markersize=3)  # 绘制折线图，添加数据点，设置点的大小
        plt.legend(['语文', '数学', '英语', '物理', '化学', '生物'])  # 设置折线名称
    def show(self):
        plt.show()

class TS:
    #总分散点图
    def __init__(self):
        datas_studentDe = datas_student.iloc[1:61, -6:]
        datas_studentDe = np.array(datas_studentDe)
        datas_studentDe = datas_studentDe.astype(np.float64)
        overalls = datas_studentDe.sum(axis=1)
        plt.rcParams['font.sans-serif'] = ['SimHei']
        x_values = [np.linspace(0, 60, 60)]
        y_values = overalls
        # 使用scatter()绘制散点
        plt.scatter(x_values, y_values, color='gray', s=80)
        # 设置图表标title()题并给坐标轴加上标签x/ylabel()
        plt.title("学生综合成绩散点图", fontsize=18)
        plt.xlabel("学号", fontsize=14)
        plt.ylabel("总分", fontsize=14)
        # 设置刻度标记大小tick_params()
        plt.tick_params(axis='both', which='major', labelsize=14)
        # plt.show()显示绘制的图形
    def show(self):
        plt.show()

class SPC:
    #六科成绩饼状图
    def __init__(self):
        # 第一步数据处理 分为物化生分为60以下，60-75，75-85，85以上，语数英分为90以下，90-105，105-115，115以上
        datas_studentDe = datas_student.iloc[1:61, -6:]
        datas_studentDe = np.array(datas_studentDe)
        datas_studentDe = datas_studentDe.astype(np.float64)
        all_subject_rate = []
        for i in range(6):
            rate = []
            subject_score = datas_studentDe[:, i]
            if i <= 2:
                r1 = sum(subject_score < 90)
                r2 = sum(subject_score < 105) - r1
                r3 = sum(subject_score < 115) - r1 - r2
                r4 = sum(subject_score < 150) - r1 - r2 - r3
                r = 60  # 60个学生 算比例用
                rate = [r1 / r, r2 / r, r3 / r, r4 / r]
            else:
                r1 = sum(subject_score < 60)
                r2 = sum(subject_score < 75) - r1
                r3 = sum(subject_score < 85) - r1 - r2
                r4 = sum(subject_score < 100) - r1 - r2 - r3
                r = 60  # 60个学生 算比例用
                rate = [r1 / r, r2 / r, r3 / r, r4 / r]
            all_subject_rate.append(rate)
        # 解决汉字乱码问题
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用指定的汉字字体类型（此处为黑体）
        fig, axj = plt.subplots(nrows=3, ncols=2, figsize=(8, 8), dpi=100)  # 建立饼图坑
        axes = axj.flatten()  # 子图展平
        feature1 = ['90以下', '90-105', '105-115', '115以上']
        feature2 = ['60以下', '60-75', '75-85', '85以上']
        subject = ['语文', '数学', '英语', '物理', '化学', '生物']
        for ax in range(0, 6):
            explode = [0.1, 0, 0, 0]
            i = ax
            if ax > 3:
                i = ax - 3
            explode[i] = 0.06
            if ax <= 2:
                axes[ax].pie(x=all_subject_rate[ax], labels=feature1, explode=explode, autopct='%3.1f%%')
                axes[ax].set_title(subject[ax])
            else:
                axes[ax].pie(x=all_subject_rate[ax], labels=feature2, explode=explode, autopct='%3.1f%%')
                axes[ax].set_title(subject[ax])
            plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.5, hspace=0.2)  # 调整子图间距
    def show(self):
        plt.show()

if __name__ == "__main__":
    Ave_scores_all_sub() #各科平均分柱状图
    alltimes_Ave_scores()#六次月考平均分折线图
    Total_scatter()#总分散点图
    scores_pie_chart()#六科成绩饼状图