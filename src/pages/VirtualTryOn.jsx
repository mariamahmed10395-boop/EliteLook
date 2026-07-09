import React, { useEffect, useRef, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { useAppContext } from '../context/AppContext.jsx'
import { sampleImageTone, classifyTone, rankColorsForTone } from '../utils/skinTone.js'

export default function VirtualTryOn() {
  const { productId } = useParams()
  const { products, cartItem } = useAppContext()
  const product = products.find((p) => p.id === productId) || cartItem?.product

  const [photoSrc, setPhotoSrc] = useState(null)
  const [cameraOn, setCameraOn] = useState(false)
  const [selectedColor, setSelectedColor] = useState(cartItem?.color || product?.colors?.[0])
  const [toneResult, setToneResult] = useState(null) // { label, recommended: [] }
  const [analyzing, setAnalyzing] = useState(false)
  const [cameraError, setCameraError] = useState('')

  const videoRef = useRef(null)
  const streamRef = useRef(null)
  const hiddenImgRef = useRef(null)

  // Always stop the camera stream when leaving the page or turning it off
  useEffect(() => {
    return () => stopCamera()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  if (!product) {
    return (
      <div className="container" style={{ padding: '48px 0', textAlign: 'center' }}>
        <h2>We couldn't find that product</h2>
        <Link to="/" className="btn btn-primary" style={{ marginTop: 16 }}>
          Back to shop
        </Link>
      </div>
    )
  }

  function stopCamera() {
    streamRef.current?.getTracks().forEach((track) => track.stop())
    streamRef.current = null
    setCameraOn(false)
  }

  async function startCamera() {
    setCameraError('')
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' } })
      streamRef.current = stream
      setCameraOn(true)
      // Video element mounts this render pass; attach the stream right after.
      requestAnimationFrame(() => {
        if (videoRef.current) videoRef.current.srcObject = stream
      })
    } catch (err) {
      setCameraError('Could not access the camera. Check your browser permissions.')
    }
  }

  function capturePhoto() {
    const video = videoRef.current
    if (!video) return
    const canvas = document.createElement('canvas')
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight
    canvas.getContext('2d').drawImage(video, 0, 0)
    setPhotoSrc(canvas.toDataURL('image/png'))
    setToneResult(null)
    stopCamera()
  }

  function handleFileUpload(e) {
    const file = e.target.files?.[0]
    if (!file) return
    const reader = new FileReader()
    reader.onload = () => {
      setPhotoSrc(reader.result)
      setToneResult(null)
    }
    reader.readAsDataURL(file)
  }

  function handleAnalyzeTone() {
    if (!photoSrc || !hiddenImgRef.current) return
    setAnalyzing(true)

    // Run on the next tick so the hidden <img> has definitely painted
    // its latest src before we read pixels from it.
    setTimeout(() => {
      try {
        const { brightness } = sampleImageTone(hiddenImgRef.current)
        const tone = classifyTone(brightness)
        const recommended = rankColorsForTone(tone.key, brightness, product.colors)
        setToneResult({ tone, recommended })
      } catch (err) {
        setToneResult({ error: true })
      }
      setAnalyzing(false)
    }, 50)
  }

  return (
    <div className="tryon-wrap">
      <div className="container">
        <h2 style={{ marginBottom: 6 }}>Virtual try-on</h2>
        <p style={{ color: 'var(--ink-soft)', marginBottom: 24 }}>
          {product.name} — see it on you before you order.
        </p>

        <div className="tryon-grid">
          {/* LEFT: photo stage */}
          <div className="tryon-stage">
            <div className="photo-frame">
              {cameraOn && (
                <video ref={videoRef} autoPlay playsInline muted />
              )}

              {!cameraOn && photoSrc && (
                <>
                  <img src={photoSrc} alt="Your photo" className="photo-base" />
                  {/* Simple overlay: the garment image placed roughly over
                      the torso area. This is intentionally simple (no pose
                      detection) per the brief — swap for real garment
                      warping/segmentation later. */}
                  <img
                    src={`/${product.image}`}
                    alt=""
                    className="overlay-garment"
                    onError={(e) => { e.target.style.display = 'none' }}
                  />
                </>
              )}

              {!cameraOn && !photoSrc && (
                <div className="photo-empty">
                  <span style={{ fontSize: '1.6rem' }}>📷</span>
                  <span>Upload a photo or open your camera to try this on</span>
                </div>
              )}
            </div>

            {cameraError && (
              <p style={{ color: '#8C1F28', fontSize: '0.85rem' }}>{cameraError}</p>
            )}

            <div className="photo-actions">
              {cameraOn ? (
                <>
                  <button className="btn btn-primary" onClick={capturePhoto}>
                    Take photo
                  </button>
                  <button className="btn btn-outline" style={{ color: 'var(--ink)' }} onClick={stopCamera}>
                    Cancel
                  </button>
                </>
              ) : (
                <>
                  <label className="btn btn-ghost" style={{ margin: 0 }}>
                    Upload photo
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleFileUpload}
                      style={{ display: 'none' }}
                    />
                  </label>
                  <button className="btn btn-primary" onClick={startCamera}>
                    Open camera
                  </button>
                </>
              )}
            </div>

            {/* Hidden image used only for pixel sampling during tone
                analysis — never shown, kept in sync with photoSrc. */}
            {photoSrc && (
              <img
                ref={hiddenImgRef}
                src={photoSrc}
                alt=""
                crossOrigin="anonymous"
                style={{ display: 'none' }}
              />
            )}
          </div>

          {/* RIGHT: color choice + recommendation */}
          <div className="tone-panel">
            <h3>Choose a color</h3>
            <div className="swatch-row" style={{ marginBottom: 18 }}>
              {product.colors.map((color) => (
                <button
                  key={color}
                  type="button"
                  className={`swatch${selectedColor === color ? ' selected' : ''}`}
                  style={{ background: color, width: 28, height: 28 }}
                  onClick={() => setSelectedColor(color)}
                  aria-label={`Color ${color}`}
                />
              ))}
            </div>

            <div className="divider-label">or</div>

            <button
              type="button"
              className="btn btn-accent btn-block"
              disabled={!photoSrc || analyzing}
              onClick={handleAnalyzeTone}
              style={{ marginTop: 12 }}
            >
              {analyzing ? 'Analyzing…' : "I'm not sure which color suits me"}
            </button>

            {!photoSrc && (
              <p style={{ fontSize: '0.78rem', color: 'var(--ink-soft)', marginTop: 8 }}>
                Add a photo first so we can take a look.
              </p>
            )}

            {toneResult && !toneResult.error && (
              <div className="tone-result">
                <strong>Detected tone: {toneResult.tone.label}</strong>
                <p style={{ marginTop: 6, color: 'var(--ink-soft)' }}>
                  Based on your photo, these available colors tend to be the most flattering:
                </p>
                <div className="tone-swatches">
                  {toneResult.recommended.map((color, i) => (
                    <div key={color} className="tone-swatch-item">
                      <button
                        type="button"
                        className={`swatch${selectedColor === color ? ' selected' : ''}`}
                        style={{ background: color }}
                        onClick={() => setSelectedColor(color)}
                        aria-label={`Recommended color ${color}`}
                      />
                      {i === 0 ? 'Best match' : `#${i + 1}`}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {toneResult?.error && (
              <p style={{ color: '#8C1F28', fontSize: '0.85rem', marginTop: 10 }}>
                Couldn't analyze that photo — try a clearer, well-lit shot.
              </p>
            )}

            <Link
              to="/cart"
              className="btn btn-primary btn-block"
              style={{ marginTop: 24 }}
            >
              Back to order
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}
