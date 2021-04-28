# project : GA_FJSP
# file   : Decode.py
# author:yasuoman
# datetime:2021/4/2 22:06
# software: PyCharm

"""
description：
说明：解码类,用于解码和画甘特图
参考书籍：柔性作业车间调度智能算法及其应用  3.2.1FJSP的染色体编码和3.2.2FJSP的染色体解码
"""
'''
说明：解码类,用于解码和画甘特图
参考书籍：柔性作业车间调度智能算法及其应用  3.2.1FJSP的染色体编码和3.2.2FJSP的染色体解码
'''
import numpy as np
import matplotlib.pyplot as plt
import os
#改成函数，不写成类了

# def __init__(self,p_table,job_op_num,chr):
#     # 1.加工时间矩阵p_table：总的工序数*m；其中不能进行加工用-1表示
#     self.p_table = p_table
#     # 2.存储每个工件具有的工序个数的列表job_op_num：长度为n;形如[2,2,3]
#     self.job_op_num = job_op_num
#     # 3.染色体chr的列表 ，长度为 总的工序数*2
#     self.chr = chr
#     #工件数
#     self.n = len(job_op_num)
#     #机器数
#     self.m = p_table.shape[1]
#     #染色体长度的一半
#     self.half_chr = p_table.shape[0]
#     #最大工序数
#     self.max_op = np.max(job_op_num)

