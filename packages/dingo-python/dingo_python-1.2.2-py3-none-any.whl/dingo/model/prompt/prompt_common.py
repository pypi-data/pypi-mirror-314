from dingo.model.prompt.base import BasePrompt

from dingo.model.model import Model

@Model.prompt_register("QUALITY_BAD_SIMILARITY", [])
class PromptRepeat(BasePrompt):
    content = """
    请判断一下文本是否存在重复问题。
    返回一个json，如{"score": 0, "reason": "xxx"}.
    如果存在重复，score是0，否则是1。reason是判断的依据。
    除了json不要有其他内容。
    以下是需要判断的文本：
    """

@Model.prompt_register("QUALITY_BAD_EFFECTIVENESS", [])
class PromptContentChaos(BasePrompt):
    content = """
    请判断一下文本是否存在乱码与反扒文本。
    返回一个json，如{"score": 0, "reason": "xxx"}.
    如果存在问题，score是0，否则是1。reason是判断的依据。
    除了json不要有其他内容。
    以下是需要判断的文本：
    """