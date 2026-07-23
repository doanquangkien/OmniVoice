#!/usr/bin/env python3
# Copyright    2026  Xiaomi Corp.        (authors:  Han Zhu)
#
# See ../../LICENSE for clarification regarding multiple authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Gradio demo for OmniVoice.

Supports voice cloning and voice design.

Usage:
    omnivoice-demo --model /path/to/checkpoint --port 8000
"""

import argparse
import logging
from typing import Any, Dict

import gradio as gr
import numpy as np
import torch

from omnivoice import OmniVoice, OmniVoiceGenerationConfig
from omnivoice.utils.common import get_best_device
from omnivoice.utils.lang_map import LANG_NAMES, lang_display_name


# ---------------------------------------------------------------------------
# Language list — all 600+ supported languages
# ---------------------------------------------------------------------------
_ALL_LANGUAGES = ["Tự động"] + sorted(lang_display_name(n) for n in LANG_NAMES)


# ---------------------------------------------------------------------------
# Voice Design instruction templates
# ---------------------------------------------------------------------------
# Each option is displayed as "English / 中文".
# The model expects English for accents and Chinese for dialects.
_CATEGORIES = {
    "Giới tính": ["Male / Nam", "Female / Nữ"],
    "Độ tuổi": [
        "Child / Trẻ em",
        "Teenager / Thiếu niên",
        "Young Adult / Thanh niên",
        "Middle-aged / Trung niên",
        "Elderly / Người già",
    ],
    "Cao độ": [
        "Very Low Pitch / Rất trầm",
        "Low Pitch / Trầm",
        "Moderate Pitch / Trung bình",
        "High Pitch / Cao",
        "Very High Pitch / Rất cao",
    ],
    "Phong cách": ["Whisper / Thì thầm"],
    "Giọng tiếng Anh": [
        "American Accent / Mỹ",
        "Australian Accent / Úc",
        "British Accent / Anh",
        "Chinese Accent / Trung Quốc",
        "Canadian Accent / Canada",
        "Indian Accent / Ấn Độ",
        "Korean Accent / Hàn Quốc",
        "Portuguese Accent / Bồ Đào Nha",
        "Russian Accent / Nga",
        "Japanese Accent / Nhật Bản",
    ],
    "Phương ngữ tiếng Trung": [
        "Henan Dialect / Hà Nam",
        "Shaanxi Dialect / Thiểm Tây",
        "Sichuan Dialect / Tứ Xuyên",
        "Guizhou Dialect / Quý Châu",
        "Yunnan Dialect / Vân Nam",
        "Guilin Dialect / Quế Lâm",
        "Jinan Dialect / Tế Nam",
        "Shijiazhuang Dialect / Thạch Gia Trang",
        "Gansu Dialect / Cam Túc",
        "Ningxia Dialect / Ninh Hạ",
        "Qingdao Dialect / Thanh Đảo",
        "Northeast Dialect / Đông Bắc",
    ],
}

_ATTR_INFO = {
    "Giọng tiếng Anh": "Chỉ áp dụng cho giọng nói tiếng Anh.",
    "Phương ngữ tiếng Trung": "Chỉ áp dụng cho giọng nói tiếng Trung.",
}

# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="omnivoice-demo",
        description="Launch a Gradio demo for OmniVoice.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--model",
        default="k2-fsa/OmniVoice",
        help="Model checkpoint path or HuggingFace repo id.",
    )
    parser.add_argument(
        "--device", default=None, help="Thiết bị sử dụng. Tự động phát hiện nếu không chỉ định."
    )
    parser.add_argument("--ip", default="0.0.0.0", help="Server IP (default: 0.0.0.0).")
    parser.add_argument(
        "--port", type=int, default=7860, help="Server port (default: 7860)."
    )
    parser.add_argument(
        "--root-path",
        default=None,
        help="Root path for reverse proxy.",
    )
    parser.add_argument(
        "--share", action="store_true", default=False, help="Create public link."
    )
    parser.add_argument(
        "--no-asr",
        action="store_true",
        default=False,
        help="Skip loading Whisper ASR model. Reference text auto-transcription"
        " will be unavailable.",
    )
    parser.add_argument(
        "--asr-model",
        default="openai/whisper-large-v3-turbo",
        help="ASR model path or HuggingFace repo id"
        " (default: openai/whisper-large-v3-turbo).",
    )
    return parser


# ---------------------------------------------------------------------------
# Build demo
# ---------------------------------------------------------------------------


def build_demo(
    model: OmniVoice,
    checkpoint: str,
    generate_fn=None,
) -> gr.Blocks:
    sampling_rate = model.sampling_rate

    # -- shared generation core --
    def _gen_core(
        text,
        language,
        ref_audio,
        instruct,
        num_step,
        guidance_scale,
        denoise,
        speed,
        duration,
        preprocess_prompt,
        postprocess_output,
        mode,
        ref_text=None,
    ):
        if not text or not text.strip():
            return None, "Vui lòng nhập nội dung văn bản cần đọc.", gr.update(interactive=True)

        gen_config = OmniVoiceGenerationConfig(
            num_step=int(num_step or 32),
            guidance_scale=float(guidance_scale) if guidance_scale is not None else 2.0,
            denoise=bool(denoise) if denoise is not None else True,
            preprocess_prompt=bool(preprocess_prompt),
            postprocess_output=bool(postprocess_output),
        )

        lang = language if (language and language != "Tự động") else None

        kw: Dict[str, Any] = dict(
            text=text.strip(), language=lang, generation_config=gen_config
        )

        if speed is not None and float(speed) != 1.0:
            kw["speed"] = float(speed)
        if duration is not None and float(duration) > 0:
            kw["duration"] = float(duration)

        if mode == "clone":
            if not ref_audio:
                return None, "Vui lòng tải lên audio tham chiếu (giọng mẫu).", gr.update(interactive=True)
            kw["voice_clone_prompt"] = model.create_voice_clone_prompt(
                ref_audio=ref_audio,
                ref_text=ref_text,
            )

        if instruct and instruct.strip():
            kw["instruct"] = instruct.strip()

        try:
            audio = model.generate(**kw)
        except Exception as e:
            return None, f"Lỗi: {type(e).__name__}: {e}", gr.update(interactive=True)

        waveform = (audio[0] * 32767).astype(np.int16)
        return (sampling_rate, waveform), "Đã xong.", gr.update(interactive=True)

    # Allow external wrappers (e.g. spaces.GPU for ZeroGPU Spaces)
    _gen = generate_fn if generate_fn is not None else _gen_core

    # =====================================================================
    # UI
    # =====================================================================
    theme = gr.themes.Soft(
        font=["Inter", "Arial", "sans-serif"],
    )
    css = """
    .gradio-container {max-width: 100% !important; font-size: 16px !important;}
    .gradio-container h1 {font-size: 1.5em !important;}
    .gradio-container .prose {font-size: 1.1em !important;}
    .compact-audio audio {height: 60px !important;}
    .compact-audio .waveform {min-height: 80px !important;}
    """

    # Reusable: language dropdown component
    def _lang_dropdown(label="Ngôn ngữ (không bắt buộc)", value="Tự động"):
        return gr.Dropdown(
            label=label,
            choices=_ALL_LANGUAGES,
            value=value,
            allow_custom_value=False,
            interactive=True,
            info="Giữ 'Tự động' để mô hình tự phát hiện ngôn ngữ.",
        )

    # Reusable: optional generation settings accordion
    def _gen_settings():
        with gr.Accordion("Cài đặt nâng cao (không bắt buộc)", open=False):
            sp = gr.Slider(
                0.5,
                1.5,
                value=1.0,
                step=0.05,
                label="Tốc độ",
                info="1.0 = bình thường. >1 nhanh hơn, <1 chậm hơn. Bị bỏ qua nếu đặt Độ dài.",
            )
            du = gr.Number(
                value=None,
                label="Độ dài (giây)",
                info=(
                    "Để trống để dùng tốc độ. Đặt giá trị cố định để ghi đè tốc độ."
                ),
            )
            ns = gr.Slider(
                4,
                64,
                value=32,
                step=1,
                label="Số bước suy luận",
                info="Mặc định: 32. Thấp hơn = nhanh hơn, cao hơn = chất lượng tốt hơn.",
            )
            dn = gr.Checkbox(
                label="Khử nhiễu",
                value=True,
                info="Mặc định: bật. Bỏ chọn để tắt khử nhiễu.",
            )
            gs = gr.Slider(
                0.0,
                4.0,
                value=2.0,
                step=0.1,
                label="Guidance Scale (CFG)",
                info="Mặc định: 2.0.",
            )
            pp = gr.Checkbox(
                label="Tiền xử lý audio tham chiếu",
                value=True,
                info="Xóa khoảng lặng, cắt gọn audio tham chiếu, "
                "thêm dấu câu cuối văn bản tham chiếu (nếu chưa có)",
            )
            po = gr.Checkbox(
                label="Hậu xử lý kết quả",
                value=True,
                info="Xóa khoảng lặng dài khỏi audio kết quả.",
            )
        return ns, gs, dn, sp, du, pp, po

    with gr.Blocks(theme=theme, css=css, title="OmniVoice Demo") as demo:
        gr.Markdown(
            """
