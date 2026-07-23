"""
OmniVoice HF Space — TTS Tiếng Việt.

Triển khai trên HuggingFace Spaces với GPU T4 (ZeroGPU).
Cung cấp cả Gradio UI và REST API endpoints.

Usage:
    python app.py
"""

import logging
from typing import Any, Dict, Optional

import numpy as np
import torch

from omnivoice import OmniVoice, OmniVoiceGenerationConfig, VoiceClonePrompt
from omnivoice.utils.common import get_best_device

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Model Loading (chạy 1 lần khi Space khởi động)
# ---------------------------------------------------------------------------
DEVICE = get_best_device()
logger.info(f"Loading OmniVoice model on {DEVICE}...")

model = OmniVoice.from_pretrained(
    "k2-fsa/OmniVoice",
    device_map=DEVICE,
    dtype=torch.float16,
    load_asr=True,  # HF Space T4 16GB — dư VRAM cho ASR
)
SAMPLING_RATE = model.sampling_rate
logger.info(f"Model ready! Sampling rate: {SAMPLING_RATE} Hz")

# ---------------------------------------------------------------------------
# Core Generation Function (có thể gọi từ UI hoặc API)
# ---------------------------------------------------------------------------
def generate_tts(
    text: str,
    ref_audio: Optional[str] = None,
    ref_text: Optional[str] = None,
    instruct: Optional[str] = None,
    voice_clone_prompt: Optional[VoiceClonePrompt] = None,
    num_step: int = 32,
    guidance_scale: float = 2.0,
    speed: Optional[float] = None,
    duration: Optional[float] = None,
    language: Optional[str] = None,
) -> tuple[np.ndarray, str]:
    """Sinh giọng nói từ văn bản.

    Args:
        text: Văn bản cần đọc.
        ref_audio: Đường dẫn audio tham chiếu (cho voice cloning).
        ref_text: Nội dung audio tham chiếu (để trống để tự động ASR).
        instruct: Mô tả giọng nói (cho voice design).
        voice_clone_prompt: VoiceClonePrompt đã encode sẵn.
        num_step: Số bước diffusion (mặc định 32).
        guidance_scale: CFG scale (mặc định 2.0).
        speed: Tốc độ nói (>1 nhanh, <1 chậm).
        duration: Độ dài cố định (giây).
        language: Mã ngôn ngữ (vd: "vi", "en").

    Returns:
        (audio_array, status_message)
    """
    if not text or not text.strip():
        raise ValueError("Vui lòng nhập nội dung văn bản.")

    gen_config = OmniVoiceGenerationConfig(
        num_step=num_step,
        guidance_scale=guidance_scale,
        denoise=True,
        preprocess_prompt=True,
        postprocess_output=True,
    )

    kw: Dict[str, Any] = dict(
        text=text.strip(),
        language=language,
        generation_config=gen_config,
    )

    if speed is not None:
        kw["speed"] = speed
    if duration is not None:
        kw["duration"] = duration

    if voice_clone_prompt is not None:
        kw["voice_clone_prompt"] = voice_clone_prompt
    elif ref_audio:
        kw["voice_clone_prompt"] = model.create_voice_clone_prompt(
            ref_audio=ref_audio,
            ref_text=ref_text,
        )

    if instruct and instruct.strip():
        kw["instruct"] = instruct.strip()

    audio = model.generate(**kw)
    return audio[0], "Đã xong!"


def create_voice_pack(
    ref_audio: str,
    ref_text: Optional[str] = None,
) -> VoiceClonePrompt:
    """Tạo VoiceClonePrompt từ audio tham chiếu.

    Args:
        ref_audio: Đường dẫn audio tham chiếu (3-10 giây).
        ref_text: Nội dung audio (để trống để tự động ASR).

    Returns:
        VoiceClonePrompt có thể lưu và tái sử dụng.
    """
    if not ref_audio:
        raise ValueError("Vui lòng cung cấp audio tham chiếu.")
    return model.create_voice_clone_prompt(
        ref_audio=ref_audio,
        ref_text=ref_text,
    )


# ---------------------------------------------------------------------------
# Gradio UI + API
# ---------------------------------------------------------------------------
import gradio as gr


