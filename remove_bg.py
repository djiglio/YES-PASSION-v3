import numpy as np
from PIL import Image

img = Image.open(r"C:\Users\Edoardo\.gemini\antigravity\brain\8fd26d1c-1b62-4003-bc5e-bc6f518ba2f9\media__1782558279542.png").convert("RGBA")
data = np.array(img)

r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]

# Calculate brightness as the max of R, G, B
brightness = np.maximum(np.maximum(r, g), b)

# Threshold for what we consider "black" or "shadow"
# Let's use 35 to ensure dark gray metallic parts aren't completely removed,
# but the pure black background and shadows fade smoothly.
threshold = 35
mask = brightness < threshold

# Apply linear transparency for dark pixels
new_alpha = (brightness[mask] / float(threshold)) * 255
a[mask] = new_alpha.astype(np.uint8)

new_data = np.stack((r, g, b, a), axis=-1)
new_img = Image.fromarray(new_data)
new_img.save("assets/logo.png", "PNG")
print("Done!")
