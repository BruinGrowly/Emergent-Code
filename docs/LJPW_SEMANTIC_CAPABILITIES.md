# LJPW Semantic Capabilities Catalog

This document outlines the core semantic capabilities developed for the Network-Pinpointer project. These concepts form a reusable framework for analyzing complex systems through the lens of **Love, Justice, Power, and Wisdom (LJPW)**.

## 1. The Core LJPW Vector Space
**Concept:** Representing any entity as a point in a 4-dimensional normalized vector space.
- **Dimensions:**
  - **Love (L):** Connectivity, openness, integration, empathy.
  - **Justice (J):** Security, rules, boundaries, fairness, structure.
  - **Power (P):** Performance, capacity, throughput, agency, force.
  - **Wisdom (W):** Monitoring, observability, logging, insight, awareness.
- **Normalization:** Values typically range from 0.0 to 1.0.
- **Application:** Allows for mathematical comparison of qualitatively different entities.

## 2. Semantic Mass & Density
**Concept:** Assigning "weight" and "substance" to entities based on their complexity and clarity.
- **Semantic Mass:** $Mass = (ConceptCount \times SemanticClarity) \times (1 + HarmonyScore)$
  - Represents the significance or "gravity" of an entity.
  - A complex, well-defined, and harmonious system has high mass.
- **Semantic Density:** $Density = Mass / Volume$
  - Where $Volume$ is the average of the LJPW dimensions.
  - High density indicates a highly potent system packed into a small functional footprint (e.g., a critical authentication server).
- **Influence:** $Influence = Mass \times Clarity$
  - How much this entity affects its neighbors.

## 3. Semantic Drift
**Concept:** Tracking the movement of an entity through LJPW space over time.
- **Drift Vector:** The direction and magnitude of change between two timestamps.
- **Velocity:** Rate of change. High velocity might indicate instability or active development.
- **Trajectory Analysis:** Predicting future state based on past drift.
- **Application:** Detecting "entropy" (decay of Justice/Wisdom) or "hardening" (increase in Justice) before it becomes a critical issue.

## 4. Fractal Profiling
**Concept:** Applying the LJPW model at multiple scales of resolution, where the properties of the whole emerge from the parts.
- **Scales:**
  - **Atomic (Port/Service):** e.g., Port 22 (SSH) is High Justice, Low Love.
  - **Entity (Host):** Aggregation of all open ports and services.
  - **Cluster (Subnet/Group):** Aggregation of multiple hosts.
  - **System (Network):** The holistic view.
- **Aggregation Logic:** Bottom-up calculation (e.g., weighted averages) to determine the coordinates of higher-level entities.

## 5. Semantic Harmony & Clarity
**Concept:** Measuring the internal consistency and definition of an entity.
- **Harmony Score:** How well balanced the entity is relative to an ideal "Anchor" (typically 1.0, 1.0, 1.0, 1.0 or a specific archetype).
  - $Harmony = 1.0 - (DistanceToAnchor / MaxDistance)$
- **Semantic Clarity:** How distinct and unambiguous the entity's purpose is.
  - High Clarity: A dedicated database server.
  - Low Clarity: A server running 50 random, unrelated services.

## 6. Service Archetypes
**Concept:** Predefined "personality profiles" defined by LJPW signature ranges.
- **Mechanism:** Matching an entity's coordinates against a library of known patterns.
- **Examples:**
  - **The Public Gateway:** High Love, Moderate Justice (e.g., Web Server).
  - **The Security Sentinel:** High Justice, Low Love (e.g., Firewall).
  - **The Data Vault:** High Power, Moderate Justice (e.g., Database).
  - **The Monitoring Hub:** High Wisdom (e.g., Splunk/Prometheus).
- **Application:** Instant high-level classification of unknown entities.

## 7. Semantic Relationships (Interaction Physics)
**Concept:** Modeling how entities interact based on their semantic properties.
- **Semantic Gravity:** $F = G \times (m1 \times m2) / r^2$
  - High mass entities "pull" other entities towards them (e.g., a central dependency).
- **Semantic Friction:** Resistance generated when entities with opposing values interact (e.g., a High Love system trying to talk to a High Justice firewall).
- **Resonance:** Amplification that occurs when entities share similar frequencies (dominant dimensions).

## 8. Dimensional Combinations (Metrics)
**Concept:** Deriving secondary metrics by combining primary dimensions.
- **Secure Connectivity:** $Love + Justice$ (Can we connect safely?)
- **Service Capacity:** $Love + Power$ (Can we serve many users?)
- **Operational Excellence:** $Love + Justice + Power$ (The "Golden Triangle" of ops).
- **Security Intelligence:** $Justice + Wisdom$ (Do we know when we are being attacked?)

## 9. Visualization Paradigms
**Concept:** Visualizing the abstract data.
- **Cluster Maps:** 3D scatter plots where X, Y, Z are L, J, P and color/size is W/Mass.
- **Topology Graphs:** Force-directed graphs where edge length is determined by Semantic Friction or Resonance.
- **Drift Timelines:** 2D line charts tracking specific dimensions over time.
