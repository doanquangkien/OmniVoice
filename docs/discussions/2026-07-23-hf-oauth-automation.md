# Mô Hình HF Space Tự Động — User Không Cần Cài Đặt

> **Mục tiêu:** User vào website, click 1 nút "Kết nối", 30 giây sau có GPU riêng.
> **Chi phí:** $0 cho cả user lẫn developer.

---

## Tổng Quan

Mỗi user sở hữu 1 HF Space riêng (GPU T4, ZeroGPU miễn phí). Website của chúng ta tự động tạo Space này qua HF API + OAuth. User không thấy gì ngoài nút "Kết nối" và màn hình "Đang thiết lập...".

```
┌──────────────────────────────────────────────────────────────┐
│  doanquangkien.com/voices                                    │
│                                                              │
│  Lần đầu:                              Những lần sau:        │
│  ┌────────────────────────┐            ┌─────────────────┐   │
│  │  🔌 Kết nối GPU        │            │  ✅ Sẵn sàng    │   │
│  │                        │            │                  │   │
│  │  Click để thiết lập    │            │  Chọn giọng:     │   │
│  │  GPU miễn phí cho      │            │  [● Nam] [○ Nữ] │   │
│  │  riêng bạn.            │            │                  │   │
│  │                        │            │  ┌────────────┐  │   │
│  │  Cần: tài khoản HF     │            │  │ Nhập text.. │  │   │
│  │  (miễn phí, 1 phút)    │            │  └────────────┘  │   │
│  │                        │            │                  │   │
│  │     [KẾT NỐI NGAY]     │            │  [🎵 TẠO]        │   │
│  └────────────────────────┘            │                  │   │
│                                         │  ═══🔉═══ ▶     │   │
│                                         └─────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

---

## Kiến Trúc Chi Tiết

### Sơ đồ tổng thể

```
┌─────────────────────────────────────────────────────────────────┐
│                        INTERNET                                  │
│                                                                  │
│  User Browser                                                    │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  doanquangkien.com/voices (GitHub Pages)                │     │
│  │                                                        │     │
│  │  ┌──────────────────────────────────────────────────┐  │     │
│  │  │  React SPA                                       │  │     │
│  │  │  - Giao diện tạo giọng nói                       │  │     │
│  │  │  - Voice selector                                │  │     │
│  │  │  - Audio player                                  │  │     │
│  │  │                                                  │  │     │
│  │  │  🔐 Auth Layer                                   │  │     │
│  │  │  - HF OAuth token (localStorage)                 │  │     │
│  │  │  - Space URL của user (localStorage)             │  │     │
│  │  │  - Health check định kỳ                          │  │     │
│  │  │                                                  │  │     │
│  │  │  🔌 API Layer                                    │  │     │
│  │  │  - POST {user_space}/api/predict                 │  │     │
│  │  └──────────────────────────────────────────────────┘  │     │
│  └────────────────────────────────────────────────────────┘     │
│        │                                                         │
│        │  OAuth redirect                                         │
│        ▼                                                         │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  HuggingFace OAuth                                      │     │
│  │  https://huggingface.co/oauth/authorize                 │     │
│  │  → User click "Allow"                                   │     │
│  │  → Redirect về web với auth code                        │     │
│  │  → Web đổi code lấy access token                        │     │
│  └────────────────────────────────────────────────────────┘     │
│        │                                                         │
│        │  HF API (dùng access token của user)                    │
│        ▼                                                         │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  HuggingFace API                                        │     │
│  │  api.huggingface.co                                     │     │
│  │                                                         │     │
│  │  POST /api/spaces/{user}/omnivoice-tts/duplicate       │     │
│  │  → Tạo Space từ template                                │     │
│  │                                                         │     │
│  │  GET  /api/spaces/{user}/omnivoice-tts/runtime          │     │
│  │  → Kiểm tra trạng thái (BUILDING → RUNNING → SLEEPING)  │     │
│  └────────────────────────────────────────────────────────┘     │
│        │                                                         │
│        │  Inference request (trực tiếp từ browser)               │
│        ▼                                                         │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  HF Space của user (GPU T4, ZeroGPU)                    │     │
│  │  https://{user}-omnivoice-tts.hf.space                  │     │
│  │                                                         │     │
│  │  ┌──────────────────────────────────────────────────┐  │     │
│  │  │  app.py (template từ developer)                  │  │     │
│  │  │  - OmniVoice model (loaded, ready)               │  │     │
│  │  │  - Voice Packs (3-5 giọng Việt)                  │  │     │
│  │  │  - Gradio API: /api/predict                      │  │     │
│  │  └──────────────────────────────────────────────────┘  │     │
│  └────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Luồng Kết Nối Lần Đầu (User Perspective)

