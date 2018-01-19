# scrapy_redis 原理解析

## connect.py

> `connect`文件引入了`redis`模块，这个是`redis-python`库的接口，用于通过`python`访问`redis`数据库，可见，这个文件主要是实现连接`redis`数据库的功能（返回的是`redis`库的`Redis`对象或者`StrictRedis`对象，这俩都是可以直接用来进行数据操作的对象）。这些连接接口在其他文件中经常被用到。其中，我们可以看到，要想连接到`redis`数据库，和其他数据库差不多，需要一个ip地址、端口号、用户名密码（可选）和一个整形的数据库编号，同时我们还可以在`scrapy`工程的`setting`文件中配置套接字的超时时间、等待时间等。

## picklecompat.py

> 这里实现了`loads`和`dumps`两个函数，其实就是实现了一个`serializer`，因为`redis`数据库不能存储复杂对象（`value`部分只能是字符串，字符串列表，字符串集合和`hash`，`key`部分只能是字符串），**所以我们存啥都要先串行化成文本才行**。这里使用的就是`python`的`pickle`模块，一个兼容py2和py3的串行化工具。这个`serializer`主要用于一会的`scheduler`存`reuqest`对象，至于为什么不使用`json`格式，因为PY3里面, `serializer`必须返回字符串keys并支持字节values, 所以呢，json/msgpack模块默认就不支持了，`item pipeline`的串行化默认用的就是`json`。

## pipelines.py

> `pipeline`文件实现了一个`item pipieline`类，和`scrapy`的`item pipeline`是同一个对象，通过从`settings`中拿到我们配置的`REDIS_ITEMS_KEY`作为`key`，把`item`串行化之后存入`redis`数据库对应的`value`中（这个`value`可以看出出是个`list`，我们的每个`item`是这个`list`中的一个结点），这个`pipeline`把提取出的`item`存起来，主要是为了方便我们延后处理数据。

## queue.py

> 该文件实现了几个容器类，可以看这些容器和`redis`交互频繁，同时使用了我们上边`picklecompat`中定义的`serializer`。这个文件实现的几个容器大体相同，只不过一个是队列，一个是栈，一个是优先级队列，这三个容器到时候会被`scheduler`对象实例化，来实现`request`的调度。比如我们使用`SpiderQueue`作为调度队列的类型，到时候`request`的调度方法就是先进先出，而采用`SpiderStack`就是先进后出了。

> 仔细看`FifoQueue`的实现, 它的`push`函数就和其他容器的一样, 只不过`push`进去的`request`请求先被`scrapy`的接口`request_to_dict`变成了一个`dict`对象（因为`request`对象实在是比较复杂，有方法有属性不好串行化），之后使用`picklecompat`中的`serializer`串行化为字符串，然后使用一个特定的`key`存入`redis`中（该key在同一个`spider`中是相同的）。而调用`pop`时，其实就是从`redis`用那个特定的`key`去读其值（一个`list`），从`list`中读取最早进去的那个，于是就先进先出了。

> 这些容器类都会作为`scheduler`调度`request`的容器，`scheduler`在每个主机上都会实例化一个，并且和`spider`一一对应，所以分布式运行时会有一个`spider`的多个实例和一个`scheduler`的多个实例存在于不同的主机上，但是，因为`scheduler`都是用相同的容器，而这些容器都连接同一个`redis`服务器，又都使用`spider`名加`queue`来作为`key`读写数据，所以不同主机上的不同爬虫实例公用一个`request`调度池，实现了分布式爬虫之间的统一调度。

## dupefilter.py

> 这个文件看起来比较复杂，重写了scrapy本身已经实现的request判重功能。因为本身scrapy单机跑的话，只需要读取内存中的request队列或者持久化的request队列（scrapy默认的持久化似乎是json格式的文件，不是数据库）就能判断这次要发出的request url是否已经请求过或者正在调度（本地读就行了）。而分布式跑的话，就需要各个主机上的scheduler都连接同一个数据库的同一个request池来判断这次的请求是否是重复的了。

> 在这个文件中，通过继承`BaseDupeFilter`重写他的方法，实现了基于`redis`的判重。根据源代码来看，`scrapy-redis`使用了`scrapy`本身的一个`fingerprint`接口`request_fingerprint`，这个接口很有趣，根据`scrapy`文档所说，他通过`hash`来判断两个`url`是否相同（相同的`url`会生成相同的`hash`结果），**但是当两个url的地址相同，get型参数相同但是顺序不同时，也会生成相同的hash结果**。所以`scrapy-redis`依旧使用`url`的`fingerprint`来判断`request`请求是否已经出现过。这个类通过连接`redis`，使用一个`key`来向`redis`的一个`set`中插入`fingerprint`（这个`key`对于同一种`spider`是相同的，`redis`是一个`key-value`的数据库，如果`key`是相同的，访问到的值就是相同的，这里使用`spider`名字+`DupeFilter`的`key`就是为了在不同主机上的不同爬虫实例，只要属于同一种`spider`，就会访问到同一个`set`，而这个`set`就是他们的`url`判重池），如果返回值为0，说明该`set`中该`fingerprint`已经存在（因为集合是没有重复值的），则返回False，如果返回值为1，说明添加了一个`fingerprint`到`set`中，则说明这个`request`没有重复，于是返回True，还顺便把新`fingerprint`加入到数据库中了。