def _build_ui():
    """Xây dựng giao diện Gradio với API endpoints rõ ràng."""

    css = """
    .gradio-container {max-width: 900px !important; margin: 0 auto !important;}
    .gradio-container h1 {font-size: 1.6em !important; text-align: center;}
    .gradio-container .prose {text-align: center; font-size: 1.05em !important;}
    .compact-audio audio {height: 54px !important;}
    footer {display: none !important;}
    """

    theme = gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="slate",
        font=["Inter", "Be Vietnam Pro", "sans-serif"],
    )

    with gr.Blocks(
        theme=theme,
        css=css,
        title="OmniVoice — TTS Tiếng Việt",
    ) as demo:
        gr.Markdown(
            """
            # 🎙 OmniVoice — Chuyển Văn Bản Thành Giọng Nói

            Hỗ trợ **646+ ngôn ngữ** · Clone giọng từ audio tham chiếu · Thiết kế giọng theo ý muốn
            """
        )

        with gr.Tabs():
            # ================================================================
            # Tab 1: Voice Clone
            # ================================================================
            with gr.TabItem("🎙 Sao chép giọng nói"):
                with gr.Row():
                    with gr.Column(scale=1):
                        text_input = gr.Textbox(
                            label="Văn bản cần đọc",
                            lines=4,
                            placeholder="Nhập nội dung bạn muốn chuyển thành giọng nói...",
                            api_name="text_input",
                        )
                        ref_audio_input = gr.Audio(
                            label="Audio tham chiếu (giọng mẫu, 3-10 giây)",
                            type="filepath",
                            api_name="ref_audio_input",
                        )
                        ref_text_input = gr.Textbox(
                            label="Nội dung audio tham chiếu (không bắt buộc)",
                            lines=2,
                            placeholder="Để trống để tự động nhận dạng bằng AI.",
                            api_name="ref_text_input",
                        )
                        instruct_input = gr.Textbox(
                            label="Mô tả giọng nói (không bắt buộc)",
                            lines=1,
                            placeholder="VD: female, low pitch, British accent",
                            visible=False,
                            api_name="instruct_input",
                        )

                        with gr.Accordion("Cài đặt nâng cao", open=False):
                            num_step_slider = gr.Slider(
                                4, 64, value=32, step=1,
                                label="Số bước suy luận",
                                info="32 = chất lượng tốt nhất. 16 = nhanh gấp đôi.",
                                api_name="num_step",
                            )
                            speed_slider = gr.Slider(
                                0.5, 1.5, value=1.0, step=0.05,
                                label="Tốc độ",
                                info="1.0 = bình thường.",
                                api_name="speed",
                            )
                            guidance_slider = gr.Slider(
                                0.0, 4.0, value=2.0, step=0.1,
                                label="Guidance Scale (CFG)",
                                api_name="guidance_scale",
                            )

                        gen_btn = gr.Button("🎵 Tạo giọng nói", variant="primary", size="lg")

                    with gr.Column(scale=1):
                        audio_output = gr.Audio(
                            label="Kết quả",
                            type="numpy",
                            api_name="audio_output",
                        )
                        status_output = gr.Textbox(
                            label="Trạng thái",
                            api_name="status_output",
                        )

                # --- Voice Clone handler ---
                def _clone_handler(text, ref_audio, ref_text, instruct,
                                   num_step, guidance_scale, speed):
                    if not ref_audio:
                        return None, "⚠️ Vui lòng tải lên audio tham chiếu."
                    try:
                        audio, status = generate_tts(
                            text=text,
                            ref_audio=ref_audio,
                            ref_text=ref_text or None,
                            instruct=instruct or None,
                            num_step=int(num_step),
                            guidance_scale=float(guidance_scale),
                            speed=float(speed) if speed != 1.0 else None,
                        )
                        waveform = (audio * 32767).astype(np.int16)
                        return (SAMPLING_RATE, waveform), f"✅ {status}"
                    except Exception as e:
                        logger.exception("Generate failed")
                        return None, f"❌ Lỗi: {type(e).__name__}: {e}"

                gen_btn.click(
                    _clone_handler,
                    inputs=[
                        text_input, ref_audio_input, ref_text_input,
                        instruct_input, num_step_slider, guidance_slider,
                        speed_slider,
                    ],
                    outputs=[audio_output, status_output],
                    concurrency_limit=1,
                )

            # ================================================================
            # Tab 2: Voice Design
            # ================================================================
            with gr.TabItem("🎨 Thiết kế giọng nói"):
                with gr.Row():
                    with gr.Column(scale=1):
                        vd_text = gr.Textbox(
                            label="Văn bản cần đọc",
                            lines=4,
                            placeholder="Nhập nội dung bạn muốn chuyển thành giọng nói...",
                            api_name="vd_text",
                        )
                        vd_instruct = gr.Textbox(
                            label="Mô tả giọng nói",
                            lines=2,
                            placeholder="VD: female, young adult, British accent",
                            api_name="vd_instruct",
                        )

                        with gr.Accordion("Cài đặt nâng cao", open=False):
                            vd_steps = gr.Slider(
                                4, 64, value=32, step=1,
                                label="Số bước suy luận",
                                api_name="vd_steps",
                            )
                            vd_speed = gr.Slider(
                                0.5, 1.5, value=1.0, step=0.05,
                                label="Tốc độ",
                                api_name="vd_speed",
                            )
                            vd_guidance = gr.Slider(
                                0.0, 4.0, value=2.0, step=0.1,
                                label="Guidance Scale",
                                api_name="vd_guidance",
                            )

                        vd_btn = gr.Button("🎵 Tạo giọng nói", variant="primary", size="lg")

                    with gr.Column(scale=1):
                        vd_audio = gr.Audio(
                            label="Kết quả",
                            type="numpy",
                            api_name="vd_audio",
                        )
                        vd_status = gr.Textbox(
                            label="Trạng thái",
                            api_name="vd_status",
                        )

                def _design_handler(text, instruct, steps, guidance, speed):
                    if not instruct or not instruct.strip():
                        return None, "⚠️ Vui lòng nhập mô tả giọng nói."
                    try:
                        audio, status = generate_tts(
                            text=text,
                            instruct=instruct,
                            num_step=int(steps),
                            guidance_scale=float(guidance),
                            speed=float(speed) if speed != 1.0 else None,
                        )
                        waveform = (audio * 32767).astype(np.int16)
                        return (SAMPLING_RATE, waveform), f"✅ {status}"
                    except Exception as e:
                        logger.exception("Design failed")
                        return None, f"❌ Lỗi: {type(e).__name__}: {e}"

                vd_btn.click(
                    _design_handler,
                    inputs=[vd_text, vd_instruct, vd_steps, vd_guidance, vd_speed],
                    outputs=[vd_audio, vd_status],
                    concurrency_limit=1,
                )

    return demo


# ---------------------------------------------------------------------------
# Launch
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    demo = _build_ui()
    demo.queue(max_size=20).launch(
        server_name="0.0.0.0",
        server_port=7860,
        show_api=True,  # Hiển thị API docs tại /api
    )
