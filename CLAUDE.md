# CLAUDE.md — OmniVoice

> **Chuyển văn bản thành giọng nói cho hơn 600 ngôn ngữ**
> *Text-to-Speech zero-shot với Diffusion Language Models*

---

## 0. Agent Tự Chủ — Đọc Phần Này Trước Tiên

> **Nếu bạn là Agent vừa được triệu tập vào dự án này, đây là thuật toán tự chủ để nắm bắt ngữ cảnh mà không cần ai hướng dẫn:**

```
BƯỚC 0: ĐỊNH VỊ — TÔI ĐANG Ở ĐÂU TRONG LỊCH SỬ DỰ ÁN?
  ├── Đọc .agents/handoff.md
  ├── Đọc dòng: "HEAD: `xxxxxxx`" (hash commit gần nhất)
  ├── Chạy: git log --oneline -10
  ├── Chạy: git status
  └── → Biết ngay: phiên trước làm gì, đang dở gì

BƯỚC 1: KIỂM TRA HÒM THƯ — CÓ VIỆC GÌ ĐANG CHỜ KHÔNG?
  ├── Mở docs/reports/README.md
  ├── Xem bảng "ĐANG CHỜ XỬ LÝ"
  └── → Biết ngay: có report nào cần action không

BƯỚC 2: NẮM NGỮ CẢNH — DỰ ÁN ĐANG Ở ĐÂU?
  ├── Đọc docs/VISION.md (tầm nhìn + hướng đi dài hạn)
  ├── Đọc docs/discussions/README.md (đang bàn gì)
  ├── Đọc docs/decisions/README.md (quyết định đã chốt)
  └── → Biết ngay: cần làm gì tiếp theo

BƯỚC 3: ĐỌC + VIẾT TIẾP WORKMAP — SỔ TAY TRUYỀN TAY
  ├── Đọc docs/workmaps/WORKMAP.md (Agent trước đang dở gì?)
  ├── VIẾT TIẾP vào WORKMAP.md — thêm section mới với tên mình
  ├── Cập nhật checklist: đánh dấu cái đã xong, thêm cái mới
  └── → KHÔNG tạo file mới — 1 file truyền tay qua các Agent

BƯỚC 4: BÁO CÁO CHO USER
  └── "Tôi đã nắm được ngữ cảnh. Việc trước: X. Việc tiếp theo: Y. Reports: Z đang chờ.
       Huynh muốn tôi làm gì?"

⏱️ Tổng thời gian: 2-3 phút → SẴN SÀNG LÀM VIỆC
```

**Sau khi tự chủ xong, nếu cần tra cứu thêm → xem bản đồ định tuyến ở Mục 3.**

---

## 1. Dự Án Là Gì

**OmniVoice** là mô hình Text-to-Speech zero-shot đa ngôn ngữ mã nguồn mở, hỗ trợ **646 ngôn ngữ**, xây dựng trên kiến trúc Diffusion Language Model.

