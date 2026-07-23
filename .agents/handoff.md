---
tags: ["#config"]
---

# Session Handoff — OmniVoice

> **Cập nhật:** 2026-07-23 — Phiên #1: Bootstrap chuyên nghiệp hóa + Thảo luận kiến trúc
> **Model:** Claude
> **Phase:** BOOTSTRAP → chuẩn bị sang PHASE 1 (HF Space Backend)

---

## 0. Commit Pointer

```
Branch:      master
HEAD:        1c9824f
Remote:      github.com/doanquangkien/OmniVoice (fork từ k2-fsa/OmniVoice)

GPU local:   Quadro T1000 (4GB VRAM) — đã kill tất cả process
Colab:       Đã test thành công với GPU T4, UI Việt hóa chạy ổn định
```

---

## 1. Đã Làm

### 1.1 Bootstrap — Thiết lập chuyên nghiệp (Phiên #1)

- Clone repo từ `github.com/doanquangkien/OmniVoice`
- Viết `OmniVoice-HuongDanSuDung.md` — tài liệu tiếng Việt toàn diện 13 chương
- Việt hóa toàn bộ UI Gradio demo (`omnivoice/cli/demo.py`)
- Fix double-click button: `concurrency_limit=1` + tự disable
- Test inference local (4GB VRAM — chậm, 10-15 phút/audio)
- Test inference Colab (T4 16GB — nhanh, 30-60 giây/audio)

### 1.2 Hệ thống quản lý dự án chuyên nghiệp

- `CLAUDE.md` — cơ chế tự chủ Agent 5 bước + bản đồ định tuyến
- `.agents/` — handoff, constitution (7 quy tắc), conventions, stack, workflow, quick-ref
- `docs/` — VISION, sessions, reports, workmaps, discussions, decisions, KNOWN-ISSUES
- `CHANGELOG.md`, `KNOWN-ISSUES.md`

### 1.3 Thảo luận kiến trúc — 3 tài liệu lớn

| # | Tài liệu | Nội dung |
|---|---|---|
| 1 | `docs/discussions/2026-07-23-architecture-for-vietnam-market.md` | Phân tích 3 hướng triển khai (EXE+CPU, SaaS, Colab Hybrid) → chốt hướng C |
| 2 | `docs/reports/2026-07-23-arch-vietnam-deployment-review.md` | Architecture review độc lập — PASS WITH CONDITIONS. Đề xuất Modal-first, HF Spaces fallback, ONNX CPU emergency |
| 3 | `docs/discussions/2026-07-23-hf-oauth-automation.md` | Mô hình HF Space OAuth tự động — user 2 click, 30 giây có GPU riêng. Lộ trình Mức 1 (thủ công) → Mức 2 (OAuth) |

### 1.4 Code — HF Space Backend

- `app.py` — Gradio app với API endpoints (gốc repo, sẵn sàng deploy lên HF Spaces)
- `requirements.txt` — dependencies cho HF Spaces
- Colab notebook tiếng Việt tại `TEST/Colab_OmniVoice_Vietnam.ipynb`

---

## 2. Trạng Thái Dự Án

```
✅ BOOTSTRAP — HOÀN THÀNH:
   ✅ Clone + khảo sát + tài liệu tiếng Việt
   ✅ Demo UI Việt hóa + fix double-click
   ✅ Hệ thống quản lý dự án chuyên nghiệp
   ✅ 3 tài liệu kiến trúc + architecture review
   ✅ HF Space backend code (app.py)
   ✅ Colab notebook tiếng Việt

⬜ PHASE 1 — HF Space Deploy:
   ⬜ Deploy app.py lên HF Spaces (doanquangkien/omnivoice-tts)
   ⬜ Tạo 3 giọng mẫu tiếng Việt (VoiceClonePrompt .pt)
   ⬜ Test API từ browser

⬜ PHASE 2 — Web App Frontend:
   ⬜ React + Vite + Tailwind SPA
   ⬜ GitHub Pages deploy

⬜ PHASE 3 — Voice Packs + Polish:
   ⬜ Voice Pack manager
   ⬜ Mobile responsive
```

