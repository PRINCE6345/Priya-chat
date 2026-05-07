import requests
from config import GF_NAME, GF_PERSONALITY

GEMINI_API = "https://livegemini.fastdevelopers.workers.dev/chat"


def get_gf_response(user_msg: str, history: list) -> str:
    history_text = "\n".join(history[-16:])

    full_prompt = f"""{GF_PERSONALITY}

Conversation history:
{history_text}

Ab sirf {GF_NAME} ki taraf se ek natural, short reply de. Koi prefix mat lagana jaise '{GF_NAME}:' — seedha reply likh."""

    try:
        res = requests.get(GEMINI_API, params={"message": full_prompt}, timeout=15)
        data = res.json()
        if data.get("status"):
            reply = data["response"].strip()
            # Remove any AI prefix if model adds it
            for prefix in [f"{GF_NAME}:", "Priya:", "AI:", "Bot:"]:
                if reply.startswith(prefix):
                    reply = reply[len(prefix):].strip()
            return reply
    except Exception:
        pass

    # Fallback replies if API fails
    fallbacks = [
        "Jaan abhi thoda busy hoon, baad mein baat karte hain? 🥺",
        "Ek second... kuch ho gaya 😅 dobara likh na",
        "Arey yaar connection problem ho gaya, phir bolo 💕",
    ]
    import random
    return random.choice(fallbacks)
