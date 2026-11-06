const $ = id => document.getElementById(id)
const read = key => { try { return sessionStorage.getItem(key) } catch { return null } }
const write = (key, value) => { try { sessionStorage.setItem(key, value) } catch { /* Optional session memory. */ } }
const homes = { public: 'index.html', investors: 'investors.html', associates: 'employees.html' }
const labels = { public: 'General Public', investors: 'Investors', associates: 'Associates' }
const file = location.pathname.split('/').pop() || 'index.html'
const investorPages = ['investors.html', 'annual-report.html', 'annual-reports.html', 'capital-allocation.html', 'investor-relations.html']
const associatePages = ['employees.html','employee-create.html','employee-sign-in.html','employee-dashboard.html','legacy-match.html','legacy-store.html','handbook.html','hours-ledger.html','wellness.html','peer-observations.html']
let audience = read('legacy-audience') || 'public'
if (investorPages.includes(file)) audience = 'investors'
else if (associatePages.includes(file)) audience = 'associates'
else if (file === 'index.html') audience = 'public'
if (!homes[audience]) audience = 'public'
write('legacy-audience', audience)
let investorStatus = read('legacy-investor-status')
if (!['accredited','intending'].includes(investorStatus)) investorStatus = null
let investorDestination = null
let pendingAudience = audience
const audiencePanel = $('audience-panel')
const menu = $('site-menu')

function updateHeader() {
  document.body.dataset.audience = audience
  $('audience-label').textContent = labels[audience]
  $('investor-chip').hidden = audience !== 'investors'
  $('investor-chip').textContent = investorStatus === 'accredited' ? 'Accredited investor ↗' : investorStatus === 'intending' ? 'Intending investor ↗' : 'Confirm status ↗'
  for (const a of document.querySelectorAll('[data-audience-home]')) a.href = homes[audience]
  for (const a of document.querySelectorAll('[data-investor-nav]')) a.hidden = audience !== 'investors'
  for (const a of document.querySelectorAll('[data-associate-nav]')) a.hidden = audience !== 'associates'
  const radio = document.querySelector(`input[name="audience"][value="${audience}"]`)
  if (radio) radio.checked = true
}
function closeAudience(focus = false) {
  audiencePanel.hidden = true
  $('audience-toggle').setAttribute('aria-expanded', 'false')
  if (focus) $('audience-toggle').focus()
}
function closeMenu(focus = false) {
  menu.hidden = true
  $('menu-toggle').setAttribute('aria-expanded','false')
  if (focus) $('menu-toggle').focus()
}
$('audience-toggle').addEventListener('click', () => {
  const opening = audiencePanel.hidden
  closeMenu()
  closeAudience()
  if (opening) {
    pendingAudience = audience
    updateHeader()
    audiencePanel.hidden = false
    $('audience-toggle').setAttribute('aria-expanded','true')
    document.querySelector('input[name="audience"]:checked').focus()
  }
})
$('audience-close').addEventListener('click', () => closeAudience(true))
$('menu-toggle').addEventListener('click', () => {
  const opening = menu.hidden
  closeAudience()
  menu.hidden = !opening
  $('menu-toggle').setAttribute('aria-expanded',String(opening))
  if (opening) menu.querySelector('a').focus()
})
for (const input of document.querySelectorAll('input[name="audience"]')) input.addEventListener('change', () => { pendingAudience = input.value })
function showDialog(id) {
  closeAudience(); closeMenu()
  for (const open of document.querySelectorAll('dialog[open]')) open.close()
  const dialog = $(id)
  if (id === 'newsletter-dialog') {
    write(`legacy-newsletter-shown-${audience}`, 'yes')
    document.querySelector(`input[name="newsletter"][value="${audience}"]`).checked = true
  }
  dialog.showModal()
}
for (const button of document.querySelectorAll('[data-open]')) button.addEventListener('click', () => showDialog(button.dataset.open))
for (const button of document.querySelectorAll('[data-close]')) button.addEventListener('click', () => button.closest('dialog').close())
for (const dialog of document.querySelectorAll('dialog')) {
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return
    const rect = dialog.getBoundingClientRect()
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close()
  })
  dialog.addEventListener('close', () => { if (dialog.id === 'phone-dialog') window.speechSynthesis?.cancel() })
}
document.addEventListener('keydown', event => {
  if (event.key === 'Escape') { if (!audiencePanel.hidden) closeAudience(true); if (!menu.hidden) closeMenu(true) }
})
document.addEventListener('click', event => { if (!event.target.closest('.experience-header')) { closeAudience(); closeMenu() } })
function prepareInvestor(destination = null) {
  investorDestination = destination
  $('investor-acknowledge').checked = false
  $('investor-accept').disabled = true
  document.querySelector(`input[name="investor-status"][value="${investorStatus || 'accredited'}"]`).checked = true
  showDialog('investor-dialog')
}
$('audience-continue').addEventListener('click', () => {
  if (pendingAudience === 'investors') prepareInvestor(homes.investors)
  else {
    audience = pendingAudience
    write('legacy-audience',audience)
    location.href = homes[audience]
  }
})
$('investor-chip').addEventListener('click', () => prepareInvestor())
$('investor-acknowledge').addEventListener('change', event => { $('investor-accept').disabled = !event.target.checked })
$('investor-accept').addEventListener('click', () => {
  if (!$('investor-acknowledge').checked) return
  investorStatus = document.querySelector('input[name="investor-status"]:checked').value
  write('legacy-investor-status',investorStatus)
  audience = 'investors'; write('legacy-audience',audience)
  $('investor-dialog').close(); updateHeader()
  if (investorDestination) location.href = investorDestination
})
$('investor-decline').addEventListener('click', () => {
  $('investor-dialog').close()
  if (file === 'investors.html' && !investorStatus) { write('legacy-audience','public'); location.href = homes.public }
})
updateHeader()
if (file === 'investors.html' && !investorStatus) prepareInvestor()

