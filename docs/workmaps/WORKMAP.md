# WORKMAP — OmniVoice

> **Sổ tay truyền tay.** Agent trước viết → Agent sau đọc + viết tiếp.
> **1 file duy nhất.** Không tạo file workmap mới — thêm section mới vào đây.

---

## ── Agent: Claude — Bootstrap Lúc 21:00 23/07/2026 ──

### 📍 Vị Trí Khi Tiếp Quản

| Field | Value |
|-------|-------|
| **Phase** | BOOTSTRAP — Thiết lập chuyên nghiệp hóa |
| **Task đang dở** | Tạo hệ thống quản lý dự án chuyên nghiệp |
| **Commit bắt đầu** | `(chưa có — repo mới clone)` |

### 📂 Files Đang Làm Việc

| File | Đang làm gì? | Status |
|------|-------------|--------|
| `CLAUDE.md` | Viết lại với cơ chế tự chủ Agent | ✅ |
| `.agents/handoff.md` | Session handoff đầu tiên | ✅ |
| `.agents/01-constitution.md` | 7 quy tắc bất biến | ✅ |
| `.agents/00-quick-ref.md` | Cây quyết định nhanh | ✅ |
| `.agents/02-workflow.md` | Vòng đời 1 task | ✅ |
| `.agents/03-conventions.md` | Coding conventions (Python, Git, UI, Model) | ✅ |
| `.agents/04-stack.md` | Tech stack + versions | ✅ |
| `docs/VISION.md` | Tầm nhìn dự án | ✅ |
| `docs/sessions/README.md` | Index session logs | ✅ |
| `docs/sessions/TEMPLATE.md` | Template session log | ✅ |
| `docs/reports/README.md` | Hòm thư reports | ✅ |
| `docs/reports/TEMPLATE.md` | Template report | ✅ |
| `docs/workmaps/TEMPLATE.md` | Template workmap section | ✅ |
| `docs/workmaps/WORKMAP.md` | File này | ✅ |
| `docs/discussions/README.md` | Index discussions | ⬜ |
| `docs/decisions/README.md` | Index ADR | ⬜ |
| `docs/KNOWN-ISSUES.md` | Bug tracking | ⬜ |
| `CHANGELOG.md` | Release notes | ⬜ |
| `SESSION-LOG_2026-07-23_01.md` | Session log đầu tiên | ⬜ |
| `git init + commit` | Khởi tạo git repo | ⬜ |

### 📋 Checklist Cập Nhật

- [x] Đọc hiểu toàn bộ codebase OmniVoice
- [x] Viết tài liệu `OmniVoice-HuongDanSuDung.md` (tiếng Việt, 13 chương)
- [x] Cài đặt môi trường + chạy demo thành công
- [x] Việt hóa toàn bộ UI Gradio
- [x] Fix double-click button + concurrency_limit
- [x] Tối ưu VRAM với `--no-asr`
- [x] Test inference thực tế (thành công, chậm trên 4GB)
- [x] Đề xuất Colab T4 cho production inference
- [x] Tạo CLAUDE.md với cơ chế tự chủ
- [x] Tạo `.agents/` structure (6 files)
- [x] Tạo `docs/sessions/` (README + TEMPLATE)
- [x] Tạo `docs/reports/` (README + TEMPLATE)
- [x] Tạo `docs/workmaps/` (WORKMAP.md + TEMPLATE)
- [x] Tạo `docs/VISION.md`
- [ ] Tạo `docs/discussions/README.md`
- [ ] Tạo `docs/decisions/README.md`
- [ ] Tạo `docs/KNOWN-ISSUES.md`
- [ ] Tạo `CHANGELOG.md`
- [ ] Tạo `SESSION-LOG_2026-07-23_01.md`
- [ ] `git init` + commit đầu tiên

### ⚡ Phát Sinh

| # | Mô tả | Hành động | Đã xong? |
|---|-------|-----------|-----------|
| 1 | 4GB VRAM quá yếu cho inference thực tế | Đề xuất Colab T4 + Kaggle Notebooks | ✅ |
| 2 | Nút Generate không chặn double-click | Fix `concurrency_limit=1` + button disable | ✅ |
| 3 | Cần cắt audio test 10s | Dùng ffmpeg cắt `TEST/audio_10s.mp3` | ✅ |

### 🔄 Nhật Ký

