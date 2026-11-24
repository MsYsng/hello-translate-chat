"""Print a decorative, QR-like pattern (SVG rects) for the quick start illustration. Not a real QR code."""
import random
random.seed(7)
N=21
def finder(r,c):
    for (R,C) in [(0,0),(0,N-7),(N-7,0)]:
        if R<=r<R+7 and C<=c<C+7:
            rr,cc=r-R,c-C
            return rr in(0,6) or cc in(0,6) or (2<=rr<=4 and 2<=cc<=4)
    return None
def qr(x,y,size):
    s=size/N; out=[]
    for r in range(N):
        for c in range(N):
            f=finder(r,c)
            if f is None:
                if (r in(7,) and c<8) or (c==7 and r<8) or (r==7 and c>=N-8) or (c==N-8 and r<8) or (r==N-8 and c<8) or (c==7 and r>=N-8): f=False
                else: f=random.random()<0.48
            if f: out.append(f'<rect x="{x+c*s:.1f}" y="{y+r*s:.1f}" width="{s+.3:.1f}" height="{s+.3:.1f}"/>')
    return "".join(out)
print(qr(0,0,100))
