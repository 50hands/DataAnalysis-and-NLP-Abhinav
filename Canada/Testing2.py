import pandas as pd
import statsmodels.api as sm
import numpy as np
from statsmodels.formula.api import ols
df=pd.DataFrame({'20-29':[1,0],'30-39':[0,2],'40-49':[0,4],'50-59':[3,5],'60-69':[11,12],'70-79':[15,25],'80-89':[35,37],'90-99':[22,10],'100-109':[2,1]})
d_melt=pd.melt(df.reset_index(),id_vars=['index'],value_vars=['20-29','30-39','40-49','50-59','60-69','70-79','80-89','90-99','100-109'])
d_melt.columns=['index','age','value']
model=ols('value~C(age)',data=d_melt).fit()
anova_table=sm.stats.anova_lm(model, typ=2)
print(anova_table)
print()
n1=409
p1=170/n1
n2=901
p2=15/n2
print('For ages above 60 and below:')
pop1=np.random.binomial(1,p1,n1)
pop2=np.random.binomial(1,p2,n2)
print(sm.stats.ttest_ind(pop1,pop2))