```
21:00 — Clone repo + khảo sát codebase
21:05 — Viết OmniVoice-HuongDanSuDung.md
21:10 — Cài đặt dependencies + chạy demo
21:15 — Việt hóa toàn bộ UI demo.py
21:20 — Phát hiện + fix double-click button
21:25 — Test inference lần 1: OOM do Whisper + OmniVoice > 4GB
21:35 — Đề xuất --no-asr, test lại
21:40 — Test inference lần 2: thành công, ~10-15 phút/audio
21:45 — Thảo luận Colab + Kaggle +VoiceClonePrompt
21:50 — Đọc NOFAW CLAUDE.md + hệ thống agents/docs
22:00 — Lập kế hoạch chuyên nghiệp hóa OmniVoice
22:05 — Triển khai: CLAUDE.md + .agents/ + docs/ structure
22:10 — Test Colab thành công — T4 16GB, inference 30-60 giây
22:20 — Thảo luận kiến trúc 3 hướng → discussion architecture
22:30 — Gọi architecture reviewer → PASS WITH CONDITIONS
22:40 — Thảo luận HF Spaces + OAuth automation
22:50 — Viết discussion HF OAuth (Mức 1 + Mức 2)
23:00 — Tạo app.py + requirements.txt cho HF Spaces
23:10 — Cập nhật handoff.md + WORKMAP.md → commit cuối phiên
```

---

## ── Agent: Claude — Phiên #1 Hoàn Tất Lúc 23:15 23/07/2026 ──

### 📍 Tổng Kết Phiên

| Field | Value |
|-------|-------|
| **Phase** | BOOTSTRAP → HOÀN THÀNH |
| **Commit cuối** | `1c9824f` |
| **Files tạo** | ~25 files mới |
| **Discussions** | 3 tài liệu kiến trúc |
| **Code** | app.py (HF Space), demo.py (Việt hóa), Colab notebook |

### 📋 Checklist Cuối Phiên

- [x] Cập nhật .agents/handoff.md
- [x] Cập nhật docs/workmaps/WORKMAP.md (file này)
- [x] Cập nhật docs/discussions/README.md
- [x] Cập nhật docs/sessions/README.md
- [x] Commit + push tất cả
- [ ] Deploy app.py lên HF Spaces (việc tiếp theo)
- [ ] Tạo 3 giọng mẫu tiếng Việt (việc tiếp theo)

### 🔄 Nhật Ký Cuối

```
23:15 — Handoff hoàn tất. Agent sau: đọc mục 3 "Việc Tiếp Theo" trong handoff.md
```

---

## ── Agent: Claude — Phiên #2 Lúc 09:00 24/07/2026 ──

### 📍 Vị Trí Khi Tiếp Quản

| Field | Value |
|-------|-------|
| **Phase** | BOOTSTRAP → PHASE 1 |
| **Task đang dở** | Chuẩn bị deploy HF Space |
| **Commit bắt đầu** | `1c9824f` |

### 📂 Việc Đã Làm

| Việc | Status |
|------|--------|
| Khám phá agy CLI + test Gemini Vision | ✅ |
| Tạo `.agents/05-agy-agent.md` — skill gọi Gemini | ✅ |
| Thảo luận kiến trúc voice.doanquangkien.com | ✅ |
| Nghiên cứu 4 options (proxy, paid Space, Modal, per-user OAuth) | ✅ |
| Chốt: Next.js + Vercel + Per-user HF Space ($0) | ✅ |
| Tạo `docs/decisions/0001-voice-domain-platform.md` (D-007 → D-012) | ✅ |
| Tạo `docs/specs/voice-doanquangkien.md` | ✅ |
| Scaffold Next.js 16.2 project (`voice-platform/`) | ✅ |
| Code toàn bộ frontend: lib, hooks, API routes, components, pages | ✅ |
| Cập nhật app.py: voice packs + base64 audio + CORS | ✅ |
| Cập nhật docs: CLAUDE.md, handoff.md, 04-stack.md, decisions/README | ✅ |

### 📋 Checklist Cập Nhật

- [x] Đọc WORKMAP + handoff — nắm ngữ cảnh
- [x] Khám phá + test agy (Gemini) ✅
- [x] Thảo luận domain + framework → chốt Next.js + Vercel ✅
- [x] Viết ADR (12 quyết định) ✅
- [x] Viết spec website ✅
- [x] Code frontend Next.js ✅
- [x] Cập nhật app.py ✅
- [x] Cập nhật tất cả docs ✅
- [ ] Tạo HF OAuth App (lấy Client ID + Secret)
- [ ] Deploy voice-platform lên Vercel
- [ ] Cấu hình custom domain voice.doanquangkien.com
- [ ] Tạo 3 VoiceClonePrompt (.pt) cho giọng mẫu
- [ ] Deploy app.py lên HF Spaces (template)
- [ ] Test end-to-end

### ⚡ Phát Sinh

| # | Mô tả | Hành động | Đã xong? |
|---|-------|-----------|-----------|
| 1 | DeepSeek Platform sắp hết tiền ($7.81 còn lại) | Cảnh báo huynh nạp thêm | ✅ |
| 2 | Gemini Vision test thành công — đọc chính xác ảnh | Đã test + document | ✅ |
| 3 | Chuyển từ React+GH Pages sang Next.js+Vercel | Cập nhật toàn bộ plan + code | ✅ |

### 🔄 Nhật Ký

