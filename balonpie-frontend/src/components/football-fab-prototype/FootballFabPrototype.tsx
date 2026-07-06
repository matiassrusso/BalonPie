// PROTOTYPE — Tarea 11. Orquestador: lee ?fab=A|B y monta la variante + el switcher.
// Solo se monta en dev (ver App.tsx: import.meta.env.DEV). Borrar este folder completo
// junto con el mount en App.tsx cuando se elija variante ganadora (ver NOTES.md).
import { useSearchParams } from "react-router-dom"
import FootballFabPrototypeA from "./FootballFabPrototypeA"
import FootballFabPrototypeB from "./FootballFabPrototypeB"
import FootballFabPrototypeSwitcher from "./FootballFabPrototypeSwitcher"

export default function FootballFabPrototype() {
  const [searchParams] = useSearchParams()
  const variant = searchParams.get("fab") === "B" ? "B" : "A"

  return (
    <>
      {variant === "A" ? <FootballFabPrototypeA /> : <FootballFabPrototypeB />}
      <FootballFabPrototypeSwitcher current={variant} />
    </>
  )
}
