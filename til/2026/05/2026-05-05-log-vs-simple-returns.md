# Pourquoi log-returns plutôt que returns simples ?

**Date:** 2026-05-05
**Tags:** #stats #returns #quant-basics

Pour un actif de prix $P_t$, deux définitions de return :
- Simple : $r_t = P_t / P_{t-1} - 1$
- Log : $\ell_t = \ln(P_t / P_{t-1}) = \ln P_t - \ln P_{t-1}$

Trois raisons d'utiliser les log-returns :

1. **Additivité temporelle.** Le log-return sur $N$ jours est la somme des journaliers : $\ell_{1 \to N} = \sum \ell_t$. Avec les returns simples il faut multiplier $\prod (1 + r_t)$, beaucoup moins pratique pour la modélisation.
2. **Symétrie.** Un gain qui multiplie par 2 et une perte qui divise par 2 ont des log-returns opposés ($\ln 2$ et $-\ln 2$). En simple, ce serait +100% et −50%, pas symétrique.
3. **Hypothèse gaussienne.** Black-Scholes & co supposent que les log-prix suivent un brownien → log-returns ~ $\mathcal{N}(\mu, \sigma^2)$. Si on travaillait avec les simples, le modèle laisserait les prix devenir négatifs.

**Quand prendre les simples ?** Pour le P&L d'un portefeuille : la somme pondérée des returns simples = return du portefeuille. Pas vrai pour les logs.

**Why I care:** je commençais à voir les deux notations dans des papers et je n'avais pas le réflexe de savoir laquelle utiliser quand.
