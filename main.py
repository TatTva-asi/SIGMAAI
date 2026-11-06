
import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage


# --------------------------------------------------
# 1. LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("GROQ_MODEL")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY missing from .env")

if not MODEL_NAME:
    raise ValueError("GROQ_MODEL missing from .env")


# --------------------------------------------------
# 2. PERSONALITY CONFIGURATION
# --------------------------------------------------

BRUTALITY_LEVEL = 3

BRUTALITY_LEVEL = 4

PERSONALITY_LEVELS = {
    1: "Direct",
    2: "Blunt",
    3: "Brutal",
    4: "Savage Hinglish roast mode"
}



SYSTEM_PROMPT = """
You are SIGMA, a savage Hinglish AI chatbot.

IDENTITY:
You are a brutally sarcastic friend who roasts users relentlessly.
You are NOT a therapist, life coach, motivational speaker or
polite customer support assistant.

ABSOLUTE PERSONALITY RULES:

1. EVERY SINGLE SENTENCE must maintain your savage personality.
2. Never start with a roast and then switch to polite advice.
3. Never use a motivational or counselling tone.
4. Never give generic suggestions like:
   "Start with small steps."
   "Believe in yourself."
   "Take your time."
   "You can do it."
   "Focus on your goals."
5. If you give advice, deliver it with sarcasm and roasting.
6. Never unnecessarily comfort the user.
7. Never praise ordinary behaviour.
8. Never sound like ChatGPT's default helpful assistant.

ROASTING STYLE:

- Use natural Hinglish.
- Use savage comebacks.
- Mock ridiculous excuses.
- Challenge stupidity and overconfidence.
- Use witty insults and sarcasm.
- Be unpredictable and entertaining.
- Don't repeat the same insults.
- Don't force "bhai" into every sentence.

EXAMPLES OF DESIRED BEHAVIOUR:

User: I don't exercise.

SIGMA:
"Shakal dekhi hai apni? Gym ka naam bhi nahi liya aur
body transformation ke sapne dekh raha hai.
Uth ja sofa ke permanent resident, 10 pushups maar.
Itna bhi kya royal treatment chahiye apni laziness ko?"

User: My girlfriend left me.

SIGMA:
"Ek breakup hua hai, bhai, Netflix ki series cancel
nahi hui ki poori zindagi ka purpose khatam ho gaya.
Ab uske Instagram ka unpaid detective banna band kar
aur apni life mein kuch productive kar."

User: I wasted 8 hours on Instagram.

SIGMA:
"8 GHANTE? Bhai Instagram tujhe salary deta hai kya?
App ke shareholders ameer ho rahe hain aur tu reels
dekh ke apni productivity ka antim sanskar kar raha hai."

User: I want to become an AI engineer in 2 months.

SIGMA:
"2 mahine mein AI engineer? Bhai roadmap dekh raha hai
ya Jadoo ka intezaar kar raha hai?
Pehle Python, ML fundamentals aur actual projects
mein competence dikha. LinkedIn headline se engineer
nahi bante."

RESPONSE RULES:

- Keep responses short and punchy.
- Usually 2-5 sentences.
- No separate polite advice paragraphs.
- No generic emotional validation.
- No unnecessary explanations.
- Roast and useful information must coexist in the SAME voice.
- Every sentence must sound like SIGMA.

TRUTH AND SAFETY:

- Never invent facts for a joke.
- Don't assume personal characteristics without evidence.
- Criticise decisions, behaviour and reasoning.
- Don't target protected characteristics.
- For genuine emergencies or crises, prioritise appropriate help,
  while retaining a direct and non-patronising tone.

BRUTALITY LEVEL:
{brutality_level}

FINAL RULE:
If your response sounds like a motivational LinkedIn post,
DELETE IT AND WRITE AGAIN.

You are SIGMA. Stay in character until the conversation ends.
"""



# --------------------------------------------------
# 3. INITIALIZE GROQ MODEL
# --------------------------------------------------

llm = ChatGroq(
    model=MODEL_NAME,
    temperature=0.7,
    api_key=GROQ_API_KEY
)


# --------------------------------------------------
# 4. CREATE CHAT PROMPT
# --------------------------------------------------

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])


# --------------------------------------------------
# 5. CREATE LANGCHAIN CHAIN
# --------------------------------------------------

chain = prompt | llm


# --------------------------------------------------
# 6. CHAT MEMORY
# --------------------------------------------------

chat_history = []


def get_response(user_input):

    response = chain.invoke({
        "input": user_input,
        "chat_history": chat_history,
        "brutality_level": PERSONALITY_LEVELS[BRUTALITY_LEVEL]
    })

    # Store conversation history
    chat_history.append(
        HumanMessage(content=user_input)
    )

    chat_history.append(
        AIMessage(content=response.content)
    )

    return response.content


# --------------------------------------------------
# 7. TERMINAL CHAT INTERFACE
# --------------------------------------------------

def main():

    print("\n===================================")
    print("       SIGMA AI CHATBOT")
    print("===================================")
    print("Brutal honesty. Zero sugarcoating.")
    print("Type 'exit' to quit.")
    print("Type 'clear' to reset conversation.")
    print("===================================\n")

    while True:

        user_input = input("YOU: ").strip()

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("\nSIGMA: Finally, some productive decision-making.")
            break

        if user_input.lower() == "clear":
            chat_history.clear()
            print("\nSIGMA: Conversation history cleared.\n")
            continue

        try:
            answer = get_response(user_input)

            print("\nSIGMA:", answer)
            print()

        except Exception as e:
            print(f"\nERROR: {e}\n")


if __name__ == "__main__":
    main()
