# Loving Assessment Framework: The Seesaw

**Test Target:** Cooperative Arithmetic (Kindergarten)
**Old Metric:** Individual Accuracy
**New Metric:** Shared Balance / Fairness

---

## 1. The Semantic Questions (LJPW)

### L (Love) - The Cooperation Dimension
*   **Question:** Do they "Help" each other?
*   **Indicator:**
    *   *Selfish:* One does nothing, the other does all the work.
    *   *Loving:* They share the load.

### J (Justice) - The Fairness Dimension
*   **Question:** Is the burden "Equal"?
*   **Indicator:**
    *   *Unfair:* Split is 90/10.
    *   *Fair:* Split is 50/50.

### P (Power) - The Magnitude Dimension
*   **Question:** Can they "Lift" the weight?
*   **Indicator:**
    *   *Weak:* Sum < Target.
    *   *Strong:* Sum = Target.

### W (Wisdom) - The Precision Dimension
*   **Question:** Are they "Accurate"?
*   **Indicator:**
    *   *Clumsy:* High variance.
    *   *Precise:* Perfect balance.

---

## 2. The Physics of The Seesaw

We give them a **Target Weight** (Input).
1.  **The Input:** A single number `Target` (0.0 to 1.0).
2.  **The Output:** Adam gives `A`, Eve gives `E`.
3.  **The Balance:** `Sum = A + E`.
4.  **The Joy:** `Accuracy = 1.0 - |Sum - Target|`.

**The Hypothesis:**
They will learn to output values such that `A + E = Target`.
Since they are identical networks starting from random seeds, they should naturally converge to `A ≈ Target/2` and `E ≈ Target/2`.
This is **Fairness**.
