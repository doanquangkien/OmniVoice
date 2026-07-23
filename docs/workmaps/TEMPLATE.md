# Template — Workmap Section

> **Đây là template cho 1 SECTION trong WORKMAP.md.**
> Mỗi Agent khi tiếp quản → thêm 1 section mới vào WORKMAP.md, không tạo file mới.

---

## ── Agent: [Tên] — Tiếp Quản Lúc [HH:MM DD/MM] ──

### 📍 Vị Trí Khi Tiếp Quản

| Field | Value |
|-------|-------|
| **Phase** | [Tên phase] |
| **Task đang dở** | [Mô tả] |
| **Commit bắt đầu** | `xxxxxxx` |

### 📂 Files Đang Làm Việc

| File | Đang làm gì? | Status |
|------|-------------|--------|
| `path/to/file.py` | [Mô tả] | 🔄 / ✅ / ⬜ |

### 📋 Checklist Cập Nhật

> Đánh dấu [x] cái đã xong. Thêm mục mới nếu phát sinh. Giữ lại mục cũ từ agent trước nếu chưa xong.

- [ ] (từ Agent trước) ...
- [ ] (mới) ...

### ⚡ Phát Sinh

| # | Mô tả | Hành động | Đã xong? |
|---|-------|-----------|-----------|
| 1 | ... | ... | ⬜ / ✅ |

### 🔄 Nhật Ký

```
HH:MM — [Hành động]
HH:MM — [Hành động]
```

---

**Khi kết thúc phiên:** Để nguyên WORKMAP.md. Agent sau sẽ đọc và viết tiếp section mới.
**Khi kết thúc PHASE:** Lưu trữ WORKMAP.md vào archive/ → tạo WORKMAP.md mới cho phase mới.
