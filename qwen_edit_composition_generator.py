"""
ComfyUI Qwen Edit Composition Prompt Generator
===============================================
Genera el prompt de INSTRUCCIÓN para Qwen-Image-Edit al fusionar:
  - Figure 1: retrato base del personaje (cara, rasgos, identidad)
  - Figure 2: outfit / ropa

Diseñado para estética editorial surreal, body horror de alta costura,
personajes no-humanos con ropa. Encuadres van desde close-up extremo
hasta tres cuartos editorial.

Qwen Edit usa lenguaje natural tipo instrucción, NO tags por comas.
"""

import random
import json


# ══════════════════════════════════════════════════════════════════════════════
#  BASE DE DATOS
# ══════════════════════════════════════════════════════════════════════════════

COMPOSITION_DATA = {

    # ── ENCUADRE (shot type) ─────────────────────────────────────────────────
    # De más cerrado a más abierto, pensado para editorial surreal
    "shot_type": [
        "extreme close-up, face filling the entire frame, chin to forehead",
        "tight close-up portrait, face and bare neck only",
        "close-up bust portrait, head and upper chest",
        "bust shot showing face, neck, and shoulder line",
        "half body shot from waist up, editorial framing",
        "three-quarter body shot from mid-thigh up",
        "full body shot head to toe, centered in frame",
        "full body shot with empty space above and below, fashion editorial",
    ],

    # ── ÁNGULO DE CÁMARA ────────────────────────────────────────────────────
    "camera_angle": [
        "straight-on frontal, camera at eye level",
        "very slight upward angle, camera just below eye level",
        "slight downward angle, camera just above eye level",
        "strong low angle, camera at chest height looking up",
        "slight three-quarter turn to the left, eye level",
        "slight three-quarter turn to the right, eye level",
        "strict side profile, camera perpendicular to face",
        "three-quarter profile, between front and side",
        "looking over shoulder, body turned away from camera",
        "tilted dutch angle, slightly rotated frame",
    ],

    # ── POSE ────────────────────────────────────────────────────────────────
    "pose": [
        "standing still, completely neutral, statuesque pose",
        "standing with arms relaxed along body sides",
        "one hand raised to chin or cheek, contemplative",
        "arms crossed loosely in front, slight tension",
        "one arm raised above head, dramatic gesture",
        "hands hanging limp at sides, eerie stillness",
        "slight lean forward toward the camera",
        "slight lean backward, receding from camera",
        "one shoulder raised, subtle tension in posture",
        "hands clasped in front at waist level",
        "one hand on hip, the other at rest",
        "both hands framing the face without touching",
        "torso twisted slightly while face looks at camera",
        "completely rigid and symmetrical, doll-like stillness",
    ],

    # ── EXPRESIÓN / MIRADA ───────────────────────────────────────────────────
    "expression": [
        "completely blank neutral expression, staring directly at camera",
        "cold expressionless gaze into the lens",
        "subtle unsettling half-smile",
        "eyes slightly downcast, introspective mood",
        "eyes closed, serene or trance-like expression",
        "mouth slightly open, ambiguous expression",
        "fierce direct stare, confrontational",
        "head slightly tilted, detached and curious expression",
        "melancholic distant gaze, looking past the camera",
        "inhuman stillness, face completely unreadable",
    ],

    # ── FONDO ────────────────────────────────────────────────────────────────
    # Pensado para realzar el personaje surreal, no competir con él
    "background": [
        "plain white seamless studio background",           # default
        "solid black background, pure darkness",
        "mid-tone gray seamless studio background",
        "very dark charcoal gray background",
        "pale cream off-white background",
        "soft gradient from white to light gray",
        "heavily blurred beige or warm gray, undefined space",
        "dark matte background with barely visible texture",
        "deep forest green background, very out of focus",
        "dusty rose pale pink studio background",
        "raw concrete wall texture, desaturated",
        "faint architectural element, extremely blurred",
        "white background with subtle shadow gradient",
        "deep navy blue out-of-focus background",
    ],

    # ── ILUMINACIÓN ─────────────────────────────────────────────────────────
    "lighting": [
        "clean flat beauty lighting, no harsh shadows",
        "soft beauty dish lighting, gentle even illumination",
        "single side lighting with soft falloff on shadow side",
        "dramatic split lighting, exactly half face in shadow",
        "harsh single light source from above, theatrical",
        "soft warm backlight creating subtle rim glow",
        "cold clinical white light from directly in front",
        "low-key chiaroscuro, deep contrast light and shadow",
        "diffuse overcast soft light, no directional shadows",
        "strong under-lighting, light source below face",
        "high contrast black and white style lighting",
        "soft ambient studio light with subtle accent on cheekbones",
    ],

    # ── ESTILO DE RENDER ─────────────────────────────────────────────────────
    "render_quality": [
        "high-end fashion editorial photograph",
        "hyperrealistic photograph, extreme skin and texture detail",
        "dark surreal editorial photograph",
        "avant-garde art photography, high contrast",
        "cinematic film still, desaturated palette",
        "museum-quality portrait photography",
        "commercial beauty campaign photograph",
    ],

    # ── TRATAMIENTO DE COLOR / MOOD ──────────────────────────────────────────
    "color_mood": [
        "natural accurate colors",
        "slightly desaturated, cold tone",
        "high contrast black and white",
        "muted earthy desaturated palette",
        "cool blue-gray color grading",
        "warm cream and ivory tones",
        "deep shadows with pale highlighted skin",
        "bleached high-key minimal palette",
    ],
}


