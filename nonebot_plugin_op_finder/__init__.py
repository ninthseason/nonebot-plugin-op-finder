__version__ = "1.0.0"

from nonebot import get_driver
from nonebot.plugin import PluginMetadata

from .config import Config
from .lib import init as lib_init
from .app import init as app_init

__plugin_meta = PluginMetadata(
    name="op-finder",
    description="显示当前正在玩原神的人",
    usage="/查找原批 /op /原批",
    type="application",
    homepage='https://github.com/ninthseason/nonebot-plugin-op-finder',
    supported_adapters={"~kaiheila"},
    config=Config,
)

global_config = get_driver().config
config = Config.parse_obj(global_config)

if config.kook_auth_key is None:
    raise ValueError("配置项kook_auth_key未设置")

lib_init(config)
app_init()