### Những gì user thấy

```
Bước 1:  ┌─────────────────────────────────┐
         │  🔌 Kết nối GPU miễn phí        │
         │                                 │
         │  Bạn cần 1 tài khoản            │
         │  HuggingFace (miễn phí).        │
         │                                 │
         │     [KẾT NỐI VỚI HUGGINGFACE]   │
         └─────────────────────────────────┘

Bước 2:  (Popup HF OAuth)
         ┌─────────────────────────────────┐
         │  OmniVoice muốn:                │
         │  ✅ Đọc profile của bạn         │
         │  ✅ Tạo Space từ template       │
         │                                 │
         │     [CHO PHÉP]   [TỪ CHỐI]      │
         └─────────────────────────────────┘

Bước 3:  ┌─────────────────────────────────┐
         │  ⚙️ Đang thiết lập GPU...       │
         │                                 │
         │  ████████░░░░  60%              │
         │  Đang tạo Space riêng cho bạn   │
         └─────────────────────────────────┘

Bước 4:  ┌─────────────────────────────────┐
         │  ✅ Sẵn sàng!                   │
         │                                 │
         │  GPU T4 16GB đã sẵn sàng.       │
         │  Bắt đầu tạo giọng nói ngay.    │
         │                                 │
         │  Chọn giọng:                    │
         │  [● Nam Bắc] [○ Nữ Bắc]         │
         │                                 │
         │  [Nhập văn bản...]              │
         │                                 │
         │  [🎵 TẠO GIỌNG NÓI]             │
         └─────────────────────────────────┘
```

### Những gì diễn ra bên dưới (user không thấy)

```
1. Browser gửi yêu cầu OAuth đến HuggingFace
2. User cho phép → HF trả về authorization code
3. Browser đổi code lấy access token (có thể qua proxy của dev)
4. Browser gọi HF API: duplicate Space template
5. HF tạo Space → build Docker → cài omnivoice → load model (2-3 phút)
6. Website poll trạng thái Space mỗi 10 giây
7. Space RUNNING → website hiển thị "✅ Sẵn sàng"
8. Lưu {space_url, hf_token} vào localStorage
```

---

## Luồng Những Lần Sau (User Perspective)

```
1. Mở doanquangkien.com/voices
2. Website tự ping Space của user (dùng URL đã lưu)
3. Nếu Space SLEEPING → "🚀 Đang đánh thức server... (~2 phút)"
   Nếu Space RUNNING → "✅ Sẵn sàng" ngay lập tức
4. Chọn giọng → nhập text → "Tạo" → nghe
```

---

## API Endpoints Cần Thiết

### 1. HF OAuth Flow

```
GET  https://huggingface.co/oauth/authorize
     ?client_id=...
     &redirect_uri=https://doanquangkien.com/voices/auth/callback
     &scope=read-repos+write-repos
     &state=random_string

POST https://huggingface.co/oauth/token
     ?code=...
     &grant_type=authorization_code
     &client_id=...
     &client_secret=...

→ Trả về: { access_token: "hf_xxxx", refresh_token: "..." }
```

### 2. HF Space Management API

```
# Tạo Space từ template
POST https://huggingface.co/api/spaces/{username}/omnivoice-tts/duplicate
Headers: Authorization: Bearer {user_token}
Body: { "template": "doanquangkien/omnivoice-tts-template" }

# Kiểm tra trạng thái Space
GET  https://huggingface.co/api/spaces/{username}/omnivoice-tts/runtime
Headers: Authorization: Bearer {user_token}
→ Trả về: { "stage": "RUNNING" | "BUILDING" | "SLEEPING" | "PAUSED" }

# Đánh thức Space (nếu SLEEPING)
POST https://huggingface.co/api/spaces/{username}/omnivoice-tts/restart
Headers: Authorization: Bearer {user_token}
```

### 3. Inference API (trên Space của user)

```
# Tạo giọng nói
POST https://{username}-omnivoice-tts.hf.space/api/predict
Headers: Authorization: Bearer {user_token}
Body: {
  "data": [
    "Xin chào, đây là giọng nói tiếng Việt.",  # text
    "nam_bac",                                     # voice_id
    32,                                            # num_step
    1.0                                            # speed
  ]
}
→ Trả về: { "data": [{ "name": "output.wav", "data": "base64..." }] }
```

---

## Code Cần Viết

### Trên HF Space Template (`app.py`)

