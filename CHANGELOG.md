# Changelog — OmniVoice

> **Lịch sử thay đổi đáng kể.** Dựa trên [Keep a Changelog](https://keepachangelog.com/).
> Base: OmniVoice v0.2.1 (k2-fsa/OmniVoice)

---

## [Unreleased]

### Added (2026-07-23)
- **CLAUDE.md** với cơ chế tự chủ Agent (tham khảo từ NOFAW)
- **Hệ thống `.agents/`**: handoff, constitution, conventions, stack, workflow, quick-ref
- **Hệ thống `docs/`**: VISION, sessions, reports, workmaps, discussions, decisions, KNOWN-ISSUES
- **Tài liệu tiếng Việt toàn diện** `OmniVoice-HuongDanSuDung.md` (13 chương)
- **CHANGELOG.md** (file này)

### Changed
- **Việt hóa toàn bộ UI** Gradio demo (`omnivoice/cli/demo.py`)
- **Fix double-click button**: thêm `concurrency_limit=1` + tự disable khi đang xử lý
- **Cập nhật `_CATEGORIES`** — nhãn tiếng Việt cho Voice Design attributes

### Known Limitations
- GPU 4GB (Quadro T1000): inference chậm 10-15 phút/audio. Khuyến nghị Colab T4.
- Chưa có git remote — cần push lên GitHub sau khi init
