import { useEffect, useState } from 'react';

function BackgroundLayout({ image, children }) {
  const [imageLoaded, setImageLoaded] = useState(false);

  useEffect(() => {
    if (!image) {
      setImageLoaded(true);
      return;
    }
    const img = new window.Image();
    img.src = image;
    img.onload = () => setImageLoaded(true);
    img.onerror = () => setImageLoaded(true);
  }, [image]);

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      width: '100vw',
      height: '100vh',
    }}>
      {/* Background image */}
      {image && (
        <div
          style={{
            position: 'absolute',
            inset: 0,
            backgroundImage: `url(${image})`,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            backgroundRepeat: 'no-repeat',
            opacity: imageLoaded ? 1 : 0,
            transition: 'opacity 500ms ease-in-out',
            zIndex: 0,
            pointerEvents: 'none',
          }}
        />
      )}

      {/* Dark gradient overlay — non-interactive */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background: 'linear-gradient(135deg, rgba(15,12,41,0.80) 0%, rgba(48,43,99,0.85) 50%, rgba(36,36,62,0.80) 100%)',
          zIndex: 1,
          pointerEvents: 'none',
        }}
      />

      {/* Scrollable content — on top, fully interactive */}
      <div
        style={{
          position: 'relative',
          zIndex: 2,
          width: '100%',
          height: '100%',
          overflowY: 'auto',
        }}
      >
        {children}
      </div>
    </div>
  );
}

export default BackgroundLayout;
