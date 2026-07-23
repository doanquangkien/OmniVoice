# Quick Reference — Agent Decision Tree

> **Mục đích:** Khi gặp tình huống, tra nhanh ở đây — không cần đọc lại toàn bộ workflow.
> **In đậm:** file cần update. In nghiêng: file cần đọc.

---

## TÌNH HUỐNG → HÀNH ĐỘNG

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                      │
│  TÔI MỚI VÀO PHIÊN, CHƯA BIẾT GÌ                                     │
│  ├── Đọc: .agents/handoff.md (việc đang dở)                          │
│  ├── Đọc: docs/discussions/README.md (đang bàn gì)                    │
│  ├── Đọc: docs/KNOWN-ISSUES.md (bug đang tồn tại)                     │
│  └── Đọc + viết tiếp: docs/workmaps/WORKMAP.md                       │
│                                                                      │
│  📬 HÒM THƯ REPORTS — NƠI MỌI AGENT GỬI BÁO CÁO                       │
│  ├── docs/reports/README.md ← VÀO ĐÂY ĐỂ XEM CÓ GÌ ĐANG CHỜ         │
│  ├── Mỗi agent xong việc → tạo 1 file report → cập nhật inbox       │
│  └── → Không bỏ sót bug, không quên việc cần làm                    │
│                                                                      │
│  🗺️ WORKMAP — SỔ TAY TRUYỀN TAY (1 FILE DUY NHẤT)                      │
│  ├── Đọc: docs/workmaps/WORKMAP.md (Agent trước đang dở gì?)       │
│  ├── VIẾT TIẾP vào WORKMAP.md — thêm section mới, không tạo file   │
│  ├── Cập nhật checklist + phát sinh                                  │
│  └── → Agent A viết → Agent B đọc + viết tiếp → truyền tay mãi    │
│                                                                      │
│  USER BÁO 1 BUG                                                      │
│  ├── Ghi vào: docs/KNOWN-ISSUES.md (thêm entry mới)                  │
│  ├── Nếu nghiêm trọng → báo user, hỏi có fix ngay không              │
│  └── Khi fix xong → cập nhật KNOWN-ISSUES.md + CHANGELOG.md          │
│                                                                      │
│  USER YÊU CẦU TÍNH NĂNG MỚI                                          │
│  ├── Chưa có spec → tạo docs/specs/feature-name.md                   │
│  ├── Có sẵn spec → đọc spec → EnterPlanMode → code                   │
│  └── Xong → CHANGELOG.md + handoff.md                                │
│                                                                      │
│  TÔI CẦN ĐƯA RA QUYẾT ĐỊNH KIẾN TRÚC                                 │
│  ├── Tạo docs/discussions/YYYY-MM-DD-topic.md                        │
│  ├── Trình bày options → hỏi user chốt                               │
│  ├── User chốt → tạo docs/decisions/NNNN-title.md (ADR)              │
│  └── Cập nhật docs/discussions/README.md + docs/decisions/README.md  │
│                                                                      │
│  TÔI VỪA COMMIT (SAU MỖI LẦN COMMIT — QUY TẮC CỨNG)                  │
│  ├── 🔒 Mở docs/workmaps/WORKMAP.md — CẬP NHẬT NGAY                  │
│  ├── Đánh dấu [x] task vừa xong trong checklist                      │
│  ├── Ghi nhật ký: HH:MM — Commit abc123: mô tả                       │
│  ├── Nếu có phát sinh → thêm vào mục Phát sinh                       │
│  └── ⏱️ Mất 30 giây — nhưng đảm bảo không quên gì                   │
│                                                                      │
│  📋 TÔI TẠO FILE .MD MỚI — ĐỪNG ĐỂ MỒ CÔI                              │
│  ├── specs/*.md → đăng ký vào CLAUDE.md + specs/README.md (nếu có)  │
│  ├── decisions/*.md → đăng ký vào decisions/README.md               │
│  ├── discussions/*.md → đăng ký vào discussions/README.md           │
│  ├── sessions/*.md → đăng ký vào sessions/README.md                 │
│  └── ❌ File không index = FILE MỒ CÔI → coi như không tồn tại      │
│                                                                      │
│  TÔI VỪA CODE XONG (>3 files hoặc >50 dòng)                          │
│  ├── Cập nhật .agents/handoff.md (BẮT BUỘC)                          │
│  ├── Tạo docs/sessions/SESSION-LOG_YYYY-MM-DD_NN.md                  │
│  ├── Cập nhật docs/sessions/README.md (thêm dòng index)              │
│  ├── Nếu có bug fix → CHANGELOG.md                                   │
│  ├── Nếu có feature → CHANGELOG.md                                   │
│  └── Commit với format [type] mô tả                                  │
│                                                                      │
│  CUỐI PHIÊN — DÙ KHÔNG CODE GÌ CẢ                                    │
│  └── Cập nhật .agents/handoff.md (BẮT BUỘC — ít nhất cập nhật       │
│      "Việc tiếp theo" nếu có thay đổi)                                │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## CHECKLIST CUỐI PHIÊN

Trước khi kết thúc phiên, agent PHẢI kiểm tra:

```
[ ] Đã cập nhật .agents/handoff.md chưa?                    ← BẮT BUỘC
[ ] Có >3 files hoặc >50 dòng thay đổi không?
    [ ] CÓ → Đã tạo session log mới chưa?
    [ ] CÓ → Đã cập nhật docs/sessions/README.md chưa?
[ ] Có fix bug nào không?
    [ ] CÓ → Đã cập nhật docs/KNOWN-ISSUES.md chưa?
    [ ] CÓ → Đã cập nhật CHANGELOG.md chưa?
[ ] Có quyết định kiến trúc mới không?
    [ ] CÓ → Đã tạo ADR chưa?
    [ ] CÓ → Đã đóng discussion liên quan chưa?
[ ] Có thay đổi tech stack không?
    [ ] CÓ → Đã cập nhật .agents/04-stack.md chưa?
[ ] Đã commit với message đúng format chưa?
```
