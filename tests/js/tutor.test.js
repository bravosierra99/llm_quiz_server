// JS side of the tutor frontend↔backend contract: asserts the EXACT payload
// shapes sent (URL, method, headers, urlencoded body) and the reply keys read
// back (data.reply / data.skipped). tests/test_tutor_contract.py consumes the
// same shapes against the real routes — change one side and a test goes red.
import { beforeEach, expect, it, vi } from 'vitest'
import { flush, loadScript } from './helpers.js'

function mountTutorPage({ seed = false } = {}) {
  document.body.innerHTML = `
    <p class="muted tutor-empty">Ask the tutor anything.</p>
    <div class="tutor-thread" id="tutor-thread"></div>
    ${seed
      ? '<div id="tutor-seed" data-mode="teach" data-session="42" data-intent="Teach me this." hidden></div>'
      : ''}
    <form method="post" action="/tutor/7/ask" class="stack card" id="tutor-form"
          data-question-id="7">
      <input type="hidden" name="back" value="/quiz?x=1">
      <textarea name="message"></textarea>
      <button type="submit">Ask →</button>
    </form>`
}

function stubFetch(payload) {
  const fn = vi.fn().mockResolvedValue({ ok: true, json: async () => payload })
  vi.stubGlobal('fetch', fn)
  return fn
}

function submitAsk(message) {
  const form = document.getElementById('tutor-form')
  form.querySelector('textarea').value = message
  form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }))
}

beforeEach(() => {
  vi.unstubAllGlobals()
  Element.prototype.scrollIntoView = vi.fn()
})

it('ask sends the exact payload the backend route consumes', async () => {
  mountTutorPage()
  const fetchFn = stubFetch({ ok: true, user: 'why?', reply: 'Mock reply' })
  await loadScript('tutor')

  submitAsk('why?')
  await flush()

  expect(fetchFn).toHaveBeenCalledTimes(1)
  const [url, opts] = fetchFn.mock.calls[0]
  expect(url).toBe('/tutor/7/ask')
  expect(opts.method).toBe('POST')
  expect(opts.headers).toEqual({
    Accept: 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
  })
  // Exactly these fields, urlencoded — what tutor_ask() parses as Form data.
  expect(opts.body).toBe(
    new URLSearchParams({ message: 'why?', back: '/quiz?x=1' }).toString()
  )
})

it('ask renders data.reply into the pending bubble and re-arms the form', async () => {
  mountTutorPage()
  stubFetch({ ok: true, user: 'why?', reply: 'Mock reply' })
  await loadScript('tutor')

  submitAsk('why?')
  await flush()

  const bubbles = [...document.querySelectorAll('.tutor-text')].map((p) => p.textContent)
  expect(bubbles).toEqual(['why?', 'Mock reply'])
  expect(document.querySelector('.tutor-pending')).toBeNull()
  const button = document.querySelector('#tutor-form button')
  expect(button.disabled).toBe(false)
  expect(button.textContent).toBe('Ask →')
})

it('ask shows the degraded message when fetch fails', async () => {
  mountTutorPage()
  vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('down')))
  await loadScript('tutor')

  submitAsk('help')
  await flush()

  const last = [...document.querySelectorAll('.tutor-text')].pop()
  expect(last.textContent).toMatch(/couldn.t reach the tutor/i)
})

it('empty message never fires a model call', async () => {
  mountTutorPage()
  const fetchFn = stubFetch({ ok: true, reply: 'x' })
  await loadScript('tutor')

  submitAsk('   ')
  await flush()

  expect(fetchFn).not.toHaveBeenCalled()
})

it('auto-seed posts mode/session_id/back to /questions/{id}/tutor', async () => {
  mountTutorPage({ seed: true })
  const fetchFn = stubFetch({ ok: true, user: 'Teach me this.', reply: 'Lesson time.' })
  await loadScript('tutor')
  await flush()

  expect(fetchFn).toHaveBeenCalledTimes(1)
  const [url, opts] = fetchFn.mock.calls[0]
  expect(url).toBe('/questions/7/tutor')
  expect(opts.body).toBe(
    new URLSearchParams({ mode: 'teach', session_id: '42', back: '/quiz?x=1' }).toString()
  )
  // The echoed 'You' bubble + the reply, same shape as a reloaded thread.
  const bubbles = [...document.querySelectorAll('.tutor-text')].map((p) => p.textContent)
  expect(bubbles).toEqual(['Teach me this.', 'Lesson time.'])
  // ?seed is dropped from the address bar so a reload can't re-fire the model call.
  expect(window.location.pathname).toBe('/tutor/7')
})
