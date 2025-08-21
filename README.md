# Evolution Grader

Evolution Grader is a modern C++ autograder designed to act as a tutor rather than a judge. It provides layered feedback, emphasizes reproducibility and security, and scales for coursework and exams.

## Vision

- **Feedback that teaches**: compile diagnostics, unit and property tests with minimal counterexamples, sanitizer and Valgrind reports, static analysis suggestions, and plain-language explanations linked to course notes.
- **Fair, reproducible, and secure**: sandboxed execution with fixed resource limits, deterministic seeds, and support for multiple compilers.
- **Integrity & scale**: similarity checking with human review, worker pools with retries, immutable artifacts.
- **Instructor and TA experience**: tests in GoogleTest/Catch2/doctest, YAML problem metadata, CI validation, analytics on common failures.

## Architecture Overview

1. **Frontend** – student/TA portal for submissions, feedback, diffs, leaderboards, and analytics.
2. **API & Orchestrator** – accepts submissions, enqueues jobs, aggregates JSON results.
3. **Worker Pods** – compile with clang++/g++, run tests, sanitizers, Valgrind, clang-tidy/format/cppcheck, emit `results.json`.
4. **Sandbox** – isolate/nsjail based execution with CPU/memory limits and no network.
5. **Storage** – PostgreSQL for metadata and S3-compatible store for artifacts.
6. **Similarity Service** – periodic MOSS/JPlag runs for manual review.

## Testing & Analysis Stack

- **Correctness**: GoogleTest, Catch2, or doctest, with optional property-based tests via RapidCheck.
- **Dynamic bug finding**: AddressSanitizer, UndefinedBehaviorSanitizer, and optional Valgrind.
- **Static & style**: clang-tidy, cppcheck, and clang-format.

## Phase 1 Defaults

- Sandbox: isolate
- C++ standard: C++20
- Warning policy: `-Wall -Wextra -Werror -Wshadow -Wconversion -pedantic`
- Default sanitizers: AddressSanitizer and UndefinedBehaviorSanitizer
- Results schema: [schema/results.schema.json](schema/results.schema.json)

## Phase 2 MVP Pipeline

- FastAPI endpoint to submit code for grading
- Worker that compiles with both `g++` and `clang++`, runs GoogleTest suites
- AddressSanitizer/UndefinedBehaviorSanitizer build for memory safety checks
- Static analysis via `clang-tidy`, `clang-format`, and `cppcheck`
- Aggregated `results.json` emitted for each submission

## Phase 3 Learning Features

- Property-based tests using RapidCheck for deeper correctness checks
- Local CLI (`python -m grader.cli <problem>`) so students can run the same checks in Docker
- Curated hint mapping that converts common compiler and sanitizer messages into plain-language tips

## Grading Rubric (template)

| Dimension                            | Typical Weight |
|-------------------------------------|----------------|
| Correctness (visible + hidden tests)| 60–70%         |
| Memory safety / UB                  | 15–20%         |
| Performance envelope                | 5–10%          |
| Style & static analysis             | 0–10%          |
| Optional student-authored tests     | 0–10%          |

## Security & Determinism

- Execute code in isolate/nsjail with network disabled, seccomp, cgroup limits, and tmpfs sandboxes.
- Pin toolchain versions and fix random seeds for consistent results.
- Ship hidden tests at run time from a secure artifact store.
- Regular similarity detection; results treated as signals and escalated for human review.

## UX That Supports Learning

- **Student view**: compile output, visible test names with short hints, hidden test summaries, sanitizer logs with fix-it tips, diff views, property-based counterexamples, cool-down resubmissions, and downloadable Docker packs.
- **Instructor/TA view**: dashboards with failure heatmaps, common sanitizer errors, slowest tests, and access to build artifacts.

## Build Phases

The roadmap is organized into phased development. See [project.md](project.md) for task tracking.

---

This README summarizes the high-level goals and architecture for building a learning-first C++ autograder.

