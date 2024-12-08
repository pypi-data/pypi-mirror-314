import time

from xhm_chat_memory.chat_message import ChatMessage
from xhm_redis.xhm_redis import XHMRedis


class ChatMemory:

    def __init__(self, redis: XHMRedis):
        self._store = redis

    def _add(self, memory_key: str, message: ChatMessage, expire: int):
        current_time_millis = int(time.time() * 1000)
        self._store.zadd(memory_key, mapping={message.to_json(): current_time_millis})
        self._store.expire(memory_key, expire)

    @classmethod
    def _get_key(cls, message: ChatMessage, version: str):
        return f"chat:room:{version}:{message.room_id}" if message.room_id else f"chat:user:{version}:{message.user_id}"

    def add(self, messages: list[ChatMessage], expire: int = 86400, version: str = "v1"):
        for message in messages:
            memory_key = self._get_key(message=message, version=version)
            self._add(memory_key=memory_key, message=message, expire=expire)

    def get(self, message: ChatMessage, version: str = "v1", top_n: int = 40, time_period: int = 14400) -> list[
        ChatMessage]:
        """
        群聊对话记录，理论上只要近期聊的消息，4 小时以内的，超过4小时的聊天记录，基本没什么作用，还容易造成干扰
        top_n=40, 获取近40条聊天记录
        time_period=14400,单位秒，获取近4小时的聊天记录
        """
        memory_key = self._get_key(message=message, version=version)
        pipeline = self._store.pipeline()
        start_time = int(time.time() * 1000) - time_period * 1000
        end_time = int(time.time() * 1000)
        pipeline.zrevrangebyscore(name=memory_key, min=start_time, max=end_time, start=0, num=top_n, withscores=True)
        messages = pipeline.execute()[0]
        chat_memory_logs = []
        for message, current_time_millis in reversed(messages):
            chat_memory_logs.append(
                ChatMessage.from_json(json_str=message, current_time_millis=int(current_time_millis)))
        return chat_memory_logs
