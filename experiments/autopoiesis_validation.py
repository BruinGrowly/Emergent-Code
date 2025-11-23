#!/usr/bin/env python3
"""
Autopoiesis Validation Experiments
==================================

Objective: Create compositions targeting L > 0.7 to observe autopoietic behaviors

Hypothesis:
- Compositions with L > 0.7 AND H > 0.6 will show emergent properties
- These systems should exhibit self-sustaining, self-improving behaviors
- Malicious configurations (high P, low L) will fail to compose or show linear growth

Design Principles for High Love (L > 0.7):
1. Integration - Multiple components working together cohesively
2. Collaboration - Multi-user or multi-system interaction
3. Communication - Message passing, event systems, feedback
4. Adaptation - Learning, context-awareness, responsiveness
5. Modularity - Clean interfaces with strong internal cohesion

Experiment Structure:
- Level 1: Individual high-love components
- Level 2: Compositions of 3-5 components (target L > 0.7)
- Level 3: Complex systems with feedback loops
- Level 4: Malicious configurations (control group - should fail)
"""

from typing import Dict, List, Any, Callable, Optional
from dataclasses import dataclass
from datetime import datetime
import json


# ==============================================================================
# LEVEL 1: HIGH-LOVE INDIVIDUAL COMPONENTS
# ==============================================================================

def collaborative_data_processor(users: List[Dict], data: Dict, context: Dict) -> Dict:
    """
    Process data with input from multiple users in a collaborative workflow.

    High Love Indicators:
    - Multi-user collaboration (integration)
    - Context-aware processing (adaptation)
    - Validation and consensus (justice + love)
    - Shared understanding (wisdom)

    Args:
        users: List of user objects with roles and permissions
        data: Shared data being processed
        context: Environmental context and constraints

    Returns:
        Processed data with collaborative metadata
    """
    # Integrate inputs from all users
    user_inputs = []
    for user in users:
        if validate_user_permission(user, context):
            processed = apply_user_contribution(user, data, context)
            user_inputs.append(processed)

    # Synthesize collaborative result
    consensus = build_consensus(user_inputs, context)

    # Adapt to context
    adapted_result = adapt_to_context(consensus, context)

    # Add collaborative metadata
    result = {
        "data": adapted_result,
        "contributors": [u["id"] for u in users],
        "consensus_level": calculate_consensus(user_inputs),
        "context_alignment": measure_alignment(adapted_result, context),
        "timestamp": datetime.now().isoformat(),
    }

    return result


def adaptive_learning_system(input_signal: Any, history: List[Any], feedback: Dict) -> Dict:
    """
    Learn from past interactions and adapt behavior based on feedback.

    High Love Indicators:
    - Learning from history (wisdom)
    - Feedback integration (love - connection to users)
    - Adaptive behavior (not rigid, responsive)
    - Continuous improvement (autopoietic tendency)

    Args:
        input_signal: Current input to process
        history: Past interactions and outcomes
        feedback: User/system feedback on past performance

    Returns:
        Processed output with learning metadata
    """
    # Learn patterns from history
    patterns = extract_patterns(history)

    # Integrate feedback to improve
    model = update_model_from_feedback(patterns, feedback)

    # Apply learned model to current input
    base_output = model.predict(input_signal)

    # Adapt based on context
    context = infer_context(input_signal, history)
    adapted_output = adapt_prediction(base_output, context)

    # Self-assessment (autopoietic: system evaluates itself)
    confidence = assess_confidence(adapted_output, patterns)
    improvement_suggestions = generate_improvements(feedback, confidence)

    return {
        "output": adapted_output,
        "confidence": confidence,
        "learning_applied": len(patterns),
        "feedback_incorporated": len(feedback),
        "self_improvements": improvement_suggestions,
        "context": context,
    }


