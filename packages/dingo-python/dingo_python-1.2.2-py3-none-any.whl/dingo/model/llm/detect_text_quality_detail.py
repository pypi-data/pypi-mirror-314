import json

from dingo.model import Model
from dingo.model.llm.common.BaseOpenAI import BaseOpenAI
from dingo.model.modelres import ModelRes
from dingo.utils import log


@Model.llm_register('detect_text_quality_detail')
class DetectTextQualityDetail(BaseOpenAI):
    @classmethod
    def process_response(cls, response: str) -> ModelRes:
        log.info(response)

        if response.startswith('```json'):
            response = response[7:]
        if response.startswith('```'):
            response = response[3:]
        if response.endswith('```'):
            response = response[:-3]
        try:
            response_json = json.loads(response)
        except:
            raise Exception(f'Convert to JSON format failed: {response}')

        result = ModelRes()
        # error_status
        if response_json.get("score") == 1:
            result.reason = [response_json.get("reason", "")]
        else:
            result.error_status = True
            result.type = response_json.get("type", 'Type')
            result.name = response_json.get("name", "Name")
            result.reason = [response_json.get("reason", "")]

        return result
