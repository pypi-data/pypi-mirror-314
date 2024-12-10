from seatools.ioc.config import cfg
from seatools.redis.dbconfig import RedisConfig
from seatools.redis.utils import new_redis
from seatools.ioc.injects import Bean
from loguru import logger


@Bean
def init_redis():
    redis_config = None
    config = cfg()
    if 'seatools' in config and 'redis' in config['seatools']:
        redis_config = config['seatools']['redis']

    if not redis_config:
        logger.warning('配置[seatools.redis]不存在, 无法自动初始redis bean实例')
        return
    if not isinstance(redis_config, dict):
        logger.error('配置[seatools.redis]属性不是字典类型, 无法自动初始redis bean实例')
        exit(1)
    try:
        config = RedisConfig(**redis_config)
        client = new_redis(config, config.config)
        # 注册bean
        Bean(name=config.name or 'redis', primary=config.primary)(client)
    except Exception as e:
        logger.error(f'配置[seatools.redis]存在不支持的参数, 请检查修改配置后重试')
        exit(1)
