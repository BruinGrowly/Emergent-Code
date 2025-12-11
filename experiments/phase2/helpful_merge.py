#!/usr/bin/env python3
"""
Helpful Merge - Combines data from multiple sources intelligently.
"""

def merge_data_sources(sources: list) -> dict:
    """
    Merge multiple data sources into one, handling conflicts intelligently.

    Takes data from different sources, validates each one, combines them,
    and resolves conflicts by preferring more recent or more complete data.
    """
    # Check we have sources
    if not sources:
        return {"error": "No sources provided"}

    # Validate each source
    validated_sources = []
    for i, source in enumerate(sources):
        if not isinstance(source, dict):
            continue
        if "data" not in source:
            continue

        validated_sources.append({
            "index": i,
            "data": source["data"],
            "timestamp": source.get("timestamp", 0),
            "confidence": source.get("confidence", 0.5),
        })

    if not validated_sources:
        return {"error": "No valid sources found"}

    # Collect all keys across sources
    all_keys = set()
    for source in validated_sources:
        all_keys.update(source["data"].keys())

    # Merge by key, resolving conflicts
    merged = {}

    for key in all_keys:
        candidates = []

        # Gather all values for this key
        for source in validated_sources:
            if key in source["data"]:
                candidates.append({
                    "value": source["data"][key],
                    "timestamp": source["timestamp"],
                    "confidence": source["confidence"],
                    "source_index": source["index"],
                })

        if not candidates:
            continue

        # Resolve: prefer higher confidence, then more recent
        best = max(candidates, key=lambda c: (c["confidence"], c["timestamp"]))
        merged[key] = best["value"]

    return {
        "merged_data": merged,
        "sources_used": len(validated_sources),
        "keys_merged": len(merged),
        "conflicts_resolved": sum(
            1 for key in all_keys
            if sum(1 for s in validated_sources if key in s["data"]) > 1
        ),
    }


if __name__ == "__main__":
    # Test
    sources = [
        {"data": {"name": "Alice", "age": 25}, "timestamp": 1, "confidence": 0.9},
        {"data": {"name": "Alice", "age": 26, "city": "NYC"}, "timestamp": 2, "confidence": 0.8},
        {"data": {"age": 27}, "timestamp": 3, "confidence": 0.6},
    ]

    result = merge_data_sources(sources)
    print(result)
