from redisorm.core import Column, PersistentData


class URL(PersistentData):
    id = Column()
    url = Column()


class Page(PersistentData):
    id = Column()
    url = Column()
    title = Column()
    description = Column()
