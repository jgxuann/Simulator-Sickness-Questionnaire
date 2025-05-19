import pandas as pd
import os

class SSQCalculator:
    def __init__(self, data_row):
        """初始化SSQ计算器，接收一行数据"""
        self.id = data_row['No.']
        self.group = data_row['Group']
        self.round = data_row['Round']
        
        # 创建症状数据Series
        symptoms = data_row[['General discomfort', 'Fatigue', 'Headache', 'Eye strain', 
                            'Difficulty focusing', 'Salivation increasing', 'Sweating', 
                            'Nausea', 'Difficulty concentrating', 'Fullness of the head', 
                            'Blurred vision', 'Dizziness with eyes open', 
                            'Dizziness with eyes closed', 'Vertigo',
                            'Stomach awareness', 'Burping']]
        
        # 计算各个分数
        self.nausea = 9.54 * self.get_nausea(symptoms)
        self.oculomotor = 7.58 * self.get_oculomotor(symptoms)
        self.disorientation = 13.92 * self.get_disorientation(symptoms)
        self.total = 3.74 * (self.get_nausea(symptoms) + self.get_oculomotor(symptoms) + self.get_disorientation(symptoms))
    
    def get_nausea(self, symptoms):
        """计算恶心分数"""
        nausea_items = ['General discomfort', 'Salivation increasing', 'Sweating', 'Nausea',
                        'Difficulty concentrating', 'Stomach awareness', 'Burping']
        return sum(symptoms[item] for item in nausea_items)
    
    def get_oculomotor(self, symptoms):
        """计算眼动分数"""
        oculomotor_items = ['General discomfort', 'Fatigue', 'Headache', 'Eye strain',
                           'Difficulty focusing', 'Difficulty concentrating', 'Blurred vision']
        return sum(symptoms[item] for item in oculomotor_items)
    
    def get_disorientation(self, symptoms):
        """计算迷失方向分数"""
        disorientation_items = ['Difficulty focusing', 'Nausea', 'Fullness of the head',
                               'Blurred vision', 'Dizziness with eyes open',
                               'Dizziness with eyes closed', 'Vertigo']
        return sum(symptoms[item] for item in disorientation_items)
    
    def get_results(self):
        """返回结果字典"""
        return {
            'ID': self.id,
            'Group': self.group,
            'Round': self.round,
            'SSQ_Total': self.total,
            'Nausea': self.nausea,
            'Oculomotor': self.oculomotor,
            'Disorientation': self.disorientation
        }


def process_ssq_data(input_file, output_file):
    """处理SSQ数据并保存结果"""
    # 读取CSV数据
    df = pd.read_csv(input_file)
    
    # 计算每一行的SSQ分数
    results = []
    for _, row in df.iterrows():
        calculator = SSQCalculator(row)
        results.append(calculator.get_results())
    
    # 创建结果DataFrame
    results_df = pd.DataFrame(results)
    
    # 保存结果到CSV
    results_df.to_csv(output_file, index=False)
    print(f"结果已保存到 {output_file}")
    
    return results_df


if __name__ == "__main__":
    # 确保输出目录存在
    os.makedirs("./results", exist_ok=True)
    
    # 处理数据
    input_file = "SSQ_result.csv"  # 修改为你的CSV数据文件名
    output_file = "SSQ_calculated_result.csv"  # 修改为CSV输出文件
    
    # 处理并显示结果
    results = process_ssq_data(input_file, output_file)
    print("\n计算结果预览:")
    print(results)

