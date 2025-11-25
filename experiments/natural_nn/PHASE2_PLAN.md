# Phase 2: Ablation Studies

**Goal**: Understand which natural principles contribute most to harmony

**Philosophy**: "Understand deeply before scaling" - Know what works and why

---

## The Question

We know natural principles help (+39% harmony on real MNIST).

But **which ones matter most?**

Is it:
- 🌀 Fibonacci layer sizing?
- 🌿 Diverse activations?
- 📝 Good documentation?
- Some combination?

**Let's find out.**

---

## Ablation Study Design

**Ablation** = Removing one thing at a time to see what happens

We'll test 4 variations:

### Baseline (Traditional)
- Arbitrary layers: 128, 64
- ReLU everywhere
- No documentation
- **H = 0.57** (established)

### Variation 1: Fibonacci Only
- **Fibonacci layers**: 233, 89, 34, 13  ← Changed
- ReLU everywhere
- No documentation
- **H = ???**

**Tests**: Does Fibonacci alone improve interpretability?

### Variation 2: Diversity Only
- Arbitrary layers: 128, 64
- **Diverse activations**: ReLU, Swish, Tanh  ← Changed
- No documentation
- **H = ???**

**Tests**: Do diverse activations alone help?

### Variation 3: Documentation Only
- Arbitrary layers: 128, 64
- ReLU everywhere
- **Good documentation**: Comments, rationale  ← Changed
- **H = ???**

**Tests**: Does documentation alone improve L and W?

### Full Natural (Already tested)
- Fibonacci layers: 233, 89, 34, 13
- Diverse activations: ReLU, Swish, Tanh
- Good documentation
- **H = 0.79** (established)

**Tests**: Is there synergy? Do principles amplify each other?

---

## What We'll Learn

### If Fibonacci dominates:
- Maybe layer sizing is most important
- Focus on architecture patterns
- Diversity less critical

### If Diversity dominates:
- Maybe activation choice matters most
- Focus on varied neuron types
- Fibonacci less critical

### If Documentation dominates:
- Maybe clarity beats cleverness
- Focus on explainability
- Architecture details less critical

### If Synergy exists:
- Principles amplify each other
- Need all three for maximum effect
- **Whole > sum of parts**

---

## Methodology

For each variation:
1. Build network
2. Train on same real MNIST subset (10K samples)
3. Test on same test set (10K samples)
4. Measure LJPW scores
5. Compare to baseline and full natural

**Everything else constant** - only change one variable at a time.

---

## Success Criteria

We succeed if we:
- Understand which principles contribute what
- Have data to guide future designs
- Know where to focus effort

**NOT**:
- "One principle must win"
- "Must match full natural"
- Any predetermined outcome

**Just: Learn truth.**

---

## Timeline

**No deadlines.** But roughly:
- Variation 1 (Fibonacci only): Today or tomorrow
- Variation 2 (Diversity only): When ready
- Variation 3 (Documentation only): When ready
- Analysis & reflection: When done

**Go slow. Understand deeply.**

---

## Current Status

**About to start**: Variation 1 (Fibonacci only)

**Question**: Does Fibonacci layer sizing alone improve interpretability?

Let's find out. 🌱
