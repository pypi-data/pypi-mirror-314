import flags

from nonebot import get_plugin_config, on_message
from nonebot.plugin import PluginMetadata

# from .config import Config


extra = None
base_config = None

try:
    from zhenxun.services.log import logger
    from zhenxun.configs.config import Config, BotConfig
    from zhenxun.configs.utils import PluginExtraData, RegisterConfig

    flags.platform = "ZHENXUN"
    logger.info("Zhenxun environment found, run as zhenxun plugin.")
    base_config = Config.get("aichat")
    extra = PluginExtraData(
        author="Expliyh",
        version="0.1.0-dev2",
        configs=[
            RegisterConfig(
                module="aichat",
                key="OPENAI_TOKEN",
                value=None,
                help="登陆OpenAI获取 https://platform.openai.com/docs/overview"
            ),
            RegisterConfig(
                module="aichat",
                key="db",
                value="builtin",
                help="数据库连接信息，builtin 使用真寻自带的数据库",
                default_value="builtin",
                type=str
            )
        ],
        admin_level=base_config.get("GROUP_AICHAT_LEVEL"),
    ).dict()
    Config.add_plugin_config(
        "aichat",
        "GROUP_AICHAT_LEVEL",
        5,
        help="管理群聊AI需要的等级",
        default_value=5,
        type=int,
    )
except Exception as e:
    pass

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_aichat",
    description="",
    usage="""
       usage：
           在 QQ 群聊或私聊中与 ChatGPT聊天
       指令：
           添加github ['用户'/'仓库'] [用户名/{owner/repo}]
           提示词 ['提示词']
           更新对话
           示例：提示词 你是一只猫娘
           示例：更新对话
           示例：添加github订阅 用户 HibiKier
           示例：添加gb订阅 仓库 HibiKier/zhenxun_bot
           示例：添加github 用户 HibiKier
           示例：删除gb订阅 HibiKier
       """.strip(),
    extra=extra,
    # config=Config,
)


# config = get_plugin_config(Config)
#
# print(config.db)

@on_message().handle()
async def on_message(message) -> None:
    message.reply('pong')
