# 导库
import pandas as pd
from sklearn.linear_model import LinearRegression as LR
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
import numpy as np # 画图
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error as MSE
import matplotlib.pyplot as plt

class ScorePre():
    def __init__(self,subject):
        #获取总数据
        datas_student = pd.read_csv('./conf/学生成绩表.csv',encoding ='ansi')
        K = len(datas_student) - 1 #学生数

        #处理数据 sno_score [[学号],[语文成绩...],[数学成绩...]...] score_C语文成绩 _M数学成绩
        sno_scores = []
        for i in range(K):
            sno_score = []
            sno = datas_student.iloc[i + 1,0]
            score_C = list(datas_student.iloc[i + 1,1::6].apply(float))
            score_M = list(datas_student.iloc[i + 1,2::6].apply(float))
            score_E = list(datas_student.iloc[i + 1,3::6].apply(float))
            score_P = list(datas_student.iloc[i + 1,4::6].apply(float))
            score_CH = list(datas_student.iloc[i + 1,5::6].apply(float))
            score_B = list(datas_student.iloc[i + 1,6::6].apply(float))
            sno_score = [sno,score_C,score_M,score_E,score_P,score_CH,score_B]
            sno_scores.append(sno_score)

        sno_scores = np.array(sno_scores)

        #训练数据
        #语文
        XScore_C = np.array(list(sno_scores[:,1]))
        XScore_C , YScore_C = XScore_C[:,:-1],XScore_C[:,-1]
        #数学
        XScore_M = np.array(list(sno_scores[:,2]))
        XScore_M , YScore_M = XScore_M[:,:-1],XScore_M[:,-1]
        #英语
        XScore_E = np.array(list(sno_scores[:,3]))
        XScore_E , YScore_E = XScore_E[:,:-1],XScore_E[:,-1]
        #物理
        XScore_P = np.array(list(sno_scores[:,4]))
        XScore_P , YScore_P = XScore_P[:,:-1],XScore_P[:,-1]
        #化学
        XScore_B = np.array(list(sno_scores[:,5]))
        XScore_B , YScore_B = XScore_B[:,:-1],XScore_B[:,-1]
        #生物
        XScore_CH = np.array(list(sno_scores[:,6]))
        XScore_CH , YScore_CH = XScore_CH[:,:-1],XScore_CH[:,-1]

        lists1 = [XScore_C,XScore_M,XScore_E,XScore_P,XScore_B,XScore_CH]
        lists2 = [YScore_C,YScore_M,YScore_E,YScore_P,YScore_B,YScore_CH]
        subjects = ['语文','数学','英语','物理','化学','生物']


        #预测数据,取最后5次成绩作为预测数据
        XtScore_C = np.array(list(sno_scores[:,1]))
        XtScore_C = XtScore_C[:,1:]
        #数学
        XtScore_M = np.array(list(sno_scores[:,2]))
        XtScore_M = XtScore_M[:,1:]
        #英语
        XtScore_E = np.array(list(sno_scores[:,3]))
        XtScore_E = XtScore_E[:,1:]
        #物理
        XtScore_P = np.array(list(sno_scores[:,4]))
        XtScore_P = XtScore_P[:,1:]
        #化学
        XtScore_B = np.array(list(sno_scores[:,5]))
        XtScore_B = XtScore_B[:,1:]
        #生物
        XtScore_CH = np.array(list(sno_scores[:,6]))
        XtScore_CH = XtScore_CH[:,1:]
        Tlists = [XtScore_C,XtScore_M,XtScore_E,XtScore_P,XtScore_B,XtScore_CH]

        #预测
        subject = subject
        index1 = subjects.index(subject)
        X,y = lists1[index1] ,lists2[index1]
        model = LR(fit_intercept=True,normalize=True).fit(X,y)
        Tx = Tlists[index1]
        yhat = model.predict(Tx)
        for i in range(len(yhat)):
            if yhat[i] - int(yhat[i]) > 0.75:
                yhat[i] = int(yhat[i]) + 1
            elif yhat[i] - int(yhat[i]) < 0.25:
                yhat[i] = int(yhat[i])
            else:
                yhat[i] = int(yhat[i]) + 0.5

        x = [i + 1 for i in range(60)]
        dicts = dict(zip(x,yhat))
        self.dicts = dicts

if __name__ == '__main__':
    window = ScorePre('生物')
