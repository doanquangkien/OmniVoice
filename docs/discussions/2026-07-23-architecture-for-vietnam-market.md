# Kiến Trúc Triển Khai Cho Thị Trường Việt Nam

> **Bối cảnh:** User Việt Nam — không GPU — cần giải pháp đơn giản, 1 click.
> **Mục tiêu:** App TTS tiếng Việt 100%, clone giọng + render, có sẵn giọng mẫu, hỗ trợ tự train.

---

## Ràng Buộc Cứng

| # | Ràng buộc | Hệ quả |
|---|---|---|
| 1 | **User không có GPU** | Không thể inference local — phải dùng cloud GPU hoặc CPU cực chậm |
| 2 | **Phân phối dạng EXE** | Cần đóng gói Python + deps → file lớn (500MB-2GB) |
| 3 | **Chỉ tiếng Việt** | Có thể cắt bỏ multilingual weights → giảm kích thước model |
| 4 | **Clone giọng + render** | Cần GPU cho diffusion 32 bước |
| 5 | **Có sẵn giọng mẫu** | VoiceClonePrompt pre-computed → load nhanh |
| 6 | **Tự train giọng mới** | Cần GPU mạnh hơn (fine-tune) → cloud bắt buộc |

---

## Phân Tích 3 Hướng Triển Khai

### Hướng A: Desktop EXE + CPU Inference

```
┌─────────────────────────────────┐
│  OmniVoice Desktop.exe          │
│  ┌───────────────────────────┐  │
│  │  PyInstaller/Nuitka       │  │
│  │  + Python 3.13            │  │
│  │  + PyTorch CPU            │  │
│  │  + OmniVoice model (VN)   │  │
│  │  + Whisper tiny/small     │  │
│  │  + Gradio/Electron UI     │  │
│  └───────────────────────────┘  │
│                                 │
│  Inference: CPU (chậm)          │
│  Model size: ~1-2 GB            │
│  EXE size: ~3-5 GB              │
└─────────────────────────────────┘
```

| Ưu | Nhược |
|---|---|
| ✅ Offline 100% — không cần mạng | 🔴 **CPU inference quá chậm** (ước tính 30-60 phút/audio) |
| ✅ Cài đặt 1 lần, dùng mãi mãi | 🔴 EXE khổng lồ (3-5 GB) — khó phân phối |
| ✅ Không phụ thuộc cloud | 🔴 Mỗi lần update model = tải lại toàn bộ EXE |
| ✅ Bảo mật tuyệt đối (local) | 🔴 Không tận dụng được GPU cloud |

> **Kết luận:** Không khả thi cho production. User chấp nhận chờ 1 phút, không phải 1 giờ.

---

### Hướng B: Web App + GPU Server (SaaS)

```
┌──────────────────────┐     HTTPS      ┌──────────────────────┐
│  User Browser        │ ◄────────────► │  GPU Server          │
│  (mọi thiết bị)      │                │  (VPS/Vercel/Fly.io) │
│                      │                │                      │
│  React/Vue SPA       │                │  FastAPI + OmniVoice │
│  Tailscale net       │                │  + Whisper ASR       │
│  Giao diện VN        │                │  + Voice DB          │
│                      │                │  GPU: A10/L4/A100    │
└──────────────────────┘                └──────────────────────┘
```

| Ưu | Nhược |
|---|---|
| ✅ User không cần GPU — chỉ cần browser | 🔴 **Chi phí GPU server cao** ($0.5-2/giờ) |
| ✅ Không cần cài đặt gì | 🔴 Cần internet ổn định |
| ✅ Update model ngay lập tức | 🔴 Chi phí vận hành liên tục |
| ✅ Dùng được trên mobile/tablet | 🔴 Phải có payment system (subscription) |
| ✅ Tailscale = bảo mật, không public internet | 🔴 Phải quản lý auth + user data |

> **Kết luận:** Tốt nhất về UX, nhưng cần vốn vận hành GPU server. Phù hợp nếu có kế hoạch thu phí.

---

### Hướng C: Hybrid — Desktop App + Colab Bridge (ĐỀ XUẤT)

