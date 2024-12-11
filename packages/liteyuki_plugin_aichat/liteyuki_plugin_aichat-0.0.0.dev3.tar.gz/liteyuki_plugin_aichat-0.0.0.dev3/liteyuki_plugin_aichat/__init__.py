import nonebot
from liteyuki.plugin import PluginMetadata, PluginType

# 定义插件元数据
__plugin_meta__ = PluginMetadata(
    name="AIChat",  # 插件名称
    version="0.0.0-dev3",  # 插件版本
    description="A simple plugin for liteyuki aichat",  # 插件描述
    type=PluginType.APPLICATION  # 插件类型
)

from nonebot import on_message
from .chat_typing import T_MessageEvent


def load_self():
    nonebot.load_plugin("liteyuki-plugin-aichat")

load_self()


@on_message().handle()
async def a_ping(message: T_MessageEvent) -> None:
    print("Ping")
    print(message.raw_message)
    if message.raw_message == "ping":
        message.reply("pong")
