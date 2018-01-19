# scrapy爬虫框架使用demo

## 环境依赖

- Linux/Mac/Windows7或以上

- Python3.5 或以上

- MongoDB 3.4

- Redis 3.2

## 部署步骤

- 1. 克隆到本地

`git clone https://github.com/tonyxyl/scrapy_demo.git`

- 2. 创建虚拟环境

`python -m venv my_venv`

- 3. 进入虚拟环境并安装依赖

`source my_venv/bin/activate`

Windows下需要进入`my_venv/Scripts`目录,执行`activate.bat`或`Activate.ps1`

`cd /path/to/scrapy_demo`

`pip install -r requirements.txt`

- 4. 跑起来

`scrapy crawl demo`

`scrapy crawl jandan_pic`  #爬取煎蛋网的无聊图、妹子图等图片版块

- 5. 其他爬虫

在spiders目录下可以查看到已有的爬虫案例


## 利用spiderkeeper管理爬虫

`pip install git+https://github.com/scrapy/scrapyd-client.git@python3-wip` #先安装scrapyd-client

`pip install spiderkeeper` #安装spiderkeeper

**配置supervisor**

```
[program:spiderkeeper]
command=spiderkeeper --server=http://localhost:6800 --username=user --password=pass
directory=/home
autostart=true
autorestart=true
startretries=3

[program:scrapyd]
command=source /home/my_venv/bin/activate
directory=/home/tony/
command=/home/my_venv/bin/scrapyd
autostart=true
autorestart=true
redirect_stderr=true
```

**部署与维护**

`curl http://localhost:6800/listversions.json?project=myspider`

> {"node_name": "localhost.localdomain", "status": "ok", "versions": ["1508438806"]}

`curl http://localhost:6800/delversion.json -d project=myspider -d version=xxx`

`source /home/my_venv/bin/activate`

`cd /home/tony/myspider`

`scrapyd-deploy myspider -p myspider`

`deactivate`

`supervisorctl restart spiderkeeper`



## scrapyd-deploy提供的接口

**调度一个爬虫**

`curl http://localhost:6800/schedule.json -d project=[myspider] -d spider=[spider_name]`

**取消一个任务**

`curl http://localhost:6800/cancel.json -d project=[myspider] -d job=[job_id]`

**爬虫列表**

`curl http://localhost:6800/listspiders.json?project=myspider`

**任务列表**

`curl http://localhost:6800/listjobs.json?project=myspider`

**项目列表**

`curl http://localhost:6800/listprojects.json`

**版本列表**

`curl http://localhost:6800/listversions.json?project=myspider`

**删除版本**

`curl http://localhost:6800/delversion.json -d project=myspider -d version=r99`

**删除项目**

`curl http://localhost:6800/delproject.json -d project=myspider`



## scrapy 命令行

`scrapy startproject [project_name]` #创建一个项目

`scrapy crawl [spider_name]`  #启动一个爬虫

`scrapy view [url]`  #查看一个链接

`scrapy version -v`  #版本信息

`scrapy check`  #当前项目检查

`scrapy shell` #进入交互环境

`scrapy list`  #当前项目爬虫列表

`scrapy genspider [spider_name] [domain]`  #生成一个爬虫