// Independent system preference banner. Choices affect only this browser tab.
let preference = read('legacy-opportunity')
const gpc = navigator.globalPrivacyControl === true
const preferenceBanner = $('system-preference-banner')
$('signal-label').title = gpc ? 'GPC signal detected; your browser privacy signal remains respected.' : ''
if (gpc && !preference) preference = 'out'
function updatePreference() {
  $('opportunity-status').textContent = preference ? `You have opted ${preference}.` : ''
}
function revealPreference() {
  closeMenu(); closeAudience()
  preferenceBanner.hidden = false
}
function choosePreference(value) {
  preference = value
  write('legacy-opportunity',preference)
  updatePreference()
  preferenceBanner.hidden = true
}
updatePreference()
preferenceBanner.hidden = Boolean(preference || read('legacy-preference-dismissed'))
for (const button of document.querySelectorAll('[data-preferences]')) button.addEventListener('click', revealPreference)
$('preference-dismiss').addEventListener('click', () => {
  preferenceBanner.hidden = true
  write('legacy-preference-dismissed','yes')
})
for (const button of document.querySelectorAll('[data-opportunity]')) button.addEventListener('click', () => choosePreference(button.dataset.opportunity))
for (const input of document.querySelectorAll('[name="signup-opportunity"]')) input.addEventListener('change', () => choosePreference(input.value))

// Newsletter invitation is independent of preferences: five seconds, once per audience per tab.
const newsletterVisitKey = `legacy-newsletter-shown-${audience}`
let newsletterTimer
function inviteNewsletter() {
  if (read(newsletterVisitKey)) return
  const focused = document.activeElement
  if (document.querySelector('dialog[open]') || !audiencePanel.hidden || !menu.hidden || ['INPUT','TEXTAREA','SELECT'].includes(focused?.tagName)) {
    newsletterTimer = setTimeout(inviteNewsletter, 500)
    return
  }
  write(newsletterVisitKey,'yes')
  showDialog('newsletter-dialog')
}
newsletterTimer = setTimeout(inviteNewsletter, 5000)
window.addEventListener('pagehide', () => clearTimeout(newsletterTimer))
const editions = { public:'The Continuity Letter', investors:'The Perpetuity Report', associates:'Family Correspondence' }
$('newsletter-form').addEventListener('submit', event => {
  event.preventDefault()
  const edition = new FormData(event.currentTarget).get('newsletter')
  $('newsletter-edition').textContent = `${editions[edition]}. The system looks forward to keeping you informed.`
  event.currentTarget.reset(); event.currentTarget.hidden = true
  $('newsletter-confirmation').hidden = false
})
$('newsletter-again').addEventListener('click', () => { $('newsletter-confirmation').hidden = true; $('newsletter-form').hidden = false })

