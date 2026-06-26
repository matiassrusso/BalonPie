import { useEffect, useState } from "react"
import { Link, useLocation } from "react-router-dom"
import { API_URL, type PosicionTabla } from "../api"
import SeasonSelector from "../components/SeasonSelector"
import { useSeason } from "../context/SeasonContext"
import "./Pages.css"

type TablaLocationState = {
  readonly highlightTeamSlug?: string
}

const LAST_TEAM_SLUG_KEY = "balonpie:last-team-slug"

function inicialEquipo(nombre: string): string {
  const [primeraPalabra = ""] = nombre.trim().split(/\s+/)
  return primeraPalabra.slice(0, 1).toUpperCase() || "?"
}

function EscudoTabla({ nombre, escudo }: { readonly nombre: string; readonly escudo: string }) {
  const [mostrarFallback, setMostrarFallback] = useState(false)

  if (mostrarFallback || escudo.trim() === "") {
    return <span className="tabla-equipo-escudo-fallback">{inicialEquipo(nombre)}</span>
  }

  return (
    <img
      src={escudo}
      alt={`Escudo de ${nombre}`}
      className="tabla-equipo-escudo"
      loading="lazy"
      onError={() => {
        setMostrarFallback(true)
      }}
    />
  )
}

export default function Tabla() {
  const { season } = useSeason()
  const [posiciones, setPosiciones] = useState<PosicionTabla[]>([])
  const location = useLocation()
  const locationState = location.state as TablaLocationState | null
  const activeTeamSlug =
    locationState?.highlightTeamSlug ?? (typeof window === "undefined" ? null : window.sessionStorage.getItem(LAST_TEAM_SLUG_KEY))

  useEffect(() => {
    fetch(`${API_URL}/tabla?season=${season}`)
      .then((res) => res.json())
      .then((data) => setPosiciones(data.posiciones))
  }, [season])

  return (
    <div className="page page-tabla">
      <header className="tabla-header">
        <div className="tabla-header-copy">
          <span className="tabla-header-kicker">Tabla de posiciones</span>
          <h1 className="tabla-header-titulo">Liga Profesional Argentina</h1>
        </div>
        <SeasonSelector />
      </header>
      <div className="tabla-scroll">
        <table className="tabla-posiciones">
          <thead>
            <tr>
              <th>#</th>
              <th>Equipo</th>
              <th>Pts</th>
              <th>PJ</th>
              <th>G</th>
              <th>E</th>
              <th>P</th>
              <th>DG</th>
              <th>Forma</th>
            </tr>
          </thead>
          <tbody>
            {posiciones.map((fila) => (
              <tr
                key={fila.equipo}
                className={fila.slug !== null && fila.slug === activeTeamSlug ? "tabla-fila tabla-fila-activa" : "tabla-fila"}
              >
                <td>{fila.posicion}</td>
                <td>
                  <div className="tabla-equipo">
                    <EscudoTabla nombre={fila.equipo} escudo={fila.escudo} />
                    {fila.slug ? <Link to={`/equipo/${fila.slug}`}>{fila.equipo}</Link> : fila.equipo}
                  </div>
                </td>
                <td>{fila.puntos}</td>
                <td>{fila.jugados}</td>
                <td>{fila.ganados}</td>
                <td>{fila.empatados}</td>
                <td>{fila.perdidos}</td>
                <td>{fila.diferencia_goles}</td>
                <td className="forma">
                  {fila.forma.map((resultado, index) => (
                    <span key={index} className={`chip-forma chip-forma-${resultado}`}>
                      {resultado}
                    </span>
                  ))}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
