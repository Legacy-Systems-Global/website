import './style.css'

// Size the wordmark so it spans the full column width.
const wrap = document.getElementById('wordmark-wrap')
const mark = document.getElementById('wordmark')

function fit() {
  mark.style.fontSize = '100px'
  // Trailing letter-spacing (.1em = 10px at 100px) shouldn't count toward the width.
  const textWidth = mark.getBoundingClientRect().width - 10
  const available = wrap.clientWidth
  if (!textWidth || !available) return
  mark.style.fontSize = Math.max(14, Math.floor((1000 * available) / textWidth) / 10) + 'px'
}

new ResizeObserver(fit).observe(wrap)
document.fonts?.ready.then(fit)
fit()