```python
# Space template — user duplicate Space này
# Đã có sẵn: OmniVoice model, 3-5 VoiceClonePrompt tiếng Việt

VOICE_PACKS = {
    "nam_bac":     VoiceClonePrompt.load("voices/nam_bac.pt"),
    "nu_bac":      VoiceClonePrompt.load("voices/nu_bac.pt"),
    "thuyet_minh": VoiceClonePrompt.load("voices/thuyet_minh.pt"),
}

def generate(text, voice_id, num_step=32, speed=1.0):
    prompt = VOICE_PACKS[voice_id]
    audio = model.generate(
        text=text,
        voice_clone_prompt=prompt,
        num_step=num_step,
        speed=speed,
    )
    return (24000, (audio[0] * 32767).astype(np.int16))

# Gradio Blocks với api_name rõ ràng
gr.Interface(
    fn=generate,
    inputs=[
        gr.Textbox(lines=4, label="Văn bản", api_name="text"),
        gr.Dropdown(choices=list(VOICE_PACKS.keys()), label="Giọng", api_name="voice"),
        gr.Slider(4, 64, value=32, label="Bước", api_name="steps"),
        gr.Slider(0.5, 1.5, value=1.0, label="Tốc độ", api_name="speed"),
    ],
    outputs=[gr.Audio(label="Kết quả", api_name="audio")],
).queue().launch()
```

### Trên Website (React)

```typescript
// services/hf.ts
class HFAuthManager {
  // Bước 1: Redirect user đến HF OAuth
  redirectToOAuth() {
    const clientId = '...';  // OAuth App của bạn
    const redirectUri = 'https://doanquangkien.com/voices/auth/callback';
    window.location.href =
      `https://huggingface.co/oauth/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&scope=read-repos+write-repos`;
  }

  // Bước 2: Handle callback, đổi code lấy token
  async handleCallback(code: string) {
    const token = await exchangeCodeForToken(code);
    localStorage.setItem('hf_token', token);
    return token;
  }
}

class SpaceManager {
  // Bước 3: Tạo Space từ template
  async createSpace(token: string) {
    const username = await getHFUsername(token);
    const spaceUrl = `${username}-omnivoice-tts`;

    // Duplicate template Space
    await fetch(`https://huggingface.co/api/spaces/${username}/omnivoice-tts/duplicate`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` },
      body: JSON.stringify({ template: 'doanquangkien/omnivoice-tts-template' }),
    });

    // Poll status cho đến khi RUNNING
    await this.waitForReady(username, token);

    localStorage.setItem('space_url', spaceUrl);
    return spaceUrl;
  }

  async waitForReady(username: string, token: string) {
    while (true) {
      const res = await fetch(
        `https://huggingface.co/api/spaces/${username}/omnivoice-tts/runtime`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      const { stage } = await res.json();
      if (stage === 'RUNNING') return;
      if (stage === 'BUILDING') { await sleep(10000); continue; }
      throw new Error(`Space failed: ${stage}`);
    }
  }
}

