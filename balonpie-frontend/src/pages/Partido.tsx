import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import { API_URL, type EventoPartido, type LineupsPartido, type PartidoDetalle } from "../api"
import AlineacionesCampo from "../components/AlineacionesCampo"
import "./Pages.css"
import "./Partido.css"

const ESTADOS_EN_VIVO = new Set(["1H", "2H", "HT", "ET", "P", "BT"])

const STAT_NOMBRES: Record<string, string> = {
  "Ball Possession": "Posesión",
  "Total Shots": "Tiros totales",
  "Shots on Goal": "Al arco",
  "Shots off Goal": "Afuera",
  "Blocked Shots": "Bloqueados",
  "Shots insidebox": "Dentro del área",
  "Shots outsidebox": "Fuera del área",
  "Fouls": "Faltas",
  "Corner Kicks": "Córners",
  "Offsides": "Fuera de juego",
  "Yellow Cards": "Amarillas",
  "Red Cards": "Rojas",
  "Goalkeeper Saves": "Atajadas",
  "Total passes": "Pases totales",
  "Passes accurate": "Pases precisos",
  "Passes %": "Precisión de pases",
  "expected_goals": "xG",
}

function formatearFecha(fechaIso: string): string {
  return new Date(fechaIso).toLocaleString("es-AR", {
    day: "2-digit",
    month: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  })
}

function inicialEquipo(nombre: string): string {
  const [primeraPalabra = ""] = nombre.trim().split(/\s+/)
  return primeraPalabra.slice(0, 1).toUpperCase() || "?"
}

function getEstadoTexto(detalle: PartidoDetalle): string {
  const { estado, minuto } = detalle
  if (ESTADOS_EN_VIVO.has(estado)) {
    if (estado === "HT") return "DESCANSO"
    return minuto ? `${minuto}'` : "EN VIVO"
  }
  if (estado === "FT") return "FT"
  if (estado === "AET") return "PRÓRROGA"
  if (estado === "PEN") return "PENALES"
  if (estado === "PST") return "POSTERGADO"
  if (estado === "CANC") return "CANCELADO"
  return formatearFecha(detalle.fecha)
}

function parsearValorStat(valor: string | number | null | undefined): number | null {
  if (valor === null || valor === undefined) return null
  if (typeof valor === "number") return valor
  const sinPct = String(valor).replace("%", "").trim()
  const num = parseFloat(sinPct)
  return isNaN(num) ? null : num
}

function calcularPct(
  local: string | number | null | undefined,
  visitante: string | number | null | undefined,
): number | null {
  const l = parsearValorStat(local)
  const v = parsearValorStat(visitante)
  if (l === null || v === null) return null
  const total = l + v
  return total === 0 ? 50 : Math.round((l / total) * 100)
}

function EscudoPartido({ nombre, escudo }: { readonly nombre: string; readonly escudo: string }) {
  const [fallback, setFallback] = useState(false)
  if (fallback || !escudo.trim()) {
    return <span className="partido-escudo-fallback">{inicialEquipo(nombre)}</span>
  }
  return (
    <img
      src={escudo}
      alt={`Escudo de ${nombre}`}
      className="partido-escudo"
      loading="lazy"
      onError={() => setFallback(true)}
    />
  )
}

function IconoEvento({ tipo, detalle }: { readonly tipo: string; readonly detalle: string }) {
  if (tipo === "Goal") {
    const esPropio = detalle.toLowerCase().includes("own")
    return <span className={`icono-gol${esPropio ? " icono-gol-pp" : ""}`} aria-hidden="true" />
  }
  if (tipo === "Card") {
    if (detalle.toLowerCase().includes("yellow")) {
      return <span className="icono-amarilla" aria-hidden="true" />
    }
    return <span className="icono-roja" aria-hidden="true" />
  }
  return <span className="icono-otro" aria-hidden="true" />
}

function FilaEvento({
  evento,
  esLocal,
}: {
  readonly evento: EventoPartido
  readonly esLocal: boolean
}) {
  const icono = <IconoEvento tipo={evento.tipo} detalle={evento.detalle} />
  const nombre = <span className="evento-jugador">{evento.jugador}</span>

  return (
    <div className="evento-fila">
      <div className="evento-local">
        {esLocal ? <>{nombre}{icono}</> : null}
      </div>
      <div className="evento-minuto">{evento.minuto}'</div>
      <div className="evento-visitante">
        {!esLocal ? <>{icono}{nombre}</> : null}
      </div>
    </div>
  )
}

