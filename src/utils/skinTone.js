/**
 * Simple skin-tone brightness detection + color recommendation.
 *
 * This is deliberately simple, as requested: it samples pixels from
 * the center of the photo (a reasonable stand-in for "where the face
 * usually is" without pulling in a face-detection model), averages
 * their brightness, and buckets the result into three tone
 * categories. Each category maps to a general rule about which kinds
 * of colors tend to read as "flattering" (a mix of contrast and
 * warmth), and that rule is used to rank the product's actual
 * available colors — so the recommendation always comes from colors
 * the product really offers, never an invented one.
 *
 * Swap this out for a real ML model later; the function signatures
 * are the seam to do that without touching the UI.
 */

/**
 * Draws an image element to an offscreen canvas and samples a center
 * crop to approximate average skin brightness/tone.
 * @param {HTMLImageElement} imageEl
 * @returns {{ r: number, g: number, b: number, brightness: number }}
 */
export function sampleImageTone(imageEl) {
  const canvas = document.createElement('canvas')
  const w = (canvas.width = 100)
  const h = (canvas.height = 100)
  const ctx = canvas.getContext('2d')

  // Draw the image scaled into a 100x100 square so sampling is cheap
  // and consistent regardless of the original photo's resolution.
  ctx.drawImage(imageEl, 0, 0, w, h)

  // Sample a center box (roughly where a face is if the photo is a
  // reasonably framed portrait/selfie).
  const boxSize = 40
  const startX = (w - boxSize) / 2
  const startY = (h - boxSize) / 2
  const { data } = ctx.getImageData(startX, startY, boxSize, boxSize)

  let r = 0, g = 0, b = 0, count = 0
  for (let i = 0; i < data.length; i += 4) {
    r += data[i]
    g += data[i + 1]
    b += data[i + 2]
    count++
  }
  r = Math.round(r / count)
  g = Math.round(g / count)
  b = Math.round(b / count)

  // Standard perceived-luminance formula
  const brightness = Math.round(0.299 * r + 0.587 * g + 0.114 * b)

  return { r, g, b, brightness }
}

/**
 * Buckets a brightness value (0-255) into a tone category.
 */
export function classifyTone(brightness) {
  if (brightness >= 180) return { key: 'light', label: 'Light' }
  if (brightness >= 120) return { key: 'medium', label: 'Medium' }
  return { key: 'deep', label: 'Deep' }
}

function hexToRgb(hex) {
  const clean = hex.replace('#', '')
  const bigint = parseInt(clean, 16)
  return {
    r: (bigint >> 16) & 255,
    g: (bigint >> 8) & 255,
    b: bigint & 255,
  }
}

function relativeBrightness({ r, g, b }) {
  return 0.299 * r + 0.587 * g + 0.114 * b
}

/**
 * Ranks a list of hex colors by how "flattering" they are for a given
 * tone category, using a simple brightness-contrast heuristic: score
 * each color by how well its contrast against the detected skin
 * brightness matches the ideal contrast for that tone category.
 *  - Light/medium skin tones: colors a bit darker than the skin tend
 *    to read as grounded rather than washed out.
 *  - Deep skin tones: colors a bit brighter than the skin tend to
 *    pop rather than blend in.
 * @param {string} toneKey - 'light' | 'medium' | 'deep'
 * @param {number} skinBrightness - 0-255 brightness from sampleImageTone
 * @param {string[]} availableColors - hex colors from the product
 * @returns {string[]} colors sorted best-match first
 */
export function rankColorsForTone(toneKey, skinBrightness, availableColors) {
  const idealDelta = { light: 90, medium: 60, deep: 90 }[toneKey] ?? 70
  // For light/medium tones we generally want the color darker than skin
  // (positive delta = skin brighter than color). For deep tones, a color
  // brighter than skin tends to pop more flatteringly.
  const direction = toneKey === 'deep' ? -1 : 1

  return [...availableColors]
    .map((hex) => {
      const brightness = relativeBrightness(hexToRgb(hex))
      const actualDelta = direction * (skinBrightness - brightness)
      const distanceFromIdeal = Math.abs(actualDelta - idealDelta)
      return { hex, distanceFromIdeal }
    })
    .sort((a, b) => a.distanceFromIdeal - b.distanceFromIdeal)
    .map((entry) => entry.hex)
}
