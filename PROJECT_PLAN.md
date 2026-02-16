# PROJECT_PLAN — Streaming Diarized STT with Bounded-Delay Speaker Label Stabilization

## 0) What you’re building (read this first)
Build a **real-time diarized speech-to-text (STT)** system that outputs an incremental transcript with **stable speaker labels**. The research centerpiece is a **bounded-delay stabilization algorithm**: the system can revise speaker labels within the last `D` seconds to reduce speaker flips while keeping latency low.

By the end, you should have:
- **A streaming demo**: incremental transcript events, with revisions inside the last `D` seconds
- **A reproducible eval harness**: DER/JER, flip-rate, latency/RTF, plots vs `D`
- **A production-shaped service**: containerized, observable, testable, with a runbook

## 1) How to use this plan (daily/weekly rhythm)
- **Daily cadence (5h/day)**:
  - 60–90 min reading/notes (until that week’s reading list is done)
  - 3–3.5h implementation
  - 30–60 min eval + writing (plots, runbook notes, failure cases)
- **Weekly cadence**:
  - finish “Reading” early in the week (it’s intentionally bounded)
  - build “Deliverables”
  - verify “Definition of Done” before moving on

## 2) Quick glossary (keep this mental model)
- **ASR**: automatic speech recognition (audio → words).
- **Diarization**: “who spoke when?” (audio → speaker turns).
- **Diarized STT**: ASR text attributed to speakers (who said what, when).
- **VAD**: voice activity detection (speech vs non-speech).
- **RTTM**: a standard text format for speaker turn annotations/predictions.
- **DER / JER**: diarization error rates (scoring for diarization quality).
- **WER / CER**: word/character error rate (scoring for ASR quality).
- **RTF**: real-time factor; `RTF = processing_time / audio_duration` (lower is better; `< 1` is faster than realtime).
- **Latency**: how long after audio arrives you emit text/labels (report p50/p95).
- **Stabilization window `D`**: how far back you’re allowed to revise speaker labels to reduce flipping.