class InferenceAPI {
  // Bước 4: Gọi Space API để tạo giọng nói
  async generate(text: string, voiceId: string, speed: number = 1.0) {
    const spaceUrl = localStorage.getItem('space_url');
    const token = localStorage.getItem('hf_token');

    const res = await fetch(`https://${spaceUrl}.hf.space/api/predict`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ data: [text, voiceId, 32, speed] }),
    });

    const { data } = await res.json();
    return data[0].data; // base64 audio
  }
}
```

---

## Cần Chuẩn Bị

### Từ phía Developer

| # | Cần làm | Mục đích |
|---|---|---|
| 1 | Đăng ký HF OAuth App (Settings → OAuth Apps) | Lấy `client_id` + `client_secret` |
| 2 | Tạo Space template `doanquangkien/omnivoice-tts-template` | Space mẫu để user duplicate |
| 3 | Encode 3-5 VoiceClonePrompt tiếng Việt (dùng Colab) | Giọng mẫu cho user chọn |
| 4 | Deploy website lên GitHub Pages / Vercel | Frontend cố định |
| 5 | Optional: Proxy server nhẹ (Vercel Functions) | Giấu `client_secret`, đổi code lấy token |

### Từ phía User

| # | Cần làm | Thời gian |
|---|---|---|
| 1 | Có tài khoản HuggingFace (email + password) | 1 phút |
| 2 | Click "Cho phép" trong popup OAuth | 5 giây |
| — | **Không cần gì thêm** | — |

---

## Các Trạng Thái Website

### Trạng thái 1: Chưa kết nối

```
┌─────────────────────────────────┐
│  🔌 Chưa kết nối GPU            │
│                                 │
│  Để tạo giọng nói, bạn cần      │
│  kết nối với GPU miễn phí       │
│  từ HuggingFace.                │
│                                 │
│  🕐 Mất ~3 phút, chỉ làm 1 lần  │
│  💰 Hoàn toàn miễn phí          │
│  🔒 GPU của riêng bạn           │
│                                 │
│     [🔌 KẾT NỐI NGAY]           │
└─────────────────────────────────┘
```

### Trạng thái 2: Đang thiết lập

```
┌─────────────────────────────────┐
│  ⚙️ Đang thiết lập GPU...       │
│                                 │
│  ████████████░░░  80%           │
│                                 │
│  ✅ Tài khoản HF: OK            │
│  ✅ Tạo Space: OK               │
│  ⏳ Cài đặt model... (2 phút)   │
│                                 │
│  Không tắt trang này nhé!       │
└─────────────────────────────────┘
```

### Trạng thái 3: Space đang ngủ

```
┌─────────────────────────────────┐
│  🚀 Đang đánh thức server...    │
│                                 │
│  GPU của bạn đang ngủ để        │
│  tiết kiệm tài nguyên.          │
│  Đang khởi động lại...          │
│                                 │
│  ⏳ Khoảng 2-3 phút             │
│                                 │
│  (Chỉ xảy ra khi lâu không dùng)│
└─────────────────────────────────┘
```

### Trạng thái 4: Sẵn sàng

```
┌─────────────────────────────────┐
│  ✅ Sẵn sàng                    │
│                                 │
│  Chọn giọng:                    │
│  [● Nam Bắc] [○ Nữ Bắc] [○ Khác]│
│                                 │
│  ┌─────────────────────────┐    │
│  │ Nhập văn bản cần đọc... │    │
│  └─────────────────────────┘    │
│                                 │
│  [🎵 TẠO GIỌNG NÓI]             │
│                                 │
│  ── Kết quả ──                  │
│  ═══════🔉═══════ ▶ 00:12       │
│  [⬇ Tải về]                     │
└─────────────────────────────────┘
```

### Trạng thái 5: Đang tạo

```
┌─────────────────────────────────┐
│  🎵 Đang tạo giọng nói...       │
│                                 │
│  ████████░░░░  65%              │
│                                 │
│  Bước 21/32 — khoảng 15s nữa    │
│                                 │
│  [HỦY]                          │
└─────────────────────────────────┘
```

---

## Rủi Ro & Giải Pháp

| Rủi ro | Mức độ | Giải pháp |
|---|---|---|
| **HF từ chối OAuth App** (chưa được review) | 🟡 | Fallback: hướng dẫn user tạo token thủ công (Mức 1) |
| **Space build fail** (lỗi dependency) | 🟡 | Test template kỹ trước khi public; hiển thị log lỗi cho user |
| **User hết ZeroGPU quota** (dùng nhiều quá) | 🟡 | Hiển thị "Bạn đã dùng hết GPU hôm nay. Quay lại sau hoặc nâng cấp lên HF Pro ($9/tháng)" |
| **Space bị xóa** (user xóa nhầm) | 🟢 | Nút "Tạo lại Space" — duplicate lại từ template, giữ nguyên voice packs |
| **HF API thay đổi** | 🟢 | Version pin trong code; monitor HF changelog |

---

## So Sánh Cuối Cùng

| | Colab | HF Space Mức 1 (Thủ công) | **HF Space Mức 2 (OAuth Auto)** |
|---|---|---|---|
| **User setup** | 3-5 phút, 4 bước | 1-3 phút, 3 bước | **30 giây, 2 click** |
| **Cần tài khoản** | Google | HuggingFace | HuggingFace |
| **ToS** | 🔴 Vi phạm | ✅ OK | ✅ OK |
| **Ổn định** | ❌ Ngắt 1-3h | ✅ Persistent | ✅ Persistent |
| **Dev effort** | Thấp (notebook) | Trung bình | **Cao (OAuth + Space API)** |
| **UX** | ⭐⭐ | ⭐⭐⭐ | **⭐⭐⭐⭐⭐** |
| **Thời gian build** | 1 ngày | 2-3 ngày | **1-2 tuần** |

---

## Lộ Trình Đề Xuất

```
Tuần 1-2: Mức 1 (user tự duplicate Space, paste token)
          → Validate model hoạt động, có user thật test
          → Thu thập feedback

Tuần 3-4: Mức 2 (OAuth tự động)
          → Chỉ build nếu Mức 1 có >50 user
          → Đầu tư OAuth khi đã chắc chắn model ổn định
```

---

*Sẵn sàng thảo luận và điều chỉnh.*