---

## 3. Việc Tiếp Theo

### Ưu tiên CAO (Phase 1)
1. **Deploy app.py lên HF Spaces** — tạo Space `doanquangkien/omnivoice-tts`
2. **Tạo 3 giọng mẫu tiếng Việt** — dùng Colab để encode VoiceClonePrompt:
   - Nam Bắc (giọng nam, Hà Nội)
   - Nữ Bắc (giọng nữ, Hà Nội)
   - Trầm ấm (giọng nam trung niên, thuyết minh)
3. **Test API** — gọi `/api/predict` từ browser, xác nhận hoạt động

### Ưu tiên TRUNG BÌNH (Phase 2)
4. Build web app React SPA, deploy GitHub Pages
5. Tích hợp với HF Space API
6. Lộ trình Mức 1: user tự duplicate Space + paste token

---

## 4. Quyết Định Đã Chốt

| # | Quyết định | Ghi chú |
|---|---|---|
| **D-001** | Kiến trúc: GitHub Pages (frontend) + HF Spaces (GPU backend) | $0 toàn bộ, không vi phạm ToS |
| **D-002** | Ưu tiên Gradio API (tận dụng code sẵn) cho MVP, FastAPI cho production | app.py đã có sẵn cả 2 chế độ |
| **D-003** | Voice Packs lưu trên HF Dataset, cache local | `.ovoice` format (zip: pt + wav + metadata.json) |
| **D-004** | Lộ trình 2 mức: Mức 1 (thủ công, 1-2 tuần) → Mức 2 (OAuth, 3-4 tuần) | Chỉ build Mức 2 khi Mức 1 có >50 user |
| **D-005** | Website 1 trang duy nhất: chọn giọng → nhập text → tạo → nghe | Không auth, không login, không phức tạp |
| **D-006** | Chỉ tập trung tiếng Việt 100% | Cắt bỏ đa ngôn ngữ khỏi UI |

---

## 5. Lưu Ý Cho Agent Sau

| # | Lưu ý |
|---|-------|
| 1 | **Kiến trúc đã chốt:** GitHub Pages + HF Spaces. Đừng đề xuất lại Colab hay Desktop EXE |
| 2 | **app.py đã có ở gốc repo** — sẵn sàng deploy lên HF Spaces. Cần test thực tế |
| 3 | **4GB VRAM local là giới hạn cứng** — mọi inference production phải qua cloud GPU |
| 4 | **UI Việt hóa** tại `omnivoice/cli/demo.py` — không phải app.py. app.py là bản rút gọn cho HF Spaces |
| 5 | **Audio tham chiếu test** tại `TEST/audio_10s.mp3` |
| 6 | **3 tài liệu kiến trúc** trong `docs/discussions/` và `docs/reports/` — đọc trước khi đề xuất thay đổi |
| 7 | **Colab notebook** tại `TEST/Colab_OmniVoice_Vietnam.ipynb` — dùng để encode VoiceClonePrompt |
| 8 | **Ngrok không nên dùng** — Cloudflare Tunnel hoặc HF Spaces built-in URL |
| 9 | **Voice Pack format** `.ovoice` = zip(pt + wav + metadata.json) — chưa implement, mới có spec |
| 10 | **Architecture review** tại `docs/reports/2026-07-23-arch-vietnam-deployment-review.md` — 4 điều kiện MUST FIX trước khi production |

---

## 6. Lệnh Nhanh

```bash
# Demo local (có UI Việt hóa)
omnivoice-demo --no-asr --port 7860

# HF Space (app.py ở gốc repo)
python app.py

# Colab
# Mở https://colab.research.google.com/github/doanquangkien/OmniVoice/blob/master/TEST/Colab_OmniVoice_Vietnam.ipynb

# Git
git push origin master
```
