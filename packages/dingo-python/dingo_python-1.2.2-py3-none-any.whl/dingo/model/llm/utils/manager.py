from dingo.config.config import DynamicLLMConfig
from dingo.model.llm.prompts.prompt import CONTEXT, IMAGE


def match_prompt(prompt_id):
    context_attributes = [attr for attr in dir(CONTEXT) if not attr.startswith('_')]
    image_attributes = [attr for attr in dir(IMAGE) if not attr.startswith('_')]
    total_attributes = context_attributes + image_attributes
    if prompt_id not in total_attributes:
        raise ValueError("You are trying to access an undefined prompt. Please use correct prompt via classic.py.")
    if prompt_id in context_attributes:
        return getattr(CONTEXT, prompt_id)
    else:
        return getattr(IMAGE, prompt_id)


def get_prompt(input_config: DynamicLLMConfig):
    if input_config.prompt is not None:
        return input_config.prompt
    if input_config.prompt_id is not None:
        return match_prompt(input_config.prompt_id)
    raise ValueError("Both prompt and prompt_id are not set.")
