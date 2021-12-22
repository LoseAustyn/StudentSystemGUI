# 导库
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import DVTeacher

#获取总数据
datas_student = pd.read_csv('./conf/学生成绩表.csv',encoding ='ansi')
studentsNum = len(datas_student)-1 #学生人数

#获取第六次月考成绩
datas_studentDe = datas_student.iloc[1:61,-6:]
datas_studentDe = np.array(datas_studentDe)
datas_studentDe = datas_studentDe.astype(np.float64)

#学生成绩雷达图
def score_radarChart(no):
    sno = no #获取学号，获取数据
    score = datas_studentDe[sno-1] #列表有0下标，学号没有，所以要-1
    for i in range(3):
        score[i] = score[i]/1.5
    print(score)
    matplotlib.rcParams['font.family']='SimHei'
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    labels = np.array(['语文','数学','英语','物理','化学','生物'])
    nAttr = 6
    data = score
    angles = np.linspace(0,2*np.pi,nAttr,endpoint=False)
    data = np.concatenate((data,[data[0]]))
    angles = np.concatenate((angles,[angles[0]]))
    labels=np.concatenate((labels,[labels[0]]))
    fig = plt.figure(facecolor="white")
    plt.subplot(111,polar=True)
    plt.plot(angles,data,'bo-',color ='b',linewidth=2)
    plt.fill(angles,data,facecolor='g',alpha=0.25)
    plt.thetagrids(angles*180/np.pi,labels)
    plt.ylim(0,100)
    plt.figtext(0.52,0.97,'学生各科能力',ha='center')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    no = 1 #1为学号，用于接收学号
    score_radarChart(no) #传学号
