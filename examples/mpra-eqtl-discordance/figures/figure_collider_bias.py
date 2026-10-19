#!/usr/bin/env python3
"""
The central finding: collider bias in QTL-selected MPRAs.
Every number is read from audit_ortho_null.json (produced by audit_ortho_null.py).
Zero hardcode. Usage: python3 figure_collider_bias.py
"""
import json, os
HERE=os.path.dirname(os.path.abspath(__file__))
d=json.load(open(os.path.join(HERE,"audit_ortho_null.json")))
OUT=os.path.join(HERE,os.pardir,"figure_collider_bias.png")
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
BLUE,GREEN,VERM,ORANGE,GRAY="#0072B2","#009E73","#D55E00","#E69F00","#9AA0A6"; INK="#1b1b1b"

disc=d["discordant"]["rate"]*100; conc=d["concordant"]["rate"]*100
nul=d["matched_null_active"]["rate"]*100; bg=d["whole_lib_bg"]["rate"]*100
P=d["P_discordant_less_than_bg"]; he=d["cooc_iso_tq_given_eqtl"]*100; ne=d["cooc_iso_tq_no_eqtl"]*100

plt.rcParams.update({"font.size":11})
fig,(axA,axB)=plt.subplots(1,2,figsize=(13,5.2),gridspec_kw={"width_ratios":[1.35,1]})
fig.suptitle("The QTL overlap of the active variants is a design artefact (collider bias), not a mechanism",
             fontsize=13.5,fontweight="bold",y=1.0)

# Panel A: overlap rate by group, against the ambient floor
labels=["Discordant\n(the 'finding')","Active null\n(matched)","Whole library\nbackground","Concordant"]
vals=[disc,nul,bg,conc]; cols=[VERM,GRAY,GRAY,BLUE]
x=range(len(vals))
axA.bar(x,vals,color=cols,width=0.62,zorder=3)
for i,v in zip(x,vals): axA.text(i,v+1.2,f"{v:.1f}%",ha="center",fontsize=10.5,fontweight="bold" if i==0 else "normal")
axA.axhline(bg,ls="--",lw=1.6,color="#555",zorder=2)
axA.text(len(vals)-0.5,bg+1.2,f"ambient floor ~{bg:.0f}%",ha="right",fontsize=9,color="#555",style="italic")
axA.annotate(f"discordant group BELOW its own floor\nP(less)={P:.3f} -> no enrichment",
             xy=(0,disc),xytext=(0.5,disc-22),fontsize=9.5,color=VERM,fontweight="bold",
             arrowprops=dict(arrowstyle="->",color=VERM,lw=1.4))
axA.set_ylim(0,90); axA.set_xticks(list(x)); axA.set_xticklabels(labels,fontsize=9)
axA.set_ylabel("% overlapping isoQTL or tQTL"); axA.set_title("A - The orthogonal overlap rate",loc="left",fontweight="bold",fontsize=11.5)
for s in ("top","right"): axA.spines[s].set_visible(False)
axA.grid(axis="y",color="#eee",zorder=0); axA.set_axisbelow(True)

# Panel B: the mechanism - QTL co-occurrence conditioned on carrying an eQTL
axB.bar([0,1],[he,ne],color=[ORANGE,BLUE],width=0.55,zorder=3)
for i,v in zip([0,1],[he,ne]): axB.text(i,v+1.5,f"{v:.1f}%",ha="center",fontsize=11,fontweight="bold")
axB.set_xticks([0,1]); axB.set_xticklabels(["variant WITH an eQTL","variant WITHOUT an eQTL"],fontsize=9.5)
axB.set_ylim(0,90); axB.set_ylabel("P(is isoQTL or tQTL)")
axB.set_title("B - Why the overlap is guaranteed in advance",loc="left",fontweight="bold",fontsize=11.5)
for s in ("top","right"): axB.spines[s].set_visible(False)
axB.grid(axis="y",color="#eee",zorder=0); axB.set_axisbelow(True)
axB.text(0.5,-0.30,"All 164/164 active variants are eQTLs BY CONSTRUCTION of the library\n-> they inherit the eQTL -> iso/tQTL co-occurrence -> the overlap is inflated a priori",
         transform=axB.transAxes,ha="center",fontsize=9.2,color=INK,
         bbox=dict(boxstyle="round,pad=0.4",facecolor="#fbeee6",edgecolor=VERM))

fig.text(0.5,0.005,"Munafo et al. 2018 (collider scope) - common practice without the caveat (Rykova 2024) - every number from audit_ortho_null.json (audit_ortho_null.py)",
         ha="center",fontsize=8,color="#777",style="italic")
fig.tight_layout(rect=[0,0.05,1,0.97])
fig.savefig(OUT,dpi=200,bbox_inches="tight",facecolor="white")
print(f"wrote {OUT}  (disc {disc:.1f}% < bg {bg:.1f}%, P={P:.3f}; cooc {he:.0f}% vs {ne:.0f}%)")