```
┌─────────────────────────────────────────────────────────┐
│  OmniVoice Desktop.exe (~200 MB)                        │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │  Electron/Tauri shell                             │ │
│  │  ┌─────────────────────────────────────────────┐  │ │
│  │  │  React UI (tiếng Việt)                      │  │ │
│  │  │  - Soạn văn bản                             │  │ │
│  │  │  - Chọn giọng có sẵn / upload giọng mới     │  │ │
│  │  │  - Lịch sử audio đã tạo                     │  │ │
│  │  │  - Quản lý Voice Pack                       │  │ │
│  │  └─────────────────────────────────────────────┘  │ │
│  │                                                    │ │
│  │  ┌─────────────────────────────────────────────┐  │ │
│  │  │  Colab Bridge (background service)           │  │ │
│  │  │  - Kết nối tới Colab notebook của user      │  │ │
│  │  │  - Gửi text + ref_audio → nhận audio        │  │ │
│  │  │  - Queue + retry + progress bar             │  │ │
│  │  │  - Health check + auto-reconnect            │  │ │
│  │  └─────────────────────────────────────────────┘  │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  FALLBACK: CPU Inference (khẩn cấp)              │  │
│  │  - PyTorch CPU + num_step=4                      │  │
│  │  - Rất chậm nhưng vẫn chạy nếu mất mạng         │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                          │ ngrok/cloudflared tunnel
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Google Colab (GPU T4 16GB — MIỄN PHÍ)                  │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │  OmniVoice Colab Runtime                          │ │
│  │  - Cài đặt tự động (pip install omnivoice)        │ │
│  │  - Load model + Voice Packs từ Google Drive       │ │
│  │  - Gradio API endpoint (/generate)                │ │
│  │  - ngrok public URL → gửi về Desktop App          │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  Thời gian setup: 3-5 phút (1 lần)                      │
│  Thời gian inference: 30-60 giây/audio                  │
│  Giới hạn: 4-6h GPU/ngày (free)                         │
└─────────────────────────────────────────────────────────┘
```

| Ưu | Nhược |
|---|---|
| ✅ **User không cần GPU** — dùng GPU Colab miễn phí | ⚠️ Cần Google account |
| ✅ **EXE nhẹ** (~200 MB, chỉ chứa UI) | ⚠️ Setup lần đầu 3-5 phút (1 lần duy nhất) |
| ✅ **Inference nhanh** (30-60s trên T4) | ⚠️ Cần internet khi dùng |
| ✅ **Chi phí = $0** cho cả dev lẫn user | ⚠️ Colab ngắt sau 4-6h, phải reconnect |
| ✅ **Có fallback CPU** khi mất mạng | ⚠️ Phụ thuộc vào chính sách Colab của Google |
| ✅ **Voice Packs lưu trên Google Drive** | |

> **Kết luận:** 🏆 **ĐỀ XUẤT HƯỚNG NÀY** — giải quyết được tất cả ràng buộc: user nghèo GPU, EXE nhẹ, inference nhanh, chi phí $0.

---

## So Sánh 3 Hướng

| Tiêu chí | A: EXE + CPU | B: SaaS Web | C: Hybrid Colab |
|---|---|---|---|
| **Cần GPU user?** | Không | Không | Không |
| **Tốc độ inference** | 🔴 30-60 phút | 🟢 10-30 giây | 🟢 30-60 giây |
| **Chi phí vận hành** | 🟢 $0 | 🔴 $200-500/tháng | 🟢 $0 |
| **Kích thước app** | 🔴 3-5 GB | 🟢 0 MB | 🟢 ~200 MB |
| **Offline được?** | ✅ Có | ❌ Không | ⚠️ Fallback CPU |
| **Cập nhật model** | 🔴 Tải lại toàn bộ | 🟢 Ngay lập tức | 🟢 Cập nhật Colab notebook |
| **Bảo mật** | 🟢 Tuyệt đối | ⚠️ Audio qua server | ⚠️ Audio qua Colab |
| **Setup lần đầu** | 🟢 Cài 1 lần | 🟢 Không cần | ⚠️ 3-5 phút |
| **Phù hợp user VN?** | ❌ Quá chậm | ⚠️ Cần thu phí | ✅ Tối ưu |

---

## Kiến Trúc Đề Xuất Chi Tiết (Hướng C)

### Luồng Người Dùng

