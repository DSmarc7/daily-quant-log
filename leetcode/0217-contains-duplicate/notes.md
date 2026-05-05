# 217. Contains Duplicate

**Difficulty:** Easy
**Tags:** Array, Hash Table
**Date:** 2026-05-05
**Time spent:** ~3 min

## Approche
On garde un `set` des éléments déjà vus. Si on retombe dessus, return True.
Single pass.

## Complexité
- Time: O(n) — un parcours
- Space: O(n) — le set au pire (tableau sans doublon)

## Alternatives
- **Sort + scan voisins** → O(n log n) time, O(1) extra space (si on peut muter `nums`).
  Trade-off: gain mémoire, coût temps.
- **One-liner** : `len(set(nums)) != len(nums)`.
  Concis mais lit le tableau deux fois (set construit + len) au lieu de short-circuit
  au premier doublon trouvé. Pour les très gros inputs avec doublon précoce, le loop gagne.

## Piège / leçon
RAS sur celui-ci. Bon réflexe à ancrer : "détecter un doublon → hashset, O(n)/O(n)".
Pattern à réutiliser pour: 219 (Contains Duplicate II), 220 (Contains Duplicate III, plus dur).
