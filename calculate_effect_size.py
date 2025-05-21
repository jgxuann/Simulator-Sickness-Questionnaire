import pandas as pd
import pingouin as pg
import numpy as np
from scipy.stats import t, shapiro, levene

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

# 创建一个汇总表格显示前提条件检验结果
print("\n===== t检验前提条件检验结果 =====")
print(f"{'指标':<15}{'差值正态性':<40}{'方差齐性':<30}{'建议'}")
print("-" * 90)

result_data = []

# 对每个指标进行处理
for metric in metrics:
    # 转换为宽格式（Pre vs Post）
    wide_df = df.pivot(index='ID', columns='Condition', values=metric).reset_index()
    wide_df_clean = wide_df.dropna()
    
    # 添加差值和百分比变化列
    wide_df_clean['Diff'] = wide_df_clean['Post'] - wide_df_clean['Pre']
    wide_df_clean['Pct_Change'] = ((wide_df_clean['Post'] - wide_df_clean['Pre']) / wide_df_clean['Pre']) * 100
    
    # 添加指标名称列
    wide_df_clean['Metric'] = metric
    
    # 将处理后的数据添加到结果列表
    result_data.append(wide_df_clean)

# 合并所有指标的数据
combined_data = pd.concat(result_data, ignore_index=True)

# 保存为CSV文件
combined_data.to_csv('metrics_pre_post_data.csv', index=False)

print("数据已处理并保存为 'metrics_pre_post_data.csv'")

# 对每个指标执行配对t检验及效应量分析
for metric in metrics:
    # 转换为宽格式（Pre vs Post）
    wide_df = df.pivot(index='ID', columns='Condition', values=metric).reset_index()
    wide_df_clean = wide_df.dropna()
    pre_data = wide_df_clean['Pre']
    post_data = wide_df_clean['Post']
    diff_data = post_data - pre_data  # 计算差值

    print("数据已处理并保存为 'metrics_pre_post_data.csv'")
    
    # ========== 检验t检验的前提条件 ==========
    
    # 1. 差值正态性检验 (Shapiro-Wilk test)
    diff_normality = shapiro(diff_data)
    is_normal = diff_normality[1] > 0.05
    
    # 2. 方差齐性检验 (Levene's test)
    variance_test = levene(pre_data, post_data)
    has_equal_var = variance_test[1] > 0.05
    
    # 格式化输出前提条件检验结果
    normality_result = f"W={diff_normality[0]:.3f}, p={diff_normality[1]:.3f} {'(满足)' if is_normal else '(不满足)'}"
    variance_result = f"F={variance_test[0]:.3f}, p={variance_test[1]:.3f} {'(满足)' if has_equal_var else '(不满足)'}"
    
    if is_normal:
        recommendation = "使用配对t检验"
    else:
        recommendation = "使用Wilcoxon符号秩检验"
    
    print(f"{metric:<15}{normality_result:<40}{variance_result:<30}{recommendation}")
    
    # 详细分析
    print(f"\n=== 正在分析指标: {metric} ===")
    print(f"\n前提条件检验:")
    print(f"1. 差值正态性检验 (Shapiro-Wilk): W={diff_normality[0]:.4f}, p={diff_normality[1]:.4f}")
    print(f"   结论: 差值{'符合' if is_normal else '不符合'}正态分布")
    print(f"2. 方差齐性检验 (Levene): F={variance_test[0]:.4f}, p={variance_test[1]:.4f}")
    print(f"   结论: 两组数据方差{'具有齐性' if has_equal_var else '不具有齐性'}")
    print(f"   注: 对于配对t检验，方差齐性不是必要条件，主要关注差值的正态性")
    
    try:
        # 配对t检验
        ttest_result = pg.ttest(pre_data, post_data, paired=True)
        print(f"\n[{metric}] 处理前后配对t检验结果：")
        print(ttest_result.round(4))
        
        # 如果差值不符合正态分布，也进行Wilcoxon检验作为参考
        if not is_normal:
            wilcoxon_result = pg.wilcoxon(pre_data, post_data)
            print(f"\n由于差值不符合正态分布，提供Wilcoxon符号秩检验结果作为参考：")
            print(wilcoxon_result.round(4))
        
        # 计算Pre和Post的均值和标准差
        pre_mean = pre_data.mean()
        pre_sd = pre_data.std()
        post_mean = post_data.mean()
        post_sd = post_data.std()
        print(f"\n{metric}：")
        print(f"  Pre 组: 均值 = {pre_mean:.2f}, 标准差 = {pre_sd:.2f}")
        print(f"  Post组: 均值 = {post_mean:.2f}, 标准差 = {post_sd:.2f}")

        # 均值变化
        mean_diff = (post_data - pre_data).mean()
        print(f"均值变化：Post - Pre = {mean_diff:.2f} (负值表示下降)")
        
        # ========== 效应量分析 ==========
        n = len(pre_data)
        
        # 1. Cohen's d
        cohen_d = ttest_result['cohen-d'].values[0]
        
        # 2. Cohen's d 的置信区间（通过t分布计算）
        se_d = np.sqrt((1/n) + (cohen_d**2)/(2*n))  # 标准误
        t_alpha = t.ppf(0.975, df=n-1)              # 临界值
        ci_lower = cohen_d - t_alpha * se_d
        ci_upper = cohen_d + t_alpha * se_d
        
        # 输出结果
        print(f"\n效应量分析：")
        print(f"  - Cohen's d  = {cohen_d:.3f} (95% CI: [{ci_lower:.3f}, {ci_upper:.3f}])")
        print(f"  - Hedges' g  = {hedges_g:.3f}")
        print(f"  - Glass's Δ  = {glass_delta:.3f}")
        
    except Exception as e:
        print(f"\n[{metric}] 分析失败，错误信息：{e}")
    
    print("\n" + "="*50 + "\n")

print("\n重要说明:")
print("1. 对于配对t检验，差值(Post-Pre)的正态性是最关键的前提条件")
print("2. 如果差值不符合正态分布(p≤0.05)，应考虑使用Wilcoxon符号秩检验")
print("3. 方差齐性对配对t检验不是必要条件，但提供了额外信息")