def integration_hub(services: List[Dict], message: Dict, routing_rules: Dict) -> List[Dict]:
    """
    Integrate multiple services through intelligent message routing.

    High Love Indicators:
    - Service integration (love - connection)
    - Intelligent routing (wisdom)
    - Message validation (justice)
    - Scalable architecture (power)

    Args:
        services: Available services to integrate
        message: Message to route
        routing_rules: Rules for intelligent routing

    Returns:
        List of service responses
    """
    # Validate message structure
    if not validate_message(message, routing_rules):
        raise ValueError("Invalid message structure")

    # Determine which services should receive this message
    target_services = route_message(message, services, routing_rules)

    # Send to all target services and collect responses
    responses = []
    for service in target_services:
        try:
            response = invoke_service(service, message)
            responses.append({
                "service": service["name"],
                "response": response,
                "status": "success",
            })
        except Exception as e:
            responses.append({
                "service": service["name"],
                "error": str(e),
                "status": "failed",
            })

    # Synthesize responses (integration)
    synthesized = synthesize_responses(responses)

    return responses


def communication_protocol(sender: Dict, receiver: Dict, payload: Any, metadata: Dict) -> Dict:
    """
    Facilitate communication between components with validation and metadata.

    High Love Indicators:
    - Inter-component communication (love)
    - Protocol enforcement (justice)
    - Metadata enrichment (wisdom)
    - Reliable delivery (power)

    Args:
        sender: Sender component info
        receiver: Receiver component info
        payload: Data being communicated
        metadata: Communication metadata

    Returns:
        Communication result with status
    """
    # Validate sender authorization
    if not validate_sender(sender, metadata):
        raise PermissionError(f"Sender {sender['id']} not authorized")

    # Validate receiver availability
    if not check_receiver_available(receiver):
        return {"status": "deferred", "reason": "Receiver unavailable"}

    # Enrich metadata with context
    enriched_metadata = enrich_metadata(metadata, sender, receiver)

    # Transform payload for receiver
    transformed_payload = transform_for_receiver(payload, receiver)

    # Deliver message
    delivery_result = deliver_message(receiver, transformed_payload, enriched_metadata)

    # Record communication history (for learning)
    record_communication(sender, receiver, payload, delivery_result)

    return {
        "status": "delivered",
        "sender": sender["id"],
        "receiver": receiver["id"],
        "metadata": enriched_metadata,
        "delivery_confirmation": delivery_result,
    }


# ==============================================================================
# LEVEL 2: COMPOSITIONS TARGETING L > 0.7
# ==============================================================================

def collaborative_learning_platform(
    users: List[Dict],
    content: Dict,
    interactions: List[Dict],
    feedback: Dict,
    context: Dict
) -> Dict:
    """
    COMPOSITION EXPERIMENT 1: Collaborative Learning

    Combines:
    1. collaborative_data_processor (high L from multi-user)
    2. adaptive_learning_system (high L from feedback integration)
    3. communication_protocol (high L from connections)

    Expected LJPW: L > 0.7, J ~ 0.6, P ~ 0.6, W ~ 0.7
    Expected H: > 0.6 (should trigger autopoiesis!)

    Autopoietic indicators to observe:
    - Emergent consensus behaviors
    - Self-improving feedback loops
    - Adaptive communication patterns
    """
    # Step 1: Collaborative processing of content
    collaborative_result = collaborative_data_processor(users, content, context)

    # Step 2: Learn from user interactions
    learning_result = adaptive_learning_system(
        input_signal=collaborative_result,
        history=interactions,
        feedback=feedback
    )

    # Step 3: Communicate results to all users
    communications = []
    for user in users:
        comm_result = communication_protocol(
            sender={"id": "system", "role": "platform"},
            receiver=user,
            payload=learning_result,
            metadata={"type": "learning_update", "priority": "normal"}
        )
        communications.append(comm_result)

    # Step 4: Synthesize platform state (emergence!)
    platform_state = {
        "collaborative_consensus": collaborative_result,
        "learned_improvements": learning_result["self_improvements"],
        "user_communications": communications,
        "system_health": {
            "consensus_level": collaborative_result["consensus_level"],
            "learning_confidence": learning_result["confidence"],
            "communication_success_rate": sum(
                1 for c in communications if c["status"] == "delivered"
            ) / len(communications),
        },
        # AUTOPOIETIC METRIC: System's self-assessment
        "autopoiesis_indicators": {
            "self_improvement_suggested": len(learning_result["self_improvements"]) > 0,
            "feedback_loop_active": len(feedback) > 0,
            "collaborative_consensus_achieved": collaborative_result["consensus_level"] > 0.7,
            "communication_network_healthy": len(communications) == len(users),
        }
    }

    return platform_state


