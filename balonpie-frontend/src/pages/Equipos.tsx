import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import { API_URL, type EquipoResumen } from "../api"
import MotionCard from "../components/MotionCard"
import "./Pages.css"

const COMPETICION_ORDEN = [
  "Liga Profesional",
  "Copa Argentina",
  "Copa Libertadores",
  "Copa Sudamericana",
] as const

function agruparEquipos(equipos: readonly EquipoResumen[]): Array<{ competencia: string; equipos: EquipoResumen[] }> {
  const grupos = new Map<string, EquipoResumen[]>()

  for (const equipo of equipos) {
    const existentes = grupos.get(equipo.competencia)
    if (existentes) {
      existentes.push(equipo)
      continue
    }

    grupos.set(equipo.competencia, [equipo])
  }

  const orden = new Map<string, number>(COMPETICION_ORDEN.map((competencia, index) => [competencia, index]))

  return Array.from(grupos.entries())
    .map(([competencia, agrupados]) => ({
      competencia,
      equipos: agrupados,
    }))
    .sort((a, b) => (orden.get(a.competencia) ?? Number.MAX_SAFE_INTEGER) - (orden.get(b.competencia) ?? Number.MAX_SAFE_INTEGER))
}

export default function Equipos() {
  const [equipos, setEquipos] = useState<EquipoResumen[]>([])
  const [query, setQuery] = useState("")

  useEffect(() => {
    fetch(`${API_URL}/equipos`)
      .then((res) => res.json())
      .then((data) => setEquipos(data.equipos))
  }, [])

  const filtrados = query.trim()
    ? equipos.filter((e) => e.nombre.toLowerCase().includes(query.toLowerCase()))
    : equipos

  const grupos = agruparEquipos(filtrados)

  return (
    <div className="page page-equipos">
      <div className="page-header">
        <h1>Equipos</h1>
      </div>
      <input
        type="search"
        className="equipos-buscador"
        placeholder="Buscar equipo…"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <div className="equipos-listado">
        {grupos.length === 0 && query.trim() && (
          <div className="equipos-sin-resultados">Sin resultados para "{query}"</div>
        )}
        {grupos.map((grupo) => (
          <section key={grupo.competencia} className="equipos-grupo">
            <header className="equipos-grupo-header">{grupo.competencia}</header>
            <div className="equipos-grupo-lista">
              {grupo.equipos.map((equipo, index) => (
                <MotionCard key={equipo.slug} index={index}>
                  <Link to={`/equipo/${equipo.slug}`} className="equipo-fila">
                    <div className="equipo-fila-main">
                      <img src={equipo.escudo} alt={`Escudo de ${equipo.nombre}`} className="equipo-fila-escudo" loading="lazy" />
                      <span className="equipo-fila-nombre">{equipo.nombre}</span>
                    </div>
                    <span className="equipo-fila-chevron" aria-hidden="true">
                      ›
                    </span>
                  </Link>
                </MotionCard>
              ))}
            </div>
          </section>
        ))}
      </div>
    </div>
  )
}
