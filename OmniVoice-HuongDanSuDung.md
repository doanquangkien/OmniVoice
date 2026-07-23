# OmniVoice — Hướng Dẫn Sử Dụng Toàn Diện

> **Nguồn**: [github.com/k2-fsa/OmniVoice](https://github.com/k2-fsa/OmniVoice) — Phiên bản 0.2.1
>
> OmniVoice là mô hình Text-to-Speech (TTS) zero-shot đa ngôn ngữ, hỗ trợ **646 ngôn ngữ** với tổng cộng 581k giờ dữ liệu huấn luyện. Xây dựng trên kiến trúc Diffusion Language Model, tốc độ inference nhanh gấp **40 lần real-time** (RTF ~0.025).

---

## Mục lục

1. [Tính năng chính](#1-tính-năng-chính)
2. [Cài đặt](#2-cài-đặt)
3. [Ba chế độ sinh giọng nói](#3-ba-chế-độ-sinh-giọng-nói)
   - [Voice Cloning](#31-voice-cloning-sao-chép-giọng)
   - [Voice Design](#32-voice-design-thiết-kế-giọng)
   - [Auto Voice](#33-auto-voice)
4. [Tham số điều khiển sinh](#4-tham-số-điều-khiển-sinh-generation-parameters)
5. [Điều khiển phi ngôn ngữ & phát âm](#5-điều-khiển-phi-ngôn-ngữ--phát-âm)
6. [Sinh giọng dài (Long-form)](#6-sinh-giọng-dài-long-form)
7. [Voice Cloning nâng cao](#7-voice-cloning-nâng-cao)
8. [Voice Design chi tiết](#8-voice-design-chi-tiết)
9. [CLI Tools](#9-cli-tools)
10. [Training & Fine-tuning](#10-training--fine-tuning)
11. [Evaluation](#11-evaluation)
12. [Mẹo & lưu ý quan trọng](#12-mẹo--lưu-ý-quan-trọng)
13. [Danh sách ngôn ngữ hỗ trợ](#13-danh-sách-ngôn-ngữ-hỗ-trợ)

---

## 1. Tính năng chính

| Tính năng | Mô tả |
|---|---|
| **646+ ngôn ngữ** | Phủ ngôn ngữ rộng nhất trong các mô hình TTS zero-shot |
| **Voice Cloning** | Sao chép giọng nói từ audio tham chiếu ngắn (3-10 giây) |
| **Voice Design** | Thiết kế giọng nói qua thuộc tính: giới tính, tuổi, cao độ, accent, dialect... |
| **Non-verbal** | Chèn âm thanh phi ngôn ngữ: `[laughter]`, `[sigh]`, `[surprise-ah]`... |
| **Sửa phát âm** | Pinyin (tiếng Trung), CMU phoneme (tiếng Anh) |
| **Tốc độ cao** | RTF thấp nhất 0.025 — nhanh hơn real-time 40 lần |
| **Kiến trúc Diffusion LM** | Thiết kế tinh gọn, scalable |

---

## 2. Cài đặt

### Yêu cầu

- Python >= 3.10
- PyTorch >= 2.4 (khuyến nghị 2.8.0)
- GPU NVIDIA (CUDA) / Apple Silicon (MPS) / Intel Arc (XPU)

### Cách 1: pip

```bash
# B1: Cài PyTorch
# NVIDIA GPU:
pip install torch==2.8.0+cu128 torchaudio==2.8.0+cu128 --extra-index-url https://download.pytorch.org/whl/cu128

# Apple Silicon:
pip install torch==2.8.0 torchaudio==2.8.0

# Intel Arc GPU (XPU):
pip install torch torchaudio --index-url https://pytorch-extension.intel.com/release-whl/stable/xpu/us/

# B2: Cài OmniVoice
pip install omnivoice                                          # Từ PyPI (bản ổn định)
pip install git+https://github.com/k2-fsa/OmniVoice.git        # Từ GitHub (mới nhất)
pip install -e .                                               # Dev mode (clone repo trước)

# Optional: text normalization
pip install "omnivoice[tn]"

# Optional: evaluation
pip install "omnivoice[eval]"
```

### Cách 2: uv (nhanh hơn)

```bash
git clone https://github.com/k2-fsa/OmniVoice.git
cd OmniVoice
uv sync
# Dùng mirror nếu mạng chậm:
uv sync --default-index "https://mirrors.aliyun.com/pypi/simple"

# Với extras:
uv sync --extra tn
uv sync --extra eval
```

---

## 3. Ba chế độ sinh giọng nói

### 3.1 Voice Cloning (Sao chép giọng)

Sao chép giọng từ audio tham chiếu ngắn. Đây là chế độ **ổn định nhất**.

```python
from omnivoice import OmniVoice
import soundfile as sf
import torch

# Khởi tạo model
model = OmniVoice.from_pretrained(
    "k2-fsa/OmniVoice",
    device_map="cuda:0",      # Apple Silicon: "mps", Intel Arc: "xpu"
    dtype=torch.float16
)

# Sinh giọng nói — có ref_text
audio = model.generate(
    text="Xin chào, đây là bản sao giọng nói.",
    ref_audio="ref.wav",
    ref_text="Nội dung của audio tham chiếu.",
)

# Sinh giọng nói — KHÔNG ref_text (tự động dùng Whisper ASR)
audio = model.generate(
    text="Xin chào, đây là bản sao giọng nói.",
    ref_audio="ref.wav",
)

sf.write("out.wav", audio[0], 24000)  # Sample rate mặc định: 24kHz
```

**Mẹo khi dùng Voice Cloning:**

- Audio tham chiếu nên dài **3-10 giây** — dài hơn làm chậm inference và có thể giảm chất lượng
- Clone cùng ngôn ngữ giữa audio tham chiếu và văn bản đích cho phát âm chuẩn nhất
- Clone cross-lingual: giọng sẽ mang accent của ngôn ngữ tham chiếu
- Chuẩn hóa chữ số Ả Rập: `"I have 2345 apples."` → truyền `normalize_text=True` (cần `pip install "omnivoice[tn]"`)
- Có thể chỉ định model Whisper khác hoặc thiết bị ASR riêng qua `asr_model_name="..."` và `asr_device="cuda:1"` trong `from_pretrained()`

### 3.2 Voice Design (Thiết kế giọng)

Tạo giọng nói qua mô tả thuộc tính — **không cần audio tham chiếu**.

```python
audio = model.generate(
    text="This is a test for voice design.",
    instruct="female, young adult, high pitch, british accent",
)
```

> **Lưu ý**: Voice Design chỉ được huấn luyện trên dữ liệu tiếng Trung và tiếng Anh. Có thể hoạt động với ngôn ngữ khác nhưng có thể không ổn định với ngôn ngữ ít tài nguyên.

### 3.3 Auto Voice

Để model tự chọn giọng ngẫu nhiên:

```python
audio = model.generate(text="This is a sentence without any voice prompt.")
```

---

## 4. Tham số điều khiển sinh (Generation Parameters)

Tất cả tham số đều có thể truyền qua `model.generate(...)` hoặc qua `OmniVoiceGenerationConfig`.

```python
# Cách 1: Keyword arguments
audio = model.generate(text="Hello world", num_step=32, guidance_scale=2.0)

# Cách 2: Config dataclass
from omnivoice import OmniVoiceGenerationConfig
config = OmniVoiceGenerationConfig(num_step=32, guidance_scale=2.0)
audio = model.generate(text="Hello world", generation_config=config)
```

### Decoding (Giải mã)

| Tham số | Kiểu | Mặc định | Ý nghĩa |
|---|---|---|---|
| `num_step` | int | 32 | Số bước unmask lặp. Cao hơn = chất lượng tốt hơn nhưng chậm hơn. Dùng 16 để inference nhanh |
| `denoise` | bool | True | Thêm token `<\|denoise\|>` để tạo giọng sạch hơn |
| `guidance_scale` | float | 2.0 | Classifier-free guidance scale |
| `t_shift` | float | 0.1 | Time-step shift cho noise schedule. Giá trị nhỏ ưu tiên các bước đầu |

### Sampling (Lấy mẫu)

| Tham số | Kiểu | Mặc định | Ý nghĩa |
|---|---|---|---|
| `position_temperature` | float | 5.0 | Nhiệt độ chọn vị trí mask. 0 = greedy (xác định). Cao hơn = ngẫu nhiên hơn |
| `class_temperature` | float | 0.0 | Nhiệt độ chọn token mỗi bước. 0 = greedy. Cao hơn = ngẫu nhiên hơn |
| `layer_penalty_factor` | float | 5.0 | Hệ số phạt các codebook layer sâu hơn, khuyến khích layer thấp unmask trước |

### Duration & Speed (Độ dài & Tốc độ)

```python
# Cố định 10 giây output
audio = model.generate(text="Hello", duration=10.0)

# Nói nhanh hơn 1.2x
audio = model.generate(text="Hello", speed=1.2)

# Dùng list cho batch mode
audio = model.generate(text=["Hello", "World"], duration=[10.0, None], speed=[None, 0.8])
```

| Tham số | Kiểu | Mặc định | Ý nghĩa |
|---|---|---|---|
| `duration` | float / list[float\|None] | None | Cố định độ dài output (giây). Ghi đè `speed` |
| `speed` | float / list[float\|None] | None | Hệ số tốc độ. >1 nhanh hơn, <1 chậm hơn. Mặc định = 1.0 khi cả 2 đều None |

**Priority**: `duration` > `speed`

> **Lưu ý**: Khi dùng `duration`, bước post-processing mặc định có thể cắt khoảng lặng cuối, làm output ngắn hơn yêu cầu. Để giữ chính xác độ dài, truyền `postprocess_output=False`.

### Pre/Post Processing (Tiền/Hậu xử lý)

| Tham số | Kiểu | Mặc định | Ý nghĩa |
|---|---|---|---|
| `preprocess_prompt` | bool | True | Tiền xử lý audio tham chiếu (xóa khoảng lặng dài, thêm dấu câu cuối ref_text) |
| `postprocess_output` | bool | True | Hậu xử lý audio sinh ra (xóa khoảng lặng dài) |
| `pad_duration` | float | 0.1 | Độ dài đệm khoảng lặng mỗi bên (giây). Đặt 0 để tắt |
| `fade_duration` | float | 0.1 | Độ dài fade-in/out (giây). Đặt 0 để tắt |

---

## 5. Điều khiển phi ngôn ngữ & phát âm

### Non-verbal symbols

Chèn tag trực tiếp trong văn bản:

```python
audio = model.generate(text="[laughter] You really got me. I didn't see that coming at all.")
```

**Danh sách tag hỗ trợ**:

| Tag | Ý nghĩa |
|---|---|
| `[laughter]` | Cười |
| `[sigh]` | Thở dài |
| `[confirmation-en]` | Xác nhận (tiếng Anh) |
| `[question-en]` | Hỏi (tiếng Anh) |
| `[question-ah]`, `[question-oh]`, `[question-ei]`, `[question-yi]` | Hỏi với âm sắc khác nhau |
| `[surprise-ah]`, `[surprise-oh]`, `[surprise-wa]`, `[surprise-yo]` | Ngạc nhiên với âm sắc khác nhau |
| `[dissatisfaction-hnn]` | Không hài lòng |

### Sửa phát âm tiếng Trung (Pinyin)

Dùng pinyin với số thanh điệu (1-4) sau chữ cần sửa:

```python
# ZHE2 = zhé, SHE2 = shé, ZHE1 = zhē
audio = model.generate(text="这批货物打ZHE2出售后他严重SHE2本了，再也经不起ZHE1腾了。")
```

### Sửa phát âm tiếng Anh (CMU phoneme)

Dùng [CMU pronunciation dictionary](https://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/cmudict.0.7a), viết HOA, trong ngoặc vuông:

```python
# B EY1 S = bass (nhạc cụ), B AE1 S = bass (cá)
audio = model.generate(text="He plays the [B EY1 S] guitar while catching a [B AE1 S] fish.")
```

---

## 6. Sinh giọng dài (Long-form)

Text được tự động chia thành các đoạn nhỏ khi độ dài ước tính vượt ngưỡng, giúp VRAM gần như không đổi khi sinh giọng dài vô hạn.

| Tham số | Kiểu | Mặc định | Ý nghĩa |
|---|---|---|---|
| `audio_chunk_duration` | float | 15.0 | Độ dài mục tiêu mỗi đoạn (giây) |
| `audio_chunk_threshold` | float | 30.0 | Ngưỡng kích hoạt chunking (giây) |

---

## 7. Voice Cloning nâng cao

### Tái sử dụng giọng đã clone qua nhiều phiên

Mã hóa audio tham chiếu một lần, lưu prompt, bỏ qua bước load audio & auto-transcribe trong các phiên sau:

```python
# === Phiên 1: Mã hóa và lưu ===
prompt = model.create_voice_clone_prompt(
    ref_audio="ref.wav",
    ref_text="Transcription of the reference audio."
)
prompt.save("my_voice.pt")

# === Phiên 2: Load và dùng ===
from omnivoice import VoiceClonePrompt

prompt = VoiceClonePrompt.load("my_voice.pt")
audio = model.generate(text="Hello again!", voice_clone_prompt=prompt)
```

### Kết hợp ref_audio và instruct

Khi cung cấp cả hai:

- **Xung đột**: Model ưu tiên theo phong cách của `ref_audio`
- **Nhất quán**: `instruct` cải thiện độ ổn định cho các thuộc tính nó mô tả
- **Ví dụ điển hình**: Clone dialect tiếng Trung — cung cấp cả audio dialect và instruct dialect (`"四川话"`) để output ổn định hơn

```python
audio = model.generate(
    text="你好世界",
    ref_audio="sichuan.wav",
    instruct="四川话",    # Giúp ổn định dialect
)
```

---

## 8. Voice Design chi tiết

### Cú pháp

Thuộc tính phân cách bằng dấu phẩy. Có thể viết bằng tiếng Anh, tiếng Trung, hoặc kết hợp:

```
"female, young adult, high pitch, british accent"    # English
"女，青年，高音调，四川话"                               # Chinese
"female, young adult, 四川话"                         # Mixed (auto-normalized)
```

- Mỗi category chỉ chọn **một** thuộc tính
- Có thể kết hợp tự do giữa các category
- Không phân biệt hoa/thường
- Có thể bỏ qua thuộc tính không cần — model tự điền phần còn lại

### Bảng thuộc tính đầy đủ

#### Gender (Giới tính)

| English | Chinese |
|---|---|
| male | 男 |
| female | 女 |

#### Age (Tuổi)

| English | Chinese |
|---|---|
| child | 儿童 |
| teenager | 少年 |
| young adult | 青年 |
| middle-aged | 中年 |
| elderly | 老年 |

#### Pitch (Cao độ)

| English | Chinese |
|---|---|
| very low pitch | 极低音调 |
| low pitch | 低音调 |
| moderate pitch | 中音调 |
| high pitch | 高音调 |
| very high pitch | 极高音调 |

#### Style (Phong cách)

| English | Chinese |
|---|---|
| whisper | 耳语 |

#### English Accent

Chỉ hiệu quả khi văn bản đích là tiếng Anh.

| Accent |
|---|
| american accent |
| british accent |
| australian accent |
| canadian accent |
| indian accent |
| chinese accent |
| korean accent |
| japanese accent |
| portuguese accent |
| russian accent |

#### Chinese Dialect

Chỉ hiệu quả khi văn bản đích là tiếng Trung.

| Dialect |
|---|
| 河南话 |
| 陕西话 |
| 四川话 |
| 贵州话 |
| 云南话 |
| 桂林话 |
| 济南话 |
| 石家庄话 |
| 甘肃话 |
| 宁夏话 |
| 青岛话 |
| 东北话 |

### Lưu ý

- Một số tổ hợp thuộc tính có thể không hoạt động tốt do giới hạn dữ liệu huấn luyện — model có thể bỏ qua một số thuộc tính
- Nếu output không như mong đợi, thử đơn giản hóa chuỗi instruct

---

## 9. CLI Tools

Ba công cụ dòng lệnh:

| Lệnh | Mô tả | File nguồn |
|---|---|---|
| `omnivoice-demo` | Web UI Gradio | [omnivoice/cli/demo.py](omnivoice/cli/demo.py) |
| `omnivoice-infer` | Sinh đơn lẻ | [omnivoice/cli/infer.py](omnivoice/cli/infer.py) |
| `omnivoice-infer-batch` | Sinh hàng loạt, đa GPU | [omnivoice/cli/infer_batch.py](omnivoice/cli/infer_batch.py) |

### Demo (Web UI)

```bash
omnivoice-demo --ip 0.0.0.0 --port 8001
# Xem đầy đủ options:
omnivoice-demo --help
```

### Single Inference

```bash
# Voice Cloning (có thể bỏ ref_text để tự động dùng Whisper)
omnivoice-infer \
    --model k2-fsa/OmniVoice \
    --text "This is a test for text to speech." \
    --ref_audio ref.wav \
    --ref_text "Transcription of the reference audio." \
    --output hello.wav

# Voice Design
omnivoice-infer \
    --model k2-fsa/OmniVoice \
    --text "This is a test for text to speech." \
    --instruct "male, British accent" \
    --output hello.wav

# Auto Voice
omnivoice-infer \
    --model k2-fsa/OmniVoice \
    --text "This is a test for text to speech." \
    --output hello.wav
```

### Batch Inference (đa GPU)

```bash
omnivoice-infer-batch \
    --model k2-fsa/OmniVoice \
    --test_list test.jsonl \
    --res_dir results/
```

**Định dạng JSONL** (`test.jsonl`):

```jsonl
{"id": "sample_001", "text": "Hello world", "ref_audio": "/path/to/ref.wav", "ref_text": "Reference transcript", "instruct": "female, british accent", "language_id": "en", "duration": 10.0, "speed": 1.0}
```

Chỉ `id` và `text` là bắt buộc. Các trường khác là tùy chọn.

---

## 10. Training & Fine-tuning

### Cấu trúc thư mục examples/

| Script | Mục đích |
|---|---|
| `run_emilia.sh` | Huấn luyện từ đầu với dataset Emilia (3 giai đoạn) |
| `run_finetune.sh` | Fine-tune từ checkpoint có sẵn với dữ liệu riêng |
| `run_eval.sh` | Đánh giá trên các test set chuẩn |

### Training từ đầu (Emilia)

**3 giai đoạn**:

| Giai đoạn | Mô tả |
|---|---|
| Stage 0 | Kiểm tra dataset Emilia và JSONL manifests đã sẵn sàng |
| Stage 1 | Tokenize audio thành WebDataset shards |
| Stage 2 | Huấn luyện đa GPU với `accelerate` |

**Điều kiện tiên quyết**:

1. Tải dataset Emilia từ [OpenXLab](https://openxlab.org.cn/datasets/Amphion/Emilia):
   ```
   download/Amphion___Emilia/
   └── raw/
       ├── EN/
       └── ZH/
   ```
2. JSONL manifests trong `data/emilia/manifests/`:
   - `emilia_en_train.jsonl`, `emilia_en_dev.jsonl`
   - `emilia_zh_train.jsonl`, `emilia_zh_dev.jsonl`
   - Có thể tự tạo hoặc tải pre-processed từ [HuggingFace](https://huggingface.co/datasets/zhu-han/Emilia-Manifests)

**Chạy**:

```bash
bash examples/run_emilia.sh
# Hoặc chạy từng giai đoạn: sửa stage=1, stop_stage=1 trong script
```

### Fine-tuning

**Bước 1 — Chuẩn bị dữ liệu JSONL**:

```jsonl
{"id": "sample_001", "audio_path": "/data/audio/001.wav", "text": "Hello world", "language_id": "en"}
{"id": "sample_002", "audio_path": "/data/audio/002.wav", "text": "你好世界", "language_id": "zh"}
```

`id`, `audio_path`, `text` là bắt buộc. `language_id` là tùy chọn.

**Bước 2 — Cấu hình script**:

```bash
TRAIN_JSONL="data/my_data_train.jsonl"
DEV_JSONL="data/my_data_dev.jsonl"
GPU_IDS="0,1"
NUM_GPUS=2
OUTPUT_DIR="exp/omnivoice_finetune"
```

**Bước 3 — Chạy**:

```bash
bash examples/run_finetune.sh
```

**Khác biệt chính giữa config train từ đầu và fine-tune**:

| Tham số | Emilia (từ đầu) | Fine-tune | Lý do |
|---|---|---|---|
| `init_from_checkpoint` | `null` | `"k2-fsa/OmniVoice"` | Load pretrained weights |
| `steps` | 300,000 | 5,000 | Ít bước hơn, tùy chỉnh theo dữ liệu |
| `learning_rate` | 1e-4 | 5e-5 | LR thấp hơn cho fine-tune |

> Nếu gặp lỗi `flex_attention`, dùng `config/train_config_finetune_sdpa.json` thay thế.

---

## 11. Evaluation

Cài đặt dependencies:

```bash
pip install omnivoice[eval]
# hoặc
uv sync --extra eval
```

**Test sets hỗ trợ**: `librispeech_pc`, `seedtts_en`, `seedtts_zh`, `fleurs`, `minimax`

```bash
bash examples/run_eval.sh
```

Chi tiết về metrics, chuẩn bị test set, và chạy từng metric riêng: [docs/evaluation.md](docs/evaluation.md)

---

## 12. Mẹo & lưu ý quan trọng

### Voice Cloning

1. **Độ dài audio tham chiếu**: Dùng **3-10 giây**. Dài hơn → chậm inference + giảm chất lượng
2. **Cùng ngôn ngữ**: Dùng audio tham chiếu cùng ngôn ngữ với văn bản đích để phát âm chuẩn
3. **Cross-lingual**: Clone giọng cross-lingual sẽ mang accent của ngôn ngữ tham chiếu
4. **Tự động transcribe**: Bỏ `ref_text` để model tự dùng Whisper ASR
5. **Chuẩn hóa chữ số**: `"I have 2345 apples."` → dùng `normalize_text=True` để đọc đúng thay vì đọc từng chữ số (cần `pip install "omnivoice[tn]"`)

### Voice Design

6. **Cross-lingual hạn chế**: Voice Design chỉ huấn luyện trên dữ liệu Trung + Anh, có thể không ổn định với ngôn ngữ ít tài nguyên
7. **Kết hợp tự do**: `"male, elderly, low pitch, whisper"` — kết hợp thuộc tính từ các category khác nhau
8. **Tối giản**: `"female"` đơn lẻ cũng hợp lệ — model tự điền phần còn lại
9. **Tổ hợp không ổn định**: Nếu output không như ý, thử đơn giản hóa instruct string

### Kết hợp Clone + Design

10. **Xung đột**: Khi `ref_audio` và `instruct` xung đột → model ưu tiên `ref_audio`
11. **Bổ trợ**: Khi nhất quán, `instruct` giúp ổn định clone. Ví dụ: `ref_audio="sichuan.wav", instruct="四川话"` cho dialect ổn định hơn

### Giới hạn

12. **Audio ngắn**: Model có thể không tạo audio ngắn (1-2 giây) ổn định nếu không có audio tham chiếu. Cung cấp `ref_audio` nếu cần sinh clip ngắn
13. **Mân Nam (Hokkien)**: Chỉ hỗ trợ input bằng [Tâi-lô romanization](https://en.wikipedia.org/wiki/T%C3%A2i-l%C3%B4), không hỗ trợ chữ Hán
14. **HF endpoint**: Nếu khó kết nối HuggingFace, set `export HF_ENDPOINT="https://hf-mirror.com"`

### Duration

15. **Post-processing**: Khi dùng `duration`, post-processing mặc định có thể cắt trailing silence làm output ngắn hơn → truyền `postprocess_output=False` nếu cần chính xác tuyệt đối

---

## 13. Danh sách ngôn ngữ hỗ trợ

OmniVoice hỗ trợ **646 ngôn ngữ**. Dưới đây là một số ngôn ngữ phổ biến:

| Ngôn ngữ | OmniVoice ID | ISO 639-3 | Giờ huấn luyện |
|---|---|---|---|
| English | en | eng | 206,061 |
| Chinese (Mandarin) | zh | cmn | 111,343 |
| Japanese | ja | jpn | 36,914 |
| Spanish | es | spa | 27,560 |
| French | fr | fra | 23,675 |
| German | de | deu | 21,927 |
| Russian | ru | rus | 20,339 |
| Portuguese | pt | por | 16,855 |
| Cantonese | yue | yue | 13,302 |
| Thai | th | tha | 10,500 |
| Italian | it | ita | 9,402 |
| Korean | ko | kor | 8,609 |
| Vietnamese | vi | vie | 8,482 |
| Indonesian | id | ind | 6,328 |
| Norwegian | no | nor | 3,850 |
| Catalan | ca | cat | 3,359 |
| Croatian | hr | hrv | 2,795 |
| Lithuanian | lt | lit | 2,629 |
| Swedish | sv | swe | 2,453 |
| Slovak | sk | slk | 2,478 |
| Greek | el | ell | 2,413 |
| Dutch | nl | nld | 2,264 |
| Bulgarian | bg | bul | 2,191 |
| Kinyarwanda | rw | kin | 2,022 |
| Ukrainian | uk | ukr | 1,852 |
| Serbian | sr | srp | 1,855 |
| Belarusian | be | bel | 1,809 |
| Danish | da | dan | 1,666 |
| Kazakh | kk | kaz | 1,537 |
| Standard Arabic | arb | arb | 1,484 |
| Latvian | lv | lav | 1,442 |
| Esperanto | eo | epo | 1,397 |
| Slovenian | sl | slv | 1,173 |
| Estonian | et | est | 960 |
| Polish | pl | pol | 912 |
| Bosnian | bs | bos | 691 |
| Icelandic | is | isl | 647 |
| Maltese | mt | mlt | 630 |
| Kabyle | kab | kab | 530 |
| Finnish | fi | fin | 469 |
| Basque | eu | eus | 480 |
| Ganda | lg | lug | 448 |
| Uighur | ug | uig | 429 |
| Tamil | ta | tam | 423 |
| Swahili | sw | swa | 418 |
| Persian | fa | fas | 366 |
| ... | ... | ... | ... |

> Xem danh sách đầy đủ 646 ngôn ngữ tại [docs/languages.md](docs/languages.md). Dữ liệu nguồn: [docs/lang_id_name_map.tsv](docs/lang_id_name_map.tsv)

---

## Tài nguyên bổ sung

| Tài nguyên | Link |
|---|---|
| Paper (arXiv) | [arxiv.org/abs/2604.00688](https://arxiv.org/abs/2604.00688) |
| Demo Page | [zhu-han.github.io/omnivoice](https://zhu-han.github.io/omnivoice) |
| HuggingFace Model | [huggingface.co/k2-fsa/OmniVoice](https://huggingface.co/k2-fsa/OmniVoice) |
| HuggingFace Space | [huggingface.co/spaces/k2-fsa/OmniVoice](https://huggingface.co/spaces/k2-fsa/OmniVoice) |
| Google Colab | [Open In Colab](https://colab.research.google.com/github/k2-fsa/OmniVoice/blob/master/docs/OmniVoice.ipynb) |
| GitHub Issues | [github.com/k2-fsa/OmniVoice/issues](https://github.com/k2-fsa/OmniVoice/issues) |
| Community Projects | [docs/community-projects.md](docs/community-projects.md) |

---

## Citation

```bibtex
@article{zhu2026omnivoice,
      title={OmniVoice: Towards Omnilingual Zero-Shot Text-to-Speech with Diffusion Language Models},
      author={Zhu, Han and Ye, Lingxuan and Kang, Wei and Yao, Zengwei and Guo, Liyong and Kuang, Fangjun and Han, Zhifeng and Zhuang, Weiji and Lin, Long and Povey, Daniel},
      journal={arXiv preprint arXiv:2604.00688},
      year={2026}
}
```

## Disclaimer

Không được sử dụng model này để sao chép giọng nói trái phép, mạo danh, gian lận, lừa đảo hoặc bất kỳ hoạt động phi pháp/phi đạo đức nào. Người dùng phải tuân thủ luật pháp địa phương và tiêu chuẩn đạo đức. Nhà phát triển không chịu trách nhiệm về việc lạm dụng model.