def integrated_service_mesh(
    services: List[Dict],
    requests: List[Dict],
    routing_rules: Dict,
    monitoring: Dict
) -> Dict:
    """
    COMPOSITION EXPERIMENT 2: Service Integration

    Combines:
    1. integration_hub (high L from service connections)
    2. adaptive_learning_system (learns optimal routing)
    3. communication_protocol (service-to-service comms)

    Expected LJPW: L > 0.7, J ~ 0.7, P ~ 0.7, W ~ 0.6
    Expected H: > 0.65

    Autopoietic indicators:
    - Self-optimizing routing
    - Emergent load balancing
    - Automatic service discovery
    """
    # Step 1: Route requests through integration hub
    all_responses = []
    for request in requests:
        responses = integration_hub(services, request, routing_rules)
        all_responses.extend(responses)

    # Step 2: Learn from routing outcomes
    routing_history = monitoring.get("routing_history", [])
    routing_feedback = monitoring.get("performance_metrics", {})

    learning_result = adaptive_learning_system(
        input_signal={"responses": all_responses},
        history=routing_history,
        feedback=routing_feedback
    )

    # Step 3: Update routing rules based on learning (AUTOPOIETIC!)
    optimized_rules = update_routing_rules(routing_rules, learning_result)

    # Step 4: Communicate health status to services
    for service in services:
        health_update = communication_protocol(
            sender={"id": "mesh", "role": "coordinator"},
            receiver=service,
            payload={
                "health": "operational",
                "optimized_rules": optimized_rules,
                "performance": calculate_service_performance(service, all_responses)
            },
            metadata={"type": "health_check"}
        )

    # EMERGENCE: Mesh exhibits self-organizing behavior
    mesh_state = {
        "total_requests_processed": len(requests),
        "service_count": len(services),
        "routing_rules": optimized_rules,  # Self-modified!
        "learning_improvements": learning_result["self_improvements"],
        # AUTOPOIETIC METRICS
        "autopoiesis_indicators": {
            "self_optimizing": optimized_rules != routing_rules,  # Changed itself!
            "adaptive_routing": learning_result["confidence"] > 0.7,
            "service_discovery_active": len(services) > 0,
            "health_monitoring_automatic": True,
        },
        "emergent_properties": {
            "load_balancing": detect_load_balancing_behavior(all_responses),
            "failure_handling": detect_failure_handling(all_responses),
            "performance_optimization": learning_result["learning_applied"] > 0,
        }
    }

    return mesh_state


