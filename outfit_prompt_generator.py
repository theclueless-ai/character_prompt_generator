"""
ComfyUI Outfit Prompt Generator — v2
=====================================
Genera prompts de conjuntos de ropa COMPLETOS sobre fondo blanco.
Sin maniquí, sin persona — solo la ropa.

Dos modos:
  NORMAL       → ropa wearable real, estética cotidiana o formal
  EXPERIMENTAL → alta costura, avant-garde, moda conceptual surreal

El output es la imagen de referencia de ropa que luego se pasa como
Figure 2 al nodo Qwen Edit Composition Generator.
"""

import random
import json


# ══════════════════════════════════════════════════════════════════════════════
#  BASE DE DATOS — ROPA NORMAL
#  Ropa wearable, cotidiana, formal, deportiva, casual — real y usable
# ══════════════════════════════════════════════════════════════════════════════

NORMAL_DATA = {

    "style": [
        "minimalist casual everyday",
        "smart casual business",
        "formal office wear",
        "elegant evening wear",
        "classic streetwear",
        "preppy academic",
        "athleisure sporty",
        "casual summer",
        "cozy autumn layered",
        "classic winter coat outfit",
        "tailored business formal",
        "relaxed weekend wear",
        "vintage 90s",
        "clean Y2K",
        "boho casual",
        "coastal summer",
        "classic French style",
        "Scandinavian minimalist",
        "classic Japanese street fashion",
        "Korean casual fashion",
    ],

    "top": [
        "classic white cotton button-down shirt",
        "fitted white ribbed tank top",
        "oversized crewneck sweatshirt",
        "slim-fit black turtleneck",
        "striped Breton long-sleeve shirt",
        "classic navy blazer",
        "linen button-up shirt in beige",
        "fitted crew-neck t-shirt",
        "knitted ribbed sweater in cream",
        "oxford shirt in light blue",
        "classic trench coat",
        "tailored double-breasted blazer",
        "cozy chunky-knit cardigan",
        "silk camisole in ivory",
        "athletic zip-up hoodie",
        "oversized graphic tee",
        "fitted polo shirt",
        "loose linen blouse",
        "wool turtleneck in camel",
        "structured crop blazer",
    ],

    "bottom": [
        "high-waist straight leg jeans in light wash",
        "slim black trousers",
        "pleated wide-leg trousers in beige",
        "classic khaki chinos",
        "midi A-line skirt in navy",
        "mini denim skirt",
        "tailored pencil skirt in charcoal",
        "flowing midi skirt in cream linen",
        "high-waist mom jeans",
        "classic black dress pants",
        "pleated midi skirt in plaid",
        "straight-leg cargo pants in olive",
        "wide-leg linen trousers",
        "fitted jogger pants in gray",
        "short athletic shorts",
    ],

    "one_piece": [
        "none — use top and bottom",
        "classic little black dress",
        "fitted sheath dress in navy",
        "flowy midi wrap dress in floral print",
        "oversized shirt dress in chambray",
        "structured blazer dress",
        "knit midi dress in cream",
        "simple slip dress in silk",
        "summer sundress in light cotton",
        "classic A-line dress in forest green",
        "elegant column gown in black",
    ],

    "footwear": [
        "classic white leather sneakers",
        "black leather oxford shoes",
        "simple ankle boots in black suede",
        "white minimalist running sneakers",
        "pointed-toe kitten heels in nude",
        "classic loafers in tan leather",
        "chunky platform sandals",
        "knee-high flat leather boots",
        "open-toe block heel mules",
        "classic ballet flats in black",
        "slip-on canvas espadrilles",
        "high-top canvas sneakers in white",
        "simple thong sandals in tan leather",
        "pointed-toe ankle strap heels",
    ],

    "bag": [
        "no bag",
        "structured top-handle leather bag in black",
        "classic canvas tote bag",
        "small leather crossbody bag in tan",
        "oversized leather shopper bag",
        "minimalist leather clutch in white",
        "woven straw basket bag",
        "simple nylon backpack",
        "chain strap leather shoulder bag",
        "small square leather bag in camel",
    ],

    "accessories": [
        "no accessories",
        "thin gold hoop earrings",
        "simple gold chain necklace",
        "classic tortoiseshell sunglasses",
        "thin leather belt in cognac",
        "white linen scarf loosely draped",
        "simple watch with leather strap",
        "layered thin gold necklaces",
        "small pearl stud earrings",
        "classic baseball cap in white",
        "knit beanie in gray",
        "silk hair scarf as headband",
        "simple drop earrings in silver",
        "delicate anklet chain",
    ],

    "color_palette": [
        "neutral whites and creams",
        "all black monochrome",
        "classic navy and white",
        "earth tones — rust, camel, olive",
        "soft pastels — blush and sage",
        "gray and charcoal tones",
        "black and white contrast",
        "warm beige and brown tones",
        "cobalt blue and white",
        "classic red and navy",
        "forest green and cream",
        "soft lavender and white",
        "muted terracotta and sand",
        "classic camel and black",
        "cool gray and pale blue",
    ],

    "fabric": [
        "cotton",
        "linen",
        "wool",
        "denim",
        "silk",
        "cashmere",
        "leather",
        "knit",
        "satin",
        "velvet",
        "suede",
        "chiffon",
    ],
}


