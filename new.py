import re
n0=input()
n1=input()
def encode(n):
    k=re.split(r'([.,!?]|--|\s)',n)
    k=[i.strip() for i in k if i.strip()]
    return k
def decode(k):
    t1=" ".join(i for i in k)
    t1=re.sub(r'\s+([.,?!])',r'\1',t1)
    return t1
k=encode(n0)
p=set(k)
d={i:j for i, j in enumerate(p)}
d[len(d)]="<|unk|>"
d[len(d)]="<|endoftext|>"
print(d)
res_d={item:id for id,item in d.items()}
k2=encode(n1)
va=[res_d.get(i,'<|unk|>') for  i in k2]
id=[d.get(i,'<|unk|>') for i in va]
print(va)
print(decode(id))