# Constitution — OmniVoice

> **Quy tắc bất biến.** Mọi agent phải tuân thủ. Thay đổi constitution cần có ADR + user approval.

---

## 1. Agent-First

Mọi code, docs, commit message đều viết để **Agent tương lai** đọc hiểu được trong thời gian ngắn nhất.

- Không "ngầm hiểu" (tribal knowledge)
- Không viết tắt không giải thích
- Comment nói **tại sao** (why), không nói **cái gì** (what — code đã nói rồi)
- Mỗi file quan trọng đều có header mô tả mục đích

---

## 2. Document Before Code

```
Thảo luận → Ghi discussion → Chốt ADR → Viết spec → Code
```

- Không code trước khi có spec được duyệt (cho tính năng mới)
- Mọi quyết định kiến trúc quan trọng phải có ADR
- Mọi cuộc thảo luận chưa chốt phải có discussion file

---

## 3. Session Log Discipline

Sau mỗi phiên làm việc có thay đổi đáng kể:

| Trigger | Hành động |
|---------|-----------|
| >3 files hoặc >50 dòng thay đổi | Ghi session log mới |
| Cuối mỗi phiên (bất kể thay đổi) | Cập nhật `handoff.md` |
| Quyết định mới được chốt | Tạo ADR |
| Bug quan trọng được fix | Ghi vào session log |

---

## 4. Commit Hygiene

```
[type] mô tả ngắn gọn bằng tiếng Việt

type ∈ {feat, fix, refactor, docs, chore, test}
```

- 1 commit = 1 thay đổi logic
- Không gộp nhiều thay đổi không liên quan vào 1 commit
- Commit message viết bằng tiếng Việt
- Nhánh chính: `main`

---

## 5. Workmap Discipline — QUY TẮC CỨNG

**Sau MỖI LẦN commit, Agent PHẢI:**

1. Mở `docs/workmaps/WORKMAP.md`
2. Cập nhật checklist: đánh dấu [x] task vừa xong
3. Ghi nhật ký: `HH:MM — Commit abc123: [mô tả ngắn]`
4. Nếu có phát sinh mới → thêm vào mục "Phát sinh"

**Không ngoại lệ.** Commit mà không update workmap = vi phạm constitution.

---

## 6. Code Quality

- DRY nhưng không over-engineer
- Function < 50 dòng
- File < 500 dòng (trừ migration/data/config files)
- Type hints cho mọi Python function
- Validate input ở edge, không ở middle

---

## 7. Model First, Code Second

- Trải nghiệm người dùng model là ưu tiên số 1
- Inference speed > code elegance
- VRAM optimization > abstraction
- API đơn giản, dễ dùng > API tổng quát, phức tạp
- Tài liệu tiếng Việt luôn được cập nhật song song với code