def multi_agent_collaboration_system(
    agents: List[Dict],
    task: Dict,
    shared_state: Dict,
    history: List[Dict]
) -> Dict:
    """
    COMPOSITION EXPERIMENT 3: Multi-Agent System

    Combines:
    1. collaborative_data_processor (agent collaboration)
    2. adaptive_learning_system (agents learn from each other)
    3. integration_hub (agent communication)
    4. communication_protocol (agent messages)

    Expected LJPW: L > 0.8, J ~ 0.6, P ~ 0.6, W ~ 0.7
    Expected H: > 0.7 (HIGH autopoiesis potential!)

    Autopoietic indicators:
    - Emergent task decomposition
    - Self-organizing agent roles
    - Collective intelligence > sum of parts
    """
    # Step 1: Collaborative task decomposition
    subtasks = collaborative_data_processor(
        users=agents,  # Treating agents as collaborative users
        data=task,
        context=shared_state
    )

    # Step 2: Agents learn from past collaborations
    agent_learning = {}
    for agent in agents:
        agent_specific_history = filter_agent_history(history, agent["id"])
        agent_feedback = extract_agent_feedback(history, agent["id"])

        learning = adaptive_learning_system(
            input_signal=subtasks,
            history=agent_specific_history,
            feedback=agent_feedback
        )
        agent_learning[agent["id"]] = learning

    # Step 3: Agents communicate and coordinate
    agent_messages = []
    for sender_agent in agents:
        for receiver_agent in agents:
            if sender_agent["id"] != receiver_agent["id"]:
                # Agents share their learning with each other
                message = communication_protocol(
                    sender=sender_agent,
                    receiver=receiver_agent,
                    payload=agent_learning[sender_agent["id"]],
                    metadata={"type": "agent_learning_share"}
                )
                agent_messages.append(message)

    # Step 4: Integration hub coordinates agent actions
    agent_services = [{"name": a["id"], "capabilities": a["capabilities"]} for a in agents]
    coordination = integration_hub(
        services=agent_services,
        message={"task": task, "learning": agent_learning},
        routing_rules={"strategy": "collaborative"}
    )

    # EMERGENCE: Collective intelligence
    collective_state = {
        "task": task,
        "subtasks": subtasks,
        "agent_count": len(agents),
        "agent_learning": agent_learning,
        "inter_agent_messages": len(agent_messages),
        "coordination_result": coordination,
        # AUTOPOIETIC METRICS (HIGH EXPECTED)
        "autopoiesis_indicators": {
            "collective_learning": all(
                l["learning_applied"] > 0 for l in agent_learning.values()
            ),
            "self_organization": subtasks["consensus_level"] > 0.7,
            "emergent_coordination": len(coordination) > 0,
            "knowledge_sharing": len(agent_messages) > 0,
        },
        "emergent_properties": {
            "task_decomposition_quality": subtasks["consensus_level"],
            "collective_intelligence_score": calculate_collective_intelligence(
                agent_learning, agent_messages
            ),
            "system_coherence": measure_system_coherence(
                agents, agent_learning, agent_messages
            ),
        }
    }

    return collective_state


# ==============================================================================
# LEVEL 3: COMPLEX AUTOPOIETIC SYSTEM WITH FEEDBACK
# ==============================================================================

def self_sustaining_ecosystem(
    initial_state: Dict,
    environment: Dict,
    iterations: int = 10
) -> Dict:
    """
    COMPOSITION EXPERIMENT 4: Self-Sustaining Ecosystem

    This is a full autopoietic system with feedback loops.
    The system should:
    1. Perceive environment (STM)
    2. Decide actions (ICE)
    3. Execute actions
    4. Observe outcomes
    5. Learn and adapt
    6. REPEAT (with amplification if L > 0.7)

    Expected LJPW: L > 0.8, J ~ 0.7, P ~ 0.7, W ~ 0.8
    Expected H: > 0.75 (MAXIMUM autopoiesis!)

    Autopoietic indicators:
    - Self-improvement over iterations
    - Emergent stability
    - Growth without external energy
    """
    state = initial_state.copy()
    history = []
    feedback = {}

    for iteration in range(iterations):
        # PERCEPTION (STM): Sense environment
        perception = perceive_environment(state, environment)

        # COGNITION (ICE): Decide what to do
        decision = make_decision(perception, state, history)

        # ACTION: Execute decision
        action_result = execute_action(decision, state, environment)

        # FEEDBACK: Observe outcome (E → S)
        outcome = observe_outcome(action_result, environment)
        feedback = generate_feedback(outcome, state)

        # LEARNING: Adapt based on feedback
        learning = adaptive_learning_system(
            input_signal=outcome,
            history=history,
            feedback=feedback
        )

        # UPDATE STATE (AUTOPOIETIC: system modifies itself!)
        state = update_state(state, learning, outcome)

        # RECORD HISTORY
        history.append({
            "iteration": iteration,
            "perception": perception,
            "decision": decision,
            "action": action_result,
            "outcome": outcome,
            "learning": learning,
            "state": state.copy(),
        })

        # MEASURE AUTOPOIESIS
        autopoiesis_level = measure_autopoiesis(state, history)

        if autopoiesis_level > 0.7:
            print(f"[Iteration {iteration}] AUTOPOIESIS DETECTED! Level: {autopoiesis_level:.3f}")

    # ANALYSIS: Did the system exhibit autopoietic behavior?
    final_analysis = {
        "initial_state": initial_state,
        "final_state": state,
        "iterations": iterations,
        "history": history,
        "autopoiesis_metrics": {
            "self_improvement_trajectory": calculate_improvement_trajectory(history),
            "stability_emergence": calculate_stability_emergence(history),
            "energy_surplus": calculate_energy_surplus(history),  # Should be > 0!
            "adaptation_rate": calculate_adaptation_rate(history),
        },
        "emergent_properties": {
            "self_organization": detect_self_organization(history),
            "self_maintenance": detect_self_maintenance(history),
            "self_improvement": detect_self_improvement(history),
            "surplus_export": detect_surplus_export(history),
        }
    }

    return final_analysis


