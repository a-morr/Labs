import pandas as pd

titanic = pd.read_csv("titanic.csv")[['Pclass','Survived','Sex','Age','Fare']]
titanic['Age'].fillna(titanic['Age'].mean())
titanic.dropna(inplace=True)
#print titanic.head()

tab = titanic.pivot_table('Survived', index='Sex', columns='Pclass',aggfunc='count')
#print tab
tab2 = titanic.pivot_table('Survived', index='Sex', columns='Pclass')
#print tab2
age = pd.cut(titanic['Age'], [0,12,18,80])
tab3 = titanic.pivot_table('Survived',index =['Sex', age], columns='Pclass',aggfunc='count')

fare = pd.qcut(titanic['Fare'], 2)
tab4 = titanic.pivot_table('Survived',index=['Sex',age],columns=[fare,'Pclass'])

tab5 = titanic.pivot_table('Survived',index=['Sex',age],columns=[fare,'Pclass'], fill_value=0.0)
print tab5
