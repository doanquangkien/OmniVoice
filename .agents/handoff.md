---
tags: ["#config"]
---

# Session Handoff — OmniVoice

> **Cập nhật:** 2026-07-24 — Phiên #2-3: Kiến trúc, Voice Packs, Colab, Single-Voice Deploy
> **Model:** Claude
> **Phase:** PHASE 1 — Single-Voice + Colab hoàn chỉnh

---

## 0. Commit Pointer

```
Branch:      master
HEAD:        0ab3a63
Remote:      github.com/doanquangkien/OmniVoice (fork từ k2-fsa/OmniVoice)

GPU local:   Quadro T1000 (4GB VRAM) — QUÁ YẾU, không dùng cho inference
HF Spaces:   doanquangkien/omnivoice-tts (template 3 giọng, private, running)
             doanquangkien/omnivoice-single (1 giọng nam công nghệ, private, running)
Colab:       T4 16GB — hoạt động tốt, ~30s/audio
Voice Packs: 3 giọng mẫu (nam công nghệ, nam trầm ấm, nữ ấm áp)
Kaggle:      Không dùng được (cần verify phone)
```

---

## 1. Đã Làm

### 1.1 Agent AGY (Gemini sub-agent)
- Khám phá + test `agy` CLI — gọi Gemini từ terminal
- Vision test thành công — phân tích ảnh DeepSeek dashboard
- Tạo `.agents/05-agy-agent.md` — cẩm nang sử dụng

### 1.2 Kiến trúc + Domain
- Nghiên cứu 4 options triển khai → chốt per-user HF Space + OAuth
- Chốt Next.js + Vercel Hobby ($0)
- 12 quyết định kiến trúc (D-001 → D-012)
- Tạo `docs/decisions/0001-voice-domain-platform.md`
- Tạo `docs/specs/voice-doanquangkien.md`

### 1.3 Frontend Next.js (voice-platform/)
- Scaffold Next.js 16.2 + TypeScript + Tailwind
- Code: lib, hooks, API routes, components, pages
- OAuth flow (PKCE client-side qua @huggingface/hub)
- Token fallback input
- Deploy lên Vercel: https://voice-platform-beige.vercel.app
- **Hiện tại:** Tạm dừng — tập trung vào HF Spaces + Colab

### 1.4 HF Spaces
- **Template 3 giọng:** `doanquangkien/omnivoice-tts` — public, ZeroGPU T4
  - 8 lỗi ZeroGPU đã fix (document tại `.agents/06-hf-spaces-guide.md`)
  - UI redesign: light theme, Be Vietnam Pro, mobile-first
- **Single voice:** `doanquangkien/omnivoice-single` — private, ZeroGPU T4
  - 1 giọng nam công nghệ, cache VoiceClonePrompt
  - `postprocess_output=False` + paragraph pause 100ms
  - Tối ưu: `position_temperature=3.0`, `language="vi"`, `speed=0.95`

### 1.5 Voice Packs
- 3 giọng mẫu 10s: `voice_packs/giong_nam_cong_nghe.mp3`, `giong_nam_tram_am.mp3`, `giong_nu_am_ap.mp3`
- Nhúng base64 trong `voice_data.py` (HF chặn binary)

### 1.6 Single-Voice Projects (Colab 1-click)
- `single-voice/` — Giọng nam công nghệ
- `single-voice-alex/` — Giọng Alex (WAV 10s, ref_text có sẵn)
- `single-voice-thanhnien/` — Giọng Thanh niên tự tin (10s, ref_text 2 câu)
- Mỗi project: `voice_data.py` + `colab_*.ipynb` (1-click Open in Colab)
- Auto-download voice_data.py từ GitHub raw URL

### 1.7 Cẩm nang
- `.agents/05-agy-agent.md` — Cách gọi Gemini làm sub-agent
- `.agents/06-hf-spaces-guide.md` — 8 lỗi HF Spaces + cách fix

