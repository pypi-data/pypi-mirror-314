import torch
from transformers import NllbTokenizer, M2M100ForConditionalGeneration

def translate_text(text, source_language, target_language):
    """
    Translates text from a source language to a target language using Sunbird's NLLB model.

    Args:
        text (str): The text to be translated.
        source_language (str): The source language code (e.g., 'eng').
        target_language (str): The target language code (e.g., 'lug').

    Returns:
        str: The translated text.
    """
    tokenizer = NllbTokenizer.from_pretrained('Sunbird/translate-nllb-1.3b-salt')
    model = M2M100ForConditionalGeneration.from_pretrained('Sunbird/translate-nllb-1.3b-salt')

    language_tokens = {
        'eng': 256047,
        'ach': 256111,
        'lgg': 256008,
        'lug': 256110,
        'nyn': 256002,
        'teo': 256006,
    }

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    inputs = tokenizer(text, return_tensors="pt").to(device)
    inputs['input_ids'][0][0] = language_tokens[source_language]
    translated_tokens = model.to(device).generate(
        **inputs,
        forced_bos_token_id=language_tokens[target_language],
        max_length=100,
        num_beams=5,
    )
    return tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
