import { SEASONS, useSeason } from "../context/SeasonContext"
import "./SeasonSelector.css"

export default function SeasonSelector() {
  const { season, setSeason } = useSeason()
  return (
    <div className="season-selector">
      {SEASONS.map((s) => (
        <button
          key={s}
          type="button"
          className={`season-btn${s === season ? " season-btn-activo" : ""}`}
          onClick={() => setSeason(s)}
        >
          {s}
        </button>
      ))}
    </div>
  )
}
