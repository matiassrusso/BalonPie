import type { EquipoLineup, JugadorLineup } from "../api"
import "./AlineacionesCampo.css"

function iniciales(nombre: string): string {
  const partes = nombre.trim().split(/\s+/)
  if (partes.length === 1) return partes[0].slice(0, 2).toUpperCase()
  return (partes[0][0] + partes[partes.length - 1][0]).toUpperCase()
}

function apellido(nombre: string): string {
  const partes = nombre.trim().split(/\s+/)
  return partes[partes.length - 1]
}

function parseGrid(grid: string | null): { col: number; row: number } | null {
  if (!grid) return null
  const partes = grid.split(":")
  if (partes.length !== 2) return null
  const col = Number(partes[0])
  const row = Number(partes[1])
  if (isNaN(col) || isNaN(row)) return null
  return { col, row }
}

interface JugadorPosicionado extends JugadorLineup {
  leftPct: number
  topPct: number
}

function posicionarJugadores(jugadores: JugadorLineup[], esLocal: boolean): JugadorPosicionado[] {
  const conGrid = jugadores
    .map((j) => ({ ...j, parsed: parseGrid(j.grid) }))
    .filter((j) => j.parsed !== null)

  if (conGrid.length === 0) return []

  const maxRow = Math.max(...conGrid.map((j) => j.parsed!.row))

  const porFila: Record<number, typeof conGrid> = {}
  for (const j of conGrid) {
    const row = j.parsed!.row
    if (!porFila[row]) porFila[row] = []
    porFila[row].push(j)
  }

  return conGrid.map((j) => {
    const { col, row } = j.parsed!
    const jugadoresEnFila = porFila[row].length
    const leftPct = ((col - 0.5) / jugadoresEnFila) * 100
    const fraccion = maxRow === 1 ? 0.5 : (row - 1) / (maxRow - 1)
    const topPct = esLocal ? 6 + fraccion * 41 : 94 - fraccion * 41
    return { ...j, leftPct, topPct }
  })
}

function PuntosEquipo({
  equipo,
  esLocal,
}: {
  readonly equipo: EquipoLineup
  readonly esLocal: boolean
}) {
  const jugadores = posicionarJugadores(equipo.once, esLocal)
  const clase = esLocal ? "alin-dot alin-dot-local" : "alin-dot alin-dot-visitante"

  return (
    <>
      {jugadores.map((j, i) => (
        <div
          key={i}
          className={clase}
          style={{ left: `${j.leftPct}%`, top: `${j.topPct}%` }}
        >
          <div className="alin-circulo">{iniciales(j.nombre)}</div>
          <div className="alin-nombre">{apellido(j.nombre)}</div>
        </div>
      ))}
    </>
  )
}

export default function AlineacionesCampo({
  local,
  visitante,
}: {
  readonly local: EquipoLineup
  readonly visitante: EquipoLineup
}) {
  return (
    <div className="alin-wrapper">
      <div className="alin-labels">
        <span className="alin-label-local">{local.equipo} · {local.formacion}</span>
        <span className="alin-label-visitante">{visitante.equipo} · {visitante.formacion}</span>
      </div>
      <div className="alin-campo">
        <div className="alin-linea-centro" />
        <PuntosEquipo equipo={local} esLocal={true} />
        <PuntosEquipo equipo={visitante} esLocal={false} />
      </div>
      <div className="alin-bancos">
        <div className="alin-banco">
          <div className="alin-banco-titulo">Suplentes · {local.equipo}</div>
          {local.suplentes.map((s, i) => (
            <div key={i} className="alin-banco-jugador">{s}</div>
          ))}
          {local.dt && <div className="alin-banco-dt">DT: {local.dt}</div>}
        </div>
        <div className="alin-banco">
          <div className="alin-banco-titulo">Suplentes · {visitante.equipo}</div>
          {visitante.suplentes.map((s, i) => (
            <div key={i} className="alin-banco-jugador">{s}</div>
          ))}
          {visitante.dt && <div className="alin-banco-dt">DT: {visitante.dt}</div>}
        </div>
      </div>
    </div>
  )
}
