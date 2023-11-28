from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

databaseURL = "mysql+mysqlconnector://root:2gED4feaeAE2HgFFFB1a4Ea2C6fHgd3D@viaduct.proxy.rlwy.net:52528/tiendaderopa"

engine = create_engine(databaseURL)

sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

base = declarative_base