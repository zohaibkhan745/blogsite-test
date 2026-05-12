from groq import Groq
from django.conf import settings


def generate_summary(text):
    """
    Send post content (REQUEST) to Groq's LLM and return a 2-3 sentence summary (RESPONSE).

    Parameters:
        text (str): The full content of the blog post.

    Returns:
        str: AI-generated summary, or an error message if the call fails.
    """
    try:
        # Step 1: Create an authenticated Groq client
        # The API key comes from blogsite/settings.py — never hardcoded here due to security
        client = Groq(api_key=settings.GROQ_API_KEY)

        # Step 2: Send the post content to the LLM with a clear instruction
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL, # 'llama3-8b-8192' from settings, you can change it
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Summarize the following blog post:\n\n"
                        f"Post content:\n{text}"
                    )
                }
            ],
            max_tokens=200,    # 1 token is 0.75 words approx so ~150 words maximum — enough for 2-3 sentences
            # What about large or small token size?
            temperature=0.4,   # Can vary between 0-1, balanced: consistent output, natural language
            # 0 mean deterministic while 1 means highly creative but might be chaotic
        )

        # Step 3: Extract the generated text from the response
        # The response is an object — the text is nested inside it
        summary = response.choices[0].message.content
        return summary

    except Exception as e:
        # If anything goes wrong (bad key, network, quota exhausted), return a safe message instead of crashing the page with a 500 error
        return f"Sorry! Summary could not be generated at this time. ({str(e)})"