# ══════════════════════════════════════════════════════════════════════════════
#  UTILITARIOS
# ══════════════════════════════════════════════════════════════════════════════

def pick(options: list, value: str) -> str:
    return random.choice(options) if value == "RANDOM" else value

def with_random(options: list) -> list:
    return ["RANDOM"] + list(options)


# ══════════════════════════════════════════════════════════════════════════════
#  PLANTILLAS DE INSTRUCCIÓN
# Diseñadas para funcionar con personajes surreales / no-humanos + ropa editorial
# ══════════════════════════════════════════════════════════════════════════════

INSTRUCTION_TEMPLATES = [
    (
        "Using Figure 1 as the character reference and Figure 2 as the outfit reference. "
        "Preserve exactly all facial features, skin texture, skin color, eye appearance, "
        "head structure, and any non-human characteristics visible in Figure 1 — "
        "do not normalize or humanize the face. "
        "Apply the complete outfit from Figure 2 to the character body, including all "
        "clothing pieces, fabric textures, colors, and accessories. "
        "Shot type: {shot}. Camera angle: {camera}. "
        "The character is {pose} with {expression}. "
        "Background: {background}. Lighting: {lighting}. "
        "Color treatment: {color_mood}. Render as {quality}. "
        "Do not alter, smooth, or simplify any facial or skin features from Figure 1."
    ),
    (
        "Compose a full character image combining Figure 1 and Figure 2. "
        "Figure 1 provides the identity: keep the face, skin texture, unusual features, "
        "eye shape, skin color, and head proportions exactly as they appear — "
        "preserve all surreal or non-human qualities without softening them. "
        "Figure 2 provides the clothing: apply the exact outfit shown including "
        "fabric detail, cut, color palette, and accessories. "
        "Framing: {shot}, {camera}. "
        "Pose: {pose}. Expression: {expression}. "
        "Background: {background}. {lighting}. "
        "{color_mood}. Final render style: {quality}. "
        "The character's unusual features from Figure 1 must remain intact and detailed."
    ),
    (
        "Create a single editorial portrait using Figure 1 for the subject's face and body "
        "and Figure 2 for the clothing. "
        "The subject's face, skin surface, texture, eye type, structural facial features, "
        "and any organic or non-human elements from Figure 1 must be transferred exactly "
        "without any beautification or normalization. "
        "Dress the subject in the outfit from Figure 2, keeping all details. "
        "Shot: {shot}. Angle: {camera}. "
        "Subject is {pose}, {expression}. "
        "Place against {background} under {lighting}. "
        "Apply {color_mood} color treatment. Style: {quality}. "
        "Do not change any features of the face from Figure 1. "
        "Do not humanize or correct non-human features."
    ),
]


# ══════════════════════════════════════════════════════════════════════════════
#  NODO
# ══════════════════════════════════════════════════════════════════════════════

