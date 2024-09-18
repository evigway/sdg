from transformers import GPTNeoForCausalLM, GPT2Tokenizer
import torch

# Load pre-trained model and tokenizer
model_name = 'EleutherAI/gpt-neo-1.3B'  # You can choose other variants like 'EleutherAI/gpt-neo-2.7B'
model = GPTNeoForCausalLM.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

def generate_similar_sentences(sentence, max_length=50, num_return_sequences=20):
    # Tokenize the input prompt
    inputs = tokenizer(sentence, return_tensors='pt', padding=True, truncation=True)

    # Generate text
    with torch.no_grad():
        outputs = model.generate(
            inputs['input_ids'],
            attention_mask=inputs['attention_mask'],
            max_length=len(inputs['input_ids'][0]) + 20,
            num_return_sequences=num_return_sequences,
            temperature=0.7,  # Controls the randomness of the output
            top_k=50,         # Limits the sampling pool to the top k tokens
            top_p=0.95,       # Nucleus sampling: limits the sampling pool to tokens with cumulative probability of top_p
            do_sample=True,
            no_repeat_ngram_size=2  # Prevents repeating the same n-grams
        )

    # Decode and return the generated texts
    sentences = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
    return sentences

# Example prompt
sentence = "Reformat this sentence - Realistic Army tanks from first person view in a marshy terrain faraway"
similar_sentences = generate_similar_sentences(sentence)

for i, p in enumerate(similar_sentences):
    print(f"Sentence {i+1}: {p}")
