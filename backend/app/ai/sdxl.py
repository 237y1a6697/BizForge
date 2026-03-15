def generate_logo(prompt: str) -> str:
    """Generate a unique inline SVG logo based on the prompt."""
    import hashlib
    from urllib.parse import quote

    h = hashlib.md5(prompt.encode()).hexdigest()
    n = int(h, 16)

    # --- Colour palettes ---
    palettes = [
        ("#6C63FF", "#a78bfa", "#ede9fe"),  # violet
        ("#ff3d81", "#fb7185", "#ffe4e6"),  # pink
        ("#00c6ff", "#38bdf8", "#e0f2fe"),  # cyan
        ("#f97316", "#fbbf24", "#fff7ed"),  # amber-orange
        ("#10b981", "#34d399", "#ecfdf5"),  # emerald
        ("#e879f9", "#c084fc", "#fdf4ff"),  # purple
        ("#0ea5e9", "#6366f1", "#eff6ff"),  # blue-indigo
        ("#f43f5e", "#fb923c", "#fff1f2"),  # rose-orange
    ]
    c1, c2, bg = palettes[n % len(palettes)]

    # --- Pick a letter from the prompt ---
    words = [w for w in prompt.strip().split() if w.isalpha()]
    letter = (words[0][0] if words else prompt[0]).upper()

    # --- Decorative icon paths (mini SVG symbols) ---
    icons = [
        # lightning bolt
        "M17 2L7 13h8l-2 9 10-11h-8z",
        # star
        "M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z",
        # diamond
        "M12 2l6 8H6z M12 22l-6-8h12z",
        # rocket
        "M12 2c0 0-5 4-5 10h10C17 6 12 2 12 2zM9 14v6h6v-6",
        # leaf
        "M17 8C8 10 5 16 5 22 5 22 12 18 14 11c0 0 3 3 2 9 4-4 5-9 4-14z",
        # infinity / loop
        "M12 12c-2-2.5-4-4-6-4a4 4 0 000 8c2 0 4-1.5 6-4zm0 0c2 2.5 4 4 6 4a4 4 0 000-8c-2 0-4 1.5-6 4z",
        # hexagon
        "M12 2l8.66 5v10L12 22l-8.66-5V7z",
        # shield
        "M12 2L4 5v6c0 5.25 3.5 10.15 8 11.5C16.5 21.15 20 16.25 20 11V5z",
    ]
    icon_path = icons[n % len(icons)]

    # --- Outer shape clip (circle vs rounded-rect) ---
    shapes = ["circle", "roundrect", "hexclip"]
    shape = shapes[n % len(shapes)]

    if shape == "circle":
        clip_def = '<clipPath id="cl"><circle cx="150" cy="150" r="130"/></clipPath>'
        bg_shape = '<circle cx="150" cy="150" r="130" fill="url(#grad)"/>'
        border = '<circle cx="150" cy="150" r="128" fill="none" stroke="white" stroke-width="4" opacity="0.3"/>'
    elif shape == "roundrect":
        clip_def = '<clipPath id="cl"><rect x="20" y="20" width="260" height="260" rx="60"/></clipPath>'
        bg_shape = '<rect x="20" y="20" width="260" height="260" rx="60" fill="url(#grad)"/>'
        border = '<rect x="22" y="22" width="256" height="256" rx="58" fill="none" stroke="white" stroke-width="4" opacity="0.3"/>'
    else:
        clip_def = '<clipPath id="cl"><polygon points="150,20 276,85 276,215 150,280 24,215 24,85"/></clipPath>'
        bg_shape = '<polygon points="150,20 276,85 276,215 150,280 24,215 24,85" fill="url(#grad)"/>'
        border = '<polygon points="150,24 272,87 272,213 150,276 28,213 28,87" fill="none" stroke="white" stroke-width="4" opacity="0.3"/>'

    # Decorative circle accents
    acc_x1, acc_y1 = 60 + (n % 40), 60 + ((n >> 4) % 40)
    acc_x2, acc_y2 = 200 + (n % 30), 200 + ((n >> 8) % 30)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="300" height="300" viewBox="0 0 300 300">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{c1}"/>
      <stop offset="100%" stop-color="{c2}"/>
    </linearGradient>
    {clip_def}
  </defs>
  {bg_shape}
  {border}
  <!-- decorative circles -->
  <circle cx="{acc_x1}" cy="{acc_y1}" r="40" fill="white" opacity="0.08"/>
  <circle cx="{acc_x2}" cy="{acc_y2}" r="55" fill="white" opacity="0.06"/>
  <!-- icon -->
  <g transform="translate(105,75) scale(1.7)" fill="white" opacity="0.22">
    <path d="{icon_path}"/>
  </g>
  <!-- letter -->
  <text x="150" y="185" text-anchor="middle" font-family="'Segoe UI',Arial,sans-serif"
        font-size="100" font-weight="800" fill="white" opacity="0.95"
        letter-spacing="-3">{letter}</text>
</svg>"""

    encoded = quote(svg)
    return f"data:image/svg+xml,{encoded}"