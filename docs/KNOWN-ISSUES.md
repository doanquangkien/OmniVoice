# Known Issues — OmniVoice

> **Bug đã biết và đang theo dõi.** Thêm entry mới khi phát hiện bug.
> Đánh dấu ✅ khi đã fix.

---

## Đang Mở

| # | Ngày | Mô tả | Mức độ | File liên quan |
|---|---|---|---|---|
| 1 | 2026-07-23 | **VRAM thrashing trên GPU 4GB** — inference rất chậm (10-15 phút/audio) do VRAM không đủ. Workaround: dùng `--no-asr` + `num_step=16` hoặc chuyển sang Colab T4 | 🟡 MEDIUM | `omnivoice/cli/demo.py` |
| 2 | 2026-07-23 | **Nút Generate không chặn double-click** (đã fix trong phiên này nhưng cần verify kỹ hơn) | 🟢 LOW | `omnivoice/cli/demo.py` |
| 3 | 2026-07-23 | **Gradio 6.0 warning** — `theme` và `css` params nên được chuyển từ `Blocks()` constructor sang `launch()` method | ⚪ LOW | `omnivoice/cli/demo.py:296` |

---

## Đã Fix

| # | Ngày fix | Mô tả | Commit |
|---|---|---|---|
| — | — | Chưa có bug nào được fix | — |
