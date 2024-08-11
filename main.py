from fastapi import FastAPI,Request,Response
from mysql import Kami, User
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

#实例化
app=FastAPI()
engine=create_engine('mysql+pymysql://root:123456@172.129.103.70/test', echo=True)
Base=declarative_base()
kami=Kami()
#get根路径返回数据库test所有数据
@app.get("/")
async def get_root():
    res=kami.inquire(User)
    return res
@app.middleware("http")
async def middle_ware(request:Request,md):
    print("requests")
    resp_ok=await md(request)
    resp_ok.headers["kami"]="hyh"
    if request.client.host in ["172.16.21.103"]:
        resp = Response(content="ops,forbidden ip")
        return resp
    else:
        return resp_ok
@app.get("/{table_name}")
async def post_table(table_name):
    res=kami.query_table(table_name)
    if res == -1:
        return "database not exist!!!"
    res=str(res)#数据类型太多，懒得处理，直接强转成字符串返回
    return res
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app="main:app",host="172.16.21.103",port=8883,reload=True)