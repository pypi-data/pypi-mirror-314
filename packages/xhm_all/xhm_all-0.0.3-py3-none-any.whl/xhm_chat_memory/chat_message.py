import json
from dataclasses import dataclass, asdict
from typing import Type, TypeVar

T = TypeVar('T')


@dataclass
class ChatMessage:
    # 群组id
    room_id: str
    # 发言人id
    user_id: str
    # 发言内容
    content: str
    # 发言类型 - 语音/视频/图片/文件
    type: str
    # 内部数据，无须外部赋值，毫秒
    current_time_millis: int = 0
    # 消息唯一标识
    message_id: str = ""

    def to_json(self) -> str:
        data = asdict(self)
        data.pop("current_time_millis")
        return json.dumps(data, ensure_ascii=False)

    @classmethod
    def from_json(cls: Type[T], json_str: str, current_time_millis: int = 0) -> T:
        # 将 JSON 字符串转换为字典
        data = json.loads(json_str)
        if current_time_millis > 0:
            data["current_time_millis"] = current_time_millis
        # 返回解包后的 dataclass 对象
        return cls(**data)