# ══════════════════════════════════════════════════════════════════════════════
#  BASE DE DATOS — ROPA EXPERIMENTAL
#  Alta costura, avant-garde, moda conceptual, wearable art, surreal fashion
# ══════════════════════════════════════════════════════════════════════════════

EXPERIMENTAL_DATA = {

    "aesthetic": [
        "avant-garde deconstructed couture",
        "dark sculptural haute couture",
        "biomechanical wearable art",
        "architectural fashion sculpture",
        "post-apocalyptic reconstructed fashion",
        "surreal dreamlike couture",
        "raw industrial deconstruction",
        "organic body horror couture",
        "latex fetish high fashion",
        "fluid gender-fluid couture",
        "Japanese conceptual deconstruction",
        "neo-gothic dark romanticism",
        "clinical medical aesthetic fashion",
        "deep sea creature couture",
        "fragmented deconstructed tailoring",
        "crystalline mineral fashion",
        "insect exoskeleton couture",
        "melted and reformed fabric sculpture",
        "origami paper architecture fashion",
        "fungal organic growth fashion",
    ],

    "garment_concept": [
        "asymmetric deconstructed jacket with exposed seams and raw edges",
        "sculptural voluminous ball gown with architectural silhouette",
        "full body latex catsuit with cutouts and molded panels",
        "coat made entirely of overlapping feathers dyed in gradient",
        "dress constructed from metal rings and chains",
        "garment that appears partially melted and re-solidified",
        "oversized coat with exaggerated sleeves wider than body",
        "dress made of transparent plastic panels over dark underlayer",
        "bodysuit covered entirely in hand-sewn crystal beads",
        "garment built from repurposed industrial material and straps",
        "floor-length coat with dramatic structured collar tower",
        "suit where fabric appears to be peeling and falling off",
        "dress made of layered black tulle erupting from waist",
        "corset-based top with exposed boning as external decoration",
        "coat with massive sculptural padded geometric panels",
        "garment assembled from interlinked metal and leather plates",
        "full-length transparent organza robe over minimal black base",
        "bodysuit with molded 3D organic shapes growing from surface",
        "dress with incredibly long train dragging five meters behind",
        "jacket with no conventional closures, held by magnets and weight",
    ],

    "surface_treatment": [
        "completely smooth matte black surface",
        "high-gloss wet-look lacquer finish",
        "heavily distressed and torn raw edges throughout",
        "hand-painted abstract pattern in black and white",
        "surface covered in hundreds of safety pins",
        "embroidered with black thread organic vine patterns",
        "encrusted entirely with irregular crystal fragments",
        "surface has been intentionally burned and scorched",
        "printed with extreme close-up human skin texture photograph",
        "coated in metallic silver spray paint",
        "covered with hand-stitched spiral patterns",
        "surface partially dissolved showing structure underneath",
        "entirely covered in black feathers",
        "studded with hundreds of metal spikes",
        "surface printed with x-ray or anatomical imagery",
        "draped in thin metal chains over entire surface",
        "wax-dipped giving rigid sculptural appearance",
        "pleated in impossibly tight micro pleats throughout",
    ],

    "silhouette": [
        "extreme hourglass with exaggerated hip and shoulder proportions",
        "completely rectangular boxy silhouette with no body definition",
        "cocoon shape — wider at middle, tapered at ends",
        "extreme A-line — tiny top expanding to enormous skirt",
        "asymmetric — full one side, almost nothing the other",
        "inverted triangle — enormous shoulders, nothing at waist",
        "column — perfectly cylindrical and vertical",
        "sculptural — geometric shapes that extend far from body",
        "draped — fabric falls from single shoulder point",
        "layered — multiple garments of different lengths visible",
    ],

    "footwear": [
        "no footwear — outfit only",
        "sculptural platform boots with abstract heel",
        "thigh-high latex boots in black",
        "architectural shoes with geometric structural heel",
        "ankle boots wrapped in chains and straps",
        "platform boots with transparent heel filled with objects",
        "knee-high lace-up boots with external metal hardware",
        "ballet heels extremely pointed at 45 degree angle",
        "boots with molded organic shapes around leg",
        "flatform boots with woven rope platform",
        "heeled boots where heel is made from animal horn shape",
    ],

    "bag_accessory": [
        "no bag or accessories",
        "sculptural clutch shaped like an anatomical object",
        "oversized exaggerated hat as main accessory",
        "arm cuffs made of resin casting organic materials",
        "collar constructed of metal rods and rings",
        "mask or face piece as wearable accessory",
        "structural cage-like garment worn over outfit",
        "chain harness worn over garment",
        "dramatically oversized statement ring on multiple fingers",
        "neck piece made of geometric laser-cut acrylic",
        "bag that appears to be an abstract sculpture",
        "gloves with elongated claw-like finger extensions",
    ],

    "color_mood": [
        "all black, no other color",
        "stark black and white only",
        "all white with deep shadow",
        "monochromatic deep burgundy",
        "raw materials — no color, only texture",
        "deep forest green and black",
        "dark navy and charcoal",
        "iridescent oil-slick multi-color",
        "bleached and faded, almost no color",
        "oxidized metal tones — bronze and rust",
        "surgical white with stark shadow",
        "deep violet and black",
        "acid yellow and black",
        "pale flesh tone — almost skin colored",
        "pure red and black",
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
#  NODO
# ══════════════════════════════════════════════════════════════════════════════

class OutfitPromptGenerator:
    """
    Genera prompts de conjuntos de ropa COMPLETOS sobre fondo blanco puro.
    Sin maniquí, sin persona.

    MODE = NORMAL       → ropa wearable real
    MODE = EXPERIMENTAL → haute couture, avant-garde, moda conceptual surreal
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {

            "seed": ("INT", {"default": 0, "min": 0, "max": 0xFFFFFFFF, "step": 1, "display": "number"}),
            "mode": (["NORMAL", "EXPERIMENTAL"],),
            "gender": (["female", "male", "androgynous"],),

            # ── Campos NORMAL ────────────────────────────────────────────────
            "N_style":         (with_random(NORMAL_DATA["style"]),),
            "N_color_palette": (with_random(NORMAL_DATA["color_palette"]),),
            "N_fabric":        (with_random(NORMAL_DATA["fabric"]),),
            "N_one_piece":     (with_random(NORMAL_DATA["one_piece"]),),
            "N_top":           (with_random(NORMAL_DATA["top"]),),
            "N_bottom":        (with_random(NORMAL_DATA["bottom"]),),
            "N_footwear":      (with_random(NORMAL_DATA["footwear"]),),
            "N_bag":           (with_random(NORMAL_DATA["bag"]),),
            "N_accessories":   (with_random(NORMAL_DATA["accessories"]),),

            # ── Campos EXPERIMENTAL ──────────────────────────────────────────
            "E_aesthetic":         (with_random(EXPERIMENTAL_DATA["aesthetic"]),),
            "E_garment_concept":   (with_random(EXPERIMENTAL_DATA["garment_concept"]),),
            "E_surface_treatment": (with_random(EXPERIMENTAL_DATA["surface_treatment"]),),
            "E_silhouette":        (with_random(EXPERIMENTAL_DATA["silhouette"]),),
            "E_footwear":          (with_random(EXPERIMENTAL_DATA["footwear"]),),
            "E_bag_accessory":     (with_random(EXPERIMENTAL_DATA["bag_accessory"]),),
            "E_color_mood":        (with_random(EXPERIMENTAL_DATA["color_mood"]),),

            # ── Extra libre ──────────────────────────────────────────────────
            "extra_details": ("STRING", {
                "default": "",
                "multiline": False,
                "placeholder": "Detalles extra opcionales...",
            }),
        }}

    RETURN_TYPES  = ("STRING", "STRING")
    RETURN_NAMES  = ("OUTFIT_PROMPT", "JSON_METADATA")
    FUNCTION      = "generate"
    CATEGORY      = "🎭 Character Generator"

    def generate(
        self, seed, mode, gender,
        N_style, N_color_palette, N_fabric, N_one_piece,
        N_top, N_bottom, N_footwear, N_bag, N_accessories,
        E_aesthetic, E_garment_concept, E_surface_treatment,
        E_silhouette, E_footwear, E_bag_accessory, E_color_mood,
        extra_details,
    ):
        if seed == 0:
            seed = random.randint(1, 0xFFFFFFFF)
        random.seed(seed)

        # ── Sufijo base común ─────────────────────────────────────────────────
        # Sin maniquí, sin persona — ropa sola sobre fondo blanco
        BASE_SUFFIX = (
            "product photography of clothing laid flat on pure white background, "
            "no mannequin, no person, no body, "
            "complete outfit ensemble arranged neatly, "
            "all pieces visible, clean white background, "
            "professional fashion product shot, "
            "sharp focus, even studio lighting, high quality"
        )

        if mode == "NORMAL":
            r_style  = pick(NORMAL_DATA["style"],         N_style)
            r_col    = pick(NORMAL_DATA["color_palette"], N_color_palette)
            r_fab    = pick(NORMAL_DATA["fabric"],        N_fabric)
            r_piece  = pick(NORMAL_DATA["one_piece"],     N_one_piece)
            r_top    = pick(NORMAL_DATA["top"],           N_top)
            r_bot    = pick(NORMAL_DATA["bottom"],        N_bottom)
            r_foot   = pick(NORMAL_DATA["footwear"],      N_footwear)
            r_bag    = pick(NORMAL_DATA["bag"],           N_bag)
            r_acc    = pick(NORMAL_DATA["accessories"],   N_accessories)

            meta = {
                "seed": seed, "mode": "NORMAL", "gender": gender,
                "style": r_style, "color_palette": r_col, "fabric": r_fab,
                "one_piece": r_piece, "top": r_top, "bottom": r_bot,
                "footwear": r_foot, "bag": r_bag, "accessories": r_acc,
                "extra_details": extra_details,
            }

            # Construir el conjunto
            garment_parts = []
            if "none" not in r_piece.lower():
                garment_parts.append(r_piece)
            else:
                garment_parts.append(r_top)
                if "none" not in r_bot.lower():
                    garment_parts.append(r_bot)

            if "no footwear" not in r_foot:
                garment_parts.append(r_foot)
            if "no bag" not in r_bag:
                garment_parts.append(r_bag)
            if "no accessories" not in r_acc:
                garment_parts.append(r_acc)

            outfit_desc = (
                f"{r_style} {gender} complete outfit, {r_col}, {r_fab} fabric, "
                + ", ".join(garment_parts)
            )

        else:  # EXPERIMENTAL
            r_aes  = pick(EXPERIMENTAL_DATA["aesthetic"],         E_aesthetic)
            r_garm = pick(EXPERIMENTAL_DATA["garment_concept"],   E_garment_concept)
            r_surf = pick(EXPERIMENTAL_DATA["surface_treatment"], E_surface_treatment)
            r_sil  = pick(EXPERIMENTAL_DATA["silhouette"],        E_silhouette)
            r_foot = pick(EXPERIMENTAL_DATA["footwear"],          E_footwear)
            r_bag  = pick(EXPERIMENTAL_DATA["bag_accessory"],     E_bag_accessory)
            r_col  = pick(EXPERIMENTAL_DATA["color_mood"],        E_color_mood)

            meta = {
                "seed": seed, "mode": "EXPERIMENTAL", "gender": gender,
                "aesthetic": r_aes, "garment_concept": r_garm,
                "surface_treatment": r_surf, "silhouette": r_sil,
                "footwear": r_foot, "bag_accessory": r_bag,
                "color_mood": r_col, "extra_details": extra_details,
            }

            garment_parts = [r_garm, r_surf, r_sil]
            if "no footwear" not in r_foot:
                garment_parts.append(r_foot)
            if "no bag" not in r_bag and "no accessories" not in r_bag:
                garment_parts.append(r_bag)

            outfit_desc = (
                f"{r_aes} {gender} complete ensemble, {r_col}, "
                + ", ".join(garment_parts)
            )

        if extra_details.strip():
            outfit_desc += f", {extra_details.strip()}"

        prompt = f"{outfit_desc}, {BASE_SUFFIX}"

        return (prompt, json.dumps(meta, indent=2, ensure_ascii=False))


# ══════════════════════════════════════════════════════════════════════════════
#  REGISTRO
# ══════════════════════════════════════════════════════════════════════════════

NODE_CLASS_MAPPINGS = {
    "OutfitPromptGenerator": OutfitPromptGenerator,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OutfitPromptGenerator": "👗 Outfit Prompt Generator",
}
