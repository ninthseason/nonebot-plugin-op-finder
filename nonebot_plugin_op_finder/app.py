no_op = [
    {
        "type": "card",
        "theme": "secondary",
        "size": "lg",
        "color": "#00ff00",
        "modules": [
            {
                "type": "section",
                "text": {
                    "type": "kmarkdown",
                    "content": "查找完成，当前没有(font)原批(font)[purple]！"
                }
            }
        ]
    }
]


def op_unit(avatar, name, time):
    return {
        "type": "section",
        "text": {
            "type": "kmarkdown",
            "content": f"(font){name}(font)[danger] 当前时长: (font){time}(font)[danger] 分钟"
        },
        "mode": "left",
        "accessory": {
            "type": "image",
            "src": avatar,
            "size": "lg"
        }
    }


def op_template(users):
    return [
        {
            "type": "card",
            "theme": "secondary",
            "size": "lg",
            "color": "#ff0000",
            "modules": [
                {
                    "type": "section",
                    "text": {
                        "type": "kmarkdown",
                        "content": "查找完成，发现(font)原批(font)[purple]！"
                    }
                },
                {
                    "type": "divider"
                }
            ] + [op_unit(i[0], i[1], i[2]) for i in users]
        }
    ]


def init():
    from nonebot import on_command
    from nonebot.adapters.kaiheila import Bot as KookBot
    from nonebot.adapters.kaiheila import Event as KookEvent
    from nonebot.adapters.kaiheila import MessageSegment

    from nonebot import logger
    from .lib import get_ops
    import time

    op_finder = on_command("查找原批", aliases={"op", "原批"})

    @op_finder.handle()
    async def _(bot: KookBot, event: KookEvent):
        # logger.debug(f"channel_type: {event.channel_type}")
        if event.channel_type == "PERSON":
            op_finder.finish()
        channel_id = event.target_id
        guild_id = event.extra.guild_id
        logger.debug(f"收到来自 guild_id|channel_id:{guild_id}|{channel_id} 的消息")
        op_users = await get_ops(guild_id)

        if len(op_users) == 0:
            # await bot.call_api("game/activity", id=1500242, data_type=1)
            await op_finder.finish(MessageSegment.Card(no_op))
        else:
            # await bot.call_api("game/delete-activity", data_type=1)
            await op_finder.finish(MessageSegment.Card(op_template(op_users)))
