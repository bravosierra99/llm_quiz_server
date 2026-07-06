import { beforeEach, expect, it, vi } from 'vitest'
import { loadScript } from './helpers.js'

beforeEach(() => {
  localStorage.clear()
  document.documentElement.removeAttribute('data-theme')
  // jsdom has no matchMedia; the no-stored-value branch consults it.
  vi.stubGlobal('matchMedia', vi.fn().mockReturnValue({ matches: false })) // OS says light
})

it('applies the saved theme at load (pre-paint)', async () => {
  localStorage.setItem('theme', 'dark')
  await loadScript('theme')
  expect(document.documentElement.getAttribute('data-theme')).toBe('dark')
})

it('ignores junk stored values', async () => {
  localStorage.setItem('theme', 'blurple')
  await loadScript('theme')
  expect(document.documentElement.hasAttribute('data-theme')).toBe(false)
})

it('toggle flips the theme and persists it', async () => {
  localStorage.setItem('theme', 'dark')
  await loadScript('theme')
  window.toggleTheme()
  expect(document.documentElement.getAttribute('data-theme')).toBe('light')
  expect(localStorage.getItem('theme')).toBe('light')
})

it('first toggle with nothing stored picks the opposite of the OS scheme', async () => {
  await loadScript('theme')
  window.toggleTheme() // OS is light (stub) -> explicit dark
  expect(document.documentElement.getAttribute('data-theme')).toBe('dark')
})
