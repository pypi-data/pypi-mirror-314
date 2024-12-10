# -*- coding: UTF-8 –*-
import os
import socket
import platform
import datetime
import time
from mdbq.config import myconfig
from mdbq.mysql import mysql
from mdbq.mysql import s_query
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import tkinter as tk

from sqlalchemy.sql.functions import count

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
        self.path = '/Users/xigua/Downloads'
        root = tk.Tk()
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        root.destroy()
        self.today = datetime.date.today()
        self.start_date = (self.today - datetime.timedelta(days=15)).strftime('%Y-%m-%d')
        self.end_date = (self.today - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    def getdata(self, db_name, table_name, pro_list, start_date=None, end_date=None):
        download = s_query.QueryDatas(username=username, password=password, host=host, port=port)
        if not start_date or not end_date:
            start_date, end_date = '2000-01-01', '2099-12-31'  # 从数据库提取数据，不能是 self.start_date
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

    def dpll_bak(self, db_name='聚合数据', table_name='店铺流量来源构成', pro_list=None, filename='店铺流量来源'):
        if not pro_list:
            pro_list = ['日期', '三级来源', '访客数']
        df = self.getdata(db_name=db_name, table_name=table_name, pro_list=pro_list, start_date='2024-11-01', end_date=self.end_date)
        if len(df) == 0:
            print(f'数据不能为空: {table_name}')
            return
        df = df[df['三级来源'] != '汇总']
        df['日期'] = pd.to_datetime(df['日期'])
        today = datetime.date.today()

        def st_date(num=1):
            return pd.to_datetime(today - datetime.timedelta(days=num))
        max_date = df['日期'].max().strftime('%Y-%m-%d')
        df1 = df[df['日期'] >= st_date(1)]
        df2 = df[df['日期'] >= st_date(7)]
        df3 = df[df['日期'] >= st_date(30)]
        df2 = df2.groupby(
            ['三级来源'],
            as_index=False).agg(
            **{
                '访客数': ('访客数', np.sum),
            }
        )
        df3 = df3.groupby(
            ['三级来源'],
            as_index=False).agg(
            **{
                '访客数': ('访客数', np.sum),
            }
        )
        # print(df)
        labels1 = df1['三级来源'].tolist()
        values1 = df1['访客数'].tolist()
        labels2 = df2['三级来源'].tolist()
        values2 = df2['访客数'].tolist()
        labels3 = df3['三级来源'].tolist()
        values3 = df3['访客数'].tolist()

        def make_sub(data_list, num):
            # 创建一个具有1行2列的网格布局
            t_p = []
            for i in range(num):
                t_p.extend([{"type": "pie"}])
            fig = make_subplots(rows=1, cols=num, specs=[t_p])
            pie_title = {1: 1, 2: 7, 3: 30}
            i = 1
            for item in data_list:
                # 计算每个扇区的百分比，并找出哪些扇区应该被保留
                total = sum(item['值'])
                # 计算每个扇区的百分比，并找出哪些扇区应该被保留
                threshold_percentage = 0.1  # 阈值百分比
                filtered_indices = [i for i, value in enumerate(item['值']) if
                                    (value / total) * 100 >= threshold_percentage]
                # 提取被保留的扇区的标签和值
                filtered_labels = [item['键'][i] for i in filtered_indices]
                filtered_values = [item['值'][i] for i in filtered_indices]

                # 添加饼图
                fig.add_trace(
                    go.Pie(labels=filtered_labels, values=filtered_values, name=f'pie {i}', textinfo='label+percent'),
                    row=1, col=i)
                # fig.add_trace(go.Pie(labels=item['键'], values=item['值'], name=f'最近{pie_title[i]}天', textinfo='label+percent'), row=1, col=i)
                fig.add_annotation(
                    text=f'最近{pie_title[i]}天',
                    x=0.15 + 0.35 * (i - 1),
                    y=0.98,
                    xref='paper',  # # 相对于整个图表区域
                    yref='paper',
                    showarrow=True,   # 显示箭头
                    align="left",  # 文本对齐方式
                    font=dict(size=16),
                )
                i += 1
                fig.update_layout(
                    title_text=f'店铺流量来源   最近一天: {max_date}',
                    xaxis_title='X Axis',
                    yaxis_title='Y Axis',
                    # width=self.screen_width // 1.4,
                    # height=self.screen_width // 2,
                    margin=dict(
                        l=100,   # 左边距
                        r=300,
                        t=100,  # 上边距
                        b=400,
                    ),
                )
                fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False, xaxis_visible=False, yaxis_visible=False)
            return fig

        data_list = [{'键': labels1, '值': values1}, {'键': labels2, '值': values2}, {'键': labels3, '值': values3}]
        fig = make_sub(data_list=data_list, num=3)
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
            title_text=f'店铺流量来源   最近数据: {max_date}',
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
            font=dict(size=16),
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
            last_date = df['日期'].max()
            # 对数据进行筛选
            df = df[
                (df['日期'] == last_date) &
                ~df['标签名称'].str.contains('unknown', case=False) &
                (df['洞察类型'] == lab) &
                (df['行为类型'] == option) &
                (df['统计周期'] == d_str)
            ]
            dict_list.update({table_name: df})

        fig = make_subplots(rows=2, cols=3)
        # 在每个子图中绘制柱形图
        count = 0
        for table_name, df in dict_list.items():
            if len(df) == 0:
                count += 1
                continue
            # print(count, table_name)
            if count > 5:
                break
            labels = df['标签名称'].tolist()
            values = df['标签人群数量'].tolist()
            df['Percentage'] = df['标签人群数量'] / df['标签人群数量'].sum() * 100
            percentages = df['Percentage']
            bar = go.Bar(
                x=labels,
                y=values,
                name=table_name,
                text=percentages.map('{:.2f}%'.format),  # 设置要显示的文本（百分比）
                # textposition = 'outside',  # 设置文本位置在柱形图外部
            )
            row = count // 3 + 1
            col = count % 3 + 1
            fig.add_trace(
                bar,
                row=row,
                col=col,
            )
            if count < 3:
                x = 0.01 + 0.395 * (count)
                y = 1.04
            else:
                x = 0.01 + 0.395 * (count % 3)
                y = 1.04 - 0.59 * (count // 3)
            fig.add_annotation(
                text=table_name,
                x=x,
                y=y,
                xref='paper',  # # 相对于整个图表区域
                yref='paper',
                showarrow=False,  # 显示箭头
                align="left",  # 文本对齐方式
                font=dict(size=16),
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
            text=f'数据日期: {last_date.strftime('%Y-%m-%d')}    统计范围: {lab}/{option} {d_str}',
            x=0.5,
            y=-0.1,
            xref='paper',  # # 相对于整个图表区域
            yref='paper',
            showarrow=False,  # 显示箭头
            align="left",  # 文本对齐方式
            font=dict(size=14),
        )
        fig.write_html(os.path.join(self.path, f'{filename}.html'))


def main():
    ds = DataShow()
    # ds.dpll()
    # ds.tg(
    #     days=15,
    #     # start_date='2024-11-01',
    #     # end_date='2024-11-30',
    # )
    ds.item_crowd(
        item_id=839148235697,
        lab='全部渠道',
        option='商详浏览',
        last_date=None,
        d_str='近30天',
    )


if __name__ == '__main__':
    main()
