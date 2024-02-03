import random

from pyecharts import options as opts
from pyecharts.charts import Grid, Line
from pyecharts.commons.utils import JsCode


def metricsboard(data_dict, save_path=''):
    """
    :param data_dict:
    :param save_path:
    """
    colors = ["#FF1493", "#FF8C00", "#0000FF", "#d48265", "#91c7ae", "#749f83", "#ca8622", "#bda29a", "#6e7074",
              "#546570", "#c4ccd3"]

    keys = list(data_dict.keys())
    if 'train' in keys:
        xaxis_data = [str(x) for x in range(len(data_dict['train']['Acc']))]
    elif 'val' in keys:
        xaxis_data = [str(x) for x in range(len(data_dict['val']['Acc']))]
    elif 'test' in keys:
        xaxis_data = [str(x) for x in range(len(data_dict['test']['Acc']))]
    else:
        return "Error! key of 'train' or 'test' or 'val'is not defined!"

    xaxis_interval = max(1, len(xaxis_data) // 10)  # 保证至少显示10个标签

    # 创建六个图表实例
    charts = []
    titles = ["Acc", "Auc", "Sen", "Spe", "Mcc", "GMean"]
    for i, title in enumerate(titles):
        # 计算每个图表标题的位置
        pos_top = "0%" if i < 3 else "50%"  # 前三个图表在上面，其余在下面
        pos_left_legend = f"{(i % 3) * 33 + 8}%"
        chart = Line(init_opts=opts.InitOpts(width="600px", height="600px")).add_xaxis(xaxis_data=xaxis_data)

        if 'train' in keys:
            chart.add_yaxis(
                series_name='Train',
                y_axis=data_dict['train'][titles[i]],
                is_smooth=True,
                label_opts=opts.LabelOpts(is_show=False),
                color=colors[0]  # 指定颜色
            )
        if 'test' in keys:
            chart.add_yaxis(
                series_name='Test',
                y_axis=data_dict['test'][titles[i]],
                is_smooth=True,
                label_opts=opts.LabelOpts(is_show=False),
                color=colors[1]  # 指定颜色
            )
        if 'val' in keys:
            chart.add_yaxis(
                series_name='Val',
                y_axis=data_dict['val'][titles[i]],
                is_smooth=True,
                label_opts=opts.LabelOpts(is_show=False),
                color=colors[2]  # 指定颜色
            )

        if 'train' in keys and 'val' in keys:
            chart.add_yaxis(
                series_name='T-V',
                y_axis=np.array(data_dict['train'][titles[i]]) - np.array(data_dict['val'][titles[i]]),
                is_smooth=True,
                label_opts=opts.LabelOpts(is_show=False),
                color=colors[3]  # 指定颜色
            )



        chart.set_global_opts(

            legend_opts=opts.LegendOpts(pos_left=pos_left_legend, pos_top=pos_top,
                                        textstyle_opts=opts.TextStyleOpts(font_size=10),
                                        item_width=10,  # 设置图例图标的宽度
                                        item_height=10  # 设置图例图标的高度
                                        ),

            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            toolbox_opts=opts.ToolboxOpts(
                is_show=True,
                feature={
                    "dataZoom": {"yAxisIndex": "none"},
                    "restore": {},
                },
                pos_left='96%',  # 工具箱位置设置为右侧
                pos_top="top",  # 工具箱位置设置为顶部
            ),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                axislabel_opts=opts.LabelOpts(
                    formatter=JsCode(f"function(x){{return x % {xaxis_interval} === 0 ? x : '';}}")),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts()
                ),
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                name=title,
                splitline_opts=opts.SplitLineOpts(is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)),
            ),

        )

        charts.append(chart)

    # 创建Grid实例并添加图表
    grid = Grid()

    # 设定Grid布局参数
    # 第一行图表的布局参数
    grid_opts_row1_col1 = opts.GridOpts(pos_left="5%", pos_right="68%", pos_top="5%", pos_bottom="55%")
    grid_opts_row1_col2 = opts.GridOpts(pos_left="37%", pos_right="36%", pos_top="5%", pos_bottom="55%")
    grid_opts_row1_col3 = opts.GridOpts(pos_left="68%", pos_right="5%", pos_top="5%", pos_bottom="55%")

    # 第二行图表的布局参数
    grid_opts_row2_col1 = opts.GridOpts(pos_left="5%", pos_right="68%", pos_top="55%", pos_bottom="5%")
    grid_opts_row2_col2 = opts.GridOpts(pos_left="37%", pos_right="36%", pos_top="55%", pos_bottom="5%")
    grid_opts_row2_col3 = opts.GridOpts(pos_left="68%", pos_right="5%", pos_top="55%", pos_bottom="5%")

    # 添加第一行的图表
    grid.add(charts[0], grid_opts=grid_opts_row1_col1)
    grid.add(charts[1], grid_opts=grid_opts_row1_col2)
    grid.add(charts[2], grid_opts=grid_opts_row1_col3)

    # 添加第二行的图表
    grid.add(charts[3], grid_opts=grid_opts_row2_col1)
    grid.add(charts[4], grid_opts=grid_opts_row2_col2)
    grid.add(charts[5], grid_opts=grid_opts_row2_col3)

    # 渲染到HTML文件
    grid.render("metrics_grid_layout_corrected.html")
    # 假设x轴数据


import numpy as np

# 设定随机种子以确保结果的可重复性
np.random.seed(0)

# 初始化字典结构
results_dict = {
    'train': {'Acc': [], 'Auc': [], 'Sen': [], 'Spe': [], 'Mcc': [], 'GMean': []},
    'test': {'Acc': [], 'Auc': [], 'Sen': [], 'Spe': [], 'Mcc': [], 'GMean': []},
    'val': {'Acc': [], 'Auc': [], 'Sen': [], 'Spe': [], 'Mcc': [], 'GMean': []}
}


# 生成数据的函数
def generate_data(start=random.uniform(0.5, 0.6), end=random.uniform(0.8, 0.95), n=300, noise_level=random.uniform(0.01, 0.1)):
    """
    生成在[start, end]范围内的n个数值，带有随机噪声。

    :param start: 数值生成的起始值
    :param end: 数值生成的结束值
    :param n: 生成的数值数量
    :param noise_level: 噪声水平，数值的波动范围
    :return: 带有噪声的数值列表
    """
    # 生成基础数值
    base_values = np.linspace(start, end, n)
    # 生成噪声
    noise = np.random.uniform(-noise_level, noise_level, n)
    # 添加噪声到基础数值
    noisy_values = base_values + noise
    # 确保生成的数值在指定范围内
    noisy_values = np.clip(noisy_values, start, end)
    return noisy_values


# 为每个指标生成500个数值
for phase in results_dict.keys():
    for metric in results_dict[phase].keys():
        results_dict[phase][metric] = generate_data().tolist()


metricsboard(results_dict)
