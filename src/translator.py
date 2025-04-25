import boto3
import json
import yaml
import os

class BedrockTranslator:
    """
    使用AWS Bedrock的Nova Pro模型进行文本翻译
    """
    
    def __init__(self, config_path="config/config.yaml"):
        """初始化Bedrock客户端"""
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        
        # 创建Bedrock客户端
        session = boto3.Session(
            profile_name=self.config['aws']['profile'],
            region_name=self.config['aws']['region']
        )
        self.bedrock_runtime = session.client(
            service_name='bedrock-runtime',
            region_name=self.config['aws']['region']
        )
        self.model_id = self.config['bedrock']['model_id']
    
    def translate_text(self, text, target_language="中文"):
        """
        使用Nova Pro模型将文本翻译为目标语言
        """
        # 构建提示
        prompt = f"""
        请将以下文本翻译成{target_language}，保持专业术语的准确性和整体文档的格式结构：

        {text}
        
        请只返回翻译后的内容，不要添加任何解释或额外的文本。
        """
        
        # 构建请求体
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4096,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        # 调用Bedrock API
        try:
            response = self.bedrock_runtime.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            
            # 解析响应
            response_body = json.loads(response.get('body').read())
            translated_text = response_body.get('content')[0].get('text')
            
            return translated_text
        
        except Exception as e:
            print(f"翻译过程中出错: {e}")
            return None
    
    def translate_large_text(self, text, chunk_size=2000, target_language="中文"):
        """
        将大文本分块翻译，然后合并结果
        """
        if len(text) <= chunk_size:
            return self.translate_text(text, target_language)
        
        # 分块处理
        chunks = []
        for i in range(0, len(text), chunk_size):
            chunk = text[i:i+chunk_size]
            chunks.append(chunk)
        
        # 翻译每个块
        translated_chunks = []
        for i, chunk in enumerate(chunks):
            print(f"正在翻译第 {i+1}/{len(chunks)} 块...")
            translated_chunk = self.translate_text(chunk, target_language)
            if translated_chunk:
                translated_chunks.append(translated_chunk)
        
        # 合并翻译结果
        return "\n".join(translated_chunks)