---

## 2. Trạng Thái Dự Án

```
✅ BOOTSTRAP — HOÀN THÀNH
✅ PHASE 1 — HF Spaces + Colab:
   ✅ 3 giọng mẫu (voice_packs/)
   ✅ HF Space template 3 giọng (omnivoice-tts)
   ✅ HF Space single voice (omnivoice-single)
   ✅ 3 Colab notebooks 1-click

⏸️ TẠM DỪNG — Frontend:
   ⏸️ voice-platform (Next.js + Vercel)

⬜ PHASE 2 — Hoàn thiện:
   ⬜ Custom domain voice.doanquangkien.com
   ⬜ HF Space PRO ($9/tháng) nếu muốn always-on
   ⬜ Thêm nhiều voice packs
```

---

## 3. Việc Tiếp Theo

1. **Test Colab notebooks** — xác nhận cả 3 giọng chạy ổn
2. **HF Space PRO** — nếu muốn bỏ giới hạn ngủ 15 phút
3. **Custom domain** — voice.doanquangkien.com trỏ về HF Space hoặc Vercel
4. **Thêm voice packs** — pattern đã có sẵn, chỉ cần audio mới + tạo folder

---

## 4. Quyết Định Đã Chốt

| # | Quyết định |
|---|-----------|
| D-001 → D-006 | Kiến trúc ban đầu |
| D-007 | Domain: voice.doanquangkien.com |
| D-008 | Per-user HF Space + OAuth 1-click |
| D-009 | Next.js + Vercel Hobby |
| D-010 | Browser gọi thẳng HF Space |
| D-011 | Trừu tượng hóa ở lớp UX |
| D-012 | Dự án cộng đồng, không thu phí |
| D-013 | **Single-voice model** — 1 giọng/Space/Colab |

---

## 5. Cấu Trúc Dự Án

```
OmniVoice/
├── app.py                    ← HF Space template (3 giọng)
├── voice_packs/              ← 3 audio mẫu 10s
├── single-voice/             ← Nam công nghệ + Colab
├── single-voice-alex/        ← Alex + Colab
├── single-voice-thanhnien/   ← Thanh niên tự tin + Colab
├── voice-platform/           ← Next.js frontend (tạm dừng)
├── .agents/                  ← System files + guides
└── docs/                     ← ADR, specs, sessions
```

---

## 6. Pattern Tạo Voice Mới

```bash
# 1. Tạo folder
mkdir single-voice-TEN && mkdir single-voice-TEN/voice_packs

# 2. Cắt audio 10s
ffmpeg -i INPUT.mp3 -t 10 -acodec copy single-voice-TEN/voice_packs/TEN_10s.mp3

# 3. Tạo voice_data.py (base64)
python -c "import base64,json; ..."

# 4. Copy + sửa Colab notebook từ template có sẵn

# 5. Push lên GitHub → Colab badge tự động hoạt động
```

---

## 7. Lưu Ý Cho Agent Sau

| # | Lưu ý |
|---|-------|
| 1 | **T1000 4GB quá yếu** — mọi inference phải qua HF Space hoặc Colab |
| 2 | **HF ZeroGPU cần Gradio** — không dùng được FastAPI thuần |
| 3 | **HF chặn binary** — audio phải nhúng base64 trong .py |
| 4 | **@spaces.GPU** phải ở module level + wire qua Gradio click |
| 5 | **Colab 1-click** — voice_data.py auto-download từ GitHub raw |
| 6 | **NotebookEdit có bug** — ghi đè toàn bộ cell, cần kiểm tra sau edit |
| 7 | **postprocess_output=False** — giữ khoảng lặng tự nhiên |
| 8 | **ref_text phải khớp audio** — nếu không VoiceClonePrompt hỏng |
| 9 | **instruct phải dùng giá trị hợp lệ** — xem danh sách trong OmniVoice source |