# OmniVoice — Chuyển văn bản thành giọng nói

Mô hình text‑to‑speech đa ngôn ngữ hỗ trợ **hơn 600 ngôn ngữ**:

- **Sao chép giọng nói** — Sao chép bất kỳ giọng nói nào từ một đoạn audio tham chiếu
- **Thiết kế giọng nói** — Tạo giọng nói tùy chỉnh theo các thuộc tính người nói

Xây dựng bởi [OmniVoice](https://github.com/k2-fsa/OmniVoice)
— Xiaomi AI Lab, đội ngũ Next‑gen Kaldi.
"""
        )

        with gr.Tabs():
            # ==============================================================
            # Voice Clone
            # ==============================================================
            with gr.TabItem("🎙 Sao chép giọng nói"):
                with gr.Row():
                    with gr.Column(scale=1):
                        vc_text = gr.Textbox(
                            label="Văn bản cần đọc",
                            lines=4,
                            placeholder="Nhập nội dung bạn muốn chuyển thành giọng nói...",
                        )
                        vc_ref_audio = gr.Audio(
                            label="Audio tham chiếu (giọng mẫu)",
                            type="filepath",
                            elem_classes="compact-audio",
                        )
                        gr.Markdown(
                            "<span style='font-size:0.85em;color:#888;'>"
                            "Khuyến nghị: audio dài 3–10 giây. "
                            "</span>"
                        )
                        vc_ref_text = gr.Textbox(
                            label=("Nội dung audio tham chiếu (không bắt buộc)"),
                            lines=2,
                            placeholder="Nội dung lời nói trong audio tham chiếu. "
                            "Để trống để tự động nhận dạng bằng ASR.",
                        )
                        vc_lang = _lang_dropdown("Ngôn ngữ (không bắt buộc)")
                        with gr.Accordion("Mô tả thêm (không bắt buộc)", open=False):
                            vc_instruct = gr.Textbox(label="Mô tả giọng (instruct)", lines=2)
                        (
                            vc_ns,
                            vc_gs,
                            vc_dn,
                            vc_sp,
                            vc_du,
                            vc_pp,
                            vc_po,
                        ) = _gen_settings()
                        vc_btn = gr.Button("🎵 Tạo giọng nói", variant="primary")
                    with gr.Column(scale=1):
                        vc_audio = gr.Audio(
                            label="Kết quả",
                            type="numpy",
                        )
                        vc_status = gr.Textbox(label="Trạng thái", lines=2)

                def _clone_fn(
                    text, lang, ref_aud, ref_text, instruct, ns, gs, dn, sp, du, pp, po
                ):
                    # Disable button immediately while processing
                    yield None, "Đang xử lý...", gr.update(interactive=False, value="Đang xử lý...")
                    result = _gen(
                        text,
                        lang,
                        ref_aud,
                        instruct,
                        ns,
                        gs,
                        dn,
                        sp,
                        du,
                        pp,
                        po,
                        mode="clone",
                        ref_text=ref_text or None,
                    )
                    yield result[0], result[1], gr.update(interactive=True, value="🎵 Tạo giọng nói")

                vc_btn.click(
                    _clone_fn,
                    inputs=[
                        vc_text,
                        vc_lang,
                        vc_ref_audio,
                        vc_ref_text,
                        vc_instruct,
                        vc_ns,
                        vc_gs,
                        vc_dn,
                        vc_sp,
                        vc_du,
                        vc_pp,
                        vc_po,
                    ],
                    outputs=[vc_audio, vc_status, vc_btn],
                    concurrency_limit=1,
                )

            # ==============================================================
            # Voice Design
            # ==============================================================
            with gr.TabItem("🎨 Thiết kế giọng nói"):
                with gr.Row():
                    with gr.Column(scale=1):
                        vd_text = gr.Textbox(
                            label="Văn bản cần đọc",
                            lines=4,
                            placeholder="Nhập nội dung bạn muốn chuyển thành giọng nói...",
                        )
                        vd_lang = _lang_dropdown("Ngôn ngữ (không bắt buộc)")

                        _AUTO = "Tự động"
                        vd_groups = []
                        for _cat, _choices in _CATEGORIES.items():
                            vd_groups.append(
                                gr.Dropdown(
                                    label=_cat,
                                    choices=[_AUTO] + _choices,
                                    value=_AUTO,
                                    info=_ATTR_INFO.get(_cat),
                                )
                            )

                        (
                            vd_ns,
                            vd_gs,
                            vd_dn,
                            vd_sp,
                            vd_du,
                            vd_pp,
                            vd_po,
                        ) = _gen_settings()
                        vd_btn = gr.Button("🎵 Tạo giọng nói", variant="primary")
                    with gr.Column(scale=1):
                        vd_audio = gr.Audio(
                            label="Kết quả",
                            type="numpy",
                        )
                        vd_status = gr.Textbox(label="Trạng thái", lines=2)

                def _build_instruct(groups):
                    """Extract instruct text from UI dropdowns.

                    Language unification and validation is handled by
                    _resolve_instruct inside _preprocess_all.
                    """
                    selected = [g for g in groups if g and g != "Tự động"]
                    if not selected:
                        return None
                    parts = []
                    for v in selected:
                        if " / " in v:
                            en, zh = v.split(" / ", 1)
                            # Dialects have no English equivalent
                            if "Dialect" in v.split(" / ")[0]:
                                parts.append(zh.strip())
                            else:
                                parts.append(en.strip())
                        else:
                            parts.append(v)
                    return ", ".join(parts)

                def _design_fn(text, lang, ns, gs, dn, sp, du, pp, po, *groups):
                    # Disable button immediately while processing
                    yield None, "Đang xử lý...", gr.update(interactive=False, value="Đang xử lý...")
                    result = _gen(
                        text,
                        lang,
                        None,
                        _build_instruct(groups),
                        ns,
                        gs,
                        dn,
                        sp,
                        du,
                        pp,
                        po,
                        mode="design",
                    )
                    yield result[0], result[1], gr.update(interactive=True, value="🎵 Tạo giọng nói")

                vd_btn.click(
                    _design_fn,
                    inputs=[
                        vd_text,
                        vd_lang,
                        vd_ns,
                        vd_gs,
                        vd_dn,
                        vd_sp,
                        vd_du,
                        vd_pp,
                        vd_po,
                    ]
                    + vd_groups,
                    outputs=[vd_audio, vd_status, vd_btn],
                    concurrency_limit=1,
                )

    return demo


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(argv=None) -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s: %(message)s",
    )
    parser = build_parser()
    args = parser.parse_args(argv)

    device = args.device or get_best_device()

    checkpoint = args.model
    if not checkpoint:
        parser.print_help()
        return 0
    logging.info(f"Loading model from {checkpoint}, device={device} ...")
    model = OmniVoice.from_pretrained(
        checkpoint,
        device_map=device,
        dtype=torch.float16,
        load_asr=not args.no_asr,
        asr_model_name=args.asr_model,
    )
    print("Model loaded.")

    demo = build_demo(model, checkpoint)

    demo.queue().launch(
        server_name=args.ip,
        server_port=args.port,
        share=args.share,
        root_path=args.root_path,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
