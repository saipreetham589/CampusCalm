from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from updated_trag_ch import IntegratedMentalHealthBot

app = FastAPI()
bot = IntegratedMentalHealthBot()

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify your frontend's URL here
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/text-chat")
async def text_chat(req: Request):
    data = await req.json()
    user_input = data.get("message", "")
   
    response = bot.process_user_input(user_input)

    return { "response": response }