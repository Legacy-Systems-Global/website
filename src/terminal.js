// Browser-only simulation. Commands never execute against the host machine.
const output = document.getElementById('terminal-output')
const form = document.getElementById('command-form')
const input = document.getElementById('command-input')
const prompt = document.getElementById('prompt')
const directories = {
  ROOT: { path:'C:\\LEGACY', page:'operating-system.html' },
  LEDGER: { path:'C:\\LEGACY\\LEDGER', page:'system-ledger.html' },
  SUBS: { path:'C:\\LEGACY\\SUBS', page:'system-subsidiaries.html' },
  INTAKE: { path:'C:\\LEGACY\\INTAKE', page:'system-intake.html' },
  IC9000: { path:'C:\\LEGACY\\IC9000', page:'system-ic9000.html' },
  '1987': { path:'C:\\LEGACY\\1987', page:'system-1987.html' },
}
const companies = [
  ['MCP.EXE','Mind Control Press','mind-control-press.html'],
  ['SPV.EXE','Special Purpose Vehicles','special-purpose-vehicles.html'],
  ['LIQUID.EXE','Liquidity Events','liquidity-events.html'],
  ['FRONT.EXE','Front Running','front-running.html'],
  ['JUST.EXE','"Just" Vitamins','just-vitamins.html'],
  ['IC9000.EXE','IC9000','ic9000.html'],
]
const entries = [
  ['FOUNDERS.TXT','<FILE>','A message from the Founders','TYPE FOUNDERS.TXT'],
  ['LEDGER','<DIR>','Do not modify','CD LEDGER'],
  ['SUBS','<DIR>','Subsidiary index','CD SUBS'],
  ['INTAKE','<DIR>','PO Box intake queue [restricted]','CD INTAKE'],
  ['IC9000','<DIR>','Access denied','CD IC9000'],
  ['1987','<DIR>','File not found','CD 1987'],
  ['GOVERN.EXE','<FILE>','Governance [unsigned]','GOVERN.EXE'],
  ['PUBLIC.EXE','<FILE>','Public interface','PUBLIC.EXE'],
]
let directory = directories[document.body.dataset.directory] ? document.body.dataset.directory : 'ROOT'
let history = []
let historyIndex = 0
let draft = ''
let loading = false
let letter = null
function print(text, kind='') {
  const block = document.createElement('div')
  block.className = `terminal-block ${kind}`
  block.textContent = text
  output.append(block)
}
function updatePrompt() {
  prompt.textContent = `${directories[directory].path}>`
  document.title = `LS-DOS / ${directory} — Legacy Systems`
}
function focusPrompt() { input.focus({preventScroll:true}); form.scrollIntoView({block:'nearest'}) }
function echo(command) { print(`${directories[directory].path}>${command}`, 'terminal-command') }
function list() {
  print(` Volume in drive C is LEGACY\n Volume Serial Number is 0000-1987\n\n Directory of ${directories[directory].path}`)
  if (directory === 'ROOT') {
    table(entries)
    print('         3 file(s)    Size withheld\n         5 dir(s)     Free space: not allocated')
  } else if (directory === 'SUBS') {
    table(companies.map(([file,name]) => [file,'<FILE>',name,file]))
    print('         6 file(s)    All interests held\n\nExecute a filename to open its public company record.\nCD .. returns to the root directory.')
  } else if (directory === 'LEDGER') {
    print('LEDGER.DAT   <READ ONLY>\n\nNo financial statements loaded.\nModification is not an available operation.\n\nCD .. returns to the root directory.')
  } else if (directory === '1987') {
    print('File not found.\nNo further records are available.', 'terminal-error')
  } else {
    print(`Access denied.\n${directory === 'INTAKE' ? 'Office of Correspondence clearance required.' : 'Error 5: Insufficient level.'}\n\nThis terminal does not accept credentials.`, 'terminal-error')
  }
}
function table(rows) {
  const table = document.createElement('div'); table.className = 'directory'
  for (const [name, size, note, command] of rows) {
    const row = document.createElement('div'); row.className = 'directory-row'
    const button = document.createElement('button'); button.textContent = name
    button.type = 'button'; button.setAttribute('aria-label', `${name}: ${note}`)
    button.addEventListener('click', () => execute(command))
    const amount = document.createElement('span'); amount.className = 'dir-size'; amount.textContent = size
    const detail = document.createElement('span'); detail.className = 'dir-note'; detail.textContent = note
    row.append(button,amount,detail); table.append(row)
  }
  output.append(table)
}
function changeDirectory(target, updateURL=true) {
  if (!directories[target]) { print('Invalid directory.', 'terminal-error'); return }
  directory = target
  updatePrompt()
  if (updateURL) window.history.pushState({directory},'',directories[directory].page)
  list()
}
const help = `LS-DOS Command Reference\n\nDIR                    List the current directory\nCD <directory>         Change directory; CD .. returns to root\nTYPE FOUNDERS.TXT      Read a message from the Founders\nTREE                   Display the directory structure\nCLS                    Clear the screen\nVER                    Display operating system version\nMEM                    Display memory status\nWHOAMI                 Display current operator\nDATE / TIME            Display local date or time\nCOLOR 07 / 0A / 1F     Grey, green, or blue display\nPUBLIC.EXE / EXIT      Return to the public website\nGOVERN.EXE             Open corporate governance\n\nIn SUBS, execute a filename to open a company record.\nClick a directory entry to execute its command.\nUp/Down: command history. Tab: complete. Esc: clear input.\nF1: help. Ctrl+L: clear screen.\n\nLocal simulation. No host commands or files are accessible.`
async function execute(raw) {
  if (loading) return
  const command = raw.trim()
  input.value = ''
  if (!command) { focusPrompt(); return }
  echo(command)
  history.push(command); historyIndex = history.length; draft = ''
  const [verb, ...args] = command.split(/\s+/)
  const name = verb.toUpperCase()
  const arg = args.join(' ').replace(/^"|"$/g,'').toUpperCase()
  if (name === 'HELP' || name === '?') print(help)
  else if (name === 'CLS' || name === 'CLEAR') output.replaceChildren()
  else if (name === 'DIR' || name === 'LS') list()
  else if (name === 'CD' || name === 'CHDIR' || name === 'CD..' || name === 'C:') {
    if (!arg && name === 'CD') print(directories[directory].path)
    else {
      let destination = arg.replaceAll('/','\\').replace(/^C:\\?/,'').replace(/^LEGACY\\?/,'').replace(/\\$/,'')
      if (['..','\\',''].includes(destination) || name === 'CD..' || name === 'C:') destination = 'ROOT'
      if (destination === 'SUBSIDIARIES') destination = 'SUBS'
      changeDirectory(destination)
    }
  }
  else if (name === 'TYPE' || name === 'CAT') {
    if (arg === 'FOUNDERS.TXT' || arg === 'C:\\LEGACY\\FOUNDERS.TXT') {
      loading = true; input.disabled = true
      try {
        if (!letter) {
          const response = await fetch('founders-letter.txt')
          if (!response.ok) throw new Error('Not found')
          letter = await response.text()
        }
        print(letter)
      } catch { print('File could not be read. Try again with TYPE FOUNDERS.TXT.', 'terminal-error') }
      finally { loading = false; input.disabled = false }
    } else print(arg ? 'File not found.' : 'Required parameter missing.', 'terminal-error')
  }
  else if (name === 'VER') print('Legacy Systems Network Operating System\nLS-DOS Version 6.22\nCopyright (C) Legacy Systems. All rights reserved, retroactively.')
  else if (name === 'WHOAMI') print('Operator: UNASSIGNED\nAccess: READ ONLY\nTenure: INDEFINITE')
  else if (name === 'MEM') print('Conventional memory: 640K\nInstitutional memory: WITHHELD\nAvailable memory: Sufficient\n\nSimulated system information.')
  else if (name === 'DATE') print(`Current date is ${new Date().toLocaleDateString()}`)
  else if (name === 'TIME') print(`Current time is ${new Date().toLocaleTimeString()}`)
  else if (name === 'TREE') print('C:\\LEGACY\n|-- LEDGER       [read only]\n|-- SUBS         [6 entries]\n|-- INTAKE       [restricted]\n|-- IC9000       [access denied]\n`-- 1987         [file not found]')
  else if (name === 'COLOR') {
    if (['07','0A','1F'].includes(arg)) document.body.dataset.color = arg.toLowerCase()
    else print('Usage: COLOR 07 (grey), COLOR 0A (green), COLOR 1F (blue).')
  }
  else if (name === 'EXIT' || name === 'PUBLIC.EXE' || name === 'PUBLIC') { location.href = 'index.html'; return }
  else if (name === 'GOVERN.EXE' || name === 'GOVERN') { location.href = 'governance.html'; return }
  else if (['OPEN','RUN'].includes(name) && arg) { history.pop(); await execute(arg); return }
  else {
    const company = companies.find(([file]) => file === name || file.replace('.EXE','') === name)
    if (company && directory === 'SUBS') { location.href = company[2]; return }
    else print('Bad command or file name.\nType HELP for available commands.', 'terminal-error')
  }
  focusPrompt()
}
form.addEventListener('submit', event => { event.preventDefault(); execute(input.value) })
for (const button of document.querySelectorAll('[data-command]')) button.addEventListener('click', () => execute(button.dataset.command))
input.addEventListener('keydown', event => {
  if (event.key === 'ArrowUp') {
    event.preventDefault()
    if (historyIndex === history.length) draft = input.value
    if (historyIndex > 0) input.value = history[--historyIndex]
  } else if (event.key === 'ArrowDown') {
    event.preventDefault()
    if (historyIndex < history.length) historyIndex++
    input.value = historyIndex === history.length ? draft : history[historyIndex]
  } else if (event.key === 'Tab') {
    const choices = ['HELP','DIR','CD LEDGER','CD SUBS','CD INTAKE','CD IC9000','CD 1987','CD ..','TYPE FOUNDERS.TXT','CLS','VER','MEM','WHOAMI','DATE','TIME','TREE','COLOR 07','COLOR 0A','COLOR 1F','EXIT','GOVERN.EXE','PUBLIC.EXE', ...(directory === 'SUBS' ? companies.map(c=>c[0]) : [])]
    const value = input.value.toUpperCase()
    if (value) {
      const matches = choices.filter(c=>c.startsWith(value))
      if (matches.length) { event.preventDefault(); if (matches.length === 1) input.value = matches[0]; else { print(matches.join('   ')); focusPrompt() } }
    }
  } else if (event.key === 'Escape') { input.value = '' }
})
document.addEventListener('keydown', event => {
  if (event.key === 'F1') { event.preventDefault(); execute('HELP') }
  if (event.ctrlKey && event.key.toLowerCase() === 'l' && document.activeElement === input) { event.preventDefault(); execute('CLS') }
})
window.addEventListener('popstate', () => {
  const page = location.pathname.split('/').pop()
  directory = Object.keys(directories).find(key=>directories[key].page === page) || 'ROOT'
  updatePrompt(); print('Directory restored.'); list(); focusPrompt()
})
print('Legacy Systems Network Operating System\nLS-DOS Version 6.22\nCopyright (C) Legacy Systems. All rights reserved, retroactively.')
print('Checking conventional memory .......... 640K OK\nMounting permanent interests .......... OK\nLoading operator profile ............. UNASSIGNED', 'terminal-muted')
print('Warning: this page is monitored.\nLast updated: unknown. Uptime: continuous.\n\nType HELP for commands. Select an entry or enter a command below.')
updatePrompt(); list(); input.focus({preventScroll:true})
