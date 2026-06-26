import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import { API_URL, type PerfilEquipo } from "../api"
import PartidoCard from "../components/PartidoCard"
import "./Pages.css"
import "./Equipo.css"

const LAST_TEAM_SLUG_KEY = "balonpie:last-team-slug"
const MENSAJE_RESULTADOS_NO_DISPONIBLES = "Resultados de la temporada 2024 no disponibles en el plan actual"

type StatItem = {
  readonly label: string
  readonly value: number
}

function inicialEquipo(nombre: string): string {
  const [primeraPalabra = ""] = nombre.trim().split(/\s+/)
  return primeraPalabra.slice(0, 1).toUpperCase() || "?"
}

function EscudoHero({ nombre, escudo }: { readonly nombre: string; readonly escudo: string }) {
  const [mostrarFallback, setMostrarFallback] = useState(false)

  if (mostrarFallback || escudo.trim() === "") {
    return <span className="equipo-hero-escudo-fallback">{inicialEquipo(nombre)}</span>
  }

  return (
    <img
      src={escudo}
      alt={`Escudo de ${nombre}`}
      className="equipo-hero-escudo"
      loading="lazy"
      onError={() => {
        setMostrarFallback(true)
      }}
    />
  )
}

export default function Equipo() {
  const { nombre } = useParams<{ nombre: string }>()
  const [perfil, setPerfil] = useState<PerfilEquipo | null>(null)
  const [sinDatos, setSinDatos] = useState(false)

  useEffect(() => {
    if (typeof window === "undefined" || !nombre) {
      return
    }

    window.sessionStorage.setItem(LAST_TEAM_SLUG_KEY, nombre)
  }, [nombre])

  useEffect(() => {
    setPerfil(null)
    setSinDatos(false)
    fetch(`${API_URL}/equipo/${nombre}`)
      .then((res) => {
        if (!res.ok) {
          setSinDatos(true)
          return null
        }
        return res.json()
      })
      .then((data) => {
        if (data) setPerfil(data)
      })
  }, [nombre])

  if (sinDatos) return <div className="page page-equipo">Sin datos disponibles por el momento.</div>
  if (!perfil) return <div className="page page-equipo">Cargando...</div>

  const { estadisticas, resultados_recientes } = perfil
  const stats: readonly StatItem[] = [
    { label: "PJ", value: estadisticas.partidos_jugados },
    { label: "G", value: estadisticas.ganados },
    { label: "E", value: estadisticas.empatados },
    { label: "P", value: estadisticas.perdidos },
    { label: "GF", value: estadisticas.goles_a_favor },
    { label: "GC", value: estadisticas.goles_en_contra },
  ]
  const tieneResultados = resultados_recientes.length > 0

  return (
    <div className="page page-equipo">
      <section className="equipo-hero">
        <EscudoHero nombre={estadisticas.equipo} escudo={estadisticas.escudo} />
        <div className="equipo-hero-copy">
          <h1 className="titulo-hero">{estadisticas.equipo}</h1>
          <span className="equipo-hero-overline">{estadisticas.liga}</span>
        </div>
      </section>
      <div className="stats-grid">
        {stats.map((stat) => (
          <div key={stat.label} className="stat-card">
            <span className="stat-label">{stat.label}</span>
            <span className="stat-valor">{stat.value}</span>
          </div>
        ))}
      </div>
      <section className="equipo-resultados">
        <header className="equipo-seccion-header">Resultados recientes</header>
        {tieneResultados ? (
          <div className="equipo-resultados-lista">
            {resultados_recientes.map((partido) => (
              <PartidoCard key={partido.id} partido={partido} />
            ))}
          </div>
        ) : (
          <div className="equipo-resultados-vacio">{MENSAJE_RESULTADOS_NO_DISPONIBLES}</div>
        )}
      </section>
    </div>
  )
}
