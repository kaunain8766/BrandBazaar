import os
import glob
import django
from PIL import Image, ImageDraw, ImageFont

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.catalog.models import Product

BRAIN_DIR = r"C:\Users\techno\.gemini\antigravity\brain\88d646cc-14a8-41b2-94b6-ac164cba42d4"
MEDIA_DIR = r"C:\Users\techno\Downloads\mybrandbazaar\media\products"

def add_product_name_banner(image_path, brand_name, product_name, output_path):
    try:
        img = Image.open(image_path).convert("RGBA")
        width, height = img.size

        overlay = Image.new("RGBA", (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)

        # Bottom banner with sleek modern styling
        banner_h = int(height * 0.15)
        banner_y = height - banner_h - 18
        margin = 18

        draw.rounded_rectangle(
            [(margin, banner_y), (width - margin, banner_y + banner_h)],
            radius=14,
            fill=(15, 23, 42, 220)  # Dark charcoal glassmorphism
        )

        try:
            font_brand = ImageFont.truetype("arialbd.ttf", int(banner_h * 0.22))
            font_title = ImageFont.truetype("arial.ttf", int(banner_h * 0.28))
        except Exception:
            font_brand = ImageFont.load_default()
            font_title = ImageFont.load_default()

        # Brand header tag
        draw.text((margin + 20, banner_y + 14), f"★ {brand_name.upper()} OFFICIAL", fill=(56, 189, 248, 255), font=font_brand)

        # Product name text
        title_text = product_name
        if len(title_text) > 42:
            title_text = title_text[:40] + "..."
        draw.text((margin + 20, banner_y + 38), title_text, fill=(255, 255, 255, 255), font=font_title)

        final_img = Image.alpha_composite(img, overlay).convert("RGB")
        final_img.save(output_path, "JPEG", quality=95)
        print(f"Applied banner: {output_path}")
        return True
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return False


def process_available_images():
    # Map product slugs to search patterns in the brain directory
    slug_patterns = {
        'levis-men-511-slim-fit-stretch-jeans': ('levis*511*', "Levi's", "Levi's Men 511 Slim Fit Stretch Jeans"),
        'levis-classic-western-denim-shirt': ('*western*denim*', "Levi's", "Levi's Classic Western Denim Shirt"),
        'allen-solly-men-solid-regular-fit-formal-shirt': ('*allen*solly*', "Allen Solly", "Allen Solly Men Solid Regular Fit Formal Shirt"),
        'nike-dri-fit-sportswear-graphic-tee': ('*nike*dri*fit*', "Nike", "Nike Dri-FIT Sportswear Graphic Training Tee"),
        'zara-floral-print-tiered-midi-dress': ('*zara*floral*', "Zara", "Zara Floral Print Tiered Midi Dress"),
        'zara-ribbed-knit-v-neck-summer-top': ('*zara*knit*', "Zara", "Zara Ribbed Knit V-Neck Summer Top"),
        'levis-kids-vintage-denim-trucker-jacket': ('*levis*kids*', "Levi's", "Levi's Kids Vintage Denim Trucker Jacket"),
        'nike-air-zoom-pegasus-40-running-shoes': ('*nike*pegasus*', "Nike", "Nike Air Zoom Pegasus 40 Running Shoes"),
        'puma-smash-v2-classic-leather-sneakers': ('*puma*smash*', "Puma", "Puma Smash v2 Classic Leather Sneakers"),
        'loreal-paris-revitalift-hyaluronic-acid-serum': ('*loreal*hyaluronic*', "L'Oréal Paris", "L'Oréal Paris Revitalift 1.5% HA Serum"),
        'maybelline-superstay-matte-ink-liquid-lipstick': ('*maybelline*matte*', "Maybelline", "Maybelline SuperStay Matte Ink Liquid Lipstick"),
        'sony-wh-1000xm5-wireless-noise-cancelling-headphones': ('*sony*wh*', "Sony", "Sony WH-1000XM5 Wireless Noise Cancelling Headphones"),
        'boat-airdopes-141-true-wireless-earbuds': ('*boat*airdopes*', "boAt", "boAt Airdopes 141 True Wireless Earbuds"),
        'samsung-galaxy-watch-6-bluetooth-44mm': ('*samsung*watch*', "Samsung", "Samsung Galaxy Watch 6 Bluetooth (44mm)"),
    }

    for slug, (pattern, brand, full_name) in slug_patterns.items():
        matches = glob.glob(os.path.join(BRAIN_DIR, pattern + ".jpg")) + glob.glob(os.path.join(BRAIN_DIR, pattern + ".png"))
        if matches:
            latest_match = max(matches, key=os.path.getmtime)
            out_path = os.path.join(MEDIA_DIR, f"{slug}.jpg")
            if add_product_name_banner(latest_match, brand, full_name, out_path):
                prod = Product.objects.filter(slug=slug).first()
                if prod:
                    prod.image = f"products/{slug}.jpg"
                    prod.save()
                    print(f" -> DB Updated for: {prod.name}")

if __name__ == "__main__":
    process_available_images()
