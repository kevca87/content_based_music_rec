def sentences_to_embedding_matrix(sentences, tokenizer=tokenizer):
    # Tokenize the sentence and convert to input IDs
    inputs = tokenizer(sentences, return_tensors="pt", padding=True, truncation=True, max_length=128)
    inputs = {k: v.to("cuda") for k, v in inputs.items()}
    # Pass inputs through the model to get hidden states
    with torch.no_grad():
        outputs = model(**inputs)
    # Extract embeddings from the last hidden state
    # Use the [CLS] token representation for each sentence
    cls_embeddings = outputs.last_hidden_state[:, 0, :]
    # Convert to numpy for easier handling, if needed
    embedding_matrix = cls_embeddings.numpy() 
    return embedding_matrix

def sentence_to_embedding(sentence, tokenizer=tokenizer):
    # Tokenize the sentence and convert to input IDs
    inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True, max_length=128)
    # Pass inputs through the model to get hidden states
    with torch.no_grad():
        outputs = model(**inputs)
    # Extract the embeddings
    # Take the output from the last hidden layer
    last_hidden_states = outputs.last_hidden_state
    # To get a single embedding for the sentence, you can use the [CLS] token's embedding
    sentence_embedding = last_hidden_states[:, 0, :].squeeze()
    return sentence_embedding