import math
import torch
import torch.nn as nn
import torch.nn.functional as F

class CausalSelfAttention(nn.Module):
    def __init__(self, d_model: int, n_heads: int, max_seq_len: int)->None:
        super().__init__()
        assert d_model % n_heads == 0
        self.n_heads=n_heads
        self.head_dim=d_model // n_heads
        self.qkv=nn.Linear(d_model, 3*d_model)
        self.out=nn.Linear(d_model, d_model)
        mask=torch.tril(torch.ones(max_seq_len, max_seq_len))
        self.register_buffer("mask", mask.view(1,1, max_seq_len, max_seq_len))

    def forward(self, x:torch.Tensor)->torch.Tensor:
        b,t,c=x.shape
        qkv=self.qkv(x)
        q,k,v=qkv.chunk(3, dim=-1)
        q=q.view(b,t,self.n_heads, self.head_dim).transpose(1,2)
        k=k.view(b,t,self.n_heads, self.head_dim).transpose(1,2)
        v=v.view(b,t,self.n_heads, self.head_dim).transpose(1,2)
        att=(q@k.transpose(-2, -1))/math.sqrt(self.head_dim)
        att=att.masked_fill(self.mask[:,:,:t,:t]==0, float("-inf"))
        att=F.softmax(att, dim=-1)
        y=att@v
        y=y.transpose(1,2).contiguous().view(b,t,c)
        return self.out(y)

class Block(nn.Module):
    def __init__(self, d_model: int, n_heads: int, max_seq_len: int)->None:
            super().__init__()
            self.ln1=nn.LayerNorm(d_model)
            self.attn=CausalSelfAttention(d_model, n_heads, max_seq_len)
            self.ln2=nn.LayerNorm(d_model)
            self.ff=nn.Sequential(
                nn.Linear(d_model, 4*d_model), 
                nn.GELU(),
                nn.Linear(4*d_model,d_model),
            )
    def forward(self, x:torch.Tensor)->torch.Tensor:
        x=x+self.attn(self.ln1(x))
        x=x+self.ff(self.ln2(x))
        return x

class TinyGPT(nn.Module):
    def __init__(self, vocab_size:int, max_seq_len: int=64, d_model: int=64, n_heads: int=4, n_layers: int=2)->None:
        super().__init__()
        self.token_emb=nn.Embedding(vocab_size, d_model)
        self.pos_emb=nn.Embedding(max_seq_len, d_model)
        self.blocks=nn.ModuleList([Block(d_model, n_heads, max_seq_len) for _ in range(n_layers)])
        self.ln=nn.LayerNorm(d_model)
        self.head=nn.Linear(d_model, vocab_size, bias=False)

    def forward(self, ids: torch.Tensor, targets: torch.Tensor | None=None):
        b,t=ids.shape
        pos=torch.arange(t, device=ids.device)
        x=self.token_emb(ids)+self.pos_emb(pos)[None, :, :]
        for block in self.blocks:
            x=block(x)
        logits=self.head(self.ln(x))
        loss=None
        if targets is not None:
            loss=F.cross_entropy(logits.view(-1, logits.size(-1)), targets.view(-1))
        return logits, loss

if __name__=="__main__":
    torch.manual_seed(0)
    model=TinyGPT(vocab_size=32)
    x=torch.randint(0, 32, (2, 16))
    y=torch.randint(0, 32, (2, 16))
    logits, loss=model(x,y)
    print("logits: ", logits.shape)
    print("Loss: ", loss.item()) #Use this instead of float(loss), cuz loss is a tensor, so backpropagation hota hai, so scalar tensor k liye .item() is best
