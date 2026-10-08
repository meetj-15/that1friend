import torch
import torch.nn.functional as F

def scaled_dot_product_attention(q : torch.Tensor, k: torch.Tensor, v: torch.Tensor)->torch.Tensor:
    d_k=q.size(-1)
    scores=q@k.transpose(-2, -1) / (d_k**0.5)
    weights=F.softmax(scores, dim=1)
    return weights@v

if __name__=="__main__":
    torch.manual_seed(7)
    q=torch.randn(1,4,8)
    k=torch.randn(1,4,8)
    v=torch.randn(1,4,8)
    out=scaled_dot_product_attention(q,k,v)
    print("shape: ", out.shape)