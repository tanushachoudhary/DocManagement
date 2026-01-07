from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://root:tanushac1811@localhost:3306/docdb"
)

with engine.connect() as conn:
    print(" Connected to MySQL")
