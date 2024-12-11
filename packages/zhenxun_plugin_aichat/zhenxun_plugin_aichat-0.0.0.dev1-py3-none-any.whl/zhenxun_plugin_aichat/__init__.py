from nonebot import get_plugin_config, on_message
from nonebot.plugin import PluginMetadata


# from .config import Config

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_aichat",
    description="",
    usage="""
       usage：
           在 QQ 群聊或私聊中与 ChatGPT聊天
       指令：
           添加github ['用户'/'仓库'] [用户名/{owner/repo}]
           删除github [用户名/{owner/repo}]
           查看github
           示例：添加github订阅 用户 HibiKier
           示例：添加gb订阅 仓库 HibiKier/zhenxun_bot
           示例：添加github 用户 HibiKier
           示例：删除gb订阅 HibiKier
       """.strip(),
    # config=Config,
)

try:
    from zhenxun.configs.config import Config, BotConfig
    from zhenxun.configs.utils import PluginExtraData, RegisterConfig

except Exception as e:
    pass


# config = get_plugin_config(Config)
#
# print(config.db)

@on_message().handle()
async def on_message(message) -> None:
    message.reply('pong')
