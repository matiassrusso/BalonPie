import { useState } from "react"
import { Link } from "react-router-dom"
import type { Partido } from "../api"
import "./PartidoCard.css"

const ESTADOS_EN_VIVO = new Set(["1H", "2H", "HT", "ET", "P", "BT"])

function formatearFecha(fechaIso: string): string {
  const fecha = new Date(fechaIso)
  return fecha.toLocaleString("es-AR", { day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit" })
}

function inicialEquipo(nombre: string): string {
  const [primeraPalabra = ""] = nombre.trim().split(/\s+/)
  return primeraPalabra.slice(0, 1).toUpperCase() || "?"
}

function EscudoEquipo({ nombre, escudo }: { nombre: string; escudo: string }) {
  const [mostrarFallback, setMostrarFallback] = useState(false)

  if (mostrarFallback || escudo.trim() === "") {
    return <span className="partido-card-escudo-fallback">{inicialEquipo(nombre)}</span>
  }

  return (
    <img
      src={escudo}
      alt={`Escudo de ${nombre}`}
      className="partido-card-escudo"
      loading="lazy"
      onError={() => {
        setMostrarFallback(true)
      }}
    />
  )
}

function EquipoLinea({
  nombre,
  escudo,
  alinear,
}: {
  nombre: string
  escudo: string
  alinear: "izquierda" | "derecha"
}) {
  return (
    <div className={`partido-card-equipo-linea partido-card-equipo-linea-${alinear}`}>
      {alinear === "derecha" ? <span className="partido-card-equipo-nombre">{nombre}</span> : null}
      <EscudoEquipo nombre={nombre} escudo={escudo} />
      {alinear === "izquierda" ? <span className="partido-card-equipo-nombre">{nombre}</span> : null}
    </div>
  )
}

export default function PartidoCard({ partido }: { partido: Partido }) {
  const enVivo = ESTADOS_EN_VIVO.has(partido.estado)
  const jugado = partido.goles_local !== null && partido.goles_visitante !== null

  return (
    <Link to={`/partido/${partido.id}`} className={`partido-card${enVivo ? " partido-card-vivo" : ""}`}>
      <div className="partido-card-equipo partido-card-equipo-local">
        <EquipoLinea nombre={partido.equipo_local} escudo={partido.escudo_local} alinear="izquierda" />
      </div>
      <div className="partido-card-centro">
        {jugado ? (
          <span className={`partido-card-marcador${jugado ? " partido-card-marcador-finalizado" : ""}`}>
            {partido.goles_local} <span className="partido-card-separador">-</span> {partido.goles_visitante}
          </span>
        ) : (
          <span className="partido-card-hora">{formatearFecha(partido.fecha)}</span>
        )}
      </div>
      <div className="partido-card-equipo partido-card-equipo-visitante">
        <EquipoLinea nombre={partido.equipo_visitante} escudo={partido.escudo_visitante} alinear="derecha" />
      </div>
      {enVivo ? <div className="partido-card-estado">EN VIVO {partido.minuto}'</div> : null}
    </Link>
  )
}
