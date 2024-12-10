# Seatools-starter-redis

seatools ioc 的 redis 启动器

## 仓库地址:
1. https://github.com/seatools-py/seatools-starter-redis
2. https://gitee.com/seatools-py/seatools-starter-redis

## 使用指南
1. 安装, `poetry add seatools-starter-redis`
2. 配置文件`config/application.yml`配置如下:
```yaml
# seatools 配置
seatools:
  # redis 配置
  redis:
    host: localhost
    port: 6379
    password: 123456
    database: 0
    # redis.Redis.from_url的额外参数
    config:
      # 示例:
      # 响应自动解码配置
      decode_responses: true
```
3. 使用示例
```python
from seatools.ioc import run, Autowired
from redis import Redis


# 启动ioc
run(scan_package_names=['seatools.ioc.starters.redis'], config='./config')

# 获取redis.Redis实例
client = Autowired(cls=Redis)

client.set(...)
client.get(...)

```
