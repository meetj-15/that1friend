# LLM notes

## Tokenization
It is the process of breaking down text, into smaller text or units so that a NLP model can process it.

## Embeddings
Token ID is just an integer, we require a meaningful numerical representation, embedding converts a token into a vector of numbers.

## Self-Attention
Self attention is the process in which each token looks at other tokens in the sequence and decide which ones are important (eg: Raman is a boy. He is dead. He->Raman)
For each token:
q=what info am i looking for
k=what info do i contain
v=what info should I provide
Attention(q,k,v)=Softmax((q*k^t)/root(dk))*v

## Residual Connections
Og input is added back to the o/p of the layer. Learn new things but do not forget old learnings.

## Layer Normalization
Normalize karta hai, so that too small, too large values are roughly normalized. Gives stable training faster
convergence.

## Causal Masking
While predicting next tokens, do not see the future (Dr. Strange type shi)

## Logits
A vector of numbers that presents the likelihood of every possible next token. From logits, do softmax P_i=(e^z_i)/(sigma_j(e^z_j))
where z is the logits

## Sampling
Perform sampling; various techniques; top k, temperature, greedy, top p

## Autoregressive Generation
Process in which model generates one token at a time, using previously generated tokens to predict the next token