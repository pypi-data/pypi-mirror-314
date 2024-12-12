from typing import Union, List, Dict, Tuple
from openai import OpenAI
import openai
import time

from pyexpat.errors import messages

from openai_wrapper.config.prompts import TRANSLATE_EN_CN, get_prompt_to_merge_answers, get_prompt_for_comment_to_dialog
from openai_wrapper.config.logger import LoggerConfig


class OpenAIUtils:
    """OpenAI API 工具类，用于处理与 OpenAI 相关的操作"""

    def __init__(self, base_url: str, api_key: str, model: str, retry_num: int = 6):
        """
        初始化 OpenAI 工具类

        Args:
            base_url: OpenAI API 基础 URL
            api_key: OpenAI API 密钥
            model: 使用的模型名称
        """
        self.base_url = base_url
        self.api_key = api_key
        self.model = model
        self.client = self.get_client(base_url, api_key)
        self.logger = LoggerConfig.get_logger()
        self.retry_num = retry_num

    @staticmethod
    def get_client(base_url: str, api_key: str) -> OpenAI:
        """
        创建 OpenAI 客户端实例

        Args:
            base_url: OpenAI API 基础 URL
            api_key: OpenAI API 密钥

        Returns:
            OpenAI 客户端实例
        """
        return OpenAI(base_url=base_url, api_key=api_key)

    def _prepare_messages(self, prompt: Union[str, List[Dict[str, str]], Dict[str, str]]) -> List[Dict[str, str]]:
        """准备消息格式"""
        if isinstance(prompt, str):
            return [{"role": "user", "content": prompt}]
        elif isinstance(prompt, list):
            return prompt
        elif isinstance(prompt, dict):
            return [prompt]
        else:
            raise TypeError("prompt 必须是字符串或者dict数组")

    def _calculate_delay(self, attempt: int, base_delay: float = 1) -> float:
        """计算重试延迟时间（指数退避）"""
        return min(base_delay * (2 ** (attempt - 1)), 60)  # 最大延迟60秒

    def chat(self, prompt: Union[str, List[Dict[str, str]], Dict[str, str]],
             temperature: float = 0.8) -> Tuple[str, List[Dict[str, str]], object]:
        """
        发送聊天请求到 OpenAI API

        Args:
            prompt: 输入提示，可以是字符串、消息字典或消息字典列表
            temperature: 温度参数，控制输出的随机性

        Returns:
            包含响应文本、更新后的消息历史和原始响应对象的元组

        Raises:
            TypeError: 当 prompt 类型不正确时抛出
        """
        messages = self._prepare_messages(prompt)
        attempt = 0

        while True:
            try:
                if attempt > 0:
                    delay = self._calculate_delay(attempt)
                    self.logger.info(f"第 {attempt} 次重试，等待 {delay} 秒...")
                    time.sleep(delay)

                res = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                )
                text = res.choices[0].message.content.strip()

                if attempt > 0:
                    self.logger.info(f"第 {attempt} 次重试成功")

                return text, messages + [{"role": "assistant", "content": text}], res

            except openai.RateLimitError as e:
                attempt += 1
                if attempt > self.retry_num:
                    self.logger.error(f"在 {self.retry_num} 次重试后仍然失败")
                    raise
                self.logger.warning(f"遇到限速错误: {e}")
                continue

            except (openai.APIError, openai.APIConnectionError) as e:
                self.logger.error(f"遇到API错误: {e}")
                raise

            except Exception as e:
                self.logger.error(f"遇到未预期的错误: {e}", exc_info=True)
                raise

    def translate_en_cn(self, text: str, temperature: float = 0.3) -> Tuple[str, List[Dict[str, str]], object]:
        """
        将英文文本翻译为中文

        Args:
            text: 要翻译的英文文本
            temperature: 温度参数，控制翻译的随机性

        Returns:
            包含翻译后的文本、更新后的消息历史和原始响应对象的元组
        """
        messages = TRANSLATE_EN_CN + [{"role": "user", "content": text}]
        translated_text, updated_messages, res = self.chat(messages, temperature)
        return translated_text, updated_messages, res

    def merge_answers(self, origin_question: str, answers: list[str], temperature: float = 0.7) -> Tuple[
        str, List[Dict[str, str]], object]:

        messages = get_prompt_to_merge_answers(origin_question, answers)
        merged_text, updated_messages, res = self.chat(messages, temperature)
        return merged_text, updated_messages, res

    def comment_to_dialog(self, origin_question: str, origin_answer: str, comment: str, temperature: float = 0.7) -> Tuple[List[Dict[str, str]], List[Dict[str, str]], object]:
        """
        将评论转换为自然的问答对话。

        Args:
            origin_question: 原始用户提问
            origin_answer: 原始助手回答
            comment: 需要转换的评论
            temperature: 温度参数，控制输出的随机性

        Returns:
            包含生成的对话（列表格式的字典）、更新后的消息历史和原始响应对象的元组
        """
        # 使用 get_prompt_for_comment_to_dialog 构造消息
        messages = get_prompt_for_comment_to_dialog(origin_question, origin_answer, comment)

        # 调用 chat 方法生成对话
        dialog_text, updated_messages, res = self.chat(messages, temperature)

        # 删除 Markdown 标识 ```json 和 ```
        cleaned_text = dialog_text.replace("```json", "").replace("```", "").strip()

        # 尝试将文本转换为列表格式的字典
        try:
            dialog_dict = eval(cleaned_text)
            if not isinstance(dialog_dict, list):
                raise ValueError("The parsed content is not a list.")
        except (SyntaxError, ValueError):
            raise ValueError("The response could not be parsed into a list of dictionaries.")

        return dialog_dict, updated_messages, res

