from openai import OpenAI

client = OpenAI(
	base_url="https://api-inference.huggingface.co/v1/",
	api_key="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"
)

messages = [
	{ "role": "user", "content": "Tell me a story" }
]

stream = client.chat.completions.create(
    model="Qwen/Qwen2.5-72B-Instruct", 
	messages=messages, 
	temperature=0.5,
	max_tokens=2048,
	top_p=0.7,
	stream=True
)

for chunk in stream:
    print(chunk.choices[0].delta.content,flush=True)