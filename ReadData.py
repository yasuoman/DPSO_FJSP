# project : FJSP
# file   : ReadData.py
# author:yasuoman
# datetime:2021/1/10 17:50
# software: PyCharm

"""
description：
说明：读FJSP数据
"""
'''
说明：读FJSP数据
'''
import numpy as np

class Input:
    def __init__(self, inputFile: str):
        self.__MAC_INFO = []
        self.__PRO_INTO = []
        self.__proNum = []
        self.__lines = None
        self.__input = inputFile
        self.Mac_Num=0
        self.Job_Num=0
        self.job_op_num=[]

    def getMatrix(self):
        self.__readExample()
        self.__initMatrix()
        for i in range(len(self.__lines)-1):
            lo = 0
            hi = 0
            for j in range(self.__proNum[i]):
                head = int(self.__lines[i][lo])
                hi = lo + 2 * head + 1

                lo += 1
                while lo < hi:
                    self.__MAC_INFO[i][j].append(int(self.__lines[i][lo]))
                    self.__PRO_INTO[i][j].append(int(self.__lines[i][lo + 1]))
                    lo += 2


        p_table=self.DataConversion()
        return p_table,self.job_op_num




    def __initMatrix(self):
        for i in range(len(self.__proNum)):
            self.__MAC_INFO.append([])
            self.__PRO_INTO.append([])
            for j in range(self.__proNum[i]):
                self.__MAC_INFO[i].append([])
                self.__PRO_INTO[i].append([])

    def __readExample(self):
        with open(self.__input) as fileObject:
            self.__lines = fileObject.readlines()

        self.__lines[0] = self.__lines[0].lstrip().rstrip().split("\t")

        self.Job_Num=int(self.__lines[0][0])
        self.Mac_Num=int(self.__lines[0][1])

        # 数据调整
        del self.__lines[0]
        #这里要少一个

        for i in range(len(self.__lines)-1):

            self.__lines[i] = self.__lines[i].lstrip().rstrip().split(" ")
            operation=int(self.__lines[i].pop(0))
            self.job_op_num.append(operation)
            self.__proNum.append(operation)
            while "" in self.__lines[i]:
                self.__lines[i].remove("")

    def DataConversion(self):

        total_op = np.sum(self.job_op_num)
        #加工时间矩阵p_table：总的工序数*m；其中不能进行加工用-1表示
        p_table = np.ones((total_op,self.Mac_Num),dtype=int)*(-1)
        index =0
        for (i1,i2) in zip(self.__MAC_INFO,self.__PRO_INTO):
            for (j1,j2) in zip(i1,i2):
                for (k1,k2) in zip(j1,j2):
                    p_table[index][k1-1]=k2
                index += 1

        return p_table