## 3) Table of contents
- [Overview (objectives and non-goals)](#4-overview-objectives-and-non-goals)
- [Architecture (system diagram and components)](#5-architecture-system-diagram-and-components)
- [Work plan (Week 0–6)](#6-work-plan-week-06-25hweek)
- [Evaluation plan (metrics + plots)](#7-evaluation-plan-metrics--plots)
- [Production plan (deploy/operate)](#8-production-plan-deployoperate)
- [Datasets + repo structure](#9-datasets--repo-structure)
- [Debugging ladder (what to check first)](#10-debugging-ladder-what-to-check-first)
- [Appendix: concepts + reading list](#appendix-concepts--bounded-reading-list)

## 4) Overview (objectives and non-goals)
**Objectives**
- **Base (must-have)**: end-to-end diarized STT (streaming or pseudo-streaming) with clear outputs and reproducible evaluation.
- **Research-level signal**: a principled stabilization method with quantified tradeoffs: stability vs delay vs DER/WER vs latency.
- **Production signal (must-have for target role)**: a deployable, maintainable service with clear interfaces, observability, reproducibility, and latency budgeting.

**Non-goals (keep scope realistic)**
- training/fine-tuning new ASR or embedding models from scratch
- chasing SOTA leaderboard numbers
- full multi-tenant production infrastructure (auth, billing, etc.)

## 5) Architecture (system diagram and components)

### 5.1 System overview (ASCII diagram)
```
                   (streaming audio frames)                (finalized audio)
  ┌───────────┐     20–40 ms hop / 0.5–2 s chunks        ┌──────────────────┐
  │   Client  │ ───────────────────────────────────────▶ │  Ingest/Buffer   │
  └─────┬─────┘                                          └───────┬──────────┘
        │                                                      fan-out
        │                                               ┌─────────┴──────────┐
        │                                               │                    │
        │                                       ┌───────▼───────┐    ┌──────▼───────┐
        │                                       │  VAD + Segm.   │    │   ASR Decode  │
        │                                       │ (hysteresis,   │    │ (chunked;     │
        │                                       │  hangover)     │    │  timestamps)  │
        │                                       └───────┬───────┘    └──────┬────────┘
        │                                               │                    │
        │                                       speech segments        word timestamps
        │                                               │                    │
        │                                       ┌───────▼────────┐   ┌──────▼────────┐
        │                                       │ Speaker Embeds  │   │ Word/Seg Align │
        │                                       │ (pretrained)    │   │ (attribution)  │
        │                                       └───────┬────────┘   └──────┬────────┘
        │                                               │                    │
        │                                     online assignment/clustering    │
        │                                               │                    │
        │                                       ┌───────▼────────────────────▼───────┐
        │                                       │  Bounded-Delay Label Stabilizer     │
        │                                       │  - revise last D seconds            │
        │                                       │  - penalize speaker switches        │
        │                                       │  - optional overlap policy          │
        │                                       └───────┬────────────────────────────┘
        │                                               │
        │                                      incremental diarized transcript
        │                                               │
        │                                       ┌───────▼─────────┐
        └───────────────────────────────────────│   API / Outputs  │
                                                │ JSON + TXT/MD    │
                                                │ metrics hooks    │
                                                └──────────────────┘
```

### 5.2 Key idea: bounded-delay speaker label stabilization
**Problem**
In streaming diarization, speaker IDs can **flip** (A↔B) and fragment due to short pauses, noise, backchannels, and embedding uncertainty. Users experience this as an unstable transcript even if batch diarization is acceptable.

**Approach (high level)**
Maintain persistent speaker identities, but allow a small retroactive correction window of `D` seconds.

At each time step:
1. Produce a provisional speaker labeling for new segments (online assignment/clustering).
2. For the rolling window `[t - D, t]`, re-optimize the mapping from “recent cluster labels” to “persistent speaker IDs” with a **switch penalty** to discourage flips.
3. Emit outputs with:
   - **stable labels** for times `< t - D` (frozen)
   - **revisable labels** within the last `D` seconds

**What you will implement (you own this)**
- **Online speaker tracking**:
  - speaker prototypes `μ_k` updated online (EMA or count-weighted average)
  - distance gating (cosine / PLDA-like score proxy)
  - “new speaker” creation and “inactive speaker” decay rules
- **Stabilization**:
  - bounded window relabeling via:
    - bipartite matching between recent clusters and persistent IDs, and/or
    - Viterbi-style resegmentation with a **switch cost**
  - output revision policy and “finalization” boundary at `t - D`

### 5.3 Components (what to build vs what to use)
**Use off-the-shelf (for speed)**
- **ASR**: `faster-whisper` (or similar) for chunked decoding + timestamps
- **Speaker embedding model**: pretrained ECAPA/x-vector-like embedding extractor

**Build yourself (for interview signal)**
- **VAD + segmentation policy**: hysteresis + hangover + min/max duration; chunking tuned for latency
- **Online diarization core**: assignment/clustering with prototype updates, gating, lifecycle
- **Bounded-delay stabilizer**: retroactive correction within `D`; switch-penalized relabeling
- **Word-to-speaker attribution**: map ASR word timestamps to stabilized speaker turns; define overlap policy
- **Evaluation harness**: reproducible runs from manifests; metrics + plots + report

### 5.4 Outputs (artifacts you’ll produce)
**Primary**
- **Incremental transcript stream** (demo): partial text + timecodes + speaker labels; revisions allowed in last `D` seconds
- **Final transcript**:
  - JSON (segments, words, speakers, confidences, timestamps)
  - TXT/Markdown (human-readable)

**Secondary**
- RTTM-like diarization output (for evaluation)
- A short mini-report inside the repo (`reports/`), generated by eval scripts

## 6) Work plan (Week 0–6, ~25h/week)
Assume ~**5 hours/day**, ~**25 hours/week**. Reading is intentionally bounded and chosen to be universal/transferable. Reading is placed ~1 week ahead of the coding it enables.

### Week 0 — setup + “speech systems primer” (prep before writing real code)
**Goal**: remove unknown-unknowns and make Week 1 implementation smooth.

**Reading (finish before Week 1)**
- Speech pipeline overview + terminology: [Speech and Language Processing (draft)](https://web.stanford.edu/~jurafsky/slp3/)
- What diarization is + standard pipeline blocks: [pyannote-audio](https://github.com/pyannote/pyannote-audio)
- Tooling familiarity (ASR API/perf): [faster-whisper](https://github.com/SYSTRAN/faster-whisper)

**Deliverables**
- Working dev env (local or Docker) + minimal “hello audio” script:
  - load audio, compute duration
  - chunk into frames (e.g., 20–40 ms hop) and print chunk timing
- Decide runtime mode(s): CPU-only vs GPU; document what you’ll benchmark against
- Create a 1-page glossary in the repo (VAD, DER, RTTM, embeddings, diarization, RTF, latency)

**Definition of Done**
- Script prints audio duration + chunk boundaries without errors
- You can explain what each block in the system diagram does and what it outputs
- You have a written (rough) latency budget and you know what you’ll measure (RTF + p50/p95 latency)

### Week 1 — skeleton + offline E2E (deliver something you can show)
**Reading (finish early this week; prepares Week 2)**
- VAD/segmentation reference: [pyannote-audio tutorials](https://github.com/pyannote/pyannote-audio/tree/develop/tutorials)
- ASR practicalities + timestamps: [faster-whisper](https://github.com/SYSTRAN/faster-whisper)

**Deliverables**
- Offline pipeline on an audio file: preprocess → VAD → embeddings → diarization (online emulation) → ASR → attribution → outputs
- Define JSON schema and create one end-to-end sample output (JSON + MD/TXT)
- Pick a tiny “gold” set (30–60 min) + `data/manifest.jsonl`; make eval runs reproducible
- Add stage timers + basic logging from day 1

**Definition of Done**
- One command/script produces: diarized transcript (JSON + MD/TXT) + minimal RTTM-like output
- `data/manifest.jsonl` exists + an example entry; eval runnable on gold set with fixed config
- JSON schema documented in `src/schemas/` (or equivalent) and versioned
- Logs include per-stage timings for: VAD/segmentation, embeddings, diarization, ASR, fusion

### Week 2 — VAD/segmentation + online diarization baseline (make it measurable)
**Reading (prepares Week 3)**
- Speaker embeddings + scoring references: [SpeechBrain](https://github.com/speechbrain/speechbrain), [pyannote-audio](https://github.com/pyannote/pyannote-audio), [NVIDIA NeMo](https://github.com/NVIDIA/NeMo)
- Diarization metrics (DER/JER + collar + UEM): [pyannote.metrics basics](https://pyannote.github.io/pyannote-metrics/basics.html), [tutorial](https://pyannote.github.io/pyannote-metrics/tutorial.html)
- Optional RTTM scoring reference: [dscore](https://github.com/nryant/dscore)
- State + smoothing intuition: [CS188 HMMs](https://inst.eecs.berkeley.edu/~cs188/textbook/hmms/), [Viterbi](https://inst.eecs.berkeley.edu/~cs188/textbook/hmms/viterbi.html)

**Deliverables**
- Implement streaming-ish VAD + segmentation policy (hysteresis, hangover, min/max duration)
- Implement online speaker state (prototypes, gating, new-speaker logic, inactive decay)
- Build naive online baseline (no stabilization) and measure DER/JER + flip-rate on gold set
- Stand up `eval/` to compute metrics + emit first plots (even if ugly)

**Definition of Done**
- One `eval/` command computes at least: DER (or a clearly stated proxy) and flip-rate
- Baseline report artifact (1-page Markdown is fine): dataset description + baseline metrics + 3 failure modes
- Online speaker tracking deterministic given fixed seed/config

### Week 3 — bounded-delay stabilizer (the research centerpiece)
**Reading (prepares Week 4)**
- Assignment / matching: [Bipartite Matching Notes (Goemans)](https://math.mit.edu/~goemans/18433S09/matching-notes.pdf)
- Dynamic programming refresher (Viterbi framing): continue [CS188 Viterbi](https://inst.eecs.berkeley.edu/~cs188/textbook/hmms/viterbi.html)
- Streaming ASR buffering ideas (not a dependency): [whisper_streaming](https://github.com/ufal/whisper_streaming)

**Deliverables**
- Implement stabilization with bounded `D` and a switch penalty; revise labels in last `D` seconds
- Produce flip-rate vs `D` and DER vs `D` curves; write “how to choose `D`” guidance
- Ablate at least: switch penalty strength, prototype update rule, gating threshold

**Definition of Done**
- Revision semantics work: final for time `< now - D`, revisable for time `>= now - D`
- Evaluate at least 3 values of `D` (include `D=0`) + plot results
- Unit tests cover stabilizer corner cases (speaker appears/disappears, short backchannels)

### Week 4 — streaming demo + attribution + latency instrumentation
**Reading (prepares Week 5)**
- Timestamp alignment and attribution pitfalls: [WhisperX](https://github.com/m-bain/whisperX)

**Deliverables**
- Pseudo-streaming demo (read file as chunks) and/or true streaming input
- Word-to-speaker attribution: word timestamps → stabilized turns; document overlap policy
- Instrument end-to-end latency and RTF; report p50/p95 latency; enforce a latency budget
- Emit incremental transcript events supporting revisions inside last `D` seconds

**Definition of Done**
- Demo script ingests audio incrementally and visibly revises speaker labels within last `D` seconds
- You can report RTF and p50/p95 emission latency on the gold set
- Attribution policy is documented with at least one concrete example

### Week 5 — productionization (deployable + operable)
**Reading (prepares Week 6)**
- Read two chapters from the open Google SRE book (bounded, universal):
  - Monitoring distributed systems
  - The four golden signals
  - Start here: [Google SRE book](https://sre.google/sre-book/table-of-contents/)

**Deliverables**
- Dockerize service (CPU + optional GPU). Single command to run demo + single command to run eval
- Structured logging + metrics endpoint; expose per-stage timings and queue depth
- Tests:
  - unit tests for stabilizer + attribution edge cases
  - one integration “golden” test (short audio) with tolerant assertions
- Runbook section: tuning knobs, expected failure modes, how to debug

**Definition of Done**
- From-scratch setup works: build image → run demo → run eval
- Service exposes health + metrics endpoints; logs are structured (JSON recommended)
- Backpressure behavior is explicit and tested
- At least one performance knob has before/after measurements (chunk size, beam size, batch size)

### Week 6 — polish to interview-ready (report + story + robustness)
**Deliverables**
- Ablations + error analysis write-up; generate final `reports/` mini-paper (plots + conclusions)
- Robustness pass: silence/noise, short backchannels, rapid turns, overlap (document clearly)
- Improve UX of outputs (clean Markdown transcript); configs reproducible/pinned
- Final demo script + screenshots (or short recording)

**Definition of Done**
- `reports/` contains: flip-rate vs `D`, DER vs `D`, latency vs `D`, ablation table, short error analysis w/ examples
- Repo reads like a shipped project: README quickstart + architecture + tuning guide + limitations
- You can do a 10–15 min live demo end-to-end without handwaving

## 7) Evaluation plan (metrics + plots)
**Metrics**
- Diarization: DER (with collar), JER; breakdown: miss / false alarm / confusion; optional overlap-aware breakdown
- ASR: WER/CER; speaker-attributed WER proxy (document limitations clearly)
- Streaming-specific: flip-rate; latency (p50/p95); RTF

**Baselines**
- Naive online: greedy speaker assignment without stabilization
- Batch-ish: diarization on finalized audio (upper bound) for comparison

**Plots you must produce**
- Flip-rate vs `D` (e.g., `D ∈ {0, 0.5, 1, 1.5, 2, 3}` seconds)
- DER vs `D`
- Latency vs `D`
- Ablation table: VAD hangover, chunk size, prototype update rule, thresholding

## 8) Production plan (deploy/operate)
Minimum production deliverables (bounded, single-service):
- **Service interface**:
  - WebSocket (or gRPC) streaming endpoint for audio frames + incremental transcript events
  - file-based batch endpoint/CLI for reproducible evaluation
- **Packaging + reproducibility**:
  - `pyproject.toml` / `requirements.txt` pinned + a `Makefile` (or task runner)
  - Docker image build; GPU optional; known-good config checked into the repo
- **Observability**:
  - structured logs, request IDs, per-stage timings (VAD, embed, diarize, ASR, fusion, stabilizer)
  - metrics endpoint: RTF, p50/p95 latency, GPU/CPU utilization (best effort), queue depth/backpressure
- **Operational safety**:
  - backpressure policy (drop/compact frames, or increase chunk size) and explicit latency budget
  - deterministic eval mode (seeded); graceful degradation if embeddings/ASR fail
- **Maintainability**:
  - unit tests for stabilization + attribution; integration test on a tiny “gold” fixture audio
  - clear runbook: how to run/debug/tune; common failure modes

## 9) Datasets + repo structure
**Datasets (choose based on availability)**
- Prefer multi-speaker datasets with speaker turn annotations (for DER)
- Use a small curated gold set (30–60 minutes total) for stable iteration
- If full diarization labels are hard, start with a small manually annotated subset (enough to show DER trends)

**Repo structure (planned)**
- `src/`
  - `audio/` preprocessing utilities
  - `vad/` streaming VAD + segmentation
  - `embeddings/` speaker embedding extraction wrapper
  - `diarization/` online clustering + speaker state
  - `stabilization/` bounded-delay relabeling
  - `asr/` chunked decoding wrapper
  - `fusion/` word-to-speaker attribution + overlap policy
  - `schemas/` output schema definitions
- `scripts/` (`run_stream_demo.*`, `run_offline_pipeline.*`)
- `eval/` (metrics + plots + report generation)
- `data/` (`manifest.jsonl` format + download notes; no raw data committed)
- `reports/` (generated plots + markdown report)

## 10) Debugging ladder (what to check first)
When metrics are bad, debug in this order (cheapest checks first):
1. **Audio IO + chunking sanity**: correct sample rate? correct timestamps? no drift?
2. **VAD/segmentation**: are you missing speech? are segments too short/long? hangover too aggressive?
3. **ASR timestamps**: do word/segment timestamps look plausible? are chunks causing truncation/repeats?
4. **Embeddings quality**: do same-speaker segments cluster in cosine space? any obvious domain mismatch?
5. **Online diarization**: thresholds too tight/loose? new-speaker creation exploding? prototypes drifting?
6. **Stabilizer**: switch penalty too low/high? revision window `D` too small/large? mapping logic stable?
7. **Attribution policy**: overlap handling causing wrong speaker tags on words?

## Success criteria
- Clear, reproducible improvement: stabilization reduces flip-rate substantially with acceptable DER impact
- A crisp report explaining: why it works, where it fails, how to tune `D` for product needs
- A demo that feels like a product capability: stable speaker-labeled incremental transcript

## Appendix: concepts + bounded reading list
You do not need to become a speech PhD to ship this. You do need working knowledge of:
- Audio + framing basics: sample rate, frames/hops, log-mel vs raw waveform (only as needed)
- VAD + segmentation: hysteresis, hangover, min/max durations, turn-taking edge cases
- Embeddings + similarity: cosine similarity, centroid/prototype updates (EMA), threshold calibration
- Online clustering / speaker tracking: gating, new-speaker creation, speaker “activity” decay
- Sequence smoothing: HMM intuition, Viterbi dynamic programming, switch costs
- Assignment / matching: bipartite matching / Hungarian method for label mapping
- ASR practicalities: chunking, timestamps, beam search basics, buffering/latency
- Evaluation: DER/JER, collars, confusion breakdown; flip-rate as a streaming UX metric
- Production: batching vs latency, backpressure, timeouts, metrics/logging, reproducible configs

