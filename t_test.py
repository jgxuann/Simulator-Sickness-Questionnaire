import pandas as pd
import pingouin as pg

# 读取数据
df = pd.read_csv('SSQ_calculated_result.csv')

# 创建Condition列（处理前/处理后）
df['Condition'] = df.apply(
    lambda row: 'Pre' if 
    (row['Group'] == 'A' and row['Round'] == 1) or 
    (row['Group'] == 'B' and row['Round'] == 2) 
    else 'Post', axis=1
)

# 定义需要分析的四个指标
metrics = ['SSQ_Total', 'Nausea', 'Oculomotor', 'Disorientation']

# 对每个指标执行配对t检验
for metric in metrics:
    print(f"\n=== 正在分析指标: {metric} ===")
    
    # 提取当前指标的数据并转换为宽格式（Pre vs Post）
    wide_df = df.pivot(
        index='ID',          # 以ID为索引
        columns='Condition', 
        values=metric
    ).reset_index()
    
    # 删除存在缺失值的样本
    wide_df_clean = wide_df.dropna()
    
    # 执行配对t检验
    try:
        ttest_result = pg.ttest(
            wide_df_clean['Pre'],
            wide_df_clean['Post'],
            paired=True,
            alternative='two-sided'
        )
        print(f"\n[{metric}] 处理前后配对t检验结果：")
        print(ttest_result.round(4))
        
        # 计算效应量补充说明
        mean_diff = (wide_df_clean['Post'] - wide_df_clean['Pre']).mean()
        print(f"均值变化：Post - Pre = {mean_diff:.2f} (负值表示下降)")
        
    except Exception as e:
        print(f"\n[{metric}] 分析失败，错误信息：{e}")
    
    print("\n" + "="*50 + "\n")