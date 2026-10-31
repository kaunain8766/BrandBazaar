import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.files.base import ContentFile
from apps.catalog.models import Brand, Category, Product, ProductImage

MEDIA_ROOT = 'media'
os.makedirs(os.path.join(MEDIA_ROOT, 'brands'), exist_ok=True)
os.makedirs(os.path.join(MEDIA_ROOT, 'categories'), exist_ok=True)
os.makedirs(os.path.join(MEDIA_ROOT, 'products'), exist_ok=True)
os.makedirs(os.path.join(MEDIA_ROOT, 'products', 'gallery'), exist_ok=True)

# -------------------------------------------------------------
# 1. BRAND LOGOS (Transparent / White card optimized vector SVG)
# -------------------------------------------------------------
BRAND_LOGOS = {
    'levis': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 120" width="300" height="120">
  <path d="M10 20 L290 20 L290 70 Q215 65 150 95 Q85 65 10 70 Z" fill="#C41230"/>
  <text x="150" y="62" font-family="'Helvetica Neue', Arial, sans-serif" font-weight="900" font-size="44" fill="#FFFFFF" text-anchor="middle" letter-spacing="1">LEVI'S</text>
  <circle cx="240" cy="40" r="4" fill="#FFFFFF"/>
</svg>''',

    'nike': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 120" width="300" height="120">
  <path d="M40 75 Q110 95 180 50 Q230 20 270 15 Q210 55 150 78 Q90 98 40 75 Z" fill="#111111"/>
  <text x="150" y="105" font-family="'Impact', Arial Black, sans-serif" font-style="italic" font-size="34" fill="#111111" text-anchor="middle" letter-spacing="3">NIKE</text>
</svg>''',

    'puma': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 120" width="300" height="120">
  <g transform="translate(60, 15) scale(0.7)">
    <path d="M40 70 C30 50 45 25 70 20 C60 30 70 45 85 40 C105 35 125 10 145 15 C130 30 145 50 160 45 C180 40 200 20 220 25 C190 55 150 80 110 85 C80 90 50 85 40 70 Z" fill="#000000"/>
  </g>
  <text x="150" y="98" font-family="'Arial Black', sans-serif" font-weight="900" font-size="32" fill="#000000" text-anchor="middle" letter-spacing="4">PUMA</text>
</svg>''',

    'sony': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 120" width="300" height="120">
  <text x="150" y="75" font-family="'Georgia', serif" font-weight="bold" font-size="52" fill="#000000" text-anchor="middle" letter-spacing="6">SONY</text>
  <line x1="60" y1="90" x2="240" y2="90" stroke="#E2E8F0" stroke-width="2"/>
</svg>''',

    'boat': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 120" width="300" height="120">
  <polygon points="120,25 150,65 120,65" fill="#E11D48"/>
  <polygon points="155,15 185,65 155,65" fill="#BE123C"/>
  <path d="M110 72 L190 72 Q150 90 110 72 Z" fill="#E11D48"/>
  <text x="150" y="106" font-family="'Century Gothic', sans-serif" font-weight="bold" font-size="28" fill="#111827" text-anchor="middle" letter-spacing="2">bo<tspan fill="#E11D48">A</tspan>t</text>
</svg>''',

    'samsung': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 120" width="300" height="120">
  <ellipse cx="150" cy="60" rx="130" ry="42" fill="#1428A0" transform="rotate(-6 150 60)"/>
  <text x="150" y="70" font-family="'Arial Black', Helvetica, sans-serif" font-weight="900" font-size="32" fill="#FFFFFF" text-anchor="middle" letter-spacing="3">SAMSUNG</text>
</svg>''',

    'zara': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 120" width="300" height="120">
  <text x="150" y="78" font-family="'Didot', 'Bodoni MT', 'Times New Roman', serif" font-weight="bold" font-size="64" fill="#000000" text-anchor="middle" letter-spacing="-3">ZARA</text>
</svg>''',

    'allen-solly': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 120" width="300" height="120">
  <circle cx="150" cy="35" r="18" fill="#1E3A8A"/>
  <path d="M142 35 L150 25 L158 35 L150 45 Z" fill="#F59E0B"/>
  <text x="150" y="75" font-family="'Trajan Pro', 'Georgia', serif" font-weight="bold" font-size="22" fill="#1E293B" text-anchor="middle" letter-spacing="3">ALLEN SOLLY</text>
  <text x="150" y="94" font-family="sans-serif" font-size="11" fill="#64748B" text-anchor="middle" letter-spacing="2">ESTD 1744 • NOTTINGHAM</text>
</svg>''',

    'loreal-paris': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 120" width="300" height="120">
  <text x="150" y="60" font-family="'Century Gothic', sans-serif" font-weight="bold" font-size="36" fill="#000000" text-anchor="middle" letter-spacing="4">L'ORÉAL</text>
  <text x="150" y="85" font-family="'Century Gothic', sans-serif" font-size="16" fill="#C5A059" text-anchor="middle" letter-spacing="6">PARIS</text>
</svg>''',

    'maybelline': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 120" width="300" height="120">
  <text x="150" y="58" font-family="'Arial Black', sans-serif" font-weight="900" font-size="26" fill="#000000" text-anchor="middle" letter-spacing="2">MAYBELLINE</text>
  <text x="150" y="82" font-family="'Arial', sans-serif" font-weight="bold" font-size="14" fill="#DB2777" text-anchor="middle" letter-spacing="5">NEW YORK</text>
</svg>''',
}

