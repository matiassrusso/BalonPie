export const API_URL = import.meta.env.VITE_API_URL

export interface Partido {
  id: number
  fecha: string
  estado: string
  minuto: number | null
  competencia: string
  equipo_local: string
  equipo_local_slug: string | null
  escudo_local: string
  equipo_visitante: string
  equipo_visitante_slug: string | null
  escudo_visitante: string
  goles_local: number | null
  goles_visitante: number | null
}

export interface EventoPartido {
  minuto: number
  tipo: string
  detalle: string
  equipo: string
  jugador: string
}

export interface PartidoDetalle extends Partido {
  eventos: EventoPartido[]
  estadisticas: Record<string, Record<string, string | number>>
  actualizado_hace: number
  stale: boolean
}

export interface PosicionTabla {
  posicion: number
  equipo: string
  slug: string | null
  escudo: string
  puntos: number
  jugados: number
  ganados: number
  empatados: number
  perdidos: number
  diferencia_goles: number
  forma: string[]
}

export interface EquipoResumen {
  nombre: string
  slug: string
  escudo: string
  competencia: string
}

export interface EstadisticasEquipo {
  equipo: string
  escudo: string
  liga: string
  partidos_jugados: number
  ganados: number
  empatados: number
  perdidos: number
  goles_a_favor: number
  goles_en_contra: number
  forma: string[]
}

export interface PerfilEquipo {
  estadisticas: EstadisticasEquipo
  resultados_recientes: Partido[]
  actualizado_hace: number
  stale: boolean
}

export interface FechaActual {
  indice: number
  nombre: string
}

export interface NavegacionFecha {
  anterior: number | null
  siguiente: number | null
  total: number
}

export interface JugadorLineup {
  nombre: string
  pos: string
  grid: string | null
}

export interface EquipoLineup {
  equipo: string
  formacion: string
  once: JugadorLineup[]
  suplentes: string[]
  dt: string | null
}

export interface LineupsPartido {
  local: EquipoLineup | null
  visitante: EquipoLineup | null
}

export interface ProximosPartidosResponse {
  partidos: Partido[]
  fecha_actual: FechaActual
  navegacion: NavegacionFecha
  actualizado_hace: number
  stale: boolean
}
