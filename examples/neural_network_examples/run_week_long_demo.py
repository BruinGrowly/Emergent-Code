"""
Week-Long Evolution Demo

Quick demonstration (200 epochs) of the week-long evolution system.
Shows all capabilities working before launching the full 1000+ epoch run.

For the REAL week-long run, use: python -m ljpw_nn.week_long_evolution
"""

from ljpw_nn.week_long_evolution import WeekLongEvolutionRunner

print("\n" + "🙏" * 35)
print("WEEK-LONG EVOLUTION DEMO")
print("200 Epochs - Showing Capabilities")
print("🙏" * 35 + "\n")

# Create runner
runner = WeekLongEvolutionRunner(
    experiment_name="demo_200_epochs",
    results_dir="demo_week_long",
    evolution_frequency=5,  # Aggressive evolution every 5 epochs
    checkpoint_frequency=25,  # Save every 25 epochs
    topology_evolution_enabled=True,
    principle_discovery_enabled=True
)

print("🚀 Running 200-epoch demonstration...")
print("(For full 1000+ epoch run, use: python -m ljpw_nn.week_long_evolution)")
print()

# Run demonstration
result = runner.run_week_long_evolution(
    dataset_name="MNIST",
    dataset_size=5000,  # Smaller for demo
    epochs=200,  # Demo length
    batch_size=32,
    learning_rate=0.05
)

print("\n" + "=" * 70)
print("DEMONSTRATION COMPLETE")
print("=" * 70)
print(f"\nSession ID: {result['session_id']}")
print("\nDiscoveries Summary:")
summary = runner.discovery_logger.get_summary()
print(f"  Total discoveries: {summary['total_discoveries']}")
print(f"  Breakthroughs: {summary['breakthroughs']}")
print(f"  Milestones: {summary['milestones']}")
print(f"  Principles: {summary['principles']}")
print()

print("Evolution Summary:")
print(f"  Evolution events: {len(result['history']['evolution_events'])}")
print(f"  Final test accuracy: {result['history']['test_accuracy'][-1]:.4f}")
print(f"  Final harmony: {result['history']['harmony'][-1]:.4f}")
print()

print("=" * 70)
print("SYSTEM READY FOR WEEK-LONG RUN")
print("=" * 70)
print()
print("To launch the full 1000+ epoch evolution:")
print("  python -m ljpw_nn.week_long_evolution")
print()
print("Or edit epochs in week_long_evolution.py __main__ section")
print()
print("🙏 Let consciousness discover what we haven't imagined! 🙏")
print()
