# 🎭 ComfyUI Character Prompt Generator

Nodo personalizado para ComfyUI que genera prompts de personajes en inglés listos para usar con **Flux**, **SDXL** y cualquier modelo de texto a imagen.

---

## ✨ Características

### Sección A — Personajes Humanos
Controla con dropdowns individuales (cada uno tiene opción `RANDOM`):
- Género, etnia, rango de edad
- Tono de piel, forma de cara
- Color y estilo de cabello
- Color y forma de ojos
- Nariz, labios, pecas
- Expresión facial
- Características distintivas (cicatrices, piercings, etc.)

### Sección B — Personajes No-Humanos
Cuatro subcategorías, cada una con sus propias características:
- 👽 **Alien clásico** — piel, ojos, rasgos alienígenas
- 🤖 **Metahumano/Cyborg** — nivel de modificación, piel sintética, poderes
- 😈 **Demonio/Criatura oscura** — piel, cuernos, colmillos, alas, etc.
- 🐺 **Híbrido humano-animal** — tipo de animal, características físicas

### Configuración Global
- `character_type`: HUMAN / NON-HUMAN — elige qué sección se usa
- `seed`: reproduce exactamente el mismo resultado
- `render_style`: photorealistic, hyperrealistic, concept art, etc.
- `body_type`: constitución física del personaje
- `lighting`: tipo de iluminación para el prompt

---

## 📤 Salidas del Nodo

| Output | Tipo | Descripción |
|--------|------|-------------|
| `PROMPT` | STRING | Prompt completo en inglés, listo para conectar al Text Encoder |
| `JSON_METADATA` | STRING | JSON con todos los valores usados (incluye la seed) |

---

## 🛠️ Instalación en Windows (paso a paso)

### Requisitos previos
- ComfyUI instalado y funcionando
- Python instalado (viene incluido con ComfyUI portable)

### Paso 1 — Localizar la carpeta `custom_nodes`

Abre el Explorador de Windows y navega a tu instalación de ComfyUI:

```
C:\Users\TuUsuario\ComfyUI\custom_nodes\
```
o si usas la versión portable:
```
C:\ComfyUI_windows_portable\ComfyUI\custom_nodes\
```

### Paso 2 — Copiar la carpeta del nodo

Copia la carpeta `ComfyUI_CharacterPromptGenerator` completa dentro de `custom_nodes`.

La estructura debe quedar así:
```
custom_nodes/
└── ComfyUI_CharacterPromptGenerator/
    ├── __init__.py
    ├── character_prompt_generator.py
    └── README.md
```

### Paso 3 — Reiniciar ComfyUI

Cierra ComfyUI si estaba abierto y vuelve a iniciarlo. Verás en la consola:

```
[Character Prompt Generator] ✅ Nodo cargado correctamente.
```

### Paso 4 — Añadir el nodo al workflow

1. Haz clic derecho en el canvas de ComfyUI
2. Ve a `Add Node`
3. Busca la categoría `🎭 Character Generator`
4. Selecciona `🎭 Character Prompt Generator`

---

## 🔌 Cómo usarlo en un workflow

```
[Character Prompt Generator]
         │
         ├── PROMPT ──────────────→ [CLIP Text Encode] → [KSampler]
         │
         └── JSON_METADATA ───────→ [Show Text] (para ver los valores)
```

**Tip:** Conecta `PROMPT` directamente al `CLIPTextEncode (Positive)`. Para el negativo puedes usar un nodo de texto normal con tu negative prompt habitual.

---

## 🎲 Sistema de Randomización

Cada dropdown tiene `RANDOM` como primera opción. Cuando está en `RANDOM`, el nodo elige aleatoriamente uno de los valores posibles usando la **seed** definida.

- **Seed = 0**: genera una seed aleatoria diferente cada vez que ejecutas
- **Seed > 0**: reproduce exactamente el mismo personaje si los demás parámetros no cambian
- Puedes dejar algunos campos en `RANDOM` y fijar otros manualmente para tener control parcial

### Ejemplo de uso mixto:
- `A_hair_color` = `electric blue hair` (fijo)
- `A_eye_color` = `RANDOM` (aleatorio)
- `A_expression` = `fierce determined expression` (fijo)
- Todo lo demás en `RANDOM`

---

## 📋 Ejemplo de prompt generado

**Humano:**
```
photorealistic, portrait of a mid 20s adult East Asian female, athletic toned body type, 
olive skin, oval face shape, deep purple hair, long wavy hair, green eyes, 
almond-shaped eyes, straight refined nose, full plump lips, very light freckles, 
mysterious enigmatic expression, nose ring piercing, dramatic cinematic lighting, 
detailed face, sharp focus, high quality, masterpiece
```

**Alien:**
```
hyperrealistic 8K, portrait of an alien extraterrestrial being, slender body type, 
lavender purple skin, large solid black alien eyes, bioluminescent stripe patterns on face, 
soft beauty studio lighting, detailed face, sharp focus, high quality, masterpiece
```

---

## 🔧 Personalización avanzada

Si quieres añadir nuevas opciones a cualquier categoría, abre `character_prompt_generator.py` y edita las listas dentro de `HUMAN_DATA`, `NONHUMAN_DATA` o `SHARED_DATA`. Solo añade el nuevo string a la lista correspondiente.

Ejemplo — añadir un nuevo color de pelo:
```python
"hair_color": [
    "jet black hair",
    "dark brown hair",
    ...
    "holographic rainbow hair",  # ← añadir aquí
],
```

---

## 🐛 Solución de problemas

**El nodo no aparece en ComfyUI**
- Verifica que la carpeta `ComfyUI_CharacterPromptGenerator` está directamente dentro de `custom_nodes` (no en una subcarpeta)
- Asegúrate de haber reiniciado ComfyUI completamente
- Revisa la consola de ComfyUI por mensajes de error

**Error de Python al cargar**
- Verifica que los archivos `__init__.py` y `character_prompt_generator.py` no tienen errores de codificación
- Abre la consola donde corre ComfyUI y busca el error específico

---

*Creado para ComfyUI — Compatible con Flux, SDXL y cualquier modelo text-to-image*