- **Repo gốc:** [github.com/k2-fsa/OmniVoice](https://github.com/k2-fsa/OmniVoice)
- **Fork của:** [github.com/doanquangkien/OmniVoice](https://github.com/doanquangkien/OmniVoice)
- **Model:** 0.6B params (dựa trên Qwen/Qwen3-0.6B-Base)
- **Giấy phép:** Apache 2.0 — được phép thương mại hóa
- **Tác giả gốc:** Han Zhu, Xiaomi AI Lab (Next-gen Kaldi team)
- **Paper:** [arXiv 2604.00688](https://arxiv.org/abs/2604.00688)

### Mục tiêu của chúng ta

Không chỉ dùng — mà còn **tùy biến, Việt hóa, tối ưu và đóng gói** OmniVoice thành công cụ chuyên nghiệp cho thị trường Việt Nam và quốc tế.

---

## 2. Cách Làm Việc Với Agent

> **Khi gọi Agent mới vào dự án, luôn yêu cầu: "Đọc CLAUDE.md" — Agent sẽ tự lần theo dấu vết để nắm toàn bộ ngữ cảnh.**

```
Huynh:     "Đọc CLAUDE.md rồi [nhiệm vụ]"
Agent:     → Đọc CLAUDE.md
           → Đọc handoff.md → biết commit pointer
           → Kiểm tra reports inbox
           → Viết tiếp WORKMAP
           → Thực thi nhiệm vụ
           → Cập nhật handoff.md cuối phiên
```

- Giao tiếp với huynh: **tiếng Việt**
- Giao tiếp với Agent phụ (nếu cần): **tiếng Anh**

---

## 3. Bản Đồ Định Tuyến

### Khi cần tra cứu:

| Tình huống | Đọc file này |
|------------|-------------|
| **Tôi mới vào, cần biết làm gì** | `.agents/handoff.md` |
| **Tôi muốn hiểu tầm nhìn + WHY** | `docs/VISION.md` ← ĐỌC ĐẦU TIÊN |
| **Tôi lúng túng, không biết ghi gì vào đâu** | `.agents/00-quick-ref.md` ← TRA ĐẦU TIÊN |
| **Tôi muốn xem reports đang chờ** | `docs/reports/README.md` ← HÒM THƯ CHUNG |
| **Tôi muốn xem workmap của Agent trước** | `docs/workmaps/WORKMAP.md` ← SỔ TAY ĐANG HOẠT ĐỘNG |
| Quy tắc bất biến | `.agents/01-constitution.md` |
| Quy trình làm việc chi tiết | `.agents/02-workflow.md` |
| Coding conventions | `.agents/03-conventions.md` |
| Tech stack + version | `.agents/04-stack.md` |
| Quyết định đã chốt | `docs/decisions/README.md` |
| Đang thảo luận gì | `docs/discussions/README.md` |
| Hướng dẫn sử dụng OmniVoice | `OmniVoice-HuongDanSuDung.md` |
| Danh sách 646 ngôn ngữ | `docs/languages.md` |
| Tham số generation | `docs/generation-parameters.md` |
| Voice Design attributes | `docs/voice-design.md` |
| Tips & lưu ý | `docs/tips.md` |
| Training & Evaluation | `examples/README.md` |
| Lịch sử các phiên | `docs/sessions/README.md` |
| Bug đang tồn tại | `docs/KNOWN-ISSUES.md` |
| Release notes | `CHANGELOG.md` |

### Khi cần ghi chép:

| Tình huống | Ghi vào đây |
|------------|-------------|
| **Cuối mỗi phiên (bắt buộc)** | `.agents/handoff.md` + update HEAD |
| >3 files hoặc >50 dòng thay đổi | `docs/sessions/SESSION-LOG_YYYY-MM-DD_NN.md` |
| User báo bug | `docs/KNOWN-ISSUES.md` |
| Fix bug xong | `CHANGELOG.md` + `docs/KNOWN-ISSUES.md` |
| Hoàn thành audit/review | `docs/reports/` ← GỬI REPORT VÀO HÒM THƯ |
| Quyết định kiến trúc mới | `docs/decisions/NNNN-title.md` (ADR) |
| Chủ đề cần thảo luận | `docs/discussions/YYYY-MM-DD-topic.md` |
| Bắt đầu tính năng mới | `docs/specs/feature-name.md` |
| Thay đổi công nghệ | `.agents/04-stack.md` |
| Đạt milestone | `git tag` + `CHANGELOG.md` + session log |

---

## 4. Quy Tắc Bất Biến (Tóm Tắt)

> Chi tiết: `.agents/01-constitution.md`

1. **Agent-First** — mọi thứ viết cho Agent tương lai đọc hiểu
2. **Document Before Code** — thảo luận → discussion → ADR → spec → code
3. **Session Log Discipline** — cuối phiên luôn update handoff.md + HEAD
4. **Commit Hygiene** — `[type] mô tả`, type ∈ {feat, fix, refactor, docs, chore, test}
5. **Workmap Discipline** — Sau MỖI commit → mở WORKMAP.md → cập nhật checklist + nhật ký
6. **Code Quality** — Function < 50 dòng, file < 500 dòng, type hints, validate ở edge
7. **Model First, Code Second** — Tối ưu trải nghiệm người dùng model, không phải cấu trúc code

---

## 5. Trạng Thái Dự Án

| | |
|---|---|
| **Phase hiện tại** | **BOOTSTRAP — Thiết lập chuyên nghiệp hóa dự án** |
| **Ngày bắt đầu** | 2026-07-23 |
| **Repo** | `github.com/doanquangkien/OmniVoice` (fork từ `k2-fsa/OmniVoice`) |
| **Môi trường** | Windows 10 Pro, Python 3.13, PyTorch 2.11, CUDA 12.8 |
| **GPU** | Quadro T1000 (4GB VRAM) — hạn chế, khuyến nghị dùng Colab T4 cho inference nặng |
| **Demo UI** | Gradio 6 — đã Việt hóa toàn bộ giao diện |
| **Tài liệu** | `OmniVoice-HuongDanSuDung.md` — hướng dẫn toàn diện tiếng Việt |

---

## 6. Lệnh Nhanh

```bash
# Cài đặt (uv)
uv sync
uv sync --extra tn         # text normalization
uv sync --extra eval       # evaluation

# Demo Web UI (local)
omnivoice-demo --ip 0.0.0.0 --port 7860
omnivoice-demo --no-asr --port 7860    # không tải Whisper (tiết kiệm VRAM)
omnivoice-demo --device cpu --no-asr   # chạy trên CPU

# Inference đơn lẻ
omnivoice-infer --model k2-fsa/OmniVoice --text "Hello" --ref_audio ref.wav --output out.wav

# Batch inference
omnivoice-infer-batch --model k2-fsa/OmniVoice --test_list test.jsonl --res_dir results/

# Google Colab (GPU T4 16GB — nhanh hơn local 10-20x)
# https://colab.research.google.com/github/k2-fsa/OmniVoice/blob/master/docs/OmniVoice.ipynb
```
