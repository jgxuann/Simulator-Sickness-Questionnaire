import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 读取数据
data = pd.read_csv('metrics_pre_post_data.csv')

# 选择需要的列
metrics = data[['Pre', 'Post', 'Metric']].melt(id_vars='Metric', var_name='Condition', value_name='Score')

# 设置绘图的风格
sns.set(style="whitegrid")

# 创建一个绘图
plt.figure(figsize=(12, 6))

# 使用条形图绘制Pre和Post的比较
sns.barplot(x='Metric', y='Score', hue='Condition', data=metrics)

# 添加标题和标签
plt.title("Comparison of Pre and Post Scores for Different Metrics", fontsize=16)
plt.xlabel("Metric", fontsize=12)
plt.ylabel("Scores", fontsize=12)

# 显示图形
plt.legend(title='Condition')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()