class QwenEditCompositionGenerator:
    """
    Genera el prompt de instrucción para Qwen-Image-Edit.
    Fusiona el retrato (Figure 1) con la ropa (Figure 2).
    Optimizado para personajes surreales, body horror editorial y alta costura.

    Outputs:
      INSTRUCTION_PROMPT  → al CLIP Text Encode (positivo) de Qwen Edit
      NEGATIVE_PROMPT     → al CLIP Text Encode (negativo)
      JSON_METADATA       → para debug y reproducibilidad
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {

            "seed":         ("INT", {"default": 0, "min": 0, "max": 0xFFFFFFFF, "step": 1, "display": "number"}),

            # ── Encuadre y cámara ───────────────────────────────────────────
            "shot_type":    (with_random(COMPOSITION_DATA["shot_type"]),),
            "camera_angle": (with_random(COMPOSITION_DATA["camera_angle"]),),
            "pose":         (with_random(COMPOSITION_DATA["pose"]),),
            "expression":   (with_random(COMPOSITION_DATA["expression"]),),

            # ── Escena ─────────────────────────────────────────────────────
            "background":     (COMPOSITION_DATA["background"],),
            "lighting":       (with_random(COMPOSITION_DATA["lighting"]),),
            "render_quality": (with_random(COMPOSITION_DATA["render_quality"]),),
            "color_mood":     (with_random(COMPOSITION_DATA["color_mood"]),),

            # ── Instrucción extra ───────────────────────────────────────────
            "extra_instruction": ("STRING", {
                "default": "",
                "multiline": True,
                "placeholder": "Extra: 'the character holds a flower', 'add fog at feet', 'extreme skin detail on face'...",
            }),

            # ── Negativo ────────────────────────────────────────────────────
            "custom_negative": ("STRING", {
                "default": "",
                "multiline": False,
                "placeholder": "Negativo extra: 'no extra people', 'no jewelry'...",
            }),
        }}

    RETURN_TYPES  = ("STRING", "STRING", "STRING")
    RETURN_NAMES  = ("INSTRUCTION_PROMPT", "NEGATIVE_PROMPT", "JSON_METADATA")
    FUNCTION      = "generate"
    CATEGORY      = "🎭 Character Generator"

    def generate(
        self,
        seed, shot_type, camera_angle, pose, expression,
        background, lighting, render_quality, color_mood,
        extra_instruction, custom_negative,
    ):
        if seed == 0:
            seed = random.randint(1, 0xFFFFFFFF)
        random.seed(seed)

        r_shot    = pick(COMPOSITION_DATA["shot_type"],    shot_type)
        r_cam     = pick(COMPOSITION_DATA["camera_angle"], camera_angle)
        r_pose    = pick(COMPOSITION_DATA["pose"],         pose)
        r_expr    = pick(COMPOSITION_DATA["expression"],   expression)
        r_bg      = background
        r_light   = pick(COMPOSITION_DATA["lighting"],     lighting)
        r_quality = pick(COMPOSITION_DATA["render_quality"], render_quality)
        r_color   = pick(COMPOSITION_DATA["color_mood"],   color_mood)

        template = random.choice(INSTRUCTION_TEMPLATES)

        instruction = template.format(
            shot       = r_shot,
            camera     = r_cam,
            pose       = r_pose,
            expression = r_expr,
            background = r_bg,
            lighting   = r_light,
            quality    = r_quality,
            color_mood = r_color,
        )

        if extra_instruction.strip():
            instruction += f" Additionally: {extra_instruction.strip()}"

        # Negativo en lenguaje natural — Qwen Edit responde mejor así
        negative_base = (
            "Do not change, smooth, normalize, or humanize any facial features or skin texture from Figure 1. "
            "Preserve all unusual, non-human, or surreal characteristics of the face exactly. "
            "Do not add extra people, duplicate figures, or unwanted background elements. "
            "Avoid blurry face, distorted anatomy, extra or missing limbs, or incorrect hand count. "
            "Do not change hair, head structure, or eye type from Figure 1. "
            "Avoid compression artifacts, watermarks, or low resolution."
        )
        negative = f"{negative_base} {custom_negative.strip()}" if custom_negative.strip() else negative_base

        meta = {
            "seed": seed,
            "shot_type": r_shot,
            "camera_angle": r_cam,
            "pose": r_pose,
            "expression": r_expr,
            "background": r_bg,
            "lighting": r_light,
            "render_quality": r_quality,
            "color_mood": r_color,
            "extra_instruction": extra_instruction,
        }

        return (instruction, negative, json.dumps(meta, indent=2, ensure_ascii=False))


# ══════════════════════════════════════════════════════════════════════════════
#  REGISTRO
# ══════════════════════════════════════════════════════════════════════════════

NODE_CLASS_MAPPINGS = {
    "QwenEditCompositionGenerator": QwenEditCompositionGenerator,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "QwenEditCompositionGenerator": "🎬 Qwen Edit Composition Generator",
}
