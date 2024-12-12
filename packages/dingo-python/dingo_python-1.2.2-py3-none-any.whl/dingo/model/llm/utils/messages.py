import json

from dingo.config.config import DynamicLLMConfig

ROLE_LIST = ["system", "assistant", "user"]


class MessageComponent:
    """
    Base class representing basic properties of a message.
    """

    def __init__(self, role, content=None):
        self.role = role
        self.content = content or []

    def to_message(self):
        """
        Converts the message component into a dictionary suitable for API requests.
        """
        return {"role": self.role, "content": self.content}

    def add_content(self, content):
        """
        Adds a content item to the message component.
        """
        self.content.append(content)


class MessageBuilder:
    """
    Message builder used to assemble message components.
    """

    def __init__(self):
        self.config = None
        self.messages = []

    def add_message(self, message):
        """
        Adds a message component to the message builder.
        """
        self.messages.append(message.to_message())

    def build(self):
        """
        Builds the final list of messages in a format suitable for API requests.
        """
        return self.messages

    @staticmethod
    def load_config(file_path):
        """
        Loads a configuration file and sets internal configuration.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file {file_path} was not found.")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in {file_path}.")

    def set_config(self, dynamic_config: DynamicLLMConfig):
        """
        设置配置文件。
        """
        self.config = dynamic_config

    @staticmethod
    def resolve_placeholder(placeholder, contents):
        """
        Resolves a placeholder and retrieves the corresponding value from contents.
        Supports concatenation of placeholders, such as "text_1 + text_2".
        """
        if '+' in placeholder:
            placeholders = [p.strip() for p in placeholder.split('+')]
            return ' '.join(contents.get(p, '') for p in placeholders)
        else:
            return contents.get(placeholder, '')

    def fill_contents(self, contents):
        """
        Fills the message content according to the configuration file.
        """
        if not self.config:
            raise ValueError("Configuration is not set. Please use set_config first.")

        builder = MessageBuilder()

        for msg in self.config.prompt_variables:
            role = msg.get("role")
            if role not in ROLE_LIST:
                raise ValueError(f"Unsupported role type. Supported type: {ROLE_LIST}.")
            content = []  # 初始化每个角色的内容列表

            for content_spec in msg.get("content"):
                placeholder = content_spec.get("placeholder")

                if placeholder:
                    value = self.resolve_placeholder(placeholder, contents)

                    if content_spec.get("type") == "text":
                        content.append({"type": "text", "text": value})
                    elif content_spec.get("type") == "image_url":
                        content.append({"type": "image_url", "image_url": {"url": value}})
                else:
                    # 如果没有占位符或者占位符未在动态数据中找到，则直接使用配置文件中的内容
                    content.append(content_spec)

            message = MessageComponent(role, content)
            builder.add_message(message)

        self.messages = builder.messages


if __name__ == "__main__":
    # example
    try:
        builder = MessageBuilder()
        dynamic_config = DynamicLLMConfig(prompt_variables=[
            {
                "role": "system",
                "content": [
                    {"type": "text", "placeholder": "system_prompt"}
                ]
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "placeholder": "custom_prompt"},
                    {"type": "image_url", "placeholder": "data_1"},
                    {"type": "image_url", "placeholder": "data_2"}
                ]
            }
        ])
        builder.set_config(dynamic_config)

        contents = {
            "system_prompt": "Image Detector",
            "custom_prompt": "Describe the image please",
            "data_1": "https://example.com/image1.jpg",
            "data_2": "https://example.com/image2.jpg"
        }

        builder.fill_contents(contents)

        messages = builder.build()
        print(messages)
    except Exception as e:
        print(f"An error occurred: {e}")
