from bytedance_ai_tools.bytedance_ai_client import ByteDanceAIClient
import asyncio
from concurrent.futures import ThreadPoolExecutor

class BytedanceTranslator:
    def __init__(self, use_ai=True, base_url=None, model_id=None):
        self.ai_client = ByteDanceAIClient(
            use_ai=use_ai,
            base_url=base_url,
            model_id=model_id,
            default_system_prompt="你是一个英文到中文的翻译助手。请将给定的英文文本翻译成中文，保持专业性和准确性。只需返回翻译结果，不需要解释。"
        )
        self.thread_pool = ThreadPoolExecutor(max_workers=None)
        self.loop = asyncio.new_event_loop()
    
    def translate(self, text):
        if not self.ai_client.use_ai:
            return text
            
        future = self.thread_pool.submit(
            self._run_async_code,
            self.ai_client.generate_response(
                user_content=text,
                parse_json=False
            )
        )
        result = future.result()
        return result if result is not None else text
    
    def _run_async_code(self, coroutine):
        return self.loop.run_until_complete(coroutine) 