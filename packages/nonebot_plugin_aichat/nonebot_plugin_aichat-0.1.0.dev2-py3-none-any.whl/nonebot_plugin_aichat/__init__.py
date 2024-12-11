from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

# from .config import Config

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_aichat",
    description="",
    usage="",
    # config=Config,
)

from nonebot.plugin.on import on_message


# config = get_plugin_config(Config)
#
# print(config.db)

@on_message().handle()
async def on_message(message) -> None:
    message.reply('pong')
