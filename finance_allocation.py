#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 17:55:40 2020

@author: hzx
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import random
# import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar, Timeline 

money = 100 # 每人100元
person_num = 100 # 共100人
medium_x = int((person_num/2)-1) #中位数位置
round_num = 17000 # 运行轮次
interval = 1000 # 保存分布的轮次间隔

person_dict={k+1:money for k in range(person_num)}
result_dicts = {}
result_dicts[0] = person_dict.copy()
for n in range(round_num): 
    for i in person_dict.keys():
        # 不允许贷款
        if person_dict[i]:
            person_dict[i]+=-1
            id_get = random.randint(1,person_num)
            # 如果随机送出编号与自己编号一致，则继续取随机编号，直至不一致
            while i == id_get:
                id_get = random.randint(1,person_num) 
            person_dict[id_get]+=1
    # 每间隔一定轮次，记录一次分布结果，便于后续动态作图
    if (n+1)%interval == 0:
        result_dicts[n+1] = person_dict.copy()

# 作图
tl = Timeline(
        init_opts=opts.InitOpts(
            width="800px",height="400px",
        )
    )
for round_n in result_dicts.keys():
    data_x = list(result_dicts[round_n].keys())
    # 每人金额顺序排序
    data_y = sorted(list(result_dicts[round_n].values()),reverse=False)
    
    bar = (
            Bar()
            .add_xaxis(data_x)
            .add_yaxis("余额", data_y)
            .set_global_opts(
                title_opts=opts.TitleOpts("{}轮次,余额".format(round_n)),
                yaxis_opts=opts.AxisOpts(
                    min_= 0,  # 最小刻度
                    max_= 500,  # 最大刻度
                ),
                legend_opts =opts.LegendOpts(is_show = False,), # 图例
            )
            .set_series_opts(
                label_opts=opts.LabelOpts( # 点标签
                    is_show=False,    
                ), 
                markpoint_opts=opts.MarkPointOpts(
                    data=[
                        opts.MarkPointItem(type_='max',name="最大值"),
                        opts.MarkPointItem(type_='min',name="最小值"),
                        opts.MarkPointItem(
                            coord=[medium_x,data_y[medium_x]],
                            value=data_y[medium_x],
                            name="中位数"), # 自定义
                    ]
                ),
            )
        )
    tl.add(bar, "{}轮".format(round_n))
tl.add_schema(is_auto_play=True, play_interval=1000) # 设置自动执行，切换步长=1s
tl.render("render.html")
