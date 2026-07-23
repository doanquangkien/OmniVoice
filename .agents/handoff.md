---
tags: ["#config"]
---

# Session Handoff — OmniVoice

> **Cập nhật:** 2026-07-23 — Phiên #1: Bootstrap — Thiết lập chuyên nghiệp hóa dự án
> **Model:** Claude
> **Phase:** BOOTSTRAP

---

## 0. Commit Pointer

```
Branch:      main (chưa có remote)
HEAD:        <sẽ cập nhật sau commit đầu tiên>
Remote:      github.com/doanquangkien/OmniVoice (fork từ k2-fsa/OmniVoice)

GPU local:   Quadro T1000 (4GB VRAM) — hạn chế, dùng Colab T4 cho inference dài
Colab:       GPU T4 16GB miễn phí — nhanh hơn local 10-20x
```

---

## 1. Đã Làm

### Phiên 2026-07-23 #1 — Bootstrap Chuyên Nghiệp Hóa

**Trọng tâm:** Clone repo → Đọc hiểu toàn bộ docs → Việt hóa UI → Thiết lập hệ thống quản lý dự án chuyên nghiệp

1. **Clone & Khảo sát:**
   - Clone từ `github.com/doanquangkien/OmniVoice`
   - Đọc toàn bộ README, docs, examples
   - Viết tài liệu `OmniVoice-HuongDanSuDung.md` (tiếng Việt, 13 chương)

2. **Môi trường Dev:**
   - Python 3.13, PyTorch 2.11+cu128, CUDA 12.8
   - GPU: Quadro T1000 (4GB VRAM)
   - Cài đặt đầy đủ dependencies

3. **Demo Web UI — Việt Hóa:**
   - Khởi động Gradio demo thành công
   - Toàn bộ UI đã Việt hóa: labels, buttons, tabs, settings, voice design categories
   - Phát hiện + fix lỗi nút "Tạo giọng nói" không chặn double-click
   - Thêm `concurrency_limit=1` + tự disable khi đang xử lý

4. **Tối ưu VRAM:**
   - `--no-asr`: bỏ Whisper, tiết kiệm ~1.8GB VRAM
   - Voice Clone vẫn chạy được trên 4GB (chậm ~10-15 phút/audio)
   - Đề xuất Colab T4 cho inference sản xuất

5. **Thiết lập chuyên nghiệp (phiên này):**
   - CLAUDE.md với cơ chế tự chủ Agent
   - `.agents/` — handoff, constitution, conventions, stack, workflow, quick-ref
   - `docs/` — VISION, sessions, reports, workmaps, discussions, decisions
   - WORKMAP.md + session log đầu tiên + CHANGELOG.md

---

## 2. Trạng Thái Dự Án

```
✅ BOOTSTRAP:
   ✅ Clone repo + khảo sát
   ✅ Tài liệu tiếng Việt toàn diện
   ✅ Demo UI Việt hóa + fix double-click
   ✅ Thiết lập hệ thống quản lý dự án chuyên nghiệp
⬜ Tối ưu inference pipeline
⬜ Colab notebook tùy chỉnh
⬜ Đóng gói Docker
⬜ CI/CD
```

---

## 3. Việc Tiếp Theo

- **Ngắn hạn:** Test inference trên Colab T4 → so sánh benchmark với local
- **Trung hạn:** Tạo Colab notebook riêng với UI Việt hóa + `--share` public link
- **Dài hạn:** Fine-tune giọng tiếng Việt, đóng gói thành API service

---

## 4. Lưu Ý Cho Agent Sau

| # | Lưu ý |
|---|-------|
| 1 | **4GB VRAM là giới hạn cứng** — luôn dùng `--no-asr` trên local, chuyển Colab cho việc nặng |
| 2 | **GPU 100% nhưng chậm** = VRAM thrashing — không phải bug |
| 3 | **UI đã Việt hóa** tại `omnivoice/cli/demo.py` — chỉnh sửa cần giữ đúng key trong `_CATEGORIES` |
| 4 | **Nút "Tạo giọng nói"** đã có `concurrency_limit=1` — không sửa thành >1 nếu chưa nâng VRAM |
| 5 | **Audio tham chiếu test** tại `TEST/audio_10s.mp3` (10 giây, MP3, mono) |
| 6 | **Model cache** tại `C:\Users\Admin\.cache\huggingface\hub\` — xóa nếu cần giải phóng disk |
| 7 | **Colab** là giải pháp inference chính cho production — T4 16GB rẻ hơn nâng cấp GPU local |
