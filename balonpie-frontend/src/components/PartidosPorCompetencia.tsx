import type { Partido } from "../api"
import PartidoCard from "./PartidoCard"

function formatearDia(fechaIso: string): string {
  const fecha = new Date(fechaIso)
  return fecha.toLocaleDateString("es-AR", { day: "2-digit", month: "2-digit" })
}

function agruparPorCompetencia(partidos: readonly Partido[]): Array<{ competencia: string; fecha: string; partidos: Partido[] }> {
  const grupos = new Map<string, { competencia: string; fecha: string; partidos: Partido[] }>()

  for (const partido of partidos) {
    const existente = grupos.get(partido.competencia)
    if (existente) {
      existente.partidos.push(partido)
      continue
    }

    grupos.set(partido.competencia, {
      competencia: partido.competencia,
      fecha: formatearDia(partido.fecha),
      partidos: [partido],
    })
  }

  return Array.from(grupos.values())
}

export default function PartidosPorCompetencia({ partidos }: { partidos: readonly Partido[] }) {
  const grupos = agruparPorCompetencia(partidos)

  return (
    <div className="partidos-bloques">
      {grupos.map((grupo) => (
        <section key={grupo.competencia} className="partidos-grupo">
          <header className="partidos-grupo-header">
            <span className="partidos-grupo-titulo">{grupo.competencia}</span>
            <span className="partidos-grupo-fecha">{grupo.fecha}</span>
          </header>
          <div className="partidos-grupo-lista">
            {grupo.partidos.map((partido) => (
              <PartidoCard key={partido.id} partido={partido} />
            ))}
          </div>
        </section>
      ))}
    </div>
  )
}
