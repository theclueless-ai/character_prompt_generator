"""
ComfyUI Character Generator Pack — 3 nodos
  🎭 CharacterPortraitGenerator       → retrato base
  👗 OutfitPromptGenerator            → prompt de ropa
  🎬 QwenEditCompositionGenerator     → instrucción para fusionar ambas con Qwen Edit
"""

from .character_prompt_generator import (
    NODE_CLASS_MAPPINGS        as _A_CLASSES,
    NODE_DISPLAY_NAME_MAPPINGS as _A_NAMES,
)
from .outfit_prompt_generator import (
    NODE_CLASS_MAPPINGS        as _B_CLASSES,
    NODE_DISPLAY_NAME_MAPPINGS as _B_NAMES,
)
from .qwen_edit_composition_generator import (
    NODE_CLASS_MAPPINGS        as _C_CLASSES,
    NODE_DISPLAY_NAME_MAPPINGS as _C_NAMES,
)

NODE_CLASS_MAPPINGS        = {**_A_CLASSES, **_B_CLASSES, **_C_CLASSES}
NODE_DISPLAY_NAME_MAPPINGS = {**_A_NAMES,   **_B_NAMES,   **_C_NAMES}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]

print("\033[92m[Character Generator] ✅  🎭 Portrait  |  👗 Outfit  |  🎬 Qwen Edit Composition\033[0m")
