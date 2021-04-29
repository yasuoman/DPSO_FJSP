# project : GA_FJSP
# file   : main.py
# author:yasuoman
# datetime:2021/4/4 13:40
# software: PyCharm

"""
description：
说明：参考文献[1]丁舒阳,黎冰,侍洪波.基于改进的离散PSO算法的FJSP的研究[J].计算机科学,2018,45(04):233-239+256.
参考书籍：柔性作业车间调度智能算法及其应用
"""
'''
说明：参考文献[1]丁舒阳,黎冰,侍洪波.基于改进的离散PSO算法的FJSP的研究[J].计算机科学,2018,45(04):233-239+256.
参考书籍：柔性作业车间调度智能算法及其应用
'''
import Decode as Decode
from ReadData import Input
from Encode import Encode
import pso as pso
import numpy as np
import copy



def solve_FJSP(file_num,run_times):
    # 读入数据
    input = Input('./Data/1_Brandimarte/BrandimarteMk'+str(file_num+1)+'.fjs')
    # input = Input('./Data/2_Kacem/Kacem4.fjs')
    p_table, job_op_num = input.getMatrix()

    # 输入：
    # # 1.加工时间矩阵p_table：总的工序数*m；其中不能进行加工用-1表示
    # p_table = np.array([
    #     [5, 4, 4], [4, 2, 3],
    #     [2, 2, 1], [3, 4, 3],
    #     [5, 4, 5], [2, -1, 2], [3, 2, 1]
    # ])
    #
    # # 2.存储每个工件具有的工序个数的列表job_op_num：长度为n;
    # job_op_num = [2, 2, 3]

    # 生成初始种群
    # 种群大小，可以根据m和n的值来调整大小，如C*m*n c为一个常系数
    # Popsize = 5*p_table.shape[1]*len(job_op_num)
    Popsize = 200
    encode = Encode(Popsize, p_table, job_op_num)
    # 全局选择的染色体
    global_chrs = encode.global_selection()
    # #局部选择的染色体
    local_chrs = encode.local_selection()
    # #随机选择的染色体
    random_chrs = encode.random_selection()
    # 合并三者,得到初始的种群
    chrs = np.vstack((global_chrs, local_chrs, random_chrs))

    # 以下是关于操作染色体的代码
    # 初始的超参数赋值
    o_mega = 0.15
    c1 = 0.5
    c2 = 0.7
    pf_max = 0.8
    pf_min = 0.2

    # 迭代次数，也可以根据m和n的值来调整大小，
    # Iter = 5*p_table.shape[1]*len(job_op_num)
    Iter = 200

    # 得到初始的个体最优位置
    P = copy.deepcopy(chrs)
    # 得到初始的全局最优位置
    # Decode.decode(chr,job_op_num,p_table,'decode')，其中的‘decode’表示不画图，只是计算适应度
    fitness_list = [Decode.decode(chr, job_op_num, p_table, 'decode',None) for chr in P]
    Pg = P[np.argmin(fitness_list)]
    for iter in range(Iter):
        # 计算pf
        pf = pf_max - (pf_max - pf_min) / Iter * iter
        # 更新种群中所有的染色体
        copy_chrs = copy.deepcopy(chrs)
        chrs = [pso.f_operator(job_op_num, p_table, chr, P[index], Pg, pf, o_mega, c1, c2) for index, chr in
                enumerate(copy_chrs)]
        # 更新个体最优位置
        P = np.array([chr1 if Decode.decode(chr1, job_op_num, p_table, 'decode',None) <= Decode.decode(chr2, job_op_num,
                                                                                                  p_table, 'decode',None)
                      else chr2 for chr1, chr2 in zip(P, chrs)])
        # 更新全局最优位置
        fitness_list = [Decode.decode(chr, job_op_num, p_table, 'decode',None) for chr in P]
        Pg = P[np.argmin(fitness_list)]

        # for chr in chrs:
        #     print(Decode.decode(chr, job_op_num, p_table, 'decode',None))
        # print("第" + str(iter + 1) + '次循环的最优fitness:', Decode.decode(Pg, job_op_num, p_table, 'decode',None))
        print("第"+str(file_num+1)+'个数据集，第'+str(run_times+1)+'次运行'+'迭代：'+str(iter+1)+'/'+str(Iter))

    fitness = Decode.decode(Pg, job_op_num, p_table, 'decode',None)

    return (Pg,fitness,job_op_num, p_table)
if __name__ == '__main__':
    #总共15个Brandimarte文件
    for i in range(15):
        #每个数据用例都测试10次，取最好的一次结果，如果为了效率可以每个数据都测试1次
        results = [solve_FJSP(i,j) for j in range(10)]
        Pg_list = [result[0] for result in results ]
        fitness_list = [result[1] for result in results ]
        job_op_num = results[0][2]
        p_table  = results[0][3]
        best_fitness_index = np.argmax(np.array(fitness_list))
        best_fitness = fitness_list[best_fitness_index]
        best_Pg = Pg_list[best_fitness_index]
        #画图，写入.txt文档
        path= './BestFitness/BrandimarteMk'+str(i+1)+'/'
        Decode.decode(best_Pg,job_op_num,p_table,'save',path)
        print(best_Pg,best_fitness)
        with open(path+'best_schedule.txt', 'w') as f:
            f.write(str(best_Pg)+'\n'+str(best_fitness))


