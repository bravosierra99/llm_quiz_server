import { vi } from 'vitest'

// The static/js files are classic scripts (side effects at load, globals on
// window), not ESM. Loading = fresh dynamic import after the test has built
// the DOM the script expects.
export async function loadScript(name) {
  vi.resetModules()
  await import(`../../app/static/js/${name}.js`)
}

// Flush the microtask/timer turns a .then chain needs to settle.
export async function flush(times = 4) {
  for (let i = 0; i < times; i++) {
    await new Promise((r) => setTimeout(r, 0))
  }
}
