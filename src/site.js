import products from './products.json'

for (const form of document.querySelectorAll('[data-demo-form]')) {
  form.addEventListener('submit', event => {
    event.preventDefault()
    if (form.dataset.demoForm === 'signin') location.href = 'employee-dashboard.html'
    else {
      form.reset()
      form.hidden = true
      const confirmation = document.getElementById('account-confirmation')
      confirmation.hidden = false
      confirmation.tabIndex = -1
      confirmation.focus()
    }
  })
}
const date = document.getElementById('start-date')
if (date) {
  const today = new Date()
  date.value = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`
}
const cart = new Map()
const cartItems = document.getElementById('cart-items')
function renderCart() {
  const count = [...cart.values()].reduce((sum, quantity) => sum + quantity, 0)
  document.getElementById('cart-count').textContent = count
  const checkout = document.getElementById('checkout')
  checkout.disabled = !count
  cartItems.replaceChildren()
  let knownTotal = 0
  let hasIssued = false
  for (const [index, quantity] of cart) {
    const product = products[index]
    const row = document.createElement('div')
    row.className = 'cart-row'
    const name = document.createElement('span')
    name.textContent = `${product.name} × ${quantity} · ${product.price}`
    const remove = document.createElement('button')
    remove.textContent = 'Remove'
    remove.setAttribute('aria-label', `Remove ${product.name}`)
    remove.addEventListener('click', () => { cart.delete(index); renderCart() })
    row.append(name, remove)
    cartItems.append(row)
    if (product.price.startsWith('$')) knownTotal += Number(product.price.slice(1)) * quantity
    else if (product.price === 'Payroll deducted') hasIssued = true
  }
  if (!count) {
    const empty = document.createElement('p')
    empty.textContent = 'Your cart is empty. Your uniform order is not.'
    cartItems.append(empty)
  }
  document.getElementById('cart-total').textContent = count ? `Priced items: $${knownTotal.toFixed(2)}${hasIssued ? ' · Issued uniform deductions are unspecified.' : ''}` : ''
}
if (cartItems) {
  for (const button of document.querySelectorAll('[data-add]')) {
    button.addEventListener('click', () => {
      const index = Number(button.dataset.add)
      cart.set(index, (cart.get(index) || 0) + 1)
      document.getElementById('order-confirmation').hidden = true
      renderCart()
    })
  }
  document.getElementById('store-category').addEventListener('change', event => {
    for (const product of document.querySelectorAll('.product')) {
      product.hidden = event.target.value !== 'all' && product.dataset.category !== event.target.value
    }
  })
  document.getElementById('checkout').addEventListener('click', () => {
    if (!cart.size) return
    cart.clear()
    renderCart()
    const confirmation = document.getElementById('order-confirmation')
    confirmation.hidden = false
    confirmation.tabIndex = -1
    confirmation.focus()
  })
}
document.getElementById('print-report')?.addEventListener('click', () => window.print())
