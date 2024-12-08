import sys
sys.path.append("src")

import pytest
from transformers import AutoTokenizer
from owlsight.processors.text_generation_processors import TextGenerationProcessorGGUF


@pytest.fixture
def setup_gguf_processor():
    """Fixture to set up the GGUF processor and tokenizer."""
    model_id = "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF"
    gguf_filename = "tinyllama-1.1b-chat-v1.0.Q2_K.gguf"
    tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
    processor = TextGenerationProcessorGGUF(model_id, gguf__filename=gguf_filename)
    return processor, tokenizer


def test_gguf_generate_response(setup_gguf_processor):
    """Test that the GGUF processor generates a valid response."""
    processor, _ = setup_gguf_processor
    prompt = "test prompt"
    max_new_tokens = 128

    response = processor.generate(prompt, max_new_tokens=max_new_tokens)
    assert isinstance(response, str), "Generated response should be a string."


def test_gguf_token_count_within_tolerance(setup_gguf_processor):
    """Test that the GGUF generated token count is within the acceptable range."""
    processor, tokenizer = setup_gguf_processor
    prompt = "test prompt"
    max_new_tokens = 128
    tolerance_fraction = 0.5

    response = processor.generate(prompt, max_new_tokens=max_new_tokens)

    # Tokenize response and calculate new tokens
    response_tokens = tokenizer.tokenize(response)
    prompt_tokens = tokenizer.tokenize(prompt)
    new_tokens = response_tokens[len(prompt_tokens):]

    # Calculate acceptable range
    lower_bound = max_new_tokens - (max_new_tokens * tolerance_fraction)
    upper_bound = max_new_tokens + (max_new_tokens * tolerance_fraction)

    assert lower_bound <= len(new_tokens) <= upper_bound, (
        f"Expected approximately {max_new_tokens} tokens "
        f"(range: {lower_bound:.2f} - {upper_bound:.2f}), got {len(new_tokens)}"
    )


def test_gguf_prompt_tokens_exclusion(setup_gguf_processor):
    """Test that the GGUF response excludes prompt tokens when counting new tokens."""
    processor, tokenizer = setup_gguf_processor
    prompt = "test prompt"
    max_new_tokens = 128

    response = processor.generate(prompt, max_new_tokens=max_new_tokens)

    # Tokenize response and calculate new tokens
    response_tokens = tokenizer.tokenize(response)
    prompt_tokens = tokenizer.tokenize(prompt)

    assert len(response_tokens) > len(prompt_tokens), "Response tokens should exceed prompt tokens."


if __name__ == "__main__":
    pytest.main([__file__])