#绘制甘特图
def draw_gatt(n,m,half_chr,job_op_num,Start_time,End_time,path):
   #备选颜色
    cnames = {
       1:'red', 2:'blue', 3:'yellow', 4:'orange', 5:'green', 6:'palegoldenrod', 7:'purple', 8:'pink', 9:'Thistle', 10:'Magenta',
             11:'SlateBlue', 12:'RoyalBlue', 13:'Cyan', 14:'Aqua',15: 'floralwhite',16: 'ghostwhite',17: 'goldenrod', 18:'mediumslateblue',
             19:'navajowhite',
             20:'navy', 21:'sandybrown', 22:'moccasin',
       'aliceblue': '#F0F8FF',
       'antiquewhite': '#FAEBD7',
       'aqua': '#00FFFF',
       'aquamarine': '#7FFFD4',
       'azure': '#F0FFFF',
       'beige': '#F5F5DC',
       'bisque': '#FFE4C4',
       'blanchedalmond': '#FFEBCD',
       'blue': '#0000FF',
       'blueviolet': '#8A2BE2',
       'brown': '#A52A2A',
       'burlywood': '#DEB887',
       'cadetblue': '#5F9EA0',
       'chartreuse': '#7FFF00',
       'chocolate': '#D2691E',
       'coral': '#FF7F50',
       'cornflowerblue': '#6495ED',
       'cornsilk': '#FFF8DC',
       'crimson': '#DC143C',
       'cyan': '#00FFFF',
       'darkblue': '#00008B',
       'darkcyan': '#008B8B',
       'darkgoldenrod': '#B8860B',
       'darkgray': '#A9A9A9',
       'darkgreen': '#006400',
       'darkkhaki': '#BDB76B',
       'darkmagenta': '#8B008B',
       'darkolivegreen': '#556B2F',
       'darkorange': '#FF8C00',
       'darkorchid': '#9932CC',
       'darkred': '#8B0000',
       'darksalmon': '#E9967A',
       'darkseagreen': '#8FBC8F',
       'darkslateblue': '#483D8B',
       'darkslategray': '#2F4F4F',
       'darkturquoise': '#00CED1',
       'darkviolet': '#9400D3',
       'deeppink': '#FF1493',
       'deepskyblue': '#00BFFF',
       'dimgray': '#696969',
       'dodgerblue': '#1E90FF',
       'firebrick': '#B22222',
       'floralwhite': '#FFFAF0',
       'forestgreen': '#228B22',
       'fuchsia': '#FF00FF',
       'gainsboro': '#DCDCDC',
       'ghostwhite': '#F8F8FF',
       'gold': '#FFD700',
       'goldenrod': '#DAA520',
       'gray': '#808080',
       'green': '#008000',
       'greenyellow': '#ADFF2F',
       'honeydew': '#F0FFF0',
       'hotpink': '#FF69B4',
       'indianred': '#CD5C5C',
       'indigo': '#4B0082',
       'ivory': '#FFFFF0',
       'khaki': '#F0E68C',
       'lavender': '#E6E6FA',
       'lavenderblush': '#FFF0F5',
       'lawngreen': '#7CFC00',
       'lemonchiffon': '#FFFACD',
       'lightblue': '#ADD8E6',
       'lightcoral': '#F08080',
       'lightcyan': '#E0FFFF',
       'lightgoldenrodyellow': '#FAFAD2',
       'lightgreen': '#90EE90',
       'lightgray': '#D3D3D3',
       'lightpink': '#FFB6C1',
       'lightsalmon': '#FFA07A',
       'lightseagreen': '#20B2AA',
       'lightskyblue': '#87CEFA',
       'lightslategray': '#778899',
       'lightsteelblue': '#B0C4DE',
       'lightyellow': '#FFFFE0',
       'lime': '#00FF00',
       'limegreen': '#32CD32',
       'linen': '#FAF0E6',
       'magenta': '#FF00FF',
       'maroon': '#800000',
       'mediumaquamarine': '#66CDAA',
       'mediumblue': '#0000CD',
       'mediumorchid': '#BA55D3',
       'mediumpurple': '#9370DB',
       'mediumseagreen': '#3CB371',
       'mediumslateblue': '#7B68EE',
       'mediumspringgreen': '#00FA9A',
       'mediumturquoise': '#48D1CC',
       'mediumvioletred': '#C71585',
       'midnightblue': '#191970',
       'mintcream': '#F5FFFA',
       'mistyrose': '#FFE4E1',
       'moccasin': '#FFE4B5',
       'navajowhite': '#FFDEAD',
       'navy': '#000080',
       'oldlace': '#FDF5E6',
       'olive': '#808000',
       'olivedrab': '#6B8E23',
       'orange': '#FFA500',
       'orangered': '#FF4500',
       'orchid': '#DA70D6',
       'palegoldenrod': '#EEE8AA',
       'palegreen': '#98FB98',
       'paleturquoise': '#AFEEEE',
       'palevioletred': '#DB7093',
       'papayawhip': '#FFEFD5',
       'peachpuff': '#FFDAB9',
       'peru': '#CD853F',
       'pink': '#FFC0CB',
       'plum': '#DDA0DD',
       'powderblue': '#B0E0E6',
       'purple': '#800080',
       'red': '#FF0000',
       'rosybrown': '#BC8F8F',
       'royalblue': '#4169E1',
       'saddlebrown': '#8B4513',
       'salmon': '#FA8072',
       'sandybrown': '#FAA460',
       'seagreen': '#2E8B57',
       'seashell': '#FFF5EE',
       'sienna': '#A0522D',
       'silver': '#C0C0C0',
       'skyblue': '#87CEEB',
       'slateblue': '#6A5ACD',
       'slategray': '#708090',
       'snow': '#FFFAFA',
       'springgreen': '#00FF7F',
       'steelblue': '#4682B4',
       'tan': '#D2B48C',
       'teal': '#008080',
       'thistle': '#D8BFD8',
       'tomato': '#FF6347',
       'turquoise': '#40E0D0',
       'violet': '#EE82EE',
       'wheat': '#F5DEB3',
       'white': '#FFFFFF',
       'whitesmoke': '#F5F5F5',
       'yellow': '#FFFF00',
       'yellowgreen': '#9ACD32'}
    M = list(cnames.values())
   # M = ['red', 'blue', 'yellow', 'orange', 'green', 'palegoldenrod', 'purple', 'pink', 'Thistle', 'Magenta',
   #       'SlateBlue', 'RoyalBlue', 'Cyan', 'Aqua', 'floralwhite', 'ghostwhite', 'goldenrod', 'mediumslateblue',
   #       'navajowhite',
   #       'navy', 'sandybrown', 'moccasin']
    for i in range(m):
        for j in range(half_chr):
            if End_time[i][j] != 0 and End_time[i][j] - Start_time[i][j] != 0:

                plt.barh(i, width=End_time[i][j] - Start_time[i][j], height=0.5, left=Start_time[i][j],
                         color=M[int(inverse_op_in_m(j,n,job_op_num)[0]-1)], edgecolor='black')
                # plt.text(x=Start_time[i][j] + 0.1, y=i, s=(int(self.inverse_op_in_m(j)[0]), int(self.inverse_op_in_m(j)[1]),End_time[i, j]),
                #          fontsize=8)
                plt.text(x=Start_time[i][j]+0.1, y=i,
                         s=(int(inverse_op_in_m(j,n,job_op_num)[0])),
                         fontsize=8)
    plt.yticks(np.arange(i + 1), np.arange(1, i + 2))

    # plt.show()


    if not os.path.exists(path):
        os.makedirs(path)

    # for root, dirs, files in os.walk(path):
    #     print(files)
    #     if 'best_fitness.png' in files:
    #         os.remove(os.path.join(root, 'best_fitness.png'))

    img_path = path+'best_fitness.png'
    if os.path.exists(img_path):
        # print(img_path)
        os.remove(img_path)
        # print('yes')
    plt.savefig(img_path)
    plt.close()

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

