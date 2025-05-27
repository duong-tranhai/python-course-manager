from fastapi import APIRouter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_together import Together
from pydantic import BaseModel

from app.config import settings

router = APIRouter()

class ChatInput(BaseModel):
    message: str

llm = Together(
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    temperature=0.7,
    max_tokens=512,
    api_key=settings.together_api_key
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful support assistant."),
    ("human", "{input}")
])

chat_chain: Runnable = prompt | llm

@router.post("/chat-ai")
async def chat_with_bot(payload: ChatInput):
    output = chat_chain.invoke({"input": payload.message})
    return {"response": output}
