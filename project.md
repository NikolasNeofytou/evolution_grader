# Project Plan

This document tracks the phased build of Evolution Grader.

## Phase 1 — Decisions & Skeleton
- [x] Choose sandbox (isolate or nsjail)
- [x] Define results.json schema
- [x] Set C++ standard and warning policy
- [x] Author first problems with visible and hidden tests

## Phase 2 — MVP Pipeline
- [x] Implement API & queue
- [x] Dockerized worker builds with clang++/g++
- [x] Run tests, ASan/UBSan, optional Valgrind
- [x] Run clang-tidy/format/cppcheck
- [x] Aggregate to results.json
- [x] Minimal web UI for upload/status/results with diffs

## Phase 3 — Learning Features
- [x] Property-based tests with RapidCheck
- [x] Local CLI for prechecks
- [x] Curated hint mapping from errors to course notes

## Phase 4 — Scale & Reliability
- [x] Autoscale workers and artifact store
- [x] Retries and rejudge tools
- [x] Instructor analytics and gradebook integration

## Phase 5 — Integrity & Exam Mode
- [x] MOSS/JPlag similarity detection with TA triage
- [x] Exam mode with frozen visible tests and stricter limits
- [x] Optional lockdown browser

## Phase 6 — Nice-to-haves
- [ ] Performance envelopes and complexity checks
- [ ] Opt-in leaderboard
- [ ] Additional language support (C, Python, MATLAB)
- [ ] Project-based autograding (CMake, multi-file)

Each task starts as unchecked and will be updated as work progresses.

