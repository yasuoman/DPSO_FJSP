# project : GA_FJSP
# file   : pso.py
# author:yasuoman
# datetime:2021/4/6 9:51
# software: PyCharm

"""
description：
说明：参考文献：[1]丁舒阳,黎冰,侍洪波.基于改进的离散PSO算法的FJSP的研究[J].计算机科学,2018,45(04):233-239+256.
"""
#目前写的是类，如果消耗内存空间过大再说，改成函数了(4.7)
'''
说明：参考文献：[1]丁舒阳,黎冰,侍洪波.基于改进的离散PSO算法的FJSP的研究[J].计算机科学,2018,45(04):233-239+256.
'''
import numpy as np


#用于求出工序在机器上的位置，返回的值是从0开始的index
#Oi,j 知道i,j的含义
def op_in_m(i,j,job_op_num):
    # 求出这道工序在相应个机器上的位置，用job_op_num来求,
    if i == 1:
        op_index = j-1
    else:
        #切片是左闭右开
        op_index = sum(job_op_num[:i - 1]) + j-1
    return op_index


#f1操作
def f1_operator(chr,half_chr,p_table):
    ms = chr[:half_chr]
    os = chr[half_chr:]
    np.random.shuffle(os)
# 基于MS的变异，我这里直接随机选择的是ms中某个基因点来改变
    #用于选择ms某个基因点的index
    # half_chr_index= np.arange(half_chr)
    # #随机选择一个基因点
    # selected_index = np.random.choice(half_chr_index)
    # #该基因点上可加工的机器的数量
    # ava_m_num = 0
    # for pro in p_table[selected_index]:
    #     if pro != -1:
    #         ava_m_num += 1
    # #如果只有一台可用的机器
    # if ava_m_num == 1:
    #     #没得选了就是第一台可用的机器
    #     ms[selected_index] = 1
    # #如果有多台
    # else:
    #     #总的待选的机器顺序号的列表
    #     total_m_list = [i + 1 for i in range(ava_m_num)]
    #     #去掉之前选的加工机器顺序号
    #     a=ms[selected_index]
    #     total_m_list.remove(ms[selected_index])
    #     #随机选择剩余的可加工机器顺序号
    #     ms[selected_index] = np.random.choice(total_m_list)
    #轮盘赌列表
    roulette=[0,1]
    if np.random.choice(roulette)==1:
        # #打乱os
        np.random.shuffle(os)
    else:
        #基于MS的变异，我这里直接随机选择的是ms中某个基因点来改变
        #用于选择ms某个基因点的index
        half_chr_index= np.arange(half_chr)
        #随机选择一个基因点
        selected_index = np.random.choice(half_chr_index)
        #该基因点上可加工的机器的数量
        ava_m_num = 0
        for pro in p_table[selected_index]:
            if pro != -1:
                ava_m_num += 1
        #如果只有一台可用的机器
        if ava_m_num == 1:
            #没得选了就是第一台可用的机器
            ms[selected_index] = 1
        #如果有多台
        else:
            #总的待选的机器顺序号的列表
            total_m_list = [i + 1 for i in range(ava_m_num)]
            #去掉之前选的加工机器顺序号
            total_m_list.remove(ms[selected_index])
            #随机选择剩余的可加工机器顺序号
            ms[selected_index] = np.random.choice(total_m_list)
    #合并ms和os
    chr = np.hstack((ms, os))
    return chr
#f2操作
def f2_operator(n,half_chr,chr_Ek,single_best_chr,job_op_num):
    # #由操作1得到的染色体
    # chr_Ek = f1_operator()
    #初始化工件编号列表
    job_num_list = [i+1 for i in range(n)]
    #打乱列表
    np.random.shuffle(job_num_list)
    #随机选择一个从1——n的数,保证任何一个集合不为空
    index = np.random.randint(1, n)
    #得到工件集1和工件集2
    job_set1 = job_num_list[:index]
    job_set2 = job_num_list[index:]
    #分成ms和os两部分
    ms_Ek = chr_Ek[:half_chr]
    os_Ek = chr_Ek[half_chr:]
    ms_P = single_best_chr[:half_chr]
    os_P = single_best_chr[half_chr:]
    #子代的os和ms
    os_F = []
    ms_F=[0 for i in range(half_chr)]
    #遍历ms和os,
    # 论文上画的图有大问题!!!!!不能简单的将os与ms对应起来，然后给ms赋值，
    # 那样会导致比如某个工序本来最多可加工的机器个数为2，但是给它的染色体上的基因却为3了。
    #正确的理解是：将选中的比如工序O（1,2）在父代对应的ms的基因值赋值到子代的ms上O（1，2）的位置

    #用来存工件出现过几次的字典，形式{1：2}表示工件1出现了2次
    os_Ek_dict = {}
    os_P_dict = {}
    for os1,os2 in zip(os_Ek,os_P):
        #现在默认Ek的在前面
        if os1 in job_set1:
            os_F.append(os1)
            if os1 in os_Ek_dict:
                os_Ek_dict[os1]+=1
            else:
                os_Ek_dict[os1] =1
            op_index=op_in_m(os1,os_Ek_dict[os1],job_op_num)
            ms_F[op_index] = ms_Ek[op_index]
            # ms_F.append(ms_Ek[os_index])
        if os2 in job_set2:
            os_F.append(os2)
            if os2 in os_P_dict:
                os_P_dict[os2]+=1
            else:
                os_P_dict[os2] =1
            op_index=op_in_m(os2,os_P_dict[os2],job_op_num)
            ms_F[op_index] = ms_P[op_index]
            # ms_F.append(ms_P[os_index])

        # # 如果都不满足，继续看下后面的基因点
        # else:
        #     continue
    # 合并子代的ms和os
    chr = np.hstack((ms_F, os_F))
    return chr
