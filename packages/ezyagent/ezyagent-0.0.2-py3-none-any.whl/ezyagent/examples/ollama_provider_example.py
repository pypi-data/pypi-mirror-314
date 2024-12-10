async with OllamaProvider() as provider:
    response = await provider.chat(
        messages=[Message(role="user", content="Why is the sky blue?")],
        model_config=ModelConfig(model_name="llama2")
    )
    print(response.content)