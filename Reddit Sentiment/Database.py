import sqlalchemy as db
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
engine=db.create_engine('mysql://u831388458_covid19:Password@123@34.89.97.3:3306/u831388458_covid19stats',pool_recycle=1)
writer=pd.ExcelWriter('BruhData.xlsx',engine='xlsxwriter')
for (tname,) in engine.execute('SHOW TABLES'):
    if 'reddit' in tname and 'sentiment' in tname:
        df=pd.read_sql_table(tname,engine)
        df.to_excel(writer,sheet_name=tname[:30])
writer.save()
