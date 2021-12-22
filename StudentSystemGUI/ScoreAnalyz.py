# 导库
import pandas as pd
import numpy as np

class ScoreAnalyz():
    def __init__(self,StudentNo):
        #获取总数据
        datas_student = pd.read_csv('./conf/学生成绩表.csv',encoding ='ansi')
        studentsNum = len(datas_student)-1 #学生人数
        #各科平均分means ， 综合成绩list overall
        datas_studentDe = datas_student.iloc[1:61,-6:]
        datas_studentDe = np.array(datas_studentDe)
        datas_studentDe = datas_studentDe.astype(np.float64)
        means = np.round(datas_studentDe.mean(axis=0),2)
        overalls = datas_studentDe.sum(axis=1)
        overallSort = sorted(overalls,reverse=True)
        subjects = ['语文','数学','英语','物理','化学','生物']
        outset = '经过数据分析'
        overallRank = '你的综合成绩排名名次是：'
        overallGreat = '在班级里属于尖子水平'
        overallGood = '在班级里属于中上水平'
        overallWorry = '在班级里属于中下水平'
        overallSad = '你的进步空间极大'
        middle1 = '成绩较好'
        middle2 = '成绩较差'
        measure = ['应多积累成语、文化常识、语言表达运用题、作文素材和文学类文本阅读的典型例题，以提升语文成绩；',
                   '应注重基础学习、制定学习计划、对知识进行查漏补缺，以提升数学成绩；',
                   '应多积累单词、积累短句、扎实语法知识、进行错题总结，以提升英语成绩；',
                   '应注重加强思维能力锻炼、多做题、总结模型，以提升物理成绩；',
                   '应牢记化学方程式、系统总结化学实验题、弄清实验本质，以提升化学成绩；',
                   '应注重课本知识、熟读课本弄清知识内部联系、联系生活实际，以提升生物成绩']
        endGood = '请继续努力，保持稳步前进，以咬定青山不放松的意志，奋力前行。'
        endBad = '千里之行从跬步，涓滴不弃成海洋，切不可妄自菲薄，只要努力总有收获，加油吧！少年。'

        #获取学号，获取数据
        sno = StudentNo
        score = datas_studentDe[sno-1] #列表有0下标，学号没有，所以要-1

        words = ''
        allScore = sum(score)
        ScoresRank = overallSort.index(allScore)+1 #列表有0下标，排名没有第0名，所有要+1
        l1 = outset+'，'+overallRank+str(ScoresRank)
        words = words  +  l1
        if ScoresRank<=0.1*studentsNum:
            l2 = overallGreat
        elif 0.1*studentsNum<ScoresRank<0.5*studentsNum:
            l2 = overallGood
        elif 0.5*studentsNum<=ScoresRank<0.9*studentsNum:
            l2 = overallWorry
        else:
            l2 = overallSad
        words = words + '，' + l2
        compareMeans = score - means
        scoreGood = []
        scoreBad = []
        for i in range(len(compareMeans)):
            if compareMeans[i] > 7 :
                scoreGood.append(i)
            else:
                scoreBad.append(i)
        l3 = ''
        if scoreGood:
            for i in range(len(scoreGood)):
                l3 = l3 + subjects[scoreGood[i]]
                if i<len(scoreGood)-1:
                    l3 = l3 + '、'
            l3 = l3 + middle1 
        l4 = ''
        if scoreBad:
            for i in range(len(scoreBad)):
                l4 = l4 + subjects[scoreBad[i]]
                if i<len(scoreBad)-1:
                    l4 = l4 + '、'
            l4 = '，'+l4 + middle2
        words = words + '，'+l3+l4
        l5 = ''
        if l4:
            for i in scoreBad:
                l5 = l5 + measure[i]
        else:
            compareMeansList = list(compareMeans)
            compareMeansSort = sorted(compareMeansList)
            i = compareMeansList.index(compareMeansSort[0])
            l5 = l5 + '虽然你的各科成绩都比较好，但通过分析，你的'+subjects[i]+'相对其他科目成绩较差，'+measure[i]
        words = words +'，' + l5
        l6 = ''
        if ScoresRank<30:
            l6 = l6 + endGood
        else:
            l6 = l6 + endBad
        words = words + l6
        self.words=words
        print(words)


if __name__ == '__main__':
    app=ScoreAnalyz(1)