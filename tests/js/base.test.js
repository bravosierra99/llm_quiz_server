import { beforeAll, beforeEach, expect, it, vi } from 'vitest'
import { flush, loadScript } from './helpers.js'

beforeAll(async () => {
  // base.js registers document-level listeners once; the DOM is rebuilt per test.
  await loadScript('base')
})

beforeEach(() => {
  document.body.innerHTML = ''
})

it('locks every button in an action row on submit (after the tick)', async () => {
  document.body.innerHTML = `
    <div class="feedback-actions">
      <form id="f"><button id="b1" type="submit">Tutor</button></form>
      <form><button id="b2" type="submit">Flag</button></form>
    </div>`
  document.getElementById('f')
    .dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }))
  // NOT disabled during the submit event itself (the submitter must serialize)...
  expect(document.getElementById('b1').disabled).toBe(false)
  await flush()
  // ...but locked one tick later, including the sibling form's button.
  expect(document.getElementById('b1').disabled).toBe(true)
  expect(document.getElementById('b2').disabled).toBe(true)
})

it('number keys pick the Nth quiz choice', () => {
  document.body.innerHTML = `
    <div id="quiz-stage"><ul class="choice-list">
      <li><input type="radio" name="answer" value="A"></li>
      <li><input type="radio" name="answer" value="B"></li>
    </ul></div>`
  document.body.dispatchEvent(
    new KeyboardEvent('keydown', { key: '2', bubbles: true, cancelable: true }))
  const radios = document.querySelectorAll('input[type=radio]')
  expect(radios[1].checked).toBe(true)
  expect(radios[0].checked).toBe(false)
})

it('number keys are ignored while typing a short answer', () => {
  document.body.innerHTML = `
    <div id="quiz-stage">
      <textarea name="answer"></textarea>
      <ul class="choice-list"><li><input type="radio" name="x"></li></ul>
    </div>`
  document.querySelector('textarea')
    .dispatchEvent(new KeyboardEvent('keydown', { key: '1', bubbles: true }))
  expect(document.querySelector('input[type=radio]').checked).toBe(false)
})

it('focusQuizStage focuses the first answer control', () => {
  document.body.innerHTML = `
    <div id="quiz-stage"><ul class="choice-list">
      <li><input id="first" type="radio" name="answer"></li>
    </ul></div>`
  window.focusQuizStage()
  expect(document.activeElement.id).toBe('first')
})
