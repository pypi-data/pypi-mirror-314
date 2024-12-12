import json
import time

from dingo.config.config import DynamicLLMConfig
from dingo.io import MetaData
from dingo.model.llm.base import BaseLLM
from dingo.model.modelres import ModelRes
from dingo.model.prompt.base import BasePrompt
from dingo.utils import log


class BaseTransformerClient(BaseLLM):
    model = None
    tokenizer = None

    dynamic_config = DynamicLLMConfig()

    @classmethod
    def set_prompt(cls, prompt: BasePrompt):
        cls.prompt = prompt

    @classmethod
    def generate_words(cls, input_data: str) -> json:
        from transformers import AutoModelForCausalLM, AutoTokenizer

        try:
            import torch
        except ImportError as e:
            log.warning("=========== llama3 register fail. Please check whether install torch. ===========")

        if cls.model is None:
            cls.model = AutoModelForCausalLM.from_pretrained(
                cls.dynamic_config.path,
                torch_dtype=torch.bfloat16,
                device_map="auto",
            )
        if cls.tokenizer is None:
            cls.tokenizer = AutoTokenizer.from_pretrained(cls.dynamic_config.path)

        messages = [
            {"role": "system", "content": input_data},
        ]

        input_ids = cls.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            return_tensors="pt"
        ).to(cls.model.device)

        terminators = [
            cls.tokenizer.eos_token_id,
            cls.tokenizer.convert_tokens_to_ids("<|eot_id|>")
        ]

        outputs = cls.model.generate(
            input_ids,
            max_new_tokens=256,
            eos_token_id=terminators,
            do_sample=True,
            temperature=0.6,
            top_p=0.9,
        )
        response = outputs[0][input_ids.shape[-1]:]
        return json.loads(cls.tokenizer.decode(response, skip_special_tokens=True))

    @classmethod
    def call_api(cls, input_data: MetaData) -> ModelRes:

        if not cls.dynamic_config.path:
            raise ValueError("path cannot be empty in llm config.")

        attempts = 0
        except_msg = ''
        while attempts < 3:
            try:
                response = cls.generate_words(cls.prompt.content % input_data.content)

                return ModelRes(
                    error_status=True if response['score'] == 0 else False,
                    type=response['type'],
                    name=response.get('name', 'DATA'),
                    reason=[response]
                )
            except Exception as e:
                attempts += 1
                time.sleep(1)
                except_msg = str(e)

        return ModelRes(
            error_status=True,
            type='QUALITY_BAD',
            name="API_LOSS",
            reason=[except_msg]
        )
