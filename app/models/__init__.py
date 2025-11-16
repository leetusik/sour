from sqlalchemy.orm import DeclarativeBase

# 1. Define your Base class here
class Base(DeclarativeBase):
    pass

# 2. Import all your models here
# This is CRITICAL for Alembic autogenerate to find your tables
# from . import something
# from . import user
# from . import post