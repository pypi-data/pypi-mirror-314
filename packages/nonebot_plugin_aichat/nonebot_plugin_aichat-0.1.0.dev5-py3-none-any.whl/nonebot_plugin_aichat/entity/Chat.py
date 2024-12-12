from .. import flags
from datetime import datetime
from typing import List, Optional
from tortoise import fields

if flags.platform == "ZHENXUN":
    from zhenxun.services.db_context import Model
    from zhenxun.services.log import logger
else:
    pass


class Chat(Model):
    """
    Chat实体类，用于存储对话的基本信息。
    """
    id = fields.IntField(pk=True)
    user_id = fields.CharField(max_length=255, unique=True)  # 使用字符串类型的UID
    prompt = fields.TextField(null=True)  # 提示词
    max_tokens = fields.IntField(null=True)  # 最长Token
    max_messages = fields.IntField(null=True)  # 最多记录的对话数
    created_at = fields.DatetimeField(auto_now_add=True)

    @classmethod
    async def get_chat_by_uid(cls, uid: str) -> 'Chat':
        """
        根据UID获取用户最新的聊天记录。
        :param uid: 用户唯一标识符
        :return: 用户最新的Chat对象
        """
        return await cls.filter(user_id=uid).order_by('-created_at').first()

    async def get_recent_messages(self, n):
        """
        获取最近的N条消息。
        """
        return await Message.filter(chat_id=self.id).order_by('-timestamp').limit(n)

    def __str__(self):
        return (f"Chat(id={self.id}, user_id={self.user_id}, prompt={self.prompt}, "
                f"max_tokens={self.max_tokens}, max_messages={self.max_messages}, "
                f"created_at={self.created_at})")


class Message(Model):
    """
    Message实体类，用于存储对话中的每条消息。
    """
    id = fields.IntField(pk=True)
    chat = fields.ForeignKeyField('models.Chat', related_name='messages')
    content = fields.TextField()
    timestamp = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"Message(id={self.id}, chat_id={self.chat.id}, content={self.content}, timestamp={self.timestamp})"
