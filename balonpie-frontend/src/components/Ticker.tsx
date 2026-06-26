import { useEffect, useState } from "react"
import { API_URL, type Partido } from "../api"
import "./Ticker.css"

export default function Ticker() {
  const [partidos, setPartidos] = useState<Partido[]>([])

  useEffect(() => {
    fetch(`${API_URL}/ultima-fecha`)
      .then((res) => res.json())
      .then((data) => setPartidos(data.partidos))
  }, [])

  if (partidos.length === 0) return null

  const items = [...partidos, ...partidos]

  return (
    <div className="ticker">
      <div className="ticker-track">
        {items.map((partido, index) => (
          <span key={`${partido.id}-${index}`} className="ticker-item">
            {partido.equipo_local} {partido.goles_local} - {partido.goles_visitante} {partido.equipo_visitante}
          </span>
        ))}
      </div>
    </div>
  )
}