#f3操作
def f3_operator(half_chr,chr_Fk,global_best_chr,pf,job_op_num):
    #分解成ms和os,其中os_Xk是不变化的
    ms_Xk = chr_Fk[:half_chr]
    os_Xk = chr_Fk[half_chr:]
    ms_Pg = global_best_chr[:half_chr]

    #产生随机向量R,值为0-1
    R = np.random.random_sample(half_chr)
    #找出R中小于pf的位置
    R_bool = R<pf

    # 论文上画的图同样有大问题!!!!!不能简单的将os与ms对应起来，然后给ms赋值，
    # 那样会导致比如某个工序本来最多可加工的机器个数为2，但是给它的染色体上的基因却为3了。
    # 正确的理解是：将选中的比如工序O（1,2）在父代对应的ms的基因值赋值到子代的ms上O（1，2）的位置
    #用来存工件出现过几次的字典，形式{1：2}表示工件1出现了2次
    #跟算子2太像了没意思哎
    os_F_dict = {}
    # os_Pg_dict = {}
    # #形式{2：（1，1）}表示:在os_Xk中，索引为2对应的工序为O(1,1)
    # index_F_dict = {}
    # #形式{（1，1）：3}表示在os_Pg中，工序为O(1,1)对应的索引值为3
    # index_Pg_dict = {}
    #以下是错误的理解写法
    # for os_index, os in enumerate(os_Xk):
    #     if os in os_F_dict:
    #         os_F_dict[os] += 1
    #     else:
    #         os_F_dict[os] = 1
    #     #只关心R中小于pf的部分
    #     if R_bool[os_index]:
    #         index_F_dict[os_index] = (os, os_F_dict[os])
    #
    # for os_index, os in enumerate(os_Pg):
    #     if os in os_Pg_dict:
    #         os_Pg_dict[os] += 1
    #     else:
    #         os_Pg_dict[os] = 1
    #     index_Pg_dict[(os, os_Pg_dict[os])] = os_index
    # #遍历，得到os_XK中索引和os_Pg中的索引的对应关系
    # for key, value in index_F_dict.items():
    #     #修改ms
    #     ms_Xk[key] = ms_Pg[index_Pg_dict[value]]


    for os_index, os in enumerate(os_Xk):
        if os in os_F_dict:
            os_F_dict[os] += 1
        else:
            os_F_dict[os] = 1
            #只关心R中小于pf的部分,那部分才用全局最优去替换子代中的部分
            if R_bool[os_index]:
                op_index = op_in_m(os, os_F_dict[os], job_op_num)
                ms_Xk[op_index] = ms_Pg[op_index]
    # 合并子代的ms和os
    chr = np.hstack((ms_Xk, os_Xk))
    return chr

#总的操作
def f_operator(job_op_num,p_table,chr,single_best_chr,global_best_chr,pf,o_mega,c1,c2):
    #获得额外的参数
    half_chr = p_table.shape[0]
    n = len(job_op_num)

    #产生0-1的随机数r1
    r1= np.random.random()
    if r1 < o_mega:
        #执行f1操作
        chr_Ek = f1_operator(chr,half_chr,p_table)
    else:
        chr_Ek = chr


    r2 = np.random.random()
    if r2 < c1:
        #执行f2操作
        chr_Fk = f2_operator(n,half_chr,chr_Ek,single_best_chr,job_op_num)
    else:
        chr_Fk = chr_Ek


    r3 = np.random.random()
    if r3 < c2:
        #执行f3操作
        chr_Xk = f3_operator(half_chr,chr_Fk,global_best_chr,pf,job_op_num)
    else:
        chr_Xk = chr_Fk

    return chr_Xk


