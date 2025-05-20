import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
from matplotlib.patches import Patch

# 读取数据
data = pd.read_csv('metrics_pre_post_data.csv')

# 自定义颜色
custom_colors = {
    'Pre': '#4871B3',    
    'Post': '#F98F34'    
}

# 创建图形和坐标轴
fig, ax = plt.subplots(figsize=(10, 6))

# 关闭网格线
plt.grid(False)

# 设置背景颜色为白色
ax.set_facecolor('white')

# 使用分组条形图绘制Pre和Post的比较
ax = sns.barplot(
    x='Metric', 
    y='Score', 
    hue='Condition', 
    data=pd.melt(data, id_vars='Metric', value_vars=['Pre', 'Post'], 
                 var_name='Condition', value_name='Score'),
    palette=custom_colors,
    errwidth=1,
    capsize=0.1,
    alpha=1.0,
    ax=ax
)

# 调整每个柱条的属性
# 获取所有柱条
bars = ax.patches

# 计算每个指标有多少个条件（通常是2个：Pre和Post）
n_metrics = len(data['Metric'].unique())
n_conditions = len(['Pre', 'Post'])  # 2个条件

# 自定义每个柱条的宽度（可以调整这个值来改变宽度）
bar_width = 0.35

# 调整每个柱条
for i, bar in enumerate(bars):
    # 确定当前柱条属于哪个指标和条件
    metric_idx = i // n_conditions
    condition_idx = i % n_conditions
    
    # 计算新的x位置（让柱条更靠近或更远离）
    original_x = bar.get_x()
    bar_center = original_x + bar.get_width()/2
    
    # 调整宽度
    bar.set_width(bar_width)
    
    # 重新定位，保持中心不变
    bar.set_x(bar_center - bar_width/2)
    
    # 可以为特定柱条添加边框或调整透明度
    if condition_idx == 0:  # Pre条件
        bar.set_edgecolor('black')
        bar.set_linewidth(1)
    else:  # Post条件
        bar.set_edgecolor('black')
        bar.set_linewidth(1)
        
    # 可以调整特定柱条的高度（例如强调某些数据）
    # 如果想增加某个柱条高度的20%
    # if metric_idx == 0 and condition_idx == 1:  # 第一个指标的Post条件
    #     current_height = bar.get_height()
    #     bar.set_height(current_height * 1.2)
    
    # 可以为特定柱条添加图案
    # if metric_idx == 1:  # 第二个指标
    #     bar.set_hatch('///')  # 添加斜线图案

# 自定义图例名称
condition_labels = {
    'Pre': 'Original Video',
    'Post': 'Processed Video'
}

# 创建自定义图例
legend_elements = [
    Patch(facecolor=custom_colors['Pre'], edgecolor='black', label=condition_labels['Pre'], alpha=0.85),
    Patch(facecolor=custom_colors['Post'], edgecolor='black', label=condition_labels['Post'], alpha=0.85)
]

# 添加自定义图例 - 调整位置和大小
ax.legend(handles=legend_elements, 
          loc='upper left',           # 位置：左上角
          fontsize=8,                # 图例文本大小
          frameon=True,               # 图例框
          framealpha=0.9,             # 框的透明度
          edgecolor='black',          # 框边缘颜色
          fancybox=True,              # 圆角图例框
          title='Experimental Condition',  # 图例标题
          title_fontsize=10           # 标题字体大小
         )

# 添加标题和标签
plt.title("", fontsize=12, color='black', pad=10)

# 自定义x轴标签
metric_labels = {
    'SSQ_Total': 'Total',
    'Nausea': 'Nausea',
    'Oculomotor': 'Oculomotor',
    'Disorientation': 'Disorientation'
}

# 获取当前x轴刻度位置和标签
current_ticks = plt.xticks()[0]
current_labels = [label.get_text() for label in ax.get_xticklabels()]

# 替换为自定义标签
new_labels = [metric_labels.get(label, label) for label in current_labels]
ax.set_xticklabels(new_labels, fontsize=9, rotation=0)

# 自定义y轴标签
ax.set_ylabel("", fontsize=12, color='white')
ax.set_xlabel("", fontsize=12, color='white')

# 自定义y轴刻度
ax.tick_params(axis='y', labelsize=9)

# 调整y轴范围以适应显著性标记
ylim = plt.ylim()
plt.ylim(ylim[0], ylim[1] * 1.25)  # 增加25%的顶部空间

# 为柱状图添加数值标签
for container in ax.containers:
    ax.bar_label(container, fmt='%.1f', fontsize=11)

# 添加边框
for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_color('black')
    spine.set_linewidth(1.2)

# 调整布局
plt.tight_layout()

# 保存图片
plt.savefig('custom_metrics_comparison.png', dpi=300, bbox_inches='tight', facecolor='white')

# 显示图形
plt.show()
