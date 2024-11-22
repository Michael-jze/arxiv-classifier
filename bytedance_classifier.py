from bytedance_ai_client import ByteDanceAIClient

def prompt_template(title, abstract):
    return f"Title: {title}\nAbstract: {abstract}"

def system_prompt(classify_types):
    return f"""你是一个论文分类助手。请将论文分类为以下类别的一个或多个：{classify_types}。
    只需返回分类结果，不需要解释。
    如果论文不属于上述任何一个类别，分类为Unknown。
    返回格式为：["LLM","Efficiency"]"""

class BytedanceClassifier:
    def __init__(self, use_ai=True, base_url=None, model_id=None, classify_types=[]):
        assert len(classify_types) > 0, "classify_types must be a non-empty list"
        self.ai_client = ByteDanceAIClient(
            use_ai=use_ai,
            base_url=base_url,
            model_id=model_id,
            default_system_prompt=system_prompt(classify_types)
        )

    async def classify_paper(self, title, abstract):
        if not self.ai_client.use_ai:
            return "Global"
            
        user_content = prompt_template(title, abstract)
        result = await self.ai_client.generate_response(
            user_content=user_content,
            parse_json=True
        )
        
        return result if result is not None else "Global" 
