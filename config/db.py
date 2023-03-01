from sqlalchemy import create_engine,MetaData

engine = create_engine("mysql+pymysql://root:mysql@localhost:3306/bd_steam")

meta = MetaData()

conn = engine.connect()




