# project : GA_FJSP
# file   : Encode.py
# author:yasuoman
# datetime:2021/4/4 15:59
# software: PyCharm

"""
description：种群初始化编码
说明：参考书籍：柔性作业车间调度智能算法及其应用  3.2.3FJSP的初始化
"""
'''
说明：参考书籍：柔性作业车间调度智能算法及其应用  3.2.3FJSP的初始化
'''
import numpy as np
import random
class Encode:
    def __init__(self,Pop_size,p_table,job_op_num):
        #Pop_size为种群个数
        self.GS_num = int(0.6 * Pop_size)  # 全局选择的个数
        self.LS_num = int(0.2 * Pop_size)  # 局部选择的个数
        self.RS_num = int(0.2 * Pop_size)  # 随机选择的个数
        self.p_table = p_table
        self.half_chr = p_table.shape[0]
        self.job_op_num = job_op_num
        self.m = p_table.shape[1]
        self.n = len(job_op_num)
    #得到初始有序的一维os
    def order_os(self):
        order_os=[(index+1) for index,op in enumerate(self.job_op_num) for i in range(op)]
        # for index,op in enumerate(self.job_op_num):
        #     for i in range(op):
        #         order_OS.append(index+1)
        #
        return order_os
    def random_selection(self):
        MS=np.empty((self.RS_num,self.half_chr),dtype=int)
        #随机选择OS
        OS = np.empty((self.RS_num, self.half_chr),dtype=int)
        order_os = self.order_os()[:]
        # 随机选择MS
        for episode in range(self.RS_num):
            #打乱os的顺序
            np.random.shuffle(order_os)
            #随机选择os
            OS[episode]=order_os[:]
            for op_index,p in enumerate(self.p_table):
                #找出该工件能够加工的机器的序号
                ava_m = [(index+1) for index in range(len(p)) if p[index]!=-1]
                #随机选择,先这样写着
                MS[episode][op_index]=np.random.choice(np.arange(len(ava_m)))+1

        chr = np.hstack((MS, OS))
        return chr
    def global_selection(self):
        MS = np.empty((self.GS_num, self.half_chr), dtype=int)
        # 随机选择OS
        OS = np.empty((self.GS_num, self.half_chr), dtype=int)
        order_os = self.order_os()[:]
        # 随机选择MS
        for episode in range(self.GS_num):
            # 打乱os的顺序
            np.random.shuffle(order_os)
            # 随机选择os
            OS[episode] = order_os[:]
            # 用于随机选择的工件集合
            job_list = [i for i in range(self.n)]
            # 初始化值为0的长度为m的负荷数组
            M_load = np.zeros(self.m, dtype=int)
            for i in range(self.n):
                #随机选择一个工件
                job_num=np.random.choice(job_list)
                #在这个工件的所有工序上进行遍历
                for op in range(sum(self.job_op_num[:job_num]), sum(self.job_op_num[:job_num])+self.job_op_num[job_num]):
                    #得到临时的机器负荷数组
                    temp_load = np.array([pro + load for (pro, load) in zip(self.p_table[op], M_load) if pro != -1])
                    #得到临时的机器负荷索引
                    temp_index = [index for (index, pro) in enumerate(self.p_table[op]) if pro != -1]
                    #选取临时的机器符合最小的索引
                    ava_min_index = np.argmin(temp_load)
                    #将最小的索引+1放入MS中，即最好的可用的机器号,注意这里的下标是op,因为是随机找的工件
                    MS[episode][op]=ava_min_index+1
                    #更新机器负荷列表
                    M_load[temp_index[ava_min_index]] = temp_load[ava_min_index]
                #删除刚刚随机的工件号，继续随机进行
                job_list.remove(job_num)

        chr = np.hstack((MS, OS))
        return chr
    def local_selection(self):
        MS = np.empty((self.LS_num, self.half_chr), dtype=int)
        # 随机选择OS
        OS = np.empty((self.LS_num, self.half_chr), dtype=int)
        order_os = self.order_os()[:]
        # 随机选择MS
        for episode in range(self.LS_num):
            # 打乱os的顺序
            np.random.shuffle(order_os)
            # 随机选择os
            OS[episode] = order_os[:]
            # 因为不能直接得到二维矩阵的列索引，这里手工设置一个
            chr_index = 0


            #依次遍历整个工件
            for i in range(self.n):
                # 初始化值/重新置为0的长度为m的负荷数组
                M_load = np.zeros(self.m, dtype=int)

                # 在这个工件的所有工序上进行遍历
                for op in range(sum(self.job_op_num[:i]),
                                sum(self.job_op_num[:i]) + self.job_op_num[i]):
                    # 得到临时的机器负荷数组
                    temp_load = np.array([pro + load for (pro, load) in zip(self.p_table[op], M_load) if pro != -1])
                    # 得到临时的机器负荷索引
                    temp_index = [index for (index, pro) in enumerate(self.p_table[op]) if pro != -1]
                    # 选取临时的机器符合最小的索引
                    ava_min_index = np.argmin(temp_load)
                    # 将最小的索引+1放入MS中，即最好的可用的机器号
                    MS[episode][chr_index] = ava_min_index + 1
                    # 列索引加1
                    chr_index += 1
                    # 更新机器负荷列表
                    M_load[temp_index[ava_min_index]] = temp_load[ava_min_index]

        chr = np.hstack((MS, OS))
        return chr

