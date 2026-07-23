# Tầm Nhìn — OmniVoice

> **Tại sao chúng ta làm dự án này? Chúng ta muốn đi đến đâu?**

---

## Bối Cảnh

OmniVoice là mô hình TTS zero-shot mạnh nhất thế giới về độ phủ ngôn ngữ (646 ngôn ngữ).
Tuy nhiên, trải nghiệm người dùng Việt Nam còn nhiều rào cản:

- Tài liệu 100% tiếng Anh
- Yêu cầu GPU cao (8GB+), trong khi phần lớn người dùng Việt Nam có GPU 4GB hoặc không có GPU
- Không có giao diện tiếng Việt
- Chưa có quy trình đơn giản để tạo và tái sử dụng giọng nói cá nhân

## Sứ Mệnh

**Đưa OmniVoice đến tay người dùng Việt Nam và quốc tế một cách dễ dàng nhất.**

## Mục Tiêu 6 Tháng

| # | Mục tiêu | Đo lường |
|---|---|---|
| 1 | **UI tiếng Việt hoàn chỉnh** — không chỉ demo Gradio, mà là web app | Người dùng VN dùng được ngay |
| 2 | **Colab notebook 1-click** — không cần cài đặt, không cần GPU | 1 click → có giọng nói |
| 3 | **Voice Pack** — đóng gói giọng nói cá nhân, tái sử dụng dễ dàng | Load + generate < 30 giây |
| 4 | **Tối ưu cho GPU yếu** — chạy được trên 4GB VRAM với chất lượng tốt | Inference < 2 phút/audio |
| 5 | **API service** — triển khai trên Vercel/Fly.io, tích hợp vào ứng dụng khác | REST API production-ready |

## Nguyên Tắc

1. **Người dùng là trên hết** — UI/UX phải đẹp, nhanh, dễ hiểu
2. **Tiếng Việt first** — mọi tài liệu, UI, hướng dẫn đều có tiếng Việt
3. **Chi phí thấp** — ưu tiên giải pháp free/cheap (Colab, Kaggle) trước khi đòi GPU xịn
4. **Mã nguồn mở** — mọi cải tiến đều public, đóng góp lại upstream nếu có thể
5. **Thực dụng** — ship nhanh, test thực tế, không over-engineer

## Không Phải Mục Tiêu

- Cạnh tranh với ElevenLabs / OpenAI TTS — họ có hàng trăm GPU, ta không
- Huấn luyện model từ đầu — ta dùng pretrained + fine-tune
- Hỗ trợ tất cả 646 ngôn ngữ như nhau — ưu tiên tiếng Việt, Anh, Trung, Nhật, Hàn
