import openai

# Set your OpenAI API key here
api_key = "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"

def generate_response(user_input):
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="davinci",
        prompt=user_input,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text
