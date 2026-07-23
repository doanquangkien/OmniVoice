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
```
