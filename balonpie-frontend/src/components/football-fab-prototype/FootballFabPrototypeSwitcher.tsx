// PROTOTYPE — Tarea 11. Barra flotante para alternar entre variantes via ?fab=A|B.
import { useEffect } from "react"
import { useSearchParams } from "react-router-dom"
import "./FootballFabPrototype.css"

const VARIANTS = [
  { key: "A", label: "Fan radial" },
  { key: "B", label: "Stack vertical" },
] as const

export default function FootballFabPrototypeSwitcher({ current }: { readonly current: string }) {
  const [searchParams, setSearchParams] = useSearchParams()

  const go = (dir: 1 | -1) => {
    const idx = VARIANTS.findIndex((v) => v.key === current)
    const next = VARIANTS[(idx + dir + VARIANTS.length) % VARIANTS.length]
    const params = new URLSearchParams(searchParams)
    params.set("fab", next.key)
    setSearchParams(params)
  }

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement
      if (["INPUT", "TEXTAREA"].includes(target.tagName) || target.isContentEditable) return
      if (e.key === "ArrowLeft") go(-1)
      if (e.key === "ArrowRight") go(1)
    }
    window.addEventListener("keydown", onKey)
    return () => window.removeEventListener("keydown", onKey)
  })

  const variant = VARIANTS.find((v) => v.key === current) ?? VARIANTS[0]

  return (
    <div className="fab-proto-switcher">
      <button type="button" onClick={() => go(-1)} aria-label="Variante anterior">←</button>
      <span>{variant.key} — {variant.label}</span>
      <button type="button" onClick={() => go(1)} aria-label="Variante siguiente">→</button>
    </div>
  )
}
