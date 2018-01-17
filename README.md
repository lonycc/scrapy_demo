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
