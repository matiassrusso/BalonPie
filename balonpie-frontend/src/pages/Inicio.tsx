import { useEffect, useState } from "react"
import { API_URL, type Partido, type ProximosPartidosResponse } from "../api"
import PartidosPorCompetencia from "../components/PartidosPorCompetencia"
import SeasonSelector from "../components/SeasonSelector"
import { useSeason } from "../context/SeasonContext"
import "./Pages.css"

export default function Inicio() {
  const { season } = useSeason()
  const [proximos, setProximos] = useState<ProximosPartidosResponse | null>(null)
  const [ultimaFecha, setUltimaFecha] = useState<Partido[]>([])
  const [fechaIndex, setFechaIndex] = useState(0)

  useEffect(() => {
    setFechaIndex(0)
    setProximos(null)
  }, [season])

  useEffect(() => {
    fetch(`${API_URL}/proximos-partidos?fecha=${fechaIndex}&season=${season}`)
      .then((res) => (res.ok ? res.json() : null))
      .then((data: ProximosPartidosResponse | null) => { if (data) setProximos(data) })
  }, [fechaIndex, season])

  useEffect(() => {
    fetch(`${API_URL}/ultima-fecha?season=${season}`)
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => { if (data) setUltimaFecha(data.partidos) })
  }, [season])

  return (
    <div className="page page-inicio">
      <div className="page-header">
        <h1>Temporada {season}</h1>
        <SeasonSelector />
      </div>
      {proximos && (
        <div className="fecha-navegacion">
          <button
            type="button"
            className="fecha-nav-boton"
            onClick={() => {
              if (proximos.navegacion.anterior !== null) {
                setFechaIndex(proximos.navegacion.anterior)
              }
            }}
            disabled={proximos.navegacion.anterior === null}
          >
            Anterior
          </button>
          <div className="fecha-navegacion-info">
            <span className="fecha-navegacion-label">{proximos.fecha_actual.nombre}</span>
            <span className="fecha-navegacion-total">
              Fecha {proximos.fecha_actual.indice + 1} de {proximos.navegacion.total}
            </span>
          </div>
          <button
            type="button"
            className="fecha-nav-boton"
            onClick={() => {
              if (proximos.navegacion.siguiente !== null) {
                setFechaIndex(proximos.navegacion.siguiente)
              }
            }}
            disabled={proximos.navegacion.siguiente === null}
          >
            Siguiente
          </button>
        </div>
      )}
      {proximos ? <PartidosPorCompetencia partidos={proximos.partidos} /> : null}
      <h2 className="inicio-seccion-titulo">Última fecha</h2>
      <PartidosPorCompetencia partidos={ultimaFecha} />
    </div>
  )
}
