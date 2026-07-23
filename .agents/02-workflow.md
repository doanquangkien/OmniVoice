# Agent Workflow — OmniVoice

> **Quy trình làm việc chuẩn.** Agent mới đọc 1 lần (2 phút). Sau đó dùng `.agents/00-quick-ref.md` để tra nhanh.

---

## Vòng Đời 1 Task

```
[0] ONBOARDING  →  [1] UNDERSTAND  →  [2] RESEARCH  →  [3] DISCUSS
                                         ↓
[7] LOG        ←  [6] VERIFY      ←  [5] IMPLEMENT ←  [4] PLAN
```

---

### Bước 0: ONBOARDING (Đầu phiên)

> → CLAUDE.md §0 — quy trình onboarding chuẩn: handoff → reports inbox → WORKMAP → báo cáo user.

---

### Bước 1: UNDERSTAND (Hiểu yêu cầu)

- Đọc kỹ yêu cầu của user
- Nếu không rõ → **hỏi lại**, không đoán
- Xác định phạm vi: chạm files nào? Ảnh hưởng gì?
- Nếu là tính năng mới → đọc spec trong `docs/specs/` (nếu có)
- Nếu user báo bug → kiểm tra `docs/KNOWN-ISSUES.md`, thêm nếu chưa có

---

### Bước 2: RESEARCH (Nghiên cứu)

- Đọc code/files liên quan
- Kiểm tra ADR: `docs/decisions/README.md`
- Kiểm tra discussion: `docs/discussions/README.md`
- Với OmniVoice: đọc [OmniVoice-HuongDanSuDung.md](../OmniVoice-HuongDanSuDung.md) nếu liên quan đến model
- Có multiple approaches → chuyển sang Bước 3

---

### Bước 3: DISCUSS (Thảo luận)

- Vấn đề mới, chưa có ADR → tạo `docs/discussions/YYYY-MM-DD-topic.md`
- Trình bày options + pros/cons → hỏi user chốt
- User chốt → tạo ADR `docs/decisions/NNNN-title.md`
- Cập nhật `docs/discussions/README.md` + `docs/decisions/README.md`

**Quy tắc:** Không tự ý chốt quyết định kiến trúc. Luôn hỏi user.

---

### Bước 4: PLAN (Lập kế hoạch)

- Xác định files cần sửa/tạo
- >5 files hoặc phức tạp → **EnterPlanMode**
- Plan gồm: files, thứ tự, dependencies, risk
- User approve → Bước 5

---

### Bước 5: IMPLEMENT (Triển khai)

- Code theo plan đã duyệt
- Theo `.agents/03-conventions.md`
- Commit nhỏ, 1 thay đổi logic/commit
- **🔒 SAU MỖI COMMIT → Mở WORKMAP.md → Cập nhật checklist + nhật ký**
- Tự review diff trước khi báo xong

---

### Bước 6: VERIFY (Kiểm tra)

- Review diff: bug? thừa/thiếu?
- UI → verify end-to-end (mở browser test)
- Model inference → test với audio tham chiếu thực tế
- VRAM → kiểm tra `nvidia-smi` trước và sau
- Báo cáo: ✅ / ⚠️ / ❌

---

### Bước 7: LOG (Ghi chép)

- Cập nhật `.agents/handoff.md` (BẮT BUỘC)
- Tạo session log nếu >3 files hoặc >50 dòng
- Cập nhật WORKMAP.md
- Commit + push (nếu có remote)
