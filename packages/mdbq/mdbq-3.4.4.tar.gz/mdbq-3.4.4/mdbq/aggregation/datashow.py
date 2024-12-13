# -*- coding: UTF-8 –*-
import decimal
import os
import re
import socket
import platform
import getpass
import datetime
import time
from mdbq.config import myconfig
from mdbq.mysql import mysql
from mdbq.mysql import s_query
from mdbq.other import ua_sj
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import tkinter as tk
import requests
from io import BytesIO
from PIL import Image
import base64
import matplotlib.pyplot as plt

from sqlalchemy.sql.functions import count

if platform.system() == 'Windows':
    D_PATH = os.path.join(f'C:\\Users\\{getpass.getuser()}\\Downloads')
elif platform.system() == 'Linux':
    D_PATH = 'Downloads'
    if not os.path.exists(D_PATH):
        os.makedirs(D_PATH)
else:
    D_PATH = os.path.join(f'/Users/{getpass.getuser()}/Downloads')

m_engine = mysql.MysqlUpload(username='', password='', host='', port=0, charset='utf8mb4')
company_engine = mysql.MysqlUpload(username='', password='', host='', port=0, charset='utf8mb4')

if socket.gethostname() == 'company' or socket.gethostname() == 'Mac2.local':
    conf = myconfig.main()
    conf_data = conf['Windows']['xigua_lx']['mysql']['remoto']
    username, password, host, port = conf_data['username'], conf_data['password'], conf_data['host'], conf_data['port']
    m_engine = mysql.MysqlUpload(
        username=username,
        password=password,
        host=host,
        port=port,
        charset='utf8mb4'
    )
    conf_data = conf['Windows']['company']['mysql']['local']
    username, password, host, port = conf_data['username'], conf_data['password'], conf_data['host'], conf_data['port']
    company_engine = mysql.MysqlUpload(
        username=username,
        password=password,
        host=host,
        port=port,
        charset='utf8mb4'
    )
    targe_host = 'company'

else:
    conf = myconfig.main()

    conf_data = conf['Windows']['company']['mysql']['remoto']
    username, password, host, port = conf_data['username'], conf_data['password'], conf_data['host'], conf_data['port']
    company_engine = mysql.MysqlUpload(
        username=username,
        password=password,
        host=host,
        port=port,
        charset='utf8mb4'
    )

    conf_data = conf['Windows']['xigua_lx']['mysql']['local']
    username, password, host, port = conf_data['username'], conf_data['password'], conf_data['host'], conf_data['port']
    m_engine = mysql.MysqlUpload(
        username=username,
        password=password,
        host=host,
        port=port,
        charset='utf8mb4'
    )
    targe_host = 'xigua_lx'


# def getdata():
#     download = s_query.QueryDatas(username=username, password=password, host=host, port=port)
#     start_date, end_date = '2024-01-01', '2024-12-20'
#     projection = {
#         '日期': 1,
#         '三级来源': 1,
#         '访客数': 1,
#     }
#     __res = []
#     for year in range(2024, datetime.datetime.today().year + 1):
#         df = download.data_to_df(
#             db_name='聚合数据',
#             table_name=f'店铺流量来源构成',
#             start_date=start_date,
#             end_date=end_date,
#             projection=projection,
#         )
#         __res.append(df)
#     df = pd.concat(__res, ignore_index=True)
#     return df


