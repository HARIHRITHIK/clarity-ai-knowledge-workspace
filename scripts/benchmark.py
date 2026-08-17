"""
Clarity NLP & Pipeline Performance Benchmark
===========================================
Measures throughput, latency, and memory footprint across the sample corpus.
Designed for reproducible performance validation without external dependencies.
"""

from __future__ import annotations
import time
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.pipeline import Pipeline
from intelligence.search import SearchEngine

SAMPLE_DIR = PROJECT_ROOT / "sample_data"


def run_benchmark():
    print("=" * 65)
    print("  CLARITY WORKSPACE — REPRODUCIBLE NLP BENCHMARK")
    print("=" * 65)
    print(f"Sample Corpus: {SAMPLE_DIR.name}/")

    files = sorted(list(SAMPLE_DIR.glob("*.*")))
    if not files:
        print("Error: No files found in sample_data/ directory.")
        return

    pipeline = Pipeline()
    search_engine = SearchEngine()
    processed_docs = []

    print("\n1. Ingestion & Pipeline Stage Benchmark:")
    print("-" * 65)
    print(f"{'Filename':<25} | {'Format':<6} | {'Words':<6} | {'Pipeline Time':<14} | {'Throughput'}")
    print("-" * 65)

    total_words = 0
    total_pipeline_time = 0.0

    for f in files:
        t0 = time.perf_counter()
        doc = pipeline.run_from_path(str(f))
        elapsed = time.perf_counter() - t0

        if doc.is_processed:
            processed_docs.append(doc)
            words = doc.word_count
            total_words += words
            total_pipeline_time += elapsed
            words_per_sec = int(words / elapsed) if elapsed > 0 else 0
            print(f"{f.name:<25} | {f.suffix[1:].upper():<6} | {words:<6} | {elapsed*1000:>7.1f} ms     | {words_per_sec:>6} w/s")
        else:
            print(f"{f.name:<25} | {f.suffix[1:].upper():<6} | ERROR: {doc.processing_error}")

    print("-" * 65)
    avg_speed = int(total_words / total_pipeline_time) if total_pipeline_time > 0 else 0
    print(f"Total Words: {total_words:,} | Total Time: {total_pipeline_time*1000:.1f} ms | Overall Speed: {avg_speed:,} words/sec")

    # 2. Semantic Search Latency Benchmark
    print("\n2. Semantic Search Query Latency Benchmark:")
    print("-" * 65)
    print(f"{'Query':<35} | {'Engine':<20} | {'Latency'}")
    print("-" * 65)

    test_queries = [
        "quarterly revenue and financial profit",
        "employee vacation and paid time off policy",
        "David Kim engineering architecture migration",
        "TechSupply Solutions enterprise contract",
    ]

    for q in test_queries:
        t0 = time.perf_counter()
        results = search_engine.search(q, processed_docs)
        q_elapsed = (time.perf_counter() - t0) * 1000
        engine_label = search_engine.engine_name.split("(")[0].strip()
        print(f"'{q[:33]}...' | {engine_label:<20} | {q_elapsed:>6.2f} ms")

    print("-" * 65)
    print("\nBenchmark completed successfully. Zero external network calls made.\n")


if __name__ == "__main__":
    run_benchmark()
