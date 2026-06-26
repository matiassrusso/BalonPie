import { NavLink } from "react-router-dom"
import "./Dock.css"

const ITEMS = [
  {
    to: "/",
    label: "Inicio",
    end: true,
    icon: (
      <path d="M3 11.5 12 4l9 7.5M5.5 10v9h13v-9" strokeLinecap="round" strokeLinejoin="round" />
    ),
  },
  {
    to: "/tabla",
    label: "Tabla",
    end: false,
    icon: (
      <path d="M4 6h16M4 12h16M4 18h16" strokeLinecap="round" />
    ),
  },
  {
    to: "/equipos",
    label: "Equipos",
    end: false,
    icon: (
      <path
        d="M8 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6Zm8 0a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM2 19c0-3 2.7-5 6-5s6 2 6 5M14 19c0-2.4 1.8-4.2 4.5-4.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    ),
  },
]

export default function Dock() {
  return (
    <nav className="dock" aria-label="Navegacion principal">
      <div className="dock-brand">
        <span className="dock-brand-mark">BP</span>
        <div className="dock-brand-copy">
          <span className="dock-brand-name">BalonPie</span>
          <span className="dock-brand-tag">Futbol argentino</span>
        </div>
      </div>
      <div className="dock-nav">
        {ITEMS.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.end}
            className={({ isActive }) => `dock-item${isActive ? " dock-item-active" : ""}`}
          >
            <svg className="dock-item-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              {item.icon}
            </svg>
            <span>{item.label}</span>
          </NavLink>
        ))}
      </div>
    </nav>
  )
}
