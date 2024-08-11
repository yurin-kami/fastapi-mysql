#import pymysql
#
#
# conn= pymysql.connect(
#     host='172.129.103.70',
#     user='root',
#     passwd='123456',
#     charset='utf8mb4',
#     cursorclass=pymysql.cursors.DictCursor
# )
# with conn.cursor() as cursor:
#     cursor.execute("show databases;")
#     print(cursor.fetchall())
#
# conn.close()
from sqlalchemy.orm import declarative_base,sessionmaker
from sqlalchemy import Column,Integer,String,create_engine,inspect,MetaData,Table
import pymysql
#定义表及其结构
engine=create_engine('mysql+pymysql://root:123456@172.129.103.70/test', echo=True)
Base=declarative_base()
class User(Base):
    __tablename__="user_table"
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(30))
    gender=Column(String(6))
    age=Column(Integer)
    professes=Column(String(20))
    def __str__(self):
        return str(self.id)+" "+self.name+" "+self.gender+" "+str(self.age)+" "+self.professes

# Base.metadata.create_all(engine)
#zhenxia的一条数据
# zhenxia=User(name="箴黠",gender="man",age=20,professes="stu")
# Session=sessionmaker(engine)
# session=Session()
# session.add(zhenxia)
# session.commit()
#定义列表，包含多条数据
add_list=[User(name="箴黠",gender="male",age=20,professes="stu"),
          User(name="箴黠rep-0",gender="male",age=20,professes="cosplayer"),
          User(name="箴黠rep-1",gender="female",age=20,professes="worker"),
          User(name="箴黠rep-2",gender="male",age=20,professes="kami"),
          User(name="箴黠rep-3",gender="female",age=20,professes="youtuber"),
          User(name="箴黠rep-4",gender="male",age=20,professes="human"),
          User(name="箴黠rep-5",gender="female",age=20,professes="zhenxiaP"),
          User(name="箴黠rep-6",gender="male",age=20,professes="hacker"),
          User(name="箴黠rep-7",gender="female",age=20,professes="gamer"),
          User(name="箴黠rep-8",gender="male",age=20,professes="otaku"),]
# session.add_all(add_list)
# session.commit()
#查询`
# data=session.query(User).order_by(User.id).all()
# for i in data:
#     print(i)
#update
# session.query(User).filter(User.name=="箴黠rep-6").update({"gender":"female"})
# for i in session.query(User.id==7).all():
#     print(i)
# avr=session.query(User.name,func.random(User.id)).group_by(User.professes).all()
# for i in avr:
#     print(i)
#定义类，用于增删查改
class Kami:
    #初始化engine和session
    def __init__(self):
        self.engine=create_engine('mysql+pymysql://root:123456@172.129.103.70/test', echo=True)
        self.session=sessionmaker(self.engine)()
        self.insp=inspect(self.engine)
    #定义方法insert用于插入数据
    def insert(self,data):
        self.session.add_all(data)
        self.session.commit()
        print("please use inquire method to show the insert")
        return "please use inquire method to show the insert"
    #定义方法inquire用于查询数据，当professes为空就查询所有数据，其他功能可以类推
    def inquire(self, table:classmethod, professes=None):
        if professes == None:
            return self.session.query(table).all()
        return self.session.query(table).filter(table.professes == professes).all()
    #定义方法创建表，只是把原本的功能封装了
    def cre_table(self):
        Base.metadata.create_all(self.engine)
        print("ok")
        return "ok"
    #定义方法删除数据库，使用pymysql库
    def del_database(self,database):
        conn = pymysql.connect(
            host='172.129.103.70',
            user='root',
            passwd='123456',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            cursor.execute(f"drop database {database} ;")
            print(cursor.fetchall())
        conn.close()
        return "Query OK"
    #定义方法删除表
    def del_table(self):
        Base.metadata.drop_all(engine)
        print("ok")
        return "ok"
    #定义方法删除数据，没有实现复杂功能
    def del_data(self,table:classmethod,name):
        data=self.session.query(table).filter(table.name==name).first()
        self.session.delete(data)
        self.session.commit()
    #定义方法更新数据，也没有实现复杂功能
    def update(self,table:classmethod,name,new_name):
        data=self.session.query(table).filter(table.name==name).first()
        data.name=new_name
        self.session.add(data)
        self.session.commit()
    #查询数据库中的表
    def get_table(self):
        return self.insp.get_table_names()
    #直接查询表内容，自动反映射表结构,返回一个列表
    def query_table(self,table:str):
        for i in self.get_table():
            if str(i) == table:
                meta = MetaData()
                table_name = Table(table, meta, autoload_with=self.engine)
                return self.session.query(table_name).all()
        return -1


if __name__ == '__main__':
    kami=Kami()
    # kami.update(table=User,name="箴黠rep-4",new_name="zhenxia-rep-4")
    # kami.del_data(table=User,name="箴黠rep-1")
    # kami.cre_table()
    # kami.insert(data=add_list)
    # res=kami.inquire(table=User)
    # for i in res:
    #     print(i)
    # print(kami.query_table('kami'))