```
09:00 — Đọc WORKMAP + handoff — nắm ngữ cảnh
09:05 — Test agy CLI + Gemini models
09:10 — Test Gemini Vision (phân tích ảnh DeepSeek dashboard)
09:15 — Tạo .agents/05-agy-agent.md
09:20 — Thảo luận domain voice.doanquangkien.com + framework
09:25 — Nghiên cứu kiến trúc (web search + Gemini 3.6 Flash)
09:30 — Chốt: Next.js + Vercel + Per-user HF Space ($0)
09:35 — Tạo ADR (D-007 → D-012) + spec website
09:40 — Scaffold Next.js 16.2 project
09:45 — Code lib (hf-oauth, hf-api, tts-api, storage) + config (voices)
09:50 — Code hooks (useAuth, useSpace, useTTS) + API routes
09:55 — Code components: UI (Button, ProgressBar, StatusBadge) + Landing (Hero, Features, HowItWorks) + Setup (ConnectGPU) + Voice (VoiceCard, VoiceSelector) + TTS (TextInput, AudioPlayer)
10:00 — Code pages: Landing (/), Dashboard (/app), Voice Clone (/voice-clone)
10:05 — Cập nhật app.py (voice packs + base64 audio)
10:10 — Cập nhật docs: CLAUDE.md, handoff.md, 04-stack.md, decisions/README
10:15 — Viết tiếp WORKMAP.md (file này)
```

---

## ⏭️ Việc Tiếp Theo Cho Agent Sau

---

## ── Agent: Claude — Phiên #2-3 Lúc 09:00-22:00 24/07/2026 ──

### 📍 Vị Trí Khi Tiếp Quản

| Field | Value |
|-------|-------|
| **Phase** | BOOTSTRAP → PHASE 1 |
| **Commit bắt đầu** | `1c9824f` |
| **Commit kết thúc** | `0ab3a63` |

### 📂 Việc Đã Làm

| Việc | Status |
|------|--------|
| Khám phá agy + test Gemini Vision | ✅ |
| Thảo luận kiến trúc voice.doanquangkien.com | ✅ |
| Nghiên cứu 4 options → chốt per-user HF Space | ✅ |
| Tạo ADR + spec website | ✅ |
| Scaffold Next.js frontend (voice-platform) | ✅ |
| Deploy HF Space template (8 lỗi ZeroGPU) | ✅ |
| Tạo 3 voice packs (nam cn, nam trầm, nữ ấm) | ✅ |
| Tạo single-voice project (nam công nghệ) | ✅ |
| Triển khai Colab 1-click (3 notebooks) | ✅ |
| Tối ưu generation config | ✅ |
| Fix postprocess_output, paragraph pause | ✅ |
| 2 cẩm nang: agy + HF Spaces | ✅ |
| Local test: T1000 quá yếu → tập trung Colab | ✅ |

### 📋 Checklist Cuối Phiên

- [x] Cập nhật handoff.md ✅
- [x] Viết tiếp WORKMAP.md (file này) ✅
- [x] Push tất cả lên GitHub ✅

### 🔄 Nhật Ký

```
09:00 — Đọc WORKMAP + handoff
09:05 — Test agy CLI + Gemini models
09:20 — Thảo luận domain + framework
09:30 — Nghiên cứu kiến trúc (web search + Gemini)
09:40 — Tạo ADR + spec
09:50 — Scaffold Next.js 16.2
10:00 — Code frontend (lib, hooks, components, pages)
10:30 — Deploy HF Space template — 8 lỗi ZeroGPU
11:00 — Fix ZeroGPU: import spaces, @spaces.GPU, async→sync
12:00 — Tạo voice packs (ffmpeg cắt 10s)
13:00 — Fix binary files → base64 embedding
14:00 — Gradio 6 compatibility fixes
15:00 — Tạo single-voice project
15:30 — Postprocess_output=False → giữ pause tự nhiên
16:00 — Paragraph splitting + pause tuning (500→250→150→100ms)
16:30 — Nghiên cứu OmniVoice generation params
17:00 — Tối ưu: position_temp=3.0, language=vi, speed=0.95
17:30 — Fix instruct invalid values
18:00 — Local test: T1000 OOM/too slow
19:00 — Tạo Colab notebook 1-click
20:00 — 3 single-voice projects (nam cn, Alex, thanhnien)
21:00 — Fix NotebookEdit bug, Colab cache
22:00 — Handoff + WORKMAP
```

1. **Đọc handoff.md** — nắm 12 quyết định kiến trúc
2. **Đọc spec** `docs/specs/voice-doanquangkien.md`
3. **Tạo HF OAuth App** — vào https://huggingface.co/settings/applications
4. **Deploy lên Vercel** — push `voice-platform/` lên GitHub → import Vercel
5. **Cấu hình domain** — `voice.doanquangkien.com` → Cloudflare DNS → Vercel
6. **Tạo VoiceClonePrompt** — dùng Colab encode 3 giọng mẫu
7. **Test end-to-end** — OAuth → Space → TTS```
