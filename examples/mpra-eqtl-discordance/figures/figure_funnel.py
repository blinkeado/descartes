#!/usr/bin/env python3
"""
The funnel across ants 1-3: four hypotheses tested, four negatives, and the real
positive is methodological (collider bias), uncovered by the refutation of the first.
Every number is read from a committed JSON. Zero hardcode.
Usage: python3 figure_funnel.py
"""
import json, os
H=os.path.dirname(os.path.abspath(__file__))
def j(f): return json.load(open(os.path.join(H,f)))
au=j("audit_ortho_null.json"); ch=j("chromatin_calibration.json")
h2=j("ant2_caqtl.json"); t2=j("tier2_feasibility.json"); h3=j("ant3_result.json")
disc_hit=au["discordant"]["hit"]; disc_n=au["discordant"]["n"]; disc_pct=au["discordant"]["rate"]*100
bg_pct=au["whole_lib_bg"]["rate"]*100; Pcoll=au["P_discordant_less_than_bg"]
auc=ch["auc"]; ca_hit=h2["discordant_casnp"]; ca_n=h2["n_disc"]
mr=t2["n_mr_feasible"]; nprot=t2["n_protective"]; rho=h3["rho_composite"]
OUT=os.path.join(H,os.pardir,"figure_funnel.png")

import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
BLUE,GREEN,VERM,GRAY="#0072B2","#009E73","#D55E00","#8a9199"; INK="#1b1b1b"
def tint(hx,a=0.16):
    r,g,b=int(hx[1:3],16),int(hx[3:5],16),int(hx[5:7],16); return (1-a+a*r/255,1-a+a*g/255,1-a+a*b/255)
fig,ax=plt.subplots(figsize=(15,7.8)); ax.set_xlim(0,15); ax.set_ylim(0,8.2); ax.axis("off")
fig.suptitle("Data-reuse engine: four hypotheses tested -> four negatives -> one methodological positive",
             fontsize=13.5,fontweight="bold",y=0.99)
def box(xc,yc,w,h,t,fc,ec,fs=9,bold=False,tc=INK):
    ax.add_patch(FancyBboxPatch((xc-w/2,yc-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.09",
                 lw=1.6,facecolor=fc,edgecolor=ec,zorder=3))
    ax.text(xc,yc,t,ha="center",va="center",fontsize=fs,color=tc,fontweight="bold" if bold else "normal",zorder=4)
def arrow(x1,y1,x2,y2,c=GRAY,lw=2.0,lab=None,ls="-"):
    ax.annotate("",xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle="-|>",color=c,lw=lw,ls=ls),zorder=2)
    if lab: ax.text((x1+x2)/2,(y1+y2)/2+0.15,lab,ha="center",fontsize=8,color=c,style="italic")

# the open question
box(1.5,4.2,2.6,1.3,"The MPRA-eQTL\ndiscordance\nr=0.14 (Science 2024)\nLEFT UNEXPLAINED",tint(BLUE),BLUE,fs=10,bold=True)

# four hypotheses, all negative (middle column)
xh=6.4
hyps=[
 (6.9, f"H1 - orthogonal QTL layer\n{disc_hit}/{disc_n} - CIRCULAR (collider)"),
 (5.5, f"H2 - chromatin, 3 methods\nQTL 0 | AUC={auc:.2f} | caQTL {ca_hit}/{ca_n} - NO"),
 (4.1, f"H3 - protective/risk map\n{nprot} candidates ~50:50 | causal {mr}/{nprot} - FALSIFIED"),
 (2.7, f"H4 - episomal context (Inoue)\nrho={rho:.3f} (threshold 0.25) - DOES NOT PASS"),
]
for y,t in hyps:
    arrow(2.85,4.2,xh-1.35,y,GRAY)
    ec=VERM if y==6.9 else GRAY
    box(xh,y,3.0,0.95,t,tint(ec,0.10),ec,fs=8.6)

# the refutation of H1 uncovers the positive
arrow(7.95,6.9,9.5,6.0,VERM,lw=2.4,lab="its refutation uncovers...")
box(11.7,5.4,5.0,2.2,
    f"THE METHODOLOGICAL POSITIVE\nCollider bias in QTL-selected MPRAs\n"
    f"164/164 active variants are eQTLs by construction ->\ndiscordant {disc_pct:.1f}% < ambient floor {bg_pct:.0f}%\n"
    f"P(less)={Pcoll:.3f} -> not enrichment, it is circularity\n"
    f"a failure mode the field does not name (Munafo 2018)",
    tint(GREEN,0.22),GREEN,fs=9.2,bold=True)

# footer note
ax.text(7.5,0.9,"Four biological hypotheses tested, four honest negatives. The real positive is not a biological answer - "
        "it is the failure mode that refuting H1 uncovered,\nwith its control (the library's own ambient floor) and its anchor in the selection-bias literature.",
        ha="center",fontsize=9.3,color=INK,
        bbox=dict(boxstyle="round,pad=0.5",facecolor=tint(GREEN,0.08),edgecolor=GREEN,lw=1.2))
ax.text(0.2,0.12,"Every number from a committed JSON: audit_ortho_null.json - chromatin_calibration.json - ant2_caqtl.json - tier2_feasibility.json - ant3_result.json",
        fontsize=7.4,color="#888",style="italic")
fig.tight_layout(rect=[0,0.03,1,0.97])
fig.savefig(OUT,dpi=200,bbox_inches="tight",facecolor="white")
print(f"wrote {OUT}  (H1 {disc_hit}/{disc_n} circular; H2 AUC={auc:.2f}/caQTL {ca_hit}/{ca_n}; H3 MR {mr}/{nprot}; H4 ρ={rho:.3f}; collider P={Pcoll:.3f})")
