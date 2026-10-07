# InBoost AI Proxy — Empirical Benchmarks & Evaluation Artifacts

This directory contains public predictions, evaluation manifests, and official Docker test harness reports for **SWE-bench Verified** evaluations comparing vanilla LLM coding agents with agents running through **InBoost AI Proxy**.

---

## 🔬 Benchmark Methodology & Two Evaluation Layers

To maintain complete scientific and engineering transparency, we explicitly differentiate between two distinct layers of evaluation:

| Evaluation Layer | Scope | How It Is Measured | Metric Reported |
| :--- | :--- | :--- | :--- |
| **Layer 1: Official Test Resolve Rate** | Does the generated patch actually solve the bug without regressing other unit tests? | Evaluated in isolated Docker containers via the **official Princeton SWE-bench harness** (`swebench.harness.run_evaluation`). | **Resolved Rate (%)** (`FAIL_TO_PASS` passed, `PASS_TO_PASS` preserved) |
| **Layer 2: Agent Execution Reliability** | Did the agent crash, loop infinitely, or abort with a 0-byte patch before testing? | Measured via **InBoost AI Proxy session instrumentation & token accounting** during agent execution. | **First-Attempt Patch Delivery Rate**, **0-Byte Abort Rate**, **Latency**, **Inference Cost Delta** |

> [!IMPORTANT]
> Official SWE-bench does not natively track wall-clock turnaround time, token spend, or circular search loops. All throughput, latency, and cost reduction numbers are measured from InBoost AI Proxy's L7 gateway telemetry and provider token accounting.

---

## 📊 Summary of Official SWE-bench Docker Harness Results

### Cohort 1: SWE-bench Verified 10 (MiniMax-M3 on SiliconFlow)
- **Directory:** [`benchmarks/swebench_verified_10/`](./swebench_verified_10/)
- **Target Model:** MiniMax-M3 (`minimax/MiniMax-Text-01`)
- **Official Docker Resolve Rate:**
  - **Baseline (Vanilla Agent):** **20.0% (2 / 10)**
  - **With InBoost AI Proxy:** **50.0% (5 / 10)** — **+150% relative gain (2.5x)**
- **0-Byte Diff Collapses:** Baseline failed on 7 / 10 tasks (70%) with empty diffs. InBoost rescued 6 tasks to produce valid patches.
- **Latency / Cost:** 722.9s → 327.5s (**-54.7% faster**), $0.1667 → $0.0928 (**-44.3% spend reduction**).

### Cohort 2: SWE-bench Verified 25 (DeepSeek-V4)
- **Directory:** [`benchmarks/swebench_verified_25/`](./swebench_verified_25/)
- **Target Model:** DeepSeek-V4
- **Official Docker Resolve Rate:**
  - **Baseline (Vanilla Agent):** **24.0% (6 / 25)**
  - **With InBoost AI Proxy:** **52.0% (13 / 25)** — **+116% relative gain (2.16x)**
- **0-Byte Diff Collapses:** Baseline failed on 17 / 25 tasks (68%). InBoost rescued 9 tasks.

---

## 🛠️ Independent Reproduction (Single Command)

You can reproduce the official SWE-bench evaluation on any machine with Docker and Python 3.10+:

```bash
# 1. Install official SWE-bench harness
pip install swebench

# 2. Run official evaluation on InBoost predictions (Cohort 10)
python3 -m swebench.harness.run_evaluation \
  --dataset_name princeton-nlp/SWE-bench_Verified \
  --predictions_path benchmarks/swebench_verified_10/predictions_inboost.jsonl \
  --run_id inboost_verified_10_eval \
  --max_workers 4

# 3. Run official evaluation on Baseline predictions (Cohort 10)
python3 -m swebench.harness.run_evaluation \
  --dataset_name princeton-nlp/SWE-bench_Verified \
  --predictions_path benchmarks/swebench_verified_10/predictions_baseline.jsonl \
  --run_id baseline_verified_10_eval \
  --max_workers 4
```

The harness will build the isolated Docker environment for each repository, run the test suites, and generate a verified `report.json` matching the provided official harness reports.
