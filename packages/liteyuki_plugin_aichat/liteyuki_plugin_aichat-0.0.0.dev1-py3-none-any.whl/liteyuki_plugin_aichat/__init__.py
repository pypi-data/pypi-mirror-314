from liteyuki.plugin import PluginMetadata, PluginType

# 定义插件元数据
__plugin_meta__ = PluginMetadata(
    name="AIChat",  # 插件名称
    version="0.0.0-dev1",  # 插件版本
    description="A simple plugin for liteyuki aichat",  # 插件描述
    type=PluginType.APPLICATION  # 插件类型
)

from liteyuki.session.event import MessageEvent

from liteyuki.session.on import on_message


@on_message().handle()
async def a_ping(message: MessageEvent) -> None:
    print("Ping")
    print(message.raw_message)
    if message.raw_message == "ping":
        message.reply("pong")
