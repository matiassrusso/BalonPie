// PROTOTYPE — Tarea 11, Variante B: stack vertical (speed-dial). Throwaway, ver NOTES.md.
import { useState } from "react"
import { Link, useLocation } from "react-router-dom"
import { FAB_PROTO_ITEMS } from "./items"
import "./FootballFabPrototype.css"

export default function FootballFabPrototypeB() {
  const [open, setOpen] = useState(false)
  const location = useLocation()

  return (
    <div className={`fab-proto fab-proto-stack${open ? " fab-proto-open" : ""}`}>
      {FAB_PROTO_ITEMS.map((item) => (
        <Link
          key={item.to}
          to={item.to}
          className={`fab-proto-item${location.pathname === item.to ? " fab-proto-item-active" : ""}`}
        >
          {item.label}
        </Link>
      ))}
      <button
        type="button"
        className="fab-proto-ball"
        onClick={() => setOpen((v) => !v)}
        aria-label="Navegacion"
      >
        ⚽
      </button>
    </div>
  )
}
