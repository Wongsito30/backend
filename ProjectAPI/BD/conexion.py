from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

databaseURL = "mysql+mysqlconnector://root:nFfaOmIJhguvIrmSFvbQYtXpASvxpvaF@monorail.proxy.rlwy.net:43985/tiendaderopa"

engine = create_engine(databaseURL)

sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

base = declarative_base