function PartidoPageHeader({ detalle }: { readonly detalle: PartidoDetalle }) {
  const estadoTexto = getEstadoTexto(detalle)
  const enVivo = ESTADOS_EN_VIVO.has(detalle.estado)
  const hayMarcador = detalle.goles_local !== null && detalle.goles_visitante !== null

  return (
    <header className="partido-header">
      <div className="partido-header-kicker">{detalle.competencia}</div>
      <div className="partido-header-main">
        <div className="partido-header-equipo partido-header-local">
          <EscudoPartido nombre={detalle.equipo_local} escudo={detalle.escudo_local} />
          <span className="partido-header-nombre">{detalle.equipo_local}</span>
        </div>
        <div className="partido-header-score">
          <span className="partido-score">
            {hayMarcador ? `${detalle.goles_local} – ${detalle.goles_visitante}` : "–"}
          </span>
          <span className={`partido-estado${enVivo ? " partido-estado-vivo" : ""}`}>
            {estadoTexto}
          </span>
        </div>
        <div className="partido-header-equipo partido-header-visitante">
          <EscudoPartido nombre={detalle.equipo_visitante} escudo={detalle.escudo_visitante} />
          <span className="partido-header-nombre">{detalle.equipo_visitante}</span>
        </div>
      </div>
    </header>
  )
}

function SeccionEventos({ detalle }: { readonly detalle: PartidoDetalle }) {
  return (
    <section>
      <div className="partido-seccion-header">Eventos</div>
      {detalle.eventos.length === 0 ? (
        <div className="partido-vacio">No hay eventos disponibles para este partido.</div>
      ) : (
        <div className="eventos-grid">
          {detalle.eventos.map((evento, index) => (
            <FilaEvento
              key={index}
              evento={evento}
              esLocal={evento.equipo === detalle.equipo_local}
            />
          ))}
        </div>
      )}
    </section>
  )
}

function SeccionEstadisticas({ detalle }: { readonly detalle: PartidoDetalle }) {
  const statsLocal = detalle.estadisticas[detalle.equipo_local] ?? {}
  const statsVisitante = detalle.estadisticas[detalle.equipo_visitante] ?? {}
  const claves = Object.keys(statsLocal)
  const hayEstadisticas = claves.length > 0

  return (
    <section>
      <div className="partido-seccion-header">Estadísticas</div>
      {!hayEstadisticas ? (
        <div className="partido-vacio">Estadísticas no disponibles para este partido.</div>
      ) : (
        <div className="stats-comparativa">
          {claves.map((clave) => {
            const vLocal = statsLocal[clave]
            const vVisitante = statsVisitante[clave]
            const pct = calcularPct(vLocal, vVisitante)
            const nombreStat = STAT_NOMBRES[clave] ?? clave
            return (
              <div key={clave} className="stat-fila">
                <div className="stat-row">
                  <span className="stat-valor-local">{vLocal ?? "—"}</span>
                  <span className="stat-nombre">{nombreStat}</span>
                  <span className="stat-valor-visitante">{vVisitante ?? "—"}</span>
                </div>
                {pct !== null && (
                  <div className="stat-barra-container">
                    <div className="stat-barra-fill" style={{ width: `${pct}%` }} />
                  </div>
                )}
              </div>
            )
          })}
        </div>
      )}
    </section>
  )
}

function SeccionAlineaciones({ lineups }: { readonly lineups: LineupsPartido | null }) {
  return (
    <section>
      <div className="partido-seccion-header">Alineaciones</div>
      {!lineups || !lineups.local || !lineups.visitante ? (
        <div className="partido-vacio">Alineaciones no disponibles para este partido.</div>
      ) : (
        <AlineacionesCampo local={lineups.local} visitante={lineups.visitante} />
      )}
    </section>
  )
}

export default function Partido() {
  const { id } = useParams<{ id: string }>()
  const [detalle, setDetalle] = useState<PartidoDetalle | null>(null)
  const [lineups, setLineups] = useState<LineupsPartido | null>(null)
  const [sinDatos, setSinDatos] = useState(false)

  useEffect(() => {
    const cargar = () => {
      fetch(`${API_URL}/partido/${id}`)
        .then((res) => {
          if (!res.ok) { setSinDatos(true); return null }
          return res.json()
        })
        .then((data) => { if (data) setDetalle(data) })
    }
    cargar()
    const intervalId = setInterval(cargar, 60_000)
    return () => clearInterval(intervalId)
  }, [id])

  useEffect(() => {
    fetch(`${API_URL}/partido/${id}/lineups`)
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => { if (data) setLineups(data) })
  }, [id])

  if (sinDatos) return <div className="page page-partido">Sin datos disponibles por el momento.</div>
  if (!detalle) return <div className="page page-partido">Cargando...</div>

  return (
    <div className="page page-partido">
      <PartidoPageHeader detalle={detalle} />
      <SeccionAlineaciones lineups={lineups} />
      <SeccionEventos detalle={detalle} />
      <SeccionEstadisticas detalle={detalle} />
    </div>
  )
}
