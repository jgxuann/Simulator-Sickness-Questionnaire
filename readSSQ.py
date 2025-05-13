# -*- coding: utf-8 -*-



import pandas as pd
import csv


class questionnaire:
    def __init__(self,index,name,speed,simulator):
        df=pd.Series(simulator,index=index)
        
        self.Name=name
      
        self.Speed=speed
        
        self.Nausea=9.540*self.get_nausea(df)
        
        self.Oculomotor=7.580*self.get_oculomotor(df)
        self.Disorientation=13.920*self.get_disorientation(df)
        
        self.Total=3.74*(self.get_nausea(df)+self.get_oculomotor(df)+self.get_disorientation(df))
        
    def get_nausea(self,ssq):
        nausea=ssq[['General discomfort','Salivation increasing','Sweating','Nausea',
                  'Difficulty concentrating','Stomach awareness','Burping']]
        return nausea.sum()

    def get_oculomotor(self,ssq):
        oculomotor=ssq[['General discomfort','Fatigue','Headache','Eye strain','Difficulty focusing',
                  'Difficulty concentrating','Blurred vision']]
        return oculomotor.sum()

    def get_disorientation(self,ssq):
        disorientation=ssq[['Difficulty focusing','Nausea','Fullness of the head','Blurred vision','Dizziness with eyes open',
               'Dizziness with eyes closed','Vertigo']]
        return disorientation.sum()



if __name__ == "__main__":
 
########################################################################################input 
    name="Anne"
    
    speed=3
    
    simulator=[0, # Question 1
               0, # Question 2
               0, # Question 3
               0, # Question 4              
               0, # Question 5
             
               0, # Question 6
               0, # Question 7
               0, # Question 8            
               0, # Question 9               
               0, # Question 10
               
               0, # Question 11
               0, # Question 12            
               0, # Question 13
               0, # Question 14
               0, # Question 15
               
               0  # Question 16 
               ]
    
    history_simulator=simulator
    print("Name: %s, Speed: %s" %(name,speed))
# end of input   
##############################################################################################   
    
    
    index=['General discomfort',
           'Fatigue',
           'Headache',
           'Eye strain',
           'Difficulty focusing',
           'Salivation increasing',
           'Sweating',
           'Nausea',
           'Difficulty concentrating',
           'Fullness of the head',
           'Blurred vision',
           'Dizziness with eyes open',
           'Dizziness with eyes closed',
           'Vertigo',
           'Stomach awareness',
           'Burping']

    user = questionnaire(index,name,speed,simulator)
    results={ 'Name':[user.Name],
         'Speed':[user.Speed],
         'SSQ':[user.Total],
         'Nausea':[user.Nausea],
         'Oculomotor':[user.Oculomotor],
         'Disorientation':[user.Disorientation]}
    
    results=pd.DataFrame(results)
    
    with open('./database/SSQ.csv', 'a') as f:
        if len(list(csv.reader(open('./database/SSQ.csv'))))>= 2:
            results.to_csv(f,mode='a', header= False,index=False)
        else:
            results.to_csv(f,mode='a',header= True,index=False)
     
    # drop of duplicated data and save it to new file
    df=pd.read_csv("./database/SSQ.csv")
    df=df.drop_duplicates(keep='last')
    df=df.sort_values(['Name', 'Speed'], ascending=[1, 1])
    with open('./database/UserSSQ.csv', 'w') as f:
        df.to_csv(f, header= True,index=False)


"""
    writer = pd.ExcelWriter('./ssq/userData.xlsx')
    df.to_excel(writer,'Sheet1',header= True,index=False)
    writer.save()
"""    
    
    
    
    
    
    
      
    