> `DupeFilter`判重会在`scheduler`类中用到，每一个`request`在进入调度之前都要进行判重，如果重复就不需要参加调度，直接舍弃就好了，不然就是白白浪费资源。

## scheduler.py

> 这个文件重写了`scheduler`类，用来代替`scrapy.core.scheduler`的原有调度器。其实对原有调度器的逻辑没有很大的改变，主要是使用了`redis`作为数据存储的媒介，以达到各个爬虫之间的统一调度。

> `scheduler`负责调度各个`spider`的`request`请求，`scheduler`初始化时，通过`settings`文件读取`queue`和`dupefilters`的类型（一般就用上边默认的），配置`queue`和`dupefilters`使用的`key`（一般就是`spider name`加上`requests`或者`dupefilters`，这样对于同一种`spider`的不同实例，就会使用相同的数据块了）。每当一个`request`要被调度时，`enqueue_request`被调用，`scheduler`使用`dupefilters`来判断这个`url`是否重复，如果不重复，就添加到`queue`的容器中（先进先出，先进后出和优先级都可以，可以在`settings`中配置）。当调度完成时，`next_request`被调用，`scheduler`就通过`queue`容器的接口，取出一个`request`，把他发送给相应的`spider`，让`spider`进行爬取工作。

> 同时我们可以看到，如果`setting`文件中配置了`SCHEDULER_PERSIST`为`False`，那么在爬虫关闭的时候`scheduler`会调用自己的`flush`函数把`redis`数据库中的`判重`和`调度池`全部清空，使得我们的爬取进度完全丢失（但是`item`没有丢失，`item`数据在另一个`key`储存）。如果设置`SCHEDULER_PERSIST`为`True`，爬虫关闭后，判重池和调度池仍然存在于`redis`数据库中，则我们再次开启爬虫时，可以接着上一次的进度继续爬取。

## spiders.py

> `spider`的改动也不是很大，主要是通过`connect`接口，给`spider`绑定了`spider_idle`信号，`spider`初始化时，通过`setup_redis`函数初始化好和`redis`的连接，之后通过`next_requests`函数从`redis`中取出`strat url`，使用的`key`是`settings`中`REDIS_START_URLS_AS_SET`定义的（注意了这里的初始化`url`池和我们上边的`queue`的`url`池不是一个东西，`queue`的池是用于调度的，初始化`url`池是存放入口`url`的，他们都存在`redis`中，但是使用不同的`key`来区分，就当成是不同的表吧），`spider`使用少量的`start url`，可以发展出很多新的`url`，这些`url`会进入`scheduler`进行判重和调度。直到`spider`跑到调度池内没有`url`的时候，会触发`spider_idle`信号，从而触发`spider`的`next_requests`函数，再次从`redis`的`start url`池中读取一些`url`。

> 最后总结一下`scrapy-redis`的总体思路：这个工程通过重写`scheduler`和`spider`类，实现了调度、`spider`启动和`redis`的交互。实现新的`dupefilter`和`queue`类，达到了判重和调度容器和`redis`的交互，因为每个主机上的爬虫进程都访问同一个`redis`数据库，所以调度和判重都统一进行统一管理，达到了分布式爬虫的目的。

> 当`spider`被初始化时，同时会初始化一个对应的`scheduler`对象，这个调度器对象通过读取`settings`，配置好自己的调度容器`queue`和判重工具`dupefilter`。每当一个`spider`产出一个`request`的时候，`scrapy`内核会把这个`reuqest`递交给这个`spider`对应的`scheduler`对象进行调度，`scheduler`对象通过访问`redis`对`request`进行判重，如果不重复就把他添加进`redis`中的调度池。当调度条件满足时，`scheduler`对象就从`redis`的调度池中取出一个request发送给`spider`，让他爬取。当`spider`爬取的所有暂时可用`url`之后，`scheduler`发现这个`spider`对应的`redis`的调度池空了，于是触发信号`spider_idle`，`spider`收到这个信号之后，直接连接`redis`读取`strart url`池，拿去新的一批`url`入口，然后再次重复上边的工作。


# feeding a spider from redis

> 爬虫文件要继承`scrapy_redis.spiders.RedisSpider`, 这允许爬虫从redis队列里取url，如果第一个request生成了更多requests, 那么爬虫将优先处理这些requests。

`scrapy runspider myspider.py`

or

`scrapy crawl [spider_name]`

`redis-cli lpush myspider:start_urls http://news.163.com`