```
LẦN ĐẦU TIÊN:
  1. Tải EXE (~200 MB) → cài đặt
  2. Mở app → popup hướng dẫn: "Bạn cần 1 tài khoản Google miễn phí"
  3. Click "Kết nối Colab" → app mở browser → user copy Colab link
  4. Colab notebook tự động:
     - pip install omnivoice
     - Tải model + Voice Packs từ Google Drive
     - Khởi động Gradio server + ngrok tunnel
     - Hiển thị URL endpoint
  5. User paste URL vào app → DONE

MỖI LẦN DÙNG SAU:
  1. Mở app → click "Kết nối"
  2. App tự mở Colab notebook (đã lưu trong Drive)
  3. Chạy cell "Connect" → 30 giây → sẵn sàng
  4. Soạn text → chọn giọng → Generate → 30-60 giây → có audio
```

### Voice Pack System

```
Voice Pack (*.ovoice) = 1 file zip chứa:
  ├── voice_clone_prompt.pt     ← Embedding đã encode sẵn
  ├── preview.wav               ← Audio demo 10 giây
  ├── metadata.json             ← Tên, mô tả, ngày tạo
  └── avatar.jpg                ← Ảnh đại diện (optional)

CÁCH TẠO:
  - User upload audio 30-60 giây
  - App gửi lên Colab → encode → trả về Voice Pack
  - Lưu vào thư viện local + Google Drive

GIỌNG MẪU (đóng gói sẵn):
  - Giọng Nam Bắc Trung (3 giọng)
  - Giọng thuyết minh phim
  - Giọng đọc sách
  - Giọng trẻ em
```

### Stack Kỹ Thuật

```
FRONTEND (Desktop App):
  - Tauri (Rust shell, ~5MB) + React (UI)
  - Tailwind CSS + shadcn/ui
  - Giao diện tiếng Việt 100%
  - Build: .exe ~50MB + runtime ~150MB

BACKEND (Colab):
  - Python FastAPI + Gradio
  - OmniVoice model (float16, T4)
  - ngrok tunnel (free tier, 1 tunnel)
  - Google Drive mount (lưu Voice Packs)

FALLBACK (Local CPU):
  - PyTorch CPU build
  - num_step=4 (siêu nhanh, chất lượng thấp)
  - Whisper tiny (ASR)
  - Chỉ dùng khi mất mạng hoặc Colab hết quota
```

---

## Các Quyết Định Cần CEO Chốt

| # | Câu hỏi | Gợi ý |
|---|---|---|
| D1 | **Hướng nào?** A (EXE+CPU) / B (SaaS) / C (Hybrid Colab)? | **C** — tối ưu cho user VN nghèo GPU |
| D2 | **Desktop framework?** Electron vs Tauri? | **Tauri** — nhẹ hơn, file .exe nhỏ hơn nhiều |
| D3 | **Colab tunnel?** ngrok vs cloudflared vs localhost.run? | **ngrok** — ổn định nhất, free 1 tunnel |
| D4 | **Voice Pack format?** File .pt đơn giản vs zip có metadata? | **Zip** — đầy đủ metadata, dễ share |
| D5 | **Số lượng giọng mẫu?** Bao nhiêu giọng pre-trained? | 3-5 giọng cơ bản |
| D6 | **Fallback CPU?** Có cần không? | **Có** — cho trường hợp khẩn cấp |
| D7 | **Tự train giọng mới?** Làm trên Colab hay bắt buộc cloud khác? | **Colab Pro** (cần GPU 16GB+ cho fine-tune) |
| D8 | **Monetization?** Miễn phí hoàn toàn hay có premium? | Premium: nhiều giọng hơn, ưu tiên queue, không giới hạn |

---

## Lộ Trình Đề Xuất

| Giai đoạn | Nội dung | Thời gian |
|---|---|---|
| **P0: Colab PoC** | Colab notebook hoạt động ổn định, test inference nhanh | 1-2 ngày |
| **P1: Voice Packs** | Tạo 3-5 giọng mẫu tiếng Việt, đóng gói .ovoice | 2-3 ngày |
| **P2: Desktop App MVP** | Tauri + React, giao diện cơ bản, kết nối Colab | 1-2 tuần |
| **P3: Polish** | Voice Pack manager, lịch sử, batch render, fallback CPU | 1 tuần |
| **P4: Beta** | Test với 10-20 user, thu thập feedback | 1 tuần |
| **P5: Release** | Public release, hướng dẫn video tiếng Việt | 1 tuần |