#op_in_m(job_op_num,i,j)的反操作
#知道index，求是哪个工序
def inverse_op_in_m(index,n,job_op_num):
    job_op_list = [(i + 1, j + 1) for i in range(n) for j in range(job_op_num[i])]
    job_op = job_op_list[index]
    return job_op
    #
#解码处理
# 输入参数：
# n:工件个数；max_op:最大工序数；chr染色体;p_table加工时间矩阵;job_op_num存储每个工件具有的工序个数的列表
def decode(chr,job_op_num,p_table,draw,path):
    #得到需要的参数
    # 工件数
    n = len(job_op_num)
    # 机器数
    m = p_table.shape[1]
    # 染色体长度的一半
    half_chr = p_table.shape[0]
    # 最大工序数
    max_op = np.max(job_op_num)

    # 大致步骤：1.根据染色体的MS部分得到机器顺序矩阵和时间顺序矩阵
    #         2.根据染色体的OS部分，插空得到最终的调度安排

    # 1.根据染色体的MS部分得到机器顺序矩阵和时间顺序矩阵

    #机器顺序矩阵，存储的是每个工序对应加工的机器的序号，值为0表示不存在此工序，
    #如Jm[0,0]=1表示工序1在机器1上进行加工
    Jm = np.zeros((n,max_op),dtype=int)
    #时间顺序矩阵，存储的是每个工序在Jm的机器上的加工时间，值为0表示不存在此工序
    # 如T[0,0]=5 表示工序1在机器1上进行加工的时间为5
    T = np.zeros((n, max_op), dtype=int)
    #染色体长度的一半 len(p_table)，得到MS和OS
    MS=chr[:half_chr]
    OS=chr[half_chr:]
    # 得到Jm和T,目前的时间复杂度约为n*max_0p*M
    # 用于帮助p_table找到相应位置
    p_index=0
    #i，j是为了得到Jm和T的下标
    for i in range(len(job_op_num)):
        for j in range(job_op_num[i]):
            # 用于计数，记住当前行有多少个可加工的机器
            count=0
            #找到符合MS的第几个机器序号
            for index in range(len(p_table[p_index])):
                if p_table[p_index][index]!=-1:
                    count+=1
                if count == MS[p_index]:
                    Jm[i][j]=index+1
                    T[i][j]=p_table[p_index][index]
                    break

            if count < MS[p_index]:
                print("false")

            p_index+=1

    #每个机器上的工序的开始加工时间，如第一行:[0,3,0,0,5,0,0]表示机器1上，工序O1,2开始加工时间为3，工序O3,1开始加工时间为5
    start_time=np.zeros((m,half_chr),dtype=int)
    # 每个机器上的工序的结束加工时间，定义类似于start_time
    end_time = np.zeros((m, half_chr), dtype=int)

    # 2.根据染色体的OS部分，插空得到最终的调度安排
    #用于得出工件的工序，如工件1出现了两次，那么就知道第二次出现的是工序O1,2
    op_count_dict={}
    #用于存储所有机器上已分配的工序个数,长度为m
    m_op=np.zeros(m,dtype=int)

    for os in OS:

        if os in op_count_dict:
            op_count_dict[os]+=1
        else:
            op_count_dict[os]=1
        #得到os对应的加工机器的序号和相应的加工时间,op_count_dict[os]代表该工件出现了几次
        m_num = Jm[os-1][op_count_dict[os]-1]

        pro_time = T[os-1][op_count_dict[os]-1]
        # 求出这个工序在相应机器上的位置
        op_index = op_in_m(os,op_count_dict[os],job_op_num)
        # 求出上一道工序在那个机器上的位置，用job_op_num来求,因此op_count_dict[os]-1这里要减去1
        prev_op_index = op_in_m(os, op_count_dict[os] - 1,job_op_num)


        #如果是工件的第一个工序也是机器的第一个工序，直接放上去
        # m_op[m_num-1]代表该机器上已加工的工序个数，op_count_dict[os]代表是这个工件的第几道工序
        if  m_op[m_num-1]==0 and op_count_dict[os]==1 :
            start_time[m_num-1][op_index]=0
            end_time[m_num-1][op_index]=pro_time

        #如果是机器的第一道工序，不是工件的第一道工序，直接从这个工件的上一个工序结束时间开始即可
        elif m_op[m_num-1]==0 and op_count_dict[os] >1 :
            # 先找到上一道工序在哪个机器上加工
            prev_m_num =Jm[os-1][op_count_dict[os]-2]
            #上一道的结束时间
            prev_end_time=end_time[prev_m_num-1][prev_op_index]
            start_time[m_num-1][op_index]=prev_end_time
            end_time[m_num-1][op_index]=prev_end_time+pro_time


        elif m_op[m_num-1]>0:

            #用来标记插到空位置了没
            flag=0
            #这里设置prev_end_time是为了最终的统一 free_start = max(max(end_time[m_num - 1]), prev_end_time)
            prev_end_time = 0
            #如果是该工件的第一道工序
            # 如果不是机器的第一道工序，是工件的第一道工序，要插空,但是不用从上一个工序的结束时间开始找
            if op_count_dict[os]==1 :
                #初始的空闲开始时间为0,画图写的
                free_start=0
            # 如果既不是机器的第一道工序，也不是是工件的第一道工序，要插空, 用从上一个工序的结束时间开始找
            else:
                # 先找到上一道工序在哪个机器上加工
                prev_m_num = Jm[os - 1][op_count_dict[os] - 2]
                # 上一道的结束时间
                prev_end_time = end_time[prev_m_num - 1][prev_op_index]
                #这里的free_start为上一个工序结束的时间
                free_start=prev_end_time

            order_start_time = np.sort(start_time[m_num-1][end_time[m_num-1]>0])
            order_end_time = np.sort(end_time[m_num-1][end_time[m_num-1] > 0])
            # if m_num==2 and os==1:
            #     a=1
            for index in range(len(order_start_time)):
                if order_start_time[index] - free_start >= pro_time:
                    start_time[m_num - 1][op_index] = free_start
                    end_time[m_num - 1][op_index] = free_start + pro_time
                    flag = 1
                    break
                # else:
                # 这里写if是因为要确保free_start的起始点是要大于或者等于prev_end_time
                if order_end_time[index] - free_start >= 0:
                    free_start = order_end_time[index]
            #如果没有插入到中间的空格，插入到末尾
            if flag == 0:
                free_start = max(np.max(end_time[m_num-1]), prev_end_time)
                start_time[m_num-1][op_index] = free_start
                end_time[m_num-1][op_index] = free_start+pro_time

        #将机器上加工的工序数＋1
        m_op[m_num-1]+=1

    # self.draw_gatt(start_time,end_time)
    #如果需要画图
    if draw =="save":
        draw_gatt(n,m,half_chr,job_op_num,start_time,end_time,path)

    c_max=np.max(end_time)

    return c_max
    # return {'fitness':c_max,'start':start_time,'end':end_time}









