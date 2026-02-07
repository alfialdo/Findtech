THEME = {
    "primary": "#A0C4FF",  # Soft Blue
    "secondary": "#B9FBC0",  # Mint Green
    "accent": "#FFD6A5",  # Pastel Orange
    "background": "#FDFFB6",  # Pale Yellow
    "text": "#2C3E50",
}

# Data Lists
BRANDS = [
    "acer",
    "asus",
    "dell",
    "hp",
    "lenovo",
    "msi",
    "microsoft",
    "apple",
    "samsung",
    "gigabyte",
]

BRAND_LOGO = {brand: f"assets/brands/{brand}.png" for brand in BRANDS}

USAGE_TYPES = ["Personal", "Business", "Gaming", "Content Design", "Academy"]

SCREEN_SIZES = {
    "Less than 13 inch (Compact)": 0.33,
    "14-16 inch (Standard)": 0.66,
    "17+ inch (Large)": 0.99,
}

EXTRAS = ["Webcam", "Thunderbolt", "Backlit Keyboard", "Card Reader", "Touchscreen"]