// One question per step; answers remain in the DOM only and are discarded on submission.
const quiz = $('assessment')
if (quiz) {
  const steps = [...quiz.querySelectorAll('.quiz-step')]
  let step = 0
  function showStep() {
    steps.forEach((element, i) => { element.hidden = i !== step })
    $('assessment-step-label').textContent = `Question ${step + 1} of ${steps.length}`
    $('assessment-progress').value = step + 1
    $('assessment-next').textContent = step === steps.length - 1 ? 'Review responses →' : 'Continue →'
    $('assessment-error').textContent = ''
    const legend = steps[step].querySelector('legend'); legend.tabIndex = -1; legend.focus({ preventScroll:true })
  }
  $('assessment-begin').addEventListener('click', () => { $('assessment-intro').hidden = true; quiz.hidden = false; showStep() })
  $('assessment-back').addEventListener('click', () => {
    if (step) { step--; showStep() }
    else { quiz.hidden = true; $('assessment-intro').hidden = false; $('assessment-begin').focus() }
  })
  $('assessment-next').addEventListener('click', () => {
    if (!steps[step].querySelector('input:checked')) { $('assessment-error').textContent = 'Please select a response to continue.'; return }
    if (step < steps.length - 1) { step++; showStep() }
    else { quiz.hidden = true; $('assessment-review').hidden = false; $('assessment-review').tabIndex = -1; $('assessment-review').focus() }
  })
  quiz.addEventListener('submit', event => { event.preventDefault(); $('assessment-next').click() })
  $('assessment-edit').addEventListener('click', () => { $('assessment-review').hidden = true; quiz.hidden = false; step = 0; showStep() })
  $('assessment-submit').addEventListener('click', () => {
    $('assessment-review').hidden = true; $('assessment-processing').hidden = false; quiz.reset()
    setTimeout(() => { location.href = 'legacy-store.html' }, 1000)
  })
}

const phoneCopy = {
  '1': 'Investor Relations. Our horizon is indefinite. Please leave a message with your name and intended holding period. A representative will respond when the quarter is ready.',
  '2': 'General inquiries. You have reached the Office of Correspondence. Your inquiry will be held with the same care as our other assets. Please leave a message.',
  '3': 'Welcome home to the Legacy family. For your convenience, your place in the queue is permanent. Please leave your associate ID and a brief message.',
  '0': 'All of our operators are currently committed. Please remain. Alternatively, leave a message. Either will be noted.'
}
function speak(text) {
  if (!window.speechSynthesis) { $('phone-listen').textContent = 'Audio unavailable — read the greeting above'; return }
  speechSynthesis.cancel()
  const utterance = new SpeechSynthesisUtterance(text)
  utterance.rate = 0.86
  speechSynthesis.speak(utterance)
}
$('phone-listen').addEventListener('click', () => speak($('phone-transcript').textContent))
for (const key of document.querySelectorAll('[data-phone]')) key.addEventListener('click', () => {
  $('phone-transcript').textContent = phoneCopy[key.dataset.phone]
  $('voicemail-form').hidden = false
})
$('voicemail-open').addEventListener('click', () => { $('voicemail-form').hidden = false; $('voicemail-form').querySelector('textarea').focus() })
$('voicemail-form').addEventListener('submit', event => {
  event.preventDefault(); event.currentTarget.reset(); event.currentTarget.hidden = true
  $('voicemail-status').textContent = 'Your message has entered the queue. Demonstration only: nothing was recorded or delivered.'
})
