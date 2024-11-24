from volcenginesdkarkruntime import Ark
from typing import List, Dict, Any, Optional
import json

class ByteDanceAIClient:
    def __init__(
        self, 
        use_ai: bool = True, 
        base_url: Optional[str] = None,
        model_id: Optional[str] = None,
        default_system_prompt: Optional[str] = None
    ):
        """
        初始化ByteDance AI客户端

        Args:
            use_ai: 是否使用AI功能
            base_url: API基础URL
            model_id: 模型ID
            default_system_prompt: 默认的system prompt
        """
        self.use_ai = use_ai
        if use_ai:
            self.client = Ark(base_url=base_url)
            self.model_id = model_id
        self.default_system_prompt = default_system_prompt or "你是一个AI助手，请回答用户的问题。"

    def generate_messages(
        self, 
        user_content: str,
        system_prompt: Optional[str] = None,
        additional_messages: Optional[List[Dict[str, str]]] = None
    ) -> List[Dict[str, str]]:
        """
        生成消息列表

        Args:
            user_content: 用户输入内容
            system_prompt: 可选的系统提示词
            additional_messages: 额外的消息列表
        """
        messages = [
            {"role": "system", "content": system_prompt or self.default_system_prompt},
            {"role": "user", "content": user_content}
        ]
        
        if additional_messages:
            messages.extend(additional_messages)
            
        return messages

    async def generate_response(
        self,
        user_content: str,
        system_prompt: Optional[str] = None,
        additional_messages: Optional[List[Dict[str, str]]] = None,
        parse_json: bool = False
    ) -> Any:
        """
        生成AI响应

        Args:
            user_content: 用户输入内容
            system_prompt: 可选的系统提示词
            additional_messages: 额外的消息列表
            parse_json: 是否将响应解析为JSON

        Returns:
            AI生成的响应或解析后的JSON
        """
        if not self.use_ai:
            return None

        try:
            messages = self.generate_messages(
                user_content,
                system_prompt,
                additional_messages
            )

            completion = self.client.chat.completions.create(
                model=self.model_id,
                messages=messages
            )

            result = completion.choices[0].message.content.strip()

            if parse_json:
                return json.loads(result)
            return result

        except Exception as e:
            print(f"Generation error: {e}")
            return None
