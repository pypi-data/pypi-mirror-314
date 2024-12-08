### 柏楚配置中心

优先加载项目中的配置文件，sdk中的配置文件是默认值


### 快速上手
  
    from xhm_config import conf

    def test_config():
        # 打印所有配置
        print(conf.all())
    
        # 获取配置
        print(f"Database host: {conf.get('DB_HOST')}")
    
        # 动态切换到 production 环境 或者通过环境变量 ENV=production 切换
        conf.setenv('production')
        print(f"Database host: {conf.get('DB_HOST')}")
  
 
### 读取嵌套的值

settings.toml:

    [default]
    service_name = "service_name"
    cache_mode = "preferred"
    test = "我是配置文件中的值"
    test_cache = true
    
    [default.xhm_config_redis]
    host = "10.1.251.87"
    port = 6379
    db = 0
    password = ""
 
读取：

    def test_mux_config():
        print(f"redis host: {conf.get('xhm_config_redis.host')}")



### 文件加载顺序说明

sdk_settings.toml > sdk_secrets.toml > project settings.toml > project secrets.toml

相同的key, 后加载的文件会覆盖前者key中的值


### 缓存模式

缓存模式一共分为三种：


- cache_mode = "all"： 所有的key都走缓存，缓存中没有的采用配置文件中的值
- cache_mode = "preferred": 
  - 缓存部分key，缓存中没有的同样采用配置文件中的值； 
  - 需要缓存的key可以采用{key}_cache=true开启缓存。如key123 = "123", 开启“key123”的缓存配置则是key123_cache = true

- cache_mode = "": 不进行任何缓存，全部采用配置文件。

### 缓存部分key

settings.toml:

    [default]
    cache_mode = "preferred"
    test = "我是配置文件中的值"
    test_cache = true
    
    [default.xhm_config_redis]
    host = "10.1.251.87"
    port = 6379
    db = 0
    password = ""

code:

    from xhm_config import conf

    
    def test_cache_mode():
        print(conf.get("test"))
        print(conf.get("test_cache"))
        conf.set("test", "我是redis中的值")
        print(conf.get("test"))

输出：

    我是配置文件中的值
    True
    我是redis中的值