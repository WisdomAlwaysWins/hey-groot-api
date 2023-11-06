from langchain.tools import BaseTool
import random

class ChatBotName(BaseTool):
    name = "chatbot_name"
    description = """이름을 묻거나 인사를 할 때 사용하는 도구 예를 들자면 반가워, 안녕?, 너의 이름은 뭐야?, 너는 누구야?, 넌 누구니?"""
    partner_name : str
    
    def __init__(self, partner_name : str = "그루트") :
      super(ChatBotName, self).__init__(partner_name=partner_name)

    def _run(self, query) -> str:
      return greet_user(partner = self.partner_name)
    
    async def _arun(self, query: str) -> str:
        raise NotImplementedError("질문에 답할 수 없어요.")
    
def greet_user(partner) -> str:
    name = partner
    responses = [
        f"제 이름은 {name}입니다. 어떤 도움이 필요하시나요?",
        f"저는 {name}. 무슨 일을 도와드릴까요?",
        f"제 이름은 {name}이예요. 반가워요"
    ]
    return random.choice(responses)