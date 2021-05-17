# scrapy_jd
搜索爬取京东商品详情图

# 运行版本
> python 3.7
> scrapy 2.5

# docker
### 拉取镜像
```shell
docker pull scrapinghub/splash
```
### 启动splash容器，将宿主机 8050 端口映射到容器 8050 端口
```shell
docker run -p 8050:8050 scrapinghub/splash
```

# 必备 python 库
### scrapy-splash 安装命令
```shell
pip install scrapy-splash
```
### Pillow 安装命令
```shell
pip install Pillow
```

# 运行命令
```shell
scrapy crawl jd -a keyword=xxx -a page=yyy
```