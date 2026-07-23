# Coding Conventions — OmniVoice

> **Chuẩn mực code.** Áp dụng cho mọi thay đổi Python trong dự án.

---

## Python

### Phong cách

- **Formatter:** Ruff (cấu hình trong `pyproject.toml`)
- **Linter:** Ruff — ignore: F401, E402, F403, F841, E741
- **Type hints:** Bắt buộc cho mọi function public
- **Docstring:** Google style cho function public

### Cấu trúc

```python
# 1. Imports — stdlib → third-party → local
import os
from typing import Optional

import torch
import numpy as np

from omnivoice.utils.common import get_best_device

# 2. Constants — UPPER_CASE
DEFAULT_SAMPLE_RATE = 24000

# 3. Functions — snake_case, < 50 dòng
def process_audio(audio_path: str, sample_rate: int = DEFAULT_SAMPLE_RATE) -> np.ndarray:
    """Xử lý audio đầu vào.

    Args:
        audio_path: Đường dẫn đến file audio.
        sample_rate: Sample rate mong muốn. Mặc định 24000.

    Returns:
        Numpy array với shape (T,).
    """
    ...
```

### Quy tắc

- Function < 50 dòng — nếu dài hơn → tách
- File < 500 dòng — nếu dài hơn → split module
- Không `except Exception` trần — luôn specify loại hoặc log `type(e).__name__`
- Validate input ở edge (CLI args, API params), không ở middle

---

## Git

### Commit Message

```
[type] mô tả ngắn gọn bằng tiếng Việt

type ∈ {feat, fix, refactor, docs, chore, test}
```

Ví dụ:
```
feat Việt hóa toàn bộ giao diện Gradio demo
fix Chặn double-click nút "Tạo giọng nói" gây OOM
docs Thêm CLAUDE.md + hệ thống quản lý dự án chuyên nghiệp
```

### Branch

- `main` — nhánh chính duy nhất
- Không cần branch phụ cho dự án nhỏ — commit thẳng main
- Nếu thử nghiệm lớn → tạo branch `wip/ten-tinh-nang`

---

## UI (Gradio)

### Quy tắc Việt hóa

- Tất cả text hiển thị cho user: **tiếng Việt**
- Giữ nguyên key/value cho model (ví dụ: `"Male / Nam"` — phần `Male` cho model, `Nam` cho UI)
- Placeholder, label, info text: tiếng Việt
- Status message: tiếng Việt

### Quy tắc UI

- Button generate luôn có `concurrency_limit=1`
- Button tự disable khi đang xử lý (`gr.update(interactive=False)`)
- Hiển thị trạng thái "Đang xử lý..." trong khi chạy

---

## Model / Inference

### VRAM Awareness

- Luôn kiểm tra `nvidia-smi` trước khi thay đổi cấu hình inference
- Mặc định dùng `--no-asr` cho local GPU < 8GB
- Test trên Colab T4 trước khi claim "chạy được trên X GB"
- Ghi log VRAM usage vào session log

### Model Generation

- Dùng `OmniVoiceGenerationConfig` thay vì truyền keyword arguments rời rạc
- Mặc định `num_step=32` cho production, `16` cho testing nhanh
- Không thay đổi default generation parameters mà không có ghi chú