class DataShow:
    def __init__(self):
        self.path = os.path.join(D_PATH, 'http_server')
        if not os.path.isdir(self.path):
            os.makedirs(self.path)
        root = tk.Tk()
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        root.destroy()
        self.today = datetime.date.today()
        self.start_date = (self.today - datetime.timedelta(days=15)).strftime('%Y-%m-%d')
        self.end_date = (self.today - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    def getdata(self, db_name, table_name, pro_list, start_date=None, end_date=None):
        download = s_query.QueryDatas(username=username, password=password, host=host, port=port)
        if not start_date:
            start_date = '2000-01-01'  # 从数据库提取数据，不能是 self.start_date
        if not end_date:
            end_date = self.today.strftime('%Y-%m-%d')
        projection = {}
        [projection.update({k: 1}) for k in pro_list]
        __res = []
        for year in range(2024, datetime.datetime.today().year + 1):
            df = download.data_to_df(
                db_name=db_name,
                table_name=table_name,
                start_date=start_date,
                end_date=end_date,
                projection=projection,
            )
            __res.append(df)
        df = pd.concat(__res, ignore_index=True)
        return df

    def pov_city(self, db_name='生意经3', filename='销售地域分布', start_date=None, end_date=None, percent=None):
        """
        生意经  省份城市销售分析
        """
        if not start_date:
            start_date = self.start_date
        if not end_date:
            end_date = self.today.strftime('%Y-%m-%d')
        pov_set = self.getdata(
            db_name='属性设置3',
            table_name=f'城市等级',
            pro_list=[],
            start_date=start_date,
            end_date=end_date
        )
        # print(pov_set)
        # 城市
        pro_list = ['日期', '店铺名称', '城市', '销售额', '退款额']
        year = datetime.datetime.today().year
        df_city = self.getdata(
            db_name=db_name,
            table_name=f'地域分析_城市_{year}',
            pro_list=pro_list,
            start_date=start_date,
            end_date=end_date
        )
        df_city = df_city[df_city['店铺名称'] == '万里马官方旗舰店']
        df_city = df_city.groupby(['店铺名称', '城市'], as_index=False).agg(
            **{'销售额': ('销售额', np.sum), '退款额': ('退款额', np.sum)})
        df_city = df_city[df_city['销售额'] > 0]

        # 省份
        pro_list = ['日期', '店铺名称', '省份', '销售额', '退款额']
        year = datetime.datetime.today().year
        df_pov = self.getdata(
            db_name=db_name,
            table_name=f'地域分析_省份_{year}',
            pro_list=pro_list,
            start_date=start_date,
            end_date=end_date
        )
        df_pov = df_pov[df_pov['店铺名称'] == '万里马官方旗舰店']
        # print(df_pov[df_pov['省份'] == '广东'])
        df_pov = df_pov.groupby(['店铺名称', '省份'], as_index=False).agg(
            **{'销售额': ('销售额', np.sum), '退款额': ('退款额', np.sum)})
        df_pov.drop_duplicates(subset='省份', keep='last', inplace=True, ignore_index=True)

        # df_pov2： gmv 的饼图
        df_pov['gmv销售'] = df_pov.apply(lambda x: x['销售额'] + x['退款额'], axis=1)
        df_pov.sort_values(['gmv销售'], ascending=[False], ignore_index=True, inplace=True)
        df_pov2 = df_pov.copy()
        sales_sum = df_pov2['gmv销售'].sum()
        df_pov2['省份'] = df_pov2.apply(lambda x: '其他' if (x['gmv销售'] / sales_sum) < percent else x['省份'], axis=1)

        # df_pov3： 销售额的饼图
        df_pov.sort_values(['销售额'], ascending=[False], ignore_index=True, inplace=True)
        df_pov3 = df_pov.copy()
        sales_sum = df_pov3['销售额'].sum()
        df_pov3['省份'] = df_pov3.apply(lambda x: '其他' if (x['销售额'] / sales_sum) < 0.016 else x['省份'], axis=1)

        # df_pov1： 省份 销售额 堆叠柱形图
        df_pov1 = df_pov.copy()
        df_pov1 = df_pov1.head(15)
        pov_sales_sum = df_pov1['销售额'].tolist()
        pov_refunds = df_pov1['退款额'].tolist()
        percentages = df_pov1['gmv销售'] / df_pov1['gmv销售'].sum() * 100
        bar_list = [('省份销售/退款', df_pov1['省份'].tolist(), pov_sales_sum, percentages, pov_refunds)]

        # 将城市等级添加到df
        pov_set = pov_set[['城市等级', '城市']]
        pov_set.drop_duplicates(subset='城市', keep='last', inplace=True, ignore_index=True)
        df_city = pd.merge(df_city, pov_set, left_on=['城市'], right_on=['城市'], how='left')
        df_level = df_city.groupby(['店铺名称', '城市等级'], as_index=False).agg(
            **{'销售额': ('销售额', np.sum), '退款额': ('退款额', np.sum)})
        pie_list = [
            ('按城市等级', df_level['城市等级'].tolist(), df_level['销售额'].tolist()),
            ('净销售 top省份', df_pov3['省份'].tolist(), df_pov3['销售额'].tolist()),
            ('GMV top省份', df_pov2['省份'].tolist(), df_pov2['gmv销售'].tolist())
        ]

        # df_city1： 城市 销售额 堆叠柱形图
        df_city.drop_duplicates(subset='城市', keep='last', inplace=True, ignore_index=True)
        df_city['gmv销售'] = df_city.apply(lambda x: x['销售额'] + x['退款额'], axis=1)
        df_city.sort_values(['销售额'], ascending=[False], ignore_index=True, inplace=True)
        df_city = df_city[df_city['城市'] != '其他']
        percentages = df_city['gmv销售'] / df_city['gmv销售'].sum() * 100
        df_city1 = df_city.head(15)
        city_sales_sum = df_city1['销售额'].tolist()
        city_refunds = df_city1['退款额'].tolist()
        bar_list += [('城市销售/退款', df_city1['城市'].tolist(), city_sales_sum, percentages, city_refunds)]

        t_p1 = []
        for i in range(3):
            t_p1.extend([{"type": "pie"}])
        t_p2 = []
        for i in range(3):
            t_p2.extend([{"type": "bar"}])
        specs = [t_p1, t_p2]
        fig = make_subplots(rows=2, cols=3, specs=specs)

        row = 0
        col = 0
        for i in range(6):
            if row // 3 == 0:
                try:
                    title, labels, values = pie_list[col % 3]
                except:
                    row += 1
                    col += 1
                    continue
                # 添加饼图
                fig.add_trace(
                    go.Pie(
                        labels=labels,
                        values=values,
                        name=title,
                        textinfo='label+percent'
                    ),
                    row=row//3 + 1,
                    col=col % 3 + 1,
                )
            else:
                try:
                    title, labels, values, percentages, refunds = bar_list[col % 3]
                except:
                    row += 1
                    col += 1
                    continue
                bar = go.Bar(
                    x=labels,
                    y=values,
                    name='销售额',
                    orientation='v',  # 垂直柱形图
                    # text=percentages.map('{:.1f}%'.format),  # 设置要显示的文本（百分比）
                    # textposition = 'outside',  # 设置文本位置在柱形图外部
                    width=0.55,  # 调整柱子最大宽度
                    # marker_color='blue',
                )
                fig.add_trace(
                    bar,
                    row=row // 3 + 1,
                    col=col % 3 + 1,
                )
                bar = go.Bar(
                    x=labels,
                    y=refunds,
                    name='退款额',
                    orientation='v',  # 垂直柱形图
                    text=percentages.map('{:.1f}%'.format),  # 设置要显示的文本（百分比）
                    textposition='outside',  # 设置文本位置在柱形图外部
                    width=0.55,  # 调整柱子最大宽度
                    # marker_color = 'red',
                )
                fig.add_trace(
                    bar,
                    row=row // 3 + 1,
                    col=col % 3 + 1,
                )

            x = 0.14 + 0.355 * (row % 3)
            y = 0.99 - 0.58 * (row // 3)
            fig.add_annotation(
                text=title,
                x=x,
                y=y,
                xref='paper',  # # 相对于整个图表区域
                yref='paper',
                showarrow=True,  # 显示箭头
                align="left",  # 文本对齐方式
                font=dict(size=14)
            )
            row += 1
            col += 1

        fig.update_layout(
            title_text=f'销售地域分布',
            margin=dict(
                l=100,  # 左边距
                r=100,
                t=80,  # 上边距
                b=80,
            ),
            legend=dict(
                orientation='v',  # 图例方向（'h' 表示水平，'v' 表示垂直）
                font=dict(
                    size=12  # 图例字体大小
                )
            ),
            barmode='stack',  # stack(堆叠)、group(并列)、overlay(覆盖)、relative(相对)
        )
        fig.add_annotation(
            text=f'统计时间周期: {start_date}~{end_date}     tips: 饼图剔除了销售<{f"{percent * 100}%"}的数据',
            x=0.5,
            y=-0.09,
            xref='paper',  # # 相对于整个图表区域
            yref='paper',
            showarrow=False,  # 显示箭头
            align="left",  # 文本对齐方式
            font=dict(size=12),
        )
        fig.write_html(os.path.join(self.path, f'{filename}.html'))


    def dpll(self, db_name='聚合数据', table_name='店铺流量来源构成', pro_list=None, filename='店铺流量来源'):
        if not pro_list:
            pro_list = ['日期', '店铺名称', '类别', '来源构成', '二级来源', '三级来源', '访客数']
        df = self.getdata(db_name=db_name, table_name=table_name, pro_list=pro_list, start_date='2024-11-01', end_date=self.end_date)
        if len(df) == 0:
            print(f'数据不能为空: {table_name}')
            return
        df['日期'] = pd.to_datetime(df['日期'])
        df = df[
            (df['店铺名称'] == '万里马官方旗舰店') &
            (df['类别'] == '非全站推广期') &
            (df['来源构成'] == '商品流量')
        ]
        today = datetime.date.today()

        def st_date(num=1):
            return pd.to_datetime(today - datetime.timedelta(days=num))
        max_date = df['日期'].max().strftime('%Y-%m-%d')

        data_list = []
        for days in [1, 7, 30]:
            df_linshi = df[df['日期'] >= st_date(num=days)]
            # 统计三级来源
            df_linshi3 = df_linshi[df_linshi['二级来源'] != '汇总']
            th_list = df_linshi3.groupby(['日期', '店铺名称', '类别', '来源构成', '二级来源']).size()
            th_list = th_list.reset_index()
            th_list = th_list[th_list[0] > 1]
            th_list = th_list['二级来源'].tolist()
            df_linshi3['三级来源'] = df_linshi3.apply(lambda x: x['三级来源'] if x['三级来源'] != '汇总' else '' if x['三级来源'] == '汇总' and x['二级来源'] in th_list  else x['二级来源'], axis=1)
            df_linshi3 = df_linshi3[df_linshi3['三级来源'] != '']
            df_linshi3 = df_linshi3.groupby(['三级来源'], as_index=False).agg(**{'访客数': ('访客数', np.sum)})

            df_linshi2 = df_linshi[(df_linshi['二级来源'] != '汇总') & (df_linshi['三级来源'] == '汇总')]
            df_linshi2 = df_linshi2.groupby(['二级来源'], as_index=False).agg(**{'访客数': ('访客数', np.sum)})
            data_list.append({'来源类型': '三级来源', '统计周期': days, '数据主体': df_linshi3})
            data_list.append({'来源类型': '二级来源', '统计周期': days, '数据主体': df_linshi2})
        # print(data_list)
        t_p1 = []
        for i in range(3):
            t_p1.extend([{"type": "pie"}])  # 折线图类型
        t_p2 = []
        for i in range(3):
            t_p2.extend([{"type": "pie"}])  # 饼图类型
        specs = [t_p1, t_p2]
        fig = make_subplots(rows=2, cols=3, specs=specs)

        count1 = 0
        count2 = 0
        for item in data_list:
            labels = item['数据主体'][item['来源类型']].tolist()
            values = item['数据主体']['访客数'].tolist()
            # 计算每个扇区的百分比，并找出哪些扇区应该被保留
            total = sum(values)
            # 计算每个扇区的百分比，并找出哪些扇区应该被保留
            threshold_percentage = 1  # 阈值百分比
            filtered_indices = [i for i, value in enumerate(values) if
                                (value / total) * 100 >= threshold_percentage]
            # 提取被保留的扇区的标签和值
            filtered_labels = [labels[i] for i in filtered_indices]
            filtered_values = [values[i] for i in filtered_indices]
            if item['来源类型'] == '二级来源':
                # 添加饼图
                fig.add_trace(
                    go.Pie(
                        labels=filtered_labels,
                        values=filtered_values,
                        name=item['来源类型'],
                        textinfo='label+percent'
                    ),
                    row=1,
                    col=count1+1,
                )
                x = 0.14 + 0.355 * (count1)
                y = 0.98
                fig.add_annotation(
                    text=f'{item['来源类型']}    最近{item['统计周期']}天',
                    x=x,
                    y=y,
                    xref='paper',  # # 相对于整个图表区域
                    yref='paper',
                    showarrow=True,  # 显示箭头
                    align="left",  # 文本对齐方式
                    font=dict(size=14),
                )
                count1 += 1
            else:
                # 添加饼图
                fig.add_trace(
                    go.Pie(
                        labels=filtered_labels,
                        values=filtered_values,
                        name=item['来源类型'],
                        textinfo='label+percent'
                    ),
                    row=2,
                    col=count2+1,
                )
                x = 0.12 + 0.39 * (count2 % 3)
                y = -0.12
                fig.add_annotation(
                    text=f'{item['来源类型']}    最近{item['统计周期']}天',
                    x=x,
                    y=y,
                    xref='paper',  # # 相对于整个图表区域
                    yref='paper',
                    showarrow=False,  # 显示箭头
                    align="left",  # 文本对齐方式
                    font=dict(size=14),
                )
                count2 += 1
        fig.update_layout(
            title_text=f'店铺流量来源',
            # xaxis_title='X Axis',
            # yaxis_title='Y Axis',
            # width=self.screen_width // 1.4,
            # height=self.screen_width // 2,
            margin=dict(
                l=100,  # 左边距
                r=100,
                t=100,  # 上边距
                b=100,
            ),
            legend=dict(
                # title='Legend Title',  # 图例标题
                orientation='v',  # 图例方向（'h' 表示水平，'v' 表示垂直）
                # x=0.5,  # 图例在图表中的 x 位置（0 到 1 的比例）
                # y=1.02,  # 图例在图表中的 y 位置（稍微超出顶部以避免遮挡数据）
                font=dict(
                    size=12  # 图例字体大小
                )
            )
        )
        fig.add_annotation(
            text=f'最近数据日期: {max_date}',
            x=0.5,
            y=-0.25,
            xref='paper',  # # 相对于整个图表区域
            yref='paper',
            showarrow=False,  # 显示箭头
            align="left",  # 文本对齐方式
            font=dict(size=12),
        )
        fig.write_html(os.path.join(self.path, f'{filename}.html'))

    def tg(self, db_name='聚合数据', table_name='多店推广场景_按日聚合', pro_list=None, filename='多店推广场景', days=None, start_date=None, end_date=None):
        """
        :param db_name:
        :param table_name:
        :param pro_list:
        :param filename:
        :param days:
        :param start_date:  如果指定，则 days 失效，如果都不指定，则设置 days = 7
        :param end_date:
        :return:
        """
        if not pro_list:
            pro_list = ['日期', '店铺名称', '营销场景', '花费', '成交金额']
        df = self.getdata(db_name=db_name, table_name=table_name, pro_list=pro_list)
        if len(df) == 0:
            print(f'数据不能为空: {table_name}')
            return
        df['日期'] = pd.to_datetime(df['日期'])
        today = datetime.date.today()

        def st_date(num=1):
            return pd.to_datetime(today - datetime.timedelta(days=num))

        if start_date and end_date:
            df = df[(df['日期'] >= pd.to_datetime(start_date)) & (df['日期'] <= pd.to_datetime(end_date))]
        elif days:
            df = df[df['日期'] >= st_date(num=days)]
        else:
            df = df[df['日期'] >= st_date(num=7)]

        df = df.groupby(['日期', '店铺名称', '营销场景'], as_index=False).agg(**{'花费': ('花费', np.sum), '成交金额': ('成交金额', np.sum)})
        max_date = df['日期'].max().strftime('%Y-%m-%d')
        min_date = df['日期'].min().strftime('%Y-%m-%d')
        df_other = df.groupby(['店铺名称'], as_index=False).agg(**{'花费': ('花费', np.sum)})
        df_other = df_other.sort_values('花费', ascending=False)
        data_list = []
        for shopname in df_other['店铺名称'].tolist():
            data_list.append(df[df['店铺名称'] == shopname])
        # df1 = df[df['店铺名称'] == '万里马官方旗舰店']
        # df2 = df[df['店铺名称'] == '万里马官方企业店']
        # df3 = df[df['店铺名称'] == '京东箱包旗舰店']
        # data_list = [df1, df2, df3]

        def make_sub(data_list):
            steps = len(data_list)
            specs = []
            t_p1 = []
            for i in range(steps):
                t_p1.extend([{"type": "xy"}])  # 折线图类型
            t_p2 = []
            for i in range(steps):
                t_p2.extend([{"type": "pie"}])  # 饼图类型
            specs = [t_p1, t_p2]

            # 创建一个包含两个子图的图表，子图排列为1行2列
            fig = make_subplots(
                rows=2,
                cols=steps,
                specs=specs,  # 注意 specs 是用列表传入
                # subplot_titles=("First Line Chart", "Second Line Chart")
            )
            count = 1
            for df in data_list:
                shop = df['店铺名称'].tolist()[0]
                # 在第 1 行添加折线图
                scences = df['营销场景'].unique()
                for scence in scences:
                    df_inside = df[df['营销场景'] == scence]
                    # if len(df_inside) < 7:
                    #     continue
                    fig.add_trace(go.Scatter(x=df_inside['日期'].tolist(), y=df_inside['花费'].tolist(), mode='lines', name=f'{scence}_{shop}'), row=1, col=count)
                # 在第 2 行添加饼图
                df = df.groupby(['营销场景'], as_index=False).agg(**{'花费': ('花费', np.sum)})
                labels = df['营销场景'].tolist()
                values = df['花费'].tolist()
                fig.add_trace(go.Pie(labels=labels, values=values, name=shop, textinfo='label+percent'), row=2, col=count)
                fig.add_annotation(
                    text=shop,
                    x=0.01 + 0.395 * (count - 1),
                    y=1.04,
                    xref='paper',  # # 相对于整个图表区域
                    yref='paper',
                    showarrow=False,  # 显示箭头
                    align="left",  # 文本对齐方式
                    font=dict(size=16),
                )
                count += 1
            return fig

        fig = make_sub(data_list=data_list)
        fig.add_annotation(
            text=f'统计范围: {min_date} ~ {max_date}',
            x=0.5,
            y=-0.15,
            xref='paper',  # # 相对于整个图表区域
            yref='paper',
            showarrow=False,  # 显示箭头
            align="left",  # 文本对齐方式
            font=dict(size=14),
        )
        fig.update_layout(
            title_text=f'多店推广花费_按日聚合',
            xaxis_title='日期',
            yaxis_title='花费',
            # width=self.screen_width // 1.4,
            # height=self.screen_width // 2,
            margin=dict(
                l=100,  # 左边距
                r=100,
                t=100,  # 上边距
                b=150,
            ),
            # legend=dict(orientation="h")
        )
        count = 1
        for item in data_list:
            roi = round(item['成交金额'].sum() / item['花费'].sum(), 2)
            fig.add_annotation(
                text=f'合计: {int(item['花费'].sum())}元 / roi: {roi}',
                x=0.15 + 0.425 * (count - 1),
                y=1.04,
                xref='paper',  # # 相对于整个图表区域
                yref='paper',
                showarrow=False,  # 显示箭头
                align="left",  # 文本对齐方式
                font=dict(size=16),
            )
            count += 1
        fig.write_html(os.path.join(self.path, f'{filename}.html'))

    def item_crowd(self, db_name='商品人群画像2', table_list=None, pro_list=None, filename='商品人群画像', item_id=None, lab='全部渠道', option='商详浏览', d_str='近30天', last_date=None):
        # item_ids = [696017020186, 714066010148, 830890472575]
        if not pro_list:
            pro_list = ['日期', '店铺名称', '洞察类型', '行为类型', '商品id', '统计周期', '标签名称', '标签人群数量']
        if not table_list:
            table_list = [
                '消费能力等级',
                '用户年龄',
                '月均消费金额',
                '大快消策略人群',
                '店铺潜新老客',
                '城市等级',
                '用户职业',
            ]
        if not item_id:
            item_id = 696017020186
        dict_list = {}
        for table_name in table_list:
            df = self.getdata(db_name=db_name, table_name=table_name, pro_list=pro_list)
            if len(df) == 0:
                print(f'{table_name}: 数据长度不能为 0')
                continue
            df['日期'] = pd.to_datetime(df['日期'])

            df['商品id'] = df['商品id'].astype('int64')
            df = df[df['商品id'] == int(item_id)]
            # 对数据进行筛选
            df = df[
                ~df['标签名称'].str.contains('unknown', case=False) &
                (df['洞察类型'] == lab) &
                (df['行为类型'] == option) &
                (df['统计周期'] == d_str)
            ]
            dict_list.update({table_name: df})

        fig = make_subplots(rows=2, cols=3)
        # 在每个子图中绘制柱形图
        count = 0
        sv_date = {}
        for table_name, df in dict_list.items():
            if len(df) == 0:
                count += 1
                continue
            # print(count, table_name)
            if count > 5:
                break
            last_date = df['日期'].max()
            sv_date.update({table_name: last_date.strftime('%Y-%m-%d')})
            df = df[df['日期'] == last_date]
            # 先进行排序，以便柱形图从高到底
            df.sort_values(['标签人群数量'], ascending=[False], ignore_index=True, inplace=True)
            labels = df['标签名称'].tolist()  # 由于上面有自定义排序，labels 和 values 要放在一起
            values = df['标签人群数量'].tolist()
            df['Percentage'] = df['标签人群数量'] / df['标签人群数量'].sum() * 100
            percentages = df['Percentage']
            bar = go.Bar(
                x=labels,
                y=values,
                name=table_name,
                orientation='v',  # 垂直柱形图
                text=percentages.map('{:.1f}%'.format),  # 设置要显示的文本（百分比）
                textposition = 'outside',  # 设置文本位置在柱形图外部
                width=0.55  # 调整柱子最大宽度
            )
            row = count // 3 + 1
            col = count % 3 + 1
            fig.add_trace(
                bar,
                row=row,
                col=col,
            )
            if count < 3:
                x = 0.01 + 0.385 * (count)
                y = 1.04
            else:
                x = 0.01 + 0.385 * (count % 3)
                y = 1.04 - 0.59 * (count // 3)
            fig.add_annotation(
                text=f'{table_name}',
                x=x,
                y=y,
                xref='paper',  # # 相对于整个图表区域
                yref='paper',
                showarrow=False,  # 显示箭头
                align="left",  # 文本对齐方式
                font=dict(size=15),
            )
            count += 1

        fig.update_layout(
            title_text=f'{db_name}    商品id: {item_id}',
            xaxis_title='标签',
            yaxis_title='人群数量',
            # width=self.screen_width // 1.4,
            # height=self.screen_width // 2,
            margin=dict(
                l=100,  # 左边距
                r=100,
                t=100,  # 上边距
                b=100,
            ),
            # legend=dict(orientation="h")
        )
        fig.add_annotation(
            text=f'统计范围: {lab}/{option} {d_str}',
            x=0.5,
            y=-0.1,
            xref='paper',  # # 相对于整个图表区域
            yref='paper',
            showarrow=False,  # 显示箭头
            align="left",  # 文本对齐方式
            font=dict(size=14),
        )
        fig.add_annotation(
            text=re.sub('[{}\',]', '', str(sv_date)),
            x=0.5,
            y=-0.135,
            xref='paper',  # # 相对于整个图表区域
            yref='paper',
            showarrow=False,  # 显示箭头
            align="left",  # 文本对齐方式
            font=dict(size=12),
        )
        fig.write_html(os.path.join(self.path, f'{filename}.html'))

    def crowd(self, db_name='人群画像2', table_list=None, pro_list=None, filename='达摩盘人群画像', crowd_id=None, last_date=None):
        # item_ids = [696017020186, 714066010148, 830890472575]
        if not pro_list:
            pro_list = ['日期', '店铺名称', '人群id', '人群名称', '标签名称', '标签人群数量']
        if not table_list:
            table_list = [
                '消费能力等级',
                '用户年龄',
                '月均消费金额',
                '大快消策略人群',
                '店铺潜新老客',
                '城市等级',
                '用户职业',
            ]
        if not crowd_id:
            crowd_id = 40457369

        dict_list = {}
        for table_name in table_list:
            df = self.getdata(db_name=db_name, table_name=table_name, pro_list=pro_list)
            if len(df) == 0:
                print(f'{table_name}: 数据长度不能为 0')
                continue
            df['日期'] = pd.to_datetime(df['日期'])

            df['人群id'] = df['人群id'].astype('int64')
            df = df[df['人群id'] == int(crowd_id)]
            # 对数据进行筛选
            df = df[
                (df['店铺名称'] == '万里马官方旗舰店')
                # ~df['标签名称'].str.contains('unknown', case=False)
            ]
            dict_list.update({table_name: df})
        crowd_name = df.head(1)['人群名称'].tolist()[0] # 随便取一条数据读取人群名称
        fig = make_subplots(rows=2, cols=3)
        # 在每个子图中绘制柱形图
        count = 0
        sv_date = {}
        unknown_dict = {}
        for table_name, df in dict_list.items():
            if len(df) == 0:
                count += 1
                continue
            # print(count, table_name)
            if count > 5:
                break
            last_date = df['日期'].max()
            df = df[df['日期'] == last_date]
            unknown = df[df['标签名称'].str.contains('unknown', case=False)]
            if len(unknown) > 0:
                unknown = unknown['标签人群数量'].tolist()[0]  # 未知人群数量值

            df = df[~df['标签名称'].str.contains('unknown', case=False)]
            # 先进行排序，以便柱形图从高到底
            df.sort_values(['标签人群数量'], ascending=[False], ignore_index=True, inplace=True)
            labels = df['标签名称'].tolist()  # 由于上面有自定义排序，labels 和 values 要放在一起
            values = df['标签人群数量'].tolist()
            crowd_sum = df['标签人群数量'].values.sum()
            sv_date.update({table_name: crowd_sum})
            unknown_dict.update({table_name: unknown})
            df['Percentage'] = df['标签人群数量'] / df['标签人群数量'].sum() * 100
            percentages = df['Percentage']
            bar = go.Bar(
                x=labels,
                y=values,
                name=table_name,
                orientation='v',  # 垂直柱形图
                text=percentages.map('{:.1f}%'.format),  # 设置要显示的文本（百分比）
                textposition = 'outside',  # 设置文本位置在柱形图外部
                width=0.55  # 调整柱子最大宽度
            )
            row = count // 3 + 1
            col = count % 3 + 1
            fig.add_trace(
                bar,
                row=row,
                col=col,
            )
            if count < 3:
                x = 0.01 + 0.42 * (count)
                y = 1.04
            else:
                x = 0.01 + 0.42 * (count % 3)
                y = 1.04 - 0.59 * (count // 3)
            fig.add_annotation(
                text=f'{table_name}  人群数量: {crowd_sum}',
                x=x,
                y=y,
                xref='paper',  # # 相对于整个图表区域
                yref='paper',
                showarrow=False,  # 显示箭头
                align="left",  # 文本对齐方式
                font=dict(size=15),
            )
            count += 1

        fig.update_layout(
            title_text=f'达摩盘人群画像    人群id: {crowd_id} / 人群名字: 【{crowd_name}】',
            xaxis_title='标签',
            yaxis_title='人群数量',
            # width=self.screen_width // 1.4,
            # height=self.screen_width // 2,
            margin=dict(
                l=100,  # 左边距
                r=100,
                t=100,  # 上边距
                b=100,
            ),
            # legend=dict(orientation="h")
        )
        res = {}
        for k, v in sv_date.items():
            res.update({k: int(v)})
        unknown_res = {}
        for k, v in unknown_dict.items():
            unknown_res.update({k: int(v)})

        fig.add_annotation(
            text=f'分析人群数量:  {re.sub('[{}\',]', '', str(res))}',
            x=0.5,
            y=-0.1,
            xref='paper',  # # 相对于整个图表区域
            yref='paper',
            showarrow=False,  # 显示箭头
            align="left",  # 文本对齐方式
            font=dict(size=12),
        )
        fig.add_annotation(
            text=f'与官方统计存在差异，官方计算中包含未知人群，数量为:  {re.sub('[{}\',]', '', str(unknown_res))}，未知人群占比越大，同官方差异越大',
            x=0.5,
            y=-0.135,
            xref='paper',  # # 相对于整个图表区域
            yref='paper',
            showarrow=False,  # 显示箭头
            align="left",  # 文本对齐方式
            font=dict(size=12),
        )
        fig.write_html(os.path.join(self.path, f'{filename}.html'))

    def item_show(self, db_name='聚合数据', table_list=None, pro_list=None, filename='商品数据', start_date=None, end_date=None):
        if not pro_list:
            pro_list = ['日期', '店铺名称', '营销场景', '商品id', '花费', '点击量', '加购量', '成交笔数', '成交金额']
        table_name = '天猫_主体报表'
        df = self.getdata(
            db_name=db_name,
            table_name=table_name,
            pro_list=pro_list,
            start_date=start_date,
            end_date=end_date
        )
        df_set = self.getdata(
            db_name='属性设置3',
            table_name='商品sku属性',
            pro_list=['商品id', '白底图'],
            start_date='2020-01-01',
            end_date=end_date
        )
        df_set = df_set[df_set['白底图'] != '0']
        df_set.drop_duplicates(subset='商品id', keep='last', inplace=True, ignore_index=True)

        if len(df) == 0:
            print(f'数据不能为空: {table_name}')
            return
        df['日期'] = pd.to_datetime(df['日期'])
        min_date = df['日期'].min().strftime('%Y-%m-%d')
        max_date = df['日期'].max().strftime('%Y-%m-%d')

        df = df.groupby(['店铺名称', '商品id'], as_index=False).agg(
            **{
                '花费': ('花费', np.sum),
                '点击量': ('点击量', np.sum),
                '加购量': ('加购量', np.sum),
                '成交笔数': ('成交笔数', np.sum),
                '成交金额': ('成交金额', np.sum),
            })
        cost_sum = df['花费'].sum()
        df['花费占比'] = df.apply(lambda x: f'{round(x['花费']/cost_sum * 100, 1)}%', axis=1)
        df['roi投产'] = df.apply(lambda x: f'{round(x['成交金额'] / x['花费'], 2)}' if x['花费'] > 0 else 0, axis=1)
        df = pd.merge(df, df_set, left_on='商品id', right_on='商品id', how='left')
        df.sort_values(['花费'], ascending=[False], ignore_index=True, inplace=True)
        df = df.head(100)
        df.reset_index(inplace=True)
        df['index'] = df['index'] + 1
        df.rename(columns={'index': '序号'}, inplace=True)

        # 创建临时目录来存储图片
        temp_dir = os.path.join(self.path, 'temp_images')
        os.makedirs(temp_dir, exist_ok=True)

        df_new = df.copy()
        df_new = df_new.head(10)
        pic_title1 = '商品花费占比'
        img_file1 = os.path.join(temp_dir, f'{pic_title1}.png')
        if not os.path.isfile(img_file1):
            font_properties = {
                'family': 'PingFang HK',  # 字体类型  PingFang HK, Hiragino Sans GB, Arial Unicode MS
                'size': 12,  # 字体大小
                'weight': 'light',  # 字体粗细（'light', 'normal', 'medium', 'semibold', 'bold', 'heavy', 'black'）
                'style': 'italic'  # 字体样式（'normal', 'italic', 'oblique'）
            }
            fig, ax = plt.subplots()
            ax.pie(df_new['花费'], labels=df_new['商品id'], autopct='%1.1f%%', startangle=140)
            ax.set_title(pic_title1, fontdict=font_properties)  # 设置饼图的标题
            ax.axis('equal')  # 确保饼图是圆形的
            plt.savefig(img_file1)  # 保存饼图为PNG文件
            plt.close()

        # # 下载图片并保存到临时目录
        # for i, url in enumerate(df['白底图']):
        #     item_id = df['商品id'].tolist()[i]
        #     img_path = os.path.join(temp_dir, f'image_{item_id}.jpg')
        #     if os.path.isfile(img_path):
        #         df.at[i, '白底图'] = img_path
        #         continue
        #     response = requests.get(url, headers={'User-Agent': ua_sj.get_ua()})
        #     if response.status_code == 200:
        #         with open(img_path, 'wb') as f:
        #             f.write(response.content)
        #         # 更新 DataFrame 中的图片地址列为本地路径
        #         df.at[i, '白底图'] = img_path
        #     else:
        #         print(f"Failed to download image at URL: {url}")

        # 转换图片列
        def convert_image_to_html(image_url_or_base64):
            if os.path.isfile(image_url_or_base64):
                # image_url_or_base64 是本地图片, 将图片路径转换为 Base64 编码的 <img> 标签
                with open(image_url_or_base64, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                img_tag = (f'<img class="img" src="data:image/jpeg;base64,{encoded_string}" alt="Image">')
                return img_tag
            else:
                # image_url_or_base64 是在线 url 或者 Base64编码的图片
                return f'<img class="img" src="{image_url_or_base64}" alt="Image">'

        # 应用这个函数到图片列
        df['Image_HTML'] = df['白底图'].apply(convert_image_to_html)

        local_file1 = os.path.join(self.path, '多店推广场景.html')
        local_file2 = os.path.join(self.path, '多店推广场景.html')
        local_file3 = os.path.join(self.path, '多店推广场景.html')
        local_file4 = os.path.join(self.path, '多店推广场景.html')
        local_file5 = os.path.join(self.path, '多店推广场景.html')

        # 创建 HTML
        html_template = """
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>商品推广数据</title>
        <style>
          .centered-table {
              margin-top: 20px;
              margin-down: 100px;
              margin-left: auto;
              margin-right: auto;
              border-collapse: collapse; /* 可选，用于合并表格边框 */
              width: 60%; /* 设置表格宽度为父容器宽度的50%，或者你可以使用固定宽度 */
          }
          thead th {
            background-color: #f2f2f2; /* 设置表头背景颜色 */
            font-size: 16px; /* 增大表头字体 */
            font-weight: bold; /* 加粗表头字体 */
            text-align: center; /* 设置表头文本居中 */
          }
          caption {
            caption-side: top; /* 标题显示在表格上方 */
            font-size: 24px; /* 设置标题字体大小 */
            font-weight: bold; /* 设置标题字体加粗 */
            text-align: center; /* 设置标题文本居中 */
            margin-bottom: 20px; /* 为标题和表格之间添加间距 */
          }
          td, th {
            border: 1px solid #ddd; /* 单元格边框 */
            line-height: 1em; /* 设置行高为2倍的当前字体大小 */
            padding: 5 5px; /* 设置左右边距，内边距增加单元格的整体高度 */
            text-align: center; /* 设置文本对齐方式 */
          }
          img {
            width: 80px; /* 设置图片宽度 */
            height: auto; /* 高度自动调整以保持宽高比 */
            /* 如果需要垂直居中且图片是块级元素，则可以使用以下样式（但通常不是必需的，因为图片默认是内联元素）
            text-align: center; /* 水平居中（适用于内联或块级子元素） */
            display: block;
            margin: 0 auto; */
          }
          button {
            border: none;
            padding: 8px 12px;
            font-size: 14px;
            cursor: pointer;
          }
          .centered-text {
            position: fixed; /* 固定定位 */
            bottom: 15px; /* 距离页面顶部10px（可根据需要调整） */
            right: calc(25vw - 420px); /* 距离页面右侧1/4宽度减去文本自身的宽度和可能的边距（这里假设文本宽度和边距共10px，实际情况需根据文本样式调整） */
            /* 如果文本宽度未知或可变，可以只使用25vw并接受可能的溢出 */
            /* right: 25vw; */ /* 直接使用25vw定位，不考虑文本宽度 */
            padding: 3px 10px; /* 可选的文本内边距 */
            background-color: rgba(255, 255, 255, 0.8); /* 可选的背景色和透明度 */
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* 可选的阴影效果 */
          }
        
          .image-container {
            position: absolute; /* 使用绝对定位 */
            width: 15%; /* 设置图片宽度 */
            left: 10px; /* 距离页面左侧20px */
            top: 50%; /* 距离页面顶部50% */
            transform: translateY(-50%); /* 向上移动自身高度的一半，以实现垂直居中 */
          }
          .image-container img {
            width: 20%; /* 设置图片宽度 */
            height: auto; /* 高度自动调整以保持宽高比 */
            /* 如果需要垂直居中且图片是块级元素，则可以使用以下样式（但通常不是必需的，因为图片默认是内联元素）*/
            display: flex;
            flex-direction: column;
            align-items: flex-start;
          }
          .button1 {
            border: none;
            padding: 8px 12px;
            font-size: 14px;
            cursor: pointer;
            position: absolute; /* 使用绝对定位 */
            left: 5%; /* 距离页面左侧20px */
            top: 10%; /* 距离页面顶部50% */
          }
          .button2 {
            border: none;
            padding: 8px 12px;
            font-size: 14px;
            cursor: pointer;
            position: absolute; /* 使用绝对定位 */
            left: 5%; /* 距离页面左侧20px */
            top: 17%; /* 距离页面顶部50% */
          }
          .button3 {
            border: none;
            padding: 8px 12px;
            font-size: 14px;
            cursor: pointer;
            position: absolute; /* 使用绝对定位 */
            left: 5%; /* 距离页面左侧20px */
            top: 24%; /* 距离页面顶部50% */
          }
          .button4 {
            border: none;
            padding: 8px 12px;
            font-size: 14px;
            cursor: pointer;
            position: absolute; /* 使用绝对定位 */
            left: 5%; /* 距离页面左侧20px */
            top: 31%; /* 距离页面顶部50% */
          }
          .button5 {
            border: none;
            padding: 8px 12px;
            font-size: 14px;
            cursor: pointer;
            position: absolute; /* 使用绝对定位 */
            left: 5%; /* 距离页面左侧20px */
            top: 38%; /* 距离页面顶部50% */
          }
          
        </style>
        </head>
        
        <div class="div-button">
            <!-- 创建一个按钮 -->
            <button id="button1" class="button1">多店推广场景</button>
            <button id="button2" class="button2">店铺流量来源</button>
            <button id="button3" class="button3">达摩盘人群画像</button>
            <button id="button4" class="button4">商品人群画像</button>
            <button id="button5" class="button5">销售地域分布</button>
        </div>
        <script>
            // 获取按钮元素
            var tg = document.getElementById('button1');
            var dpll = document.getElementById('button2');
            var dmp1 = document.getElementById('button3');
            var dmp2 = document.getElementById('button4');
            var syj = document.getElementById('button5');
            tg.addEventListener('click', function() {
                window.open('{local_file1}', '_blank');
            });
            dpll.addEventListener('click', function() {
                window.open('{local_file2}', '_blank');
            });
            dmp1.addEventListener('click', function() {
                window.open('{local_file3}', '_blank');
            });
            dmp2.addEventListener('click', function() {
                window.open('{local_file4}', '_blank');
            });
            syj.addEventListener('click', function() {
                window.open('{local_file5}', '_blank');
            });
        </script>
        
        <p class="centered-text">统计周期</p>
        <!--
        <img class="image-container" src="{img_file1}" alt="图片">
        -->
        <table class="centered-table">
          <thead>
            <caption>天猫商品推广数据</caption>
            <div>
                <tr>
                  <th>序号</th>
                  <th>商品</th>
                  <th>店铺名称</th>
                  <th>商品id</th>
                  <th>花费</th>
                  <th>花费占比</th>
                  <th>点击量</th>
                  <th>加购量</th>
                  <th>成交笔数</th>
                  <th>成交金额</th>
                  <th>roi投产</th>
                </tr>
            </div>
          </thead>
          <tbody>
            {rows}
          </tbody>
        </table>
        """
        rows = []
        for _, row in df.iterrows():
            row_html = (f'<tr>'
                        f'<td>{row["序号"]}</td>'
                        f'<td>{row["Image_HTML"]}</td>'
                        f'<td>{row["店铺名称"]}</td>'
                        f'<td>{row["商品id"]}</td>'
                        f'<td>{row["花费"]}</td>'
                        f'<td>{row["花费占比"]}</td>'
                        f'<td>{row["点击量"]}</td>'
                        f'<td>{row["加购量"]}</td>'
                        f'<td>{row["成交笔数"]}</td>'
                        f'<td>{row["成交金额"]}</td>'
                        f'<td>{row["roi投产"]}</td>'
                        f'</tr>'
                        )
            rows.append(row_html)

        final_html = html_template.replace('{rows}', ''.join(rows))
        final_html = final_html.replace('统计周期', f'统计周期: {min_date} ~ {max_date}')
        final_html = final_html.replace('{local_file1}', local_file1)
        final_html = final_html.replace('{local_file2}', local_file2)
        final_html = final_html.replace('{local_file3}', local_file3)
        final_html = final_html.replace('{local_file4}', local_file4)
        final_html = final_html.replace('{local_file5}', local_file5)
        file = os.path.join(self.path, f'{filename}.html')
        with open(file, 'w') as f:
            f.write(final_html)


def main():
    ds = DataShow()

    ds.item_show(
        db_name='聚合数据',
        table_list=None,
        pro_list=None,
        filename='天猫商品推广数据',
        start_date='2024-12-01',
        end_date=None,
    )
    # 店铺流量来源
    ds.dpll()
    # 多店聚合推广数据
    ds.tg(
        days=15,
        # start_date='2024-11-01',
        # end_date='2024-11-30',
    )

    # 商品人群画像
    item_id_list = [
        839148235697,
    ]
    for item_id in item_id_list:
        ds.item_crowd(
            item_id=item_id,
            lab='全部渠道',
            option='商详浏览',
            last_date=None,
            d_str='近30天',
        )

    # 达摩盘人群画像
    crowid_list = [
        40457166,
    ]
    for crowid in crowid_list:
        ds.crowd(
            crowd_id=crowid,
            last_date=None,
        )

    ds.pov_city(
        db_name='生意经3',
        filename='销售地域分布',
        start_date='2024-12-01',
        end_date=None,
        percent=0.015,
    )


if __name__ == '__main__':
    main()
