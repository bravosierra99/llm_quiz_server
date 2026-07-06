// The small per-page helpers: quiz reveal/self-grade, setup select-all,
// generate + question-edit field toggles.
import { expect, it } from 'vitest'
import { loadScript } from './helpers.js'

it('quiz: reveal shows the answer box and hides the button', async () => {
  document.body.innerHTML = `
    <button id="reveal-btn"></button>
    <div id="reveal-box" style="display:none"></div>
    <input id="self_correct" type="hidden" value="">`
  await loadScript('quiz')
  window.reveal()
  expect(document.getElementById('reveal-box').style.display).toBe('block')
  expect(document.getElementById('reveal-btn').style.display).toBe('none')
  window.setSelf('yes')
  expect(document.getElementById('self_correct').value).toBe('yes')
})

it('quiz setup: select-all mirrors onto enabled checkboxes of that collection only', async () => {
  document.body.innerHTML = `
    <input type="checkbox" id="all">
    <input type="checkbox" name="chapter_ids" data-coll="1" id="a">
    <input type="checkbox" name="chapter_ids" data-coll="1" id="b" disabled>
    <input type="checkbox" name="chapter_ids" data-coll="2" id="c">`
  await loadScript('quiz-setup')
  const all = document.getElementById('all')
  all.checked = true
  window.toggleColl(all, 1)
  expect(document.getElementById('a').checked).toBe(true)
  expect(document.getElementById('b').checked).toBe(false) // disabled: untouched
  expect(document.getElementById('c').checked).toBe(false) // other collection
  all.checked = false
  window.toggleColl(all, 1)
  expect(document.getElementById('a').checked).toBe(false)
})

it('generate: source mode swaps the topic field for the source picker', async () => {
  document.body.innerHTML = `
    <input type="radio" name="mode" value="topic" checked>
    <input type="radio" name="mode" value="source">
    <div id="topic-field"></div>
    <div id="source-field"></div>`
  await loadScript('generate') // runs syncMode() at load
  expect(document.getElementById('source-field').style.display).toBe('none')
  document.querySelector('input[value=source]').checked = true
  window.syncMode()
  expect(document.getElementById('source-field').style.display).toBe('')
  expect(document.getElementById('topic-field').style.display).toBe('none')
})

it('question edit: choices box only shows for MCQ', async () => {
  document.body.innerHTML = `
    <select id="qtype"><option value="mcq" selected>mcq</option>
      <option value="short">short</option></select>
    <div id="choices-field"></div>`
  await loadScript('question-edit') // runs syncType() at load
  expect(document.getElementById('choices-field').style.display).toBe('')
  document.getElementById('qtype').value = 'short'
  window.syncType()
  expect(document.getElementById('choices-field').style.display).toBe('none')
})
