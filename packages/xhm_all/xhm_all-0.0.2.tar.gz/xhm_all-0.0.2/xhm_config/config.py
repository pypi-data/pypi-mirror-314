import os
from dynaconf import Dynaconf

# 使用 try-except 判断是否安装了 Redis
try:
    from redis.connection import ConnectionPool
    from xhm_redis import BoChuRedis

    REDIS_ENABLED = True
except ImportError:
    REDIS_ENABLED = False


class CacheConfig:
    root_path: str = None

    def get_pool(self):
        if REDIS_ENABLED:
            return ConnectionPool(
                host=self.settings.xhm_config_redis.host,
                port=self.settings.xhm_config_redis.port,
                password=self.settings.xhm_config_redis.password,
                db=self.settings.xhm_config_redis.db,
                encoding="utf-8",
                decode_responses=True,
            )
        return None

    def __init__(self):
        # 加载配置
        self.settings = Dynaconf(
            settings_files=self._get_settings_files(),
            environments=True,  # 启用分层配置
            load_dotenv=True,  # 加载环境变量
            redis_enabled=False,  # 启用 Redis 后端
        )

        # 设置环境
        self.settings.setenv(os.getenv('ENV', 'default'))

        # 初始化redis
        if self.settings.cache_mode and REDIS_ENABLED:
            self._cache = BoChuRedis(connection_pool=self.get_pool())
        else:
            self._cache = None

    def _get_settings_files(self):
        # 获取项目配置文件路径
        project_settings_file, project_secrets_file = self._get_project_path()

        # 获取 SDK 配置文件路径
        sdk_settings_file = os.path.join(os.path.dirname(__file__), 'sdk_settings.toml')
        sdk_secrets_file = os.path.join(os.path.dirname(__file__), 'sdk_secrets.toml')

        # 加载顺序 sdk_settings_file>sdk_secrets_file>project_settings_file>project_secrets_file
        # 后面的文件会覆盖前面的值
        settings_files = [sdk_settings_file]
        if os.path.exists(sdk_secrets_file):
            settings_files.append(sdk_secrets_file)

        if os.path.exists(project_settings_file):
            settings_files.append(project_settings_file)
        if os.path.exists(project_secrets_file):
            settings_files.append(project_secrets_file)
        return settings_files

    def get(self, key: str):
        return self._get_width_cache_mode(key) or self.settings.get(key, None)

    def set(self, key: str, value: any):
        if self._cache:
            self._cache.set(key, value)
        else:
            raise Exception("只允许对缓存中的值进行变更，不允许对配置文件进行变更")

    def _get_width_cache_mode(self, key: str):
        # 缓存模式
        if self.settings.cache_mode == "all" or self.settings.cache_mode == "preferred" and self.settings.get(
                f"{key}_cache", False):
            return self._cache.get(key) if self._cache else None
        return None

    def setenv(self, env: str):
        return self.settings.setenv(env)

    def all(self):
        return self.settings.as_dict()

    def info(self):
        project_settings_file, project_secrets_file = self._get_project_path()
        return {
            "root_path": self.get_root_path(),
            "project_settings": project_settings_file,
            "project_secrets": project_secrets_file}

    def _get_project_path(self):
        project_settings_file = os.path.join(os.getcwd(), 'settings.toml')
        project_secrets_file = os.path.join(os.getcwd(), '.secrets.toml')
        return project_settings_file, project_secrets_file

    def get_root_path(self):
        return self.root_path if self.root_path else os.getcwd()

    def set_root_path(self, root_path: str):
        self.root_path = root_path


conf = CacheConfig()
