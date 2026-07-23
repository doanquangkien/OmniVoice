# Tech Stack — OmniVoice

> **Công nghệ đang dùng.** Cập nhật khi thay đổi version hoặc thêm dependency.

---

## Runtime

| Thành phần | Version | Ghi chú |
|---|---|---|
| **Python** | 3.13.1 | Yêu cầu >= 3.10 |
| **PyTorch** | 2.11.0+cu128 | CUDA 12.8 |
| **torchaudio** | 2.11.0+cu128 | |
| **CUDA** | 12.8 | Driver 596.36 |

## Core Dependencies

| Package | Version | Mục đích |
|---|---|---|
| `transformers` | 5.13.0 | Model loading, Whisper ASR |
| `accelerate` | 1.14.0 | Multi-GPU, device mapping |
| `soundfile` | 0.14.0 | Audio I/O |
| `librosa` | 0.11.0 | Audio processing |
| `numpy` | 2.3.5 | Array operations |
| `pydub` | 0.25.1 | Audio format conversion |
| `gradio` | 6.20.0 | Web demo UI |

## Optional Dependencies

| Package | Extra | Mục đích |
|---|---|---|
| `WeTextProcessing` | `[tn]` | Text normalization (zh/en) |
| `num2words` | `[tn]` | Integer-to-words fallback |
| `jiwer` | `[eval]` | WER calculation |
| `s3prl` | `[eval]` | Speech representations |
| `funasr` | `[eval]` | ASR models for evaluation |

## Build

| Công cụ | Version | Mục đích |
|---|---|---|
| `hatchling` | (pyproject) | Build backend |
| `uv` | latest | Package manager |

## Local Hardware

| Thành phần | Spec |
|---|---|
| **GPU** | Quadro T1000 (Turing, 4GB VRAM, Compute 7.5) |
| **Driver** | 596.36 |
| **OS** | Windows 10 Pro 19045 |
| **RAM** | (hệ thống) |

## Cloud (Colab)

| Thành phần | Spec |
|---|---|
| **GPU Free** | T4 (16GB VRAM) |
| **GPU Pro** | T4 / L4 / A100 |
| **Runtime** | Python 3.10+, PyTorch pre-installed |

## Model

| Thành phần | Spec |
|---|---|
| **OmniVoice** | 0.6B params (Qwen/Qwen3-0.6B-Base) |
| **ASR (optional)** | openai/whisper-large-v3-turbo (~1.5B params) |
| **Precision** | float16 (default) |
| **Sample rate** | 24000 Hz |