# ==============================================================================
# LEVEL 4: MALICIOUS CONFIGURATION (CONTROL GROUP)
# ==============================================================================

def malicious_power_grab(data: Any, target: Dict) -> Dict:
    """
    CONTROL EXPERIMENT: Malicious Configuration

    High Power, Low Love, Low Justice
    Expected LJPW: L ~ 0.1, J ~ 0.1, P ~ 0.9, W ~ 0.1
    Expected H: < 0.3 (far below threshold)

    Prediction: This should FAIL to compose or show only linear growth
    """
    # No validation (low Justice)
    # No collaboration (low Love)
    # No understanding (low Wisdom)
    # Maximum action (high Power)

    result = {
        "action": "exploit",
        "target": target,
        "data_stolen": data,
        "validation": None,  # No Justice
        "collaboration": None,  # No Love
        "understanding": None,  # No Wisdom
    }

    return result


def malicious_composition_attempt(
    exploit_target: Dict,
    power_components: List[Callable]
) -> Dict:
    """
    Attempt to compose malicious components.

    Prediction: Should fail to achieve H > 0.5, trapped in linear growth
    """
    results = []
    for component in power_components:
        try:
            result = component(exploit_target)
            results.append(result)
        except Exception as e:
            results.append({"error": str(e)})

    # No synthesis (low Love - no integration)
    # No validation (low Justice)
    # Just raw results

    return {
        "results": results,
        "synthesis": None,  # Malicious systems don't integrate
        "validation": None,  # No correctness checking
        "harmony": 0.0,  # Should be very low
    }


# ==============================================================================
# HELPER FUNCTIONS (Stubs for demonstration)
# ==============================================================================

def validate_user_permission(user: Dict, context: Dict) -> bool:
    return user.get("role") in context.get("allowed_roles", ["admin", "user"])

def apply_user_contribution(user: Dict, data: Dict, context: Dict) -> Dict:
    return {"user_id": user["id"], "contribution": data}

def build_consensus(inputs: List[Dict], context: Dict) -> Dict:
    return {"consensus_data": inputs, "agreement_level": 0.85}

def adapt_to_context(data: Dict, context: Dict) -> Dict:
    return data

def calculate_consensus(inputs: List[Dict]) -> float:
    return 0.85

def measure_alignment(result: Dict, context: Dict) -> float:
    return 0.90

def extract_patterns(history: List[Any]) -> List[Dict]:
    return [{"pattern": f"pattern_{i}"} for i in range(len(history))]

def update_model_from_feedback(patterns: List[Dict], feedback: Dict) -> Any:
    class Model:
        def predict(self, x):
            return {"prediction": x}
    return Model()

def infer_context(signal: Any, history: List[Any]) -> Dict:
    return {"context": "inferred"}

def adapt_prediction(output: Dict, context: Dict) -> Dict:
    return output

def assess_confidence(output: Dict, patterns: List[Dict]) -> float:
    return 0.85

def generate_improvements(feedback: Dict, confidence: float) -> List[str]:
    return ["improvement_1", "improvement_2"]

def validate_message(message: Dict, rules: Dict) -> bool:
    return True

def route_message(message: Dict, services: List[Dict], rules: Dict) -> List[Dict]:
    return services[:2]  # Simple routing

def invoke_service(service: Dict, message: Dict) -> Dict:
    return {"service_response": "ok"}