# -------------------------------------------------------------
# 2. CATEGORY HERO / CIRCLE VISUALS
# -------------------------------------------------------------
CATEGORY_VISUALS = {
    'clothes': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
  <defs>
    <linearGradient id="cg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#3B82F6;stop-opacity:1"/>
      <stop offset="100%" style="stop-color:#1E3A8A;stop-opacity:1"/>
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" fill="url(#cg)"/>
  <!-- Hanger icon -->
  <path d="M200 120 C200 95 185 90 180 100 C175 110 195 120 200 135 L120 180 L280 180 Z" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linejoin="round"/>
  <!-- Folded clothes & tie -->
  <path d="M140 185 L260 185 L250 300 L150 300 Z" fill="#EFF6FF" opacity="0.95"/>
  <!-- Collar & buttons -->
  <polygon points="175,185 200,225 185,185" fill="#3B82F6"/>
  <polygon points="225,185 200,225 215,185" fill="#2563EB"/>
  <circle cx="200" cy="245" r="4" fill="#1E3A8A"/>
  <circle cx="200" cy="265" r="4" fill="#1E3A8A"/>
  <circle cx="200" cy="285" r="4" fill="#1E3A8A"/>
  <text x="200" y="355" font-family="system-ui, sans-serif" font-weight="bold" font-size="24" fill="#FFFFFF" text-anchor="middle">CLOTHING</text>
</svg>''',

    'footwear': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
  <defs>
    <linearGradient id="fg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#10B981;stop-opacity:1"/>
      <stop offset="100%" style="stop-color:#064E3B;stop-opacity:1"/>
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" fill="url(#fg)"/>
  <!-- Sneaker vector profile -->
  <g transform="translate(45, 120)">
    <!-- Sole -->
    <path d="M20 150 Q160 160 290 140 Q295 160 280 170 Q150 180 20 170 Z" fill="#F8FAFC"/>
    <!-- Upper body -->
    <path d="M30 150 Q70 70 140 90 L210 110 Q280 120 290 140 Q150 150 30 150 Z" fill="#047857"/>
    <!-- Toe cap -->
    <path d="M230 115 Q285 125 290 140 L230 140 Z" fill="#34D399"/>
    <!-- Laces & Swoop -->
    <line x1="140" y1="95" x2="170" y2="120" stroke="#FFFFFF" stroke-width="4"/>
    <line x1="160" y1="98" x2="190" y2="122" stroke="#FFFFFF" stroke-width="4"/>
    <path d="M80 140 Q140 110 200 130" stroke="#FFFFFF" stroke-width="6" fill="none"/>
  </g>
  <text x="200" y="355" font-family="system-ui, sans-serif" font-weight="bold" font-size="24" fill="#FFFFFF" text-anchor="middle">FOOTWEAR</text>
</svg>''',

    'beauty': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#EC4899;stop-opacity:1"/>
      <stop offset="100%" style="stop-color:#831843;stop-opacity:1"/>
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" fill="url(#bg)"/>
  <!-- Skincare serum dropper bottle -->
  <g transform="translate(100, 90)">
    <!-- Bottle body -->
    <rect x="50" y="80" width="70" height="130" rx="15" fill="#FFFFFF" opacity="0.95"/>
    <rect x="65" y="55" width="40" height="25" fill="#CBD5E1"/>
    <path d="M75 55 Q85 30 85 20 Q85 30 95 55 Z" fill="#F43F5E"/>
    <!-- Label -->
    <rect x="55" y="110" width="60" height="60" rx="4" fill="#FDF2F8"/>
    <line x1="65" y1="130" x2="105" y2="130" stroke="#DB2777" stroke-width="3"/>
    <line x1="70" y1="145" x2="100" y2="145" stroke="#94A3B8" stroke-width="2"/>
  </g>
  <!-- Lipstick alongside -->
  <g transform="translate(220, 150)">
    <rect x="15" y="60" width="35" height="70" rx="4" fill="#1E293B"/>
    <rect x="20" y="40" width="25" height="20" fill="#D4AF37"/>
    <polygon points="20,40 32,5 45,40" fill="#E11D48"/>
  </g>
  <text x="200" y="355" font-family="system-ui, sans-serif" font-weight="bold" font-size="22" fill="#FFFFFF" text-anchor="middle">BEAUTY &amp; CARE</text>
</svg>''',

    'electronics': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
  <defs>
    <linearGradient id="eg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#6366F1;stop-opacity:1"/>
      <stop offset="100%" style="stop-color:#0F172A;stop-opacity:1"/>
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" fill="url(#eg)"/>
  <!-- Over-ear Headphones -->
  <g transform="translate(90, 80)">
    <!-- Headband arc -->
    <path d="M30 130 C30 30 190 30 190 130" fill="none" stroke="#FFFFFF" stroke-width="12" stroke-linecap="round"/>
    <!-- Left Ear cup -->
    <rect x="15" y="110" width="32" height="75" rx="16" fill="#38BDF8"/>
    <rect x="35" y="125" width="18" height="45" rx="6" fill="#0284C7"/>
    <!-- Right Ear cup -->
    <rect x="175" y="110" width="32" height="75" rx="16" fill="#38BDF8"/>
    <rect x="167" y="125" width="18" height="45" rx="6" fill="#0284C7"/>
  </g>
  <!-- Smartwatch display -->
  <g transform="translate(160, 230)">
    <rect x="15" y="10" width="50" height="50" rx="15" fill="#0F172A" stroke="#38BDF8" stroke-width="3"/>
    <text x="40" y="42" font-family="sans-serif" font-size="16" font-weight="bold" fill="#38BDF8" text-anchor="middle">10:08</text>
  </g>
  <text x="200" y="355" font-family="system-ui, sans-serif" font-weight="bold" font-size="24" fill="#FFFFFF" text-anchor="middle">ELECTRONICS</text>
</svg>''',
}

# -------------------------------------------------------------
# 3. HIGH-FIDELITY PRODUCT VISUALS & GALLERY ANGLES
# -------------------------------------------------------------
def make_product_svg(brand, title, subtitle, icon_type, main_color="#1E3A8A", bg_start="#F8FAFC", bg_end="#E2E8F0", tag="GENUINE"):
    """
    Renders a stunning product showcase card with drop shadows, product silhouette,
    brand badge, specifications, and certified authentic seal.
    """
    # Dynamic iconography based on product type
    if icon_type == "jeans":
        center_art = '''
        <!-- Denim Jeans silhouette -->
        <path d="M190 140 L310 140 L325 380 L265 380 L250 240 L235 380 L175 380 Z" fill="#1E3A8A" stroke="#172554" stroke-width="4"/>
        <path d="M210 155 Q250 170 290 155" fill="none" stroke="#F59E0B" stroke-width="3" stroke-dasharray="4,3"/>
        <rect x="300" y="170" width="12" height="28" fill="#DC2626"/>
        <text x="306" y="188" font-family="sans-serif" font-size="9" font-weight="bold" fill="#FFFFFF" text-anchor="middle" transform="rotate(90 306 188)">LEVI'S</text>
        '''
    elif icon_type == "denim_shirt":
        center_art = '''
        <!-- Denim Western Shirt silhouette -->
        <path d="M170 150 L230 130 L270 130 L330 150 L310 210 L285 200 L285 370 L215 370 L215 200 L190 210 Z" fill="#2563EB" stroke="#1D4ED8" stroke-width="3"/>
        <!-- Western yoke -->
        <path d="M200 170 L250 195 L300 170" fill="none" stroke="#F59E0B" stroke-width="3"/>
        <!-- Pearl snap buttons -->
        <circle cx="250" cy="220" r="4" fill="#FFFFFF" stroke="#94A3B8" stroke-width="2"/>
        <circle cx="250" cy="260" r="4" fill="#FFFFFF" stroke="#94A3B8" stroke-width="2"/>
        <circle cx="250" cy="300" r="4" fill="#FFFFFF" stroke="#94A3B8" stroke-width="2"/>
        '''
    elif icon_type == "formal_shirt":
        center_art = '''
        <!-- Formal Shirt Silhouette -->
        <path d="M165 145 L225 130 L275 130 L335 145 L320 210 L290 200 L290 375 L210 375 L210 200 L180 210 Z" fill="#BAE6FD" stroke="#38BDF8" stroke-width="2"/>
        <!-- Tie -->
        <polygon points="245,160 255,160 260,310 250,330 240,310" fill="#1E3A8A"/>
        <!-- Spread collar -->
        <polygon points="215,135 250,175 235,140" fill="#F0F9FF"/>
        <polygon points="285,135 250,175 265,140" fill="#E0F2FE"/>
        '''
    elif icon_type == "tshirt":
        center_art = '''
        <!-- Sports T-Shirt -->
        <path d="M165 150 L220 135 L280 135 L335 150 L315 210 L285 200 L285 370 L215 370 L215 200 L185 210 Z" fill="#18181B" stroke="#27272A" stroke-width="2"/>
        <!-- Swoosh on chest -->
        <path d="M230 220 Q250 230 270 215 Q255 225 240 222 Z" fill="#FFFFFF"/>
        <!-- Collar -->
        <path d="M220 135 Q250 155 280 135" fill="none" stroke="#3F3F46" stroke-width="5"/>
        '''
    elif icon_type == "dress":
        center_art = '''
        <!-- Flowy Midi Dress -->
        <path d="M225 140 L275 140 L290 210 L210 210 Z" fill="#F472B6"/>
        <path d="M210 210 Q250 220 290 210 L350 370 Q250 385 150 370 Z" fill="#FB7185" stroke="#E11D48" stroke-width="2"/>
        <!-- Floral accents -->
        <circle cx="230" cy="260" r="8" fill="#FEF08A"/>
        <circle cx="280" cy="300" r="9" fill="#FEF08A"/>
        <circle cx="220" cy="330" r="10" fill="#FEF08A"/>
        <circle cx="260" cy="350" r="8" fill="#FEF08A"/>
        '''
    elif icon_type == "top":
        center_art = '''
        <!-- Ribbed Top -->
        <path d="M215 150 L285 150 L295 290 L205 290 Z" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="3"/>
        <line x1="225" y1="160" x2="225" y2="280" stroke="#E2E8F0" stroke-width="3"/>
        <line x1="245" y1="160" x2="245" y2="280" stroke="#E2E8F0" stroke-width="3"/>
        <line x1="265" y1="160" x2="265" y2="280" stroke="#E2E8F0" stroke-width="3"/>
        <line x1="275" y1="160" x2="275" y2="280" stroke="#E2E8F0" stroke-width="3"/>
        '''
    elif icon_type == "trucker":
        center_art = '''
        <!-- Denim Trucker Jacket -->
        <path d="M165 150 L220 135 L280 135 L335 150 L320 230 L285 220 L285 360 L215 360 L215 220 L180 230 Z" fill="#3B82F6" stroke="#1D4ED8" stroke-width="3"/>
        <!-- Chest flap pockets -->
        <rect x="220" y="190" width="22" height="20" rx="3" fill="#1E40AF"/>
        <rect x="258" y="190" width="22" height="20" rx="3" fill="#1E40AF"/>
        <!-- Brass buttons -->
        <circle cx="250" cy="240" r="4" fill="#F59E0B"/>
        <circle cx="250" cy="280" r="4" fill="#F59E0B"/>
        <circle cx="250" cy="320" r="4" fill="#F59E0B"/>
        '''
    elif icon_type == "running_shoes":
        center_art = '''
        <!-- Nike Zoom Pegasus 40 Silhouette -->
        <g transform="translate(100, 190) scale(1.1)">
          <!-- Aerodynamic Sole -->
          <path d="M20 100 Q150 120 260 85 Q265 110 245 125 Q130 135 20 120 Z" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="2"/>
          <!-- Zoom Air Cushion Accent -->
          <rect x="140" y="105" width="45" height="12" rx="4" fill="#38BDF8"/>
          <!-- Shoe Upper -->
          <path d="M30 100 Q65 30 130 50 L200 65 Q255 75 260 85 Q135 95 30 100 Z" fill="#0F172A"/>
          <!-- Vibrant Swoosh -->
          <path d="M70 90 Q140 55 200 80 Q130 80 80 92 Z" fill="#38BDF8"/>
        </g>
        '''
    elif icon_type == "sneakers":
        center_art = '''
        <!-- Puma Smash v2 Silhouette -->
        <g transform="translate(100, 190) scale(1.1)">
          <!-- Rubber Cupsole -->
          <path d="M25 105 Q150 110 265 95 Q270 120 250 125 Q140 130 25 125 Z" fill="#FEF3C7" stroke="#FDE68A" stroke-width="2"/>
          <!-- White Leather Upper -->
          <path d="M35 105 Q70 45 135 60 L195 70 Q260 80 265 95 Q140 105 35 105 Z" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="2"/>
          <!-- Formstrip wave -->
          <path d="M80 95 Q145 65 210 90 L205 100 Q145 78 80 98 Z" fill="#1E3A8A"/>
        </g>
        '''
    elif icon_type == "serum":
        center_art = '''
        <!-- Skincare Serum Dropper Bottle -->
        <g transform="translate(180, 150)">
          <!-- Glass Dropper Bulb -->
          <path d="M60 40 Q70 10 70 0 Q70 10 80 40 Z" fill="#CBD5E1"/>
          <rect x="52" y="40" width="36" height="20" rx="3" fill="#94A3B8"/>
          <!-- Glass Bottle -->
          <rect x="35" y="65" width="70" height="150" rx="16" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="3"/>
          <rect x="42" y="95" width="56" height="85" rx="4" fill="#EFF6FF"/>
          <!-- Serum droplet -->
          <circle cx="70" cy="130" r="14" fill="#60A5FA" opacity="0.8"/>
          <text x="70" y="160" font-family="sans-serif" font-size="10" font-weight="bold" fill="#1E3A8A" text-anchor="middle">1.5% HA</text>
        </g>
        '''
    elif icon_type == "lipstick":
        center_art = '''
        <!-- Matte Ink Liquid Lipstick -->
        <g transform="translate(190, 150)">
          <!-- Bottle Body -->
          <rect x="40" y="80" width="40" height="130" rx="6" fill="#BE123C"/>
          <!-- White Cap -->
          <rect x="40" y="10" width="40" height="70" rx="4" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="2"/>
          <text x="60" y="150" font-family="sans-serif" font-size="10" font-weight="bold" fill="#FFFFFF" text-anchor="middle" transform="rotate(-90 60 150)">SUPERSTAY</text>
        </g>
        '''
    elif icon_type == "headphones":
        center_art = '''
        <!-- Sony WH-1000XM5 Headphones -->
        <g transform="translate(140, 130)">
          <path d="M40 130 C40 20 180 20 180 130" fill="none" stroke="#1E293B" stroke-width="14" stroke-linecap="round"/>
          <rect x="15" y="110" width="38" height="85" rx="19" fill="#0F172A"/>
          <rect x="167" y="110" width="38" height="85" rx="19" fill="#0F172A"/>
          <circle cx="34" cy="152" r="12" fill="#D4AF37"/>
          <circle cx="186" cy="152" r="12" fill="#D4AF37"/>
        </g>
        '''
    elif icon_type == "earbuds":
        center_art = '''
        <!-- boAt Airdopes 141 Case & Buds -->
        <g transform="translate(170, 170)">
          <!-- Charging Case -->
          <rect x="20" y="40" width="120" height="90" rx="35" fill="#18181B" stroke="#27272A" stroke-width="3"/>
          <circle cx="80" cy="85" r="5" fill="#22C55E"/>
          <!-- Left Earbud -->
          <circle cx="50" cy="15" r="18" fill="#DC2626"/>
          <rect x="45" y="25" width="10" height="30" rx="5" fill="#18181B"/>
          <!-- Right Earbud -->
          <circle cx="110" cy="15" r="18" fill="#DC2626"/>
          <rect x="105" y="25" width="10" height="30" rx="5" fill="#18181B"/>
        </g>
        '''
    elif icon_type == "smartwatch":
        center_art = '''
        <!-- Samsung Galaxy Watch 6 -->
        <g transform="translate(170, 140)">
          <!-- Straps -->
          <rect x="45" y="0" width="70" height="60" fill="#334155"/>
          <rect x="45" y="180" width="70" height="60" fill="#334155"/>
          <!-- Circular Dial -->
          <circle cx="80" cy="120" r="60" fill="#0F172A" stroke="#475569" stroke-width="6"/>
          <circle cx="80" cy="120" r="50" fill="#020617"/>
          <!-- Dial UI -->
          <text x="80" y="115" font-family="'Courier New', monospace" font-size="24" font-weight="bold" fill="#38BDF8" text-anchor="middle">10:08</text>
          <text x="80" y="135" font-family="sans-serif" font-size="11" fill="#22C55E" text-anchor="middle">♥ 74 BPM</text>
        </g>
        '''
    else:
        center_art = '''
        <circle cx="250" cy="250" r="80" fill="#E2E8F0"/>
        '''

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{bg_start};stop-opacity:1"/>
      <stop offset="100%" style="stop-color:{bg_end};stop-opacity:1"/>
    </linearGradient>
    <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="12" stdDeviation="15" flood-color="#000000" flood-opacity="0.12"/>
    </filter>
  </defs>

  <!-- Background Base -->
  <rect width="100%" height="100%" fill="url(#bgGrad)"/>
  <circle cx="250" cy="250" r="180" fill="#FFFFFF" opacity="0.6"/>

  <!-- Top Badge / Brand Header -->
  <g transform="translate(30, 30)">
    <rect x="0" y="0" width="100" height="26" rx="13" fill="{main_color}"/>
    <text x="50" y="17" font-family="system-ui, sans-serif" font-size="11" font-weight="bold" fill="#FFFFFF" text-anchor="middle">{tag}</text>
    <text x="115" y="18" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#475569">{brand}</text>
  </g>

  <!-- Center Product Illustration with Shadow -->
  <g filter="url(#shadow)">
    {center_art}
  </g>

  <!-- Bottom Details Overlay -->
  <rect x="30" y="420" width="440" height="50" rx="10" fill="#FFFFFF" opacity="0.95"/>
  <text x="45" y="445" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="bold" fill="#0F172A">{title}</text>
  <text x="45" y="460" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="#64748B">{subtitle}</text>
  <rect x="400" y="430" width="60" height="30" rx="6" fill="#F1F5F9"/>
  <text x="430" y="450" font-family="system-ui, sans-serif" font-size="11" font-weight="bold" fill="{main_color}" text-anchor="middle">OFFICIAL</text>
</svg>'''
    return svg.encode('utf-8')


# -------------------------------------------------------------
# RUNNER: UPDATE DATABASE MODELS & WRITE ASSETS
# -------------------------------------------------------------
print("Applying rich brand logos...")
for slug, svg_content in BRAND_LOGOS.items():
    brand = Brand.objects.filter(slug=slug).first()
    if brand:
        filepath = os.path.join(MEDIA_ROOT, 'brands', f"{slug}-logo.svg")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        brand.logo = f"brands/{slug}-logo.svg"
        brand.save()
        print(f" -> Brand logo attached for {brand.name}")

print("\nApplying category visual illustrations...")
cat_map = {
    'clothes': 'clothes',
    'footwear': 'footwear',
    'beauty-personal-care': 'beauty',
    'electronics': 'electronics',
}
for cat_slug, key in cat_map.items():
    cat = Category.objects.filter(slug=cat_slug).first()
    if cat and key in CATEGORY_VISUALS:
        filepath = os.path.join(MEDIA_ROOT, 'categories', f"{cat_slug}.svg")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(CATEGORY_VISUALS[key])
        cat.image = f"categories/{cat_slug}.svg"
        cat.save()
        print(f" -> Category image attached for {cat.name}")

print("\nGenerating rich product illustrations and gallery images...")
PRODUCT_CONFIGS = [
    {
        'slug': 'levis-men-511-slim-fit-stretch-jeans',
        'icon': 'jeans',
        'color': '#1E3A8A',
        'bg1': '#EFF6FF',
        'bg2': '#DBEAFE',
        'tag': "LEVI'S DENIM",
        'sub': "511 Slim Fit • Stretch Comfort Fabric",
    },
    {
        'slug': 'levis-classic-western-denim-shirt',
        'icon': 'denim_shirt',
        'color': '#2563EB',
        'bg1': '#F0F9FF',
        'bg2': '#E0F2FE',
        'tag': "HERITAGE",
        'sub': "Pointed Yoke • Pearl Snap Buttons",
    },
    {
        'slug': 'allen-solly-men-solid-regular-fit-formal-shirt',
        'icon': 'formal_shirt',
        'color': '#0284C7',
        'bg1': '#F8FAFC',
        'bg2': '#E2E8F0',
        'tag': "FORMAL",
        'sub': "Pure Breathable Cotton • Spread Collar",
    },
    {
        'slug': 'nike-dri-fit-sportswear-graphic-tee',
        'icon': 'tshirt',
        'color': '#18181B',
        'bg1': '#F4F4F5',
        'bg2': '#E4E4E7',
        'tag': "DRI-FIT",
        'sub': "Sweat-Wicking Tech • Signature Swoosh",
    },
    {
        'slug': 'zara-floral-print-tiered-midi-dress',
        'icon': 'dress',
        'color': '#E11D48',
        'bg1': '#FFF1F2',
        'bg2': '#FFE4E6',
        'tag': "FASHION",
        'sub': "Tiered Ruffle Silhouette • Botanical Print",
    },
    {
        'slug': 'zara-ribbed-knit-v-neck-summer-top',
        'icon': 'top',
        'color': '#475569',
        'bg1': '#F8FAFC',
        'bg2': '#F1F5F9',
        'tag': "KNITWEAR",
        'sub': "Soft Stretch Ribbed Cotton • V-Neckline",
    },
    {
        'slug': 'levis-kids-vintage-denim-trucker-jacket',
        'icon': 'trucker',
        'color': '#1D4ED8',
        'bg1': '#EFF6FF',
        'bg2': '#BFDBFE',
        'tag': "KIDS VINTAGE",
        'sub': "Classic Trucker • Heavy Brass Hardware",
    },
    {
        'slug': 'nike-air-zoom-pegasus-40-running-shoes',
        'icon': 'running_shoes',
        'color': '#0F172A',
        'bg1': '#F8FAFC',
        'bg2': '#E2E8F0',
        'tag': "ZOOM AIR",
        'sub': "Dual Air Cushioning • Breathable Mesh",
    },
    {
        'slug': 'puma-smash-v2-classic-leather-sneakers',
        'icon': 'sneakers',
        'color': '#1E3A8A',
        'bg1': '#FEFCE8',
        'bg2': '#FEF3C7',
        'tag': "ORIGINALS",
        'sub': "Clean Tennis Silhouette • SoftFoam+ Insole",
    },
    {
        'slug': 'loreal-paris-revitalift-hyaluronic-acid-serum',
        'icon': 'serum',
        'color': '#2563EB',
        'bg1': '#F0FDF4',
        'bg2': '#DCFCE7',
        'tag': "DERMATOLOGY",
        'sub': "1.5% Pure HA • Intensive Plumping Hydration",
    },
    {
        'slug': 'maybelline-superstay-matte-ink-liquid-lipstick',
        'icon': 'lipstick',
        'color': '#BE123C',
        'bg1': '#FFF1F2',
        'bg2': '#FCE7F3',
        'tag': "16HR WEAR",
        'sub': "Precision Arrow Wand • Ultra Saturated Matte",
    },
    {
        'slug': 'sony-wh-1000xm5-wireless-noise-cancelling-headphones',
        'icon': 'headphones',
        'color': '#0F172A',
        'bg1': '#F8FAFC',
        'bg2': '#E2E8F0',
        'tag': "NOISE CANCEL",
        'sub': "Dual Processor NC • 30-Hour Battery",
    },
    {
        'slug': 'boat-airdopes-141-true-wireless-earbuds',
        'icon': 'earbuds',
        'color': '#DC2626',
        'bg1': '#FEF2F2',
        'bg2': '#FEE2E2',
        'tag': "ASAP CHARGE",
        'sub': "42Hr Playback • ENx Voice Cancellation",
    },
    {
        'slug': 'samsung-galaxy-watch-6-bluetooth-44mm',
        'icon': 'smartwatch',
        'color': '#0284C7',
        'bg1': '#F0F9FF',
        'bg2': '#E0F2FE',
        'tag': "SMART TECH",
        'sub': "Sapphire Glass • BioActive Body Sensors",
    },
]

for cfg in PRODUCT_CONFIGS:
    product = Product.objects.filter(slug=cfg['slug']).first()
    if product:
        # 1. Main Product Image
        svg_bytes = make_product_svg(
            brand=product.brand.name if product.brand else "BrandBazaar",
            title=product.name[:32],
            subtitle=cfg['sub'],
            icon_type=cfg['icon'],
            main_color=cfg['color'],
            bg_start=cfg['bg1'],
            bg_end=cfg['bg2'],
            tag=cfg['tag']
        )
        filepath = os.path.join(MEDIA_ROOT, 'products', f"{product.slug}.svg")
        with open(filepath, 'wb') as f:
            f.write(svg_bytes)
        product.image = f"products/{product.slug}.svg"
        product.save()

        # 2. Attach Interactive Gallery Images for detail page thumbnail switcher
        # Angle 1: Detail View
        g1_svg = make_product_svg(
            brand=product.brand.name if product.brand else "BrandBazaar",
            title=f"{product.name[:25]} (Detail View)",
            subtitle="Close-Up Material & Build Texture",
            icon_type=cfg['icon'],
            main_color=cfg['color'],
            bg_start="#FFFFFF",
            bg_end=cfg['bg1'],
            tag="ZOOM DETAIL"
        )
        g1_path = os.path.join(MEDIA_ROOT, 'products', 'gallery', f"{product.slug}-detail.svg")
        with open(g1_path, 'wb') as f:
            f.write(g1_svg)
        
        ProductImage.objects.filter(product=product).delete()
        ProductImage.objects.create(
            product=product,
            image=f"products/gallery/{product.slug}-detail.svg",
            alt_text=f"{product.name} Detail View",
            order=1
        )

        # Angle 2: Packaging View
        g2_svg = make_product_svg(
            brand=product.brand.name if product.brand else "BrandBazaar",
            title=f"{product.name[:25]} (Packaging)",
            subtitle="Official Retail Sealed Box",
            icon_type=cfg['icon'],
            main_color="#475569",
            bg_start=cfg['bg2'],
            bg_end="#CBD5E1",
            tag="BOX PACK"
        )
        g2_path = os.path.join(MEDIA_ROOT, 'products', 'gallery', f"{product.slug}-box.svg")
        with open(g2_path, 'wb') as f:
            f.write(g2_svg)

        ProductImage.objects.create(
            product=product,
            image=f"products/gallery/{product.slug}-box.svg",
            alt_text=f"{product.name} Retail Packaging",
            order=2
        )

        print(f" -> Product image & 2 gallery angles attached for: {product.name}")

print("\nALL IMAGES AND LOGOS SUCCESSFULLY ATTACHED!")
