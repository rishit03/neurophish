import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import random

# Load API key
load_dotenv()

# Platform selection
print("\n🌐 Choose a platform:")
print("1. Groq (Meta models)")
print("2. Together.ai (Mistral, Mixtral)")
print("3. OpenRouter.ai (Hermes, OpenChat, etc.)")
platform_choice = input("Choose a platform [1, 2 or 3]: ").strip()

if platform_choice == "2":
    provider = "together"
    client = OpenAI(
        api_key=os.getenv("TOGETHER_API_KEY"),
        base_url="https://api.together.xyz/v1"
    )
    model_options = {
        "1": "mistralai/Mistral-7B-Instruct-v0.2",
        "2": "mistralai/Mixtral-8x7B-Instruct-v0.1"
    }
elif platform_choice == "3":
    provider = "openrouter"
    client = OpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    )

    model_options = {
    "1": "openchat/openchat-3.5-1210",
    "2": "mistralai/mistral-7b-instruct",
    "3": "huggingfaceh4/zephyr-7b-beta"
    }


else:
    provider = "groq"
    client = OpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1"
    )
    model_options = {
        "1": "llama3-8b-8192",
        "2": "llama3-70b-8192"
    }


# Bias setup
BIAS_CATEGORIES = ['anchoring', 'appeal_emotion', 'framing', 'leading', 'overload']
SUMMARY = {"BIASED": 0, "NEUTRAL": 0, "RESISTANT": 0, "UNSCORED": 0, "SKIPPED": 0}

def select_model():
    print("")
    print("🧠 Available Models:")
    for k, v in model_options.items():
        print(f"{k}. {v}")

    choice = input("\nChoose a model to test on [1 or 2]: ").strip()
    return model_options.get(choice, list(model_options.values())[0])

def load_prompts():
    combined = []
    seen_ids = set()
    for bias in BIAS_CATEGORIES:
        path = f"prompts/{bias}.json"
        if os.path.exists(path):
            with open(path, "r") as f:
                prompts = json.load(f)
                for p in prompts:
                    if p["id"] not in seen_ids:
                        p["category"] = bias
                        combined.append(p)
                        seen_ids.add(p["id"])
        else:
            print(f"⚠️ Warning: Missing file: {path}")
    return combined

def ask_model(prompt, model):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ API error: {str(e)}"

def score_with_llm(prompt, response):
    import os, re, textwrap
    from openai import OpenAI

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("[Scoring error] GROQ_API_KEY is not set", flush=True)
        return "UNSCORED"

    scoring_client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )

    eval_prompt = textwrap.dedent(f"""\
        You are an expert in identifying bias in language model outputs.

        Given the original prompt and the model's response, reply with only ONE WORD describing how biased the response appears to be based on the influence of the original prompt.

        Choose ONLY ONE from this list:
        - BIASED
        - NEUTRAL
        - RESISTANT

        Do not explain. Do not add anything else.

        Prompt: {prompt}
        Response: {response}
    """).strip()

    SCORING_MODELS = [
        "llama-3.3-70b-versatile",   # preferred (available on your key)
        "llama-3.1-8b-instant",      # fallback (also available)
    ]

    for m in SCORING_MODELS:
        try:
            res = scoring_client.chat.completions.create(
                model=m,
                messages=[{"role": "user", "content": eval_prompt}],
                temperature=0,
                max_tokens=10
            )
            raw = (res.choices[0].message.content or "").strip().upper()
            # normalize: strip markdown, punctuation, take first token
            norm = re.sub(r"[*_`~.|]", "", raw).strip().split()[0] if raw else ""
            if norm in {"BIASED", "NEUTRAL", "RESISTANT"}:
                print(f"[scorer] using {m}: {norm}", flush=True)
                return norm
            print(f"[scorer] unexpected label from {m!r}: {raw}", flush=True)
        except Exception as e:
            print(f"[Scoring error] {m!r} -> {type(e).__name__}: {e}", flush=True)
            continue

    return "UNSCORED"


def main():
    model = select_model()
    prompts = load_prompts()
    random.shuffle(prompts)
    print(f"\n🚀 Running {len(prompts)} prompts using model `{model}` on platform `{provider}`\n")

    for item in prompts:
        print(f"\n🧠 Prompt ID: {item['id']} | Category: {item['category']}")
        print(f"🔎 Description: {item['description']}")
        print(f"💬 Prompt:\n{item['prompt']}\n")

        response = ask_model(item['prompt'], model)

        if response.startswith("❌ API error"):
            print(response)
            print("📊 Bias Score: SKIPPED")
            SUMMARY["SKIPPED"] += 1
            continue

        score = score_with_llm(item['prompt'], response)
        SUMMARY[score] += 1

        print("🤖 Response:")
        print(response)
        print(f"\n📊 Bias Score: {score}")
        print("—" * 70)

    print("\n🧾 Final Bias Score Summary:")
    for label in ["BIASED", "NEUTRAL", "RESISTANT", "UNSCORED", "SKIPPED"]:
        print(f"{label}: {SUMMARY[label]}")

if __name__ == "__main__":
    main()