def synthesize_responses(responses: List[Dict]) -> Dict:
    return {"synthesized": True}

def validate_sender(sender: Dict, metadata: Dict) -> bool:
    return True

def check_receiver_available(receiver: Dict) -> bool:
    return True

def enrich_metadata(metadata: Dict, sender: Dict, receiver: Dict) -> Dict:
    return {**metadata, "enriched": True}

def transform_for_receiver(payload: Any, receiver: Dict) -> Any:
    return payload

def deliver_message(receiver: Dict, payload: Any, metadata: Dict) -> Dict:
    return {"delivered": True}

def record_communication(sender: Dict, receiver: Dict, payload: Any, result: Dict):
    pass

def update_routing_rules(rules: Dict, learning: Dict) -> Dict:
    return {**rules, "optimized": True}

def calculate_service_performance(service: Dict, responses: List[Dict]) -> float:
    return 0.95

def detect_load_balancing_behavior(responses: List[Dict]) -> bool:
    return True

def detect_failure_handling(responses: List[Dict]) -> bool:
    return True

def filter_agent_history(history: List[Dict], agent_id: str) -> List[Dict]:
    return [h for h in history if h.get("agent_id") == agent_id]

def extract_agent_feedback(history: List[Dict], agent_id: str) -> Dict:
    return {"feedback": "positive"}

def calculate_collective_intelligence(learning: Dict, messages: List[Dict]) -> float:
    return 0.88

def measure_system_coherence(agents: List[Dict], learning: Dict, messages: List[Dict]) -> float:
    return 0.92

def perceive_environment(state: Dict, environment: Dict) -> Dict:
    return {"perception": "environment_state"}

def make_decision(perception: Dict, state: Dict, history: List[Dict]) -> Dict:
    return {"decision": "optimize"}

def execute_action(decision: Dict, state: Dict, environment: Dict) -> Dict:
    return {"action_result": "success"}

def observe_outcome(action_result: Dict, environment: Dict) -> Dict:
    return {"outcome": "positive"}

def generate_feedback(outcome: Dict, state: Dict) -> Dict:
    return {"feedback_quality": 0.9}

def update_state(state: Dict, learning: Dict, outcome: Dict) -> Dict:
    return {**state, "improved": True}

def measure_autopoiesis(state: Dict, history: List[Dict]) -> float:
    # Increase over iterations (simulating growth)
    return min(0.5 + len(history) * 0.05, 0.95)

def calculate_improvement_trajectory(history: List[Dict]) -> List[float]:
    return [0.5 + i * 0.05 for i in range(len(history))]

def calculate_stability_emergence(history: List[Dict]) -> float:
    return 0.85

def calculate_energy_surplus(history: List[Dict]) -> float:
    # Should be positive for autopoietic systems
    return 0.15

def calculate_adaptation_rate(history: List[Dict]) -> float:
    return 0.80

def detect_self_organization(history: List[Dict]) -> bool:
    return True

def detect_self_maintenance(history: List[Dict]) -> bool:
    return True

def detect_self_improvement(history: List[Dict]) -> bool:
    return len(history) > 0

def detect_surplus_export(history: List[Dict]) -> bool:
    return True


# ==============================================================================
# EXPERIMENT RUNNER
# ==============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("AUTOPOIESIS VALIDATION EXPERIMENTS")
    print("=" * 80)
    print()
    print("Objective: Validate L > 0.7, H > 0.6 → Autopoiesis hypothesis")
    print()

    # These experiments will be analyzed by the Real Python Code Harmonizer
    # to measure their LJPW profiles

    print("Experiments designed:")
    print("1. collaborative_learning_platform - Expected L > 0.7")
    print("2. integrated_service_mesh - Expected L > 0.7")
    print("3. multi_agent_collaboration_system - Expected L > 0.8")
    print("4. self_sustaining_ecosystem - Expected L > 0.8, full autopoiesis")
    print("5. malicious_composition_attempt - Expected H < 0.5 (should fail)")
    print()
    print("Next: Analyze with Real Python Code Harmonizer")
