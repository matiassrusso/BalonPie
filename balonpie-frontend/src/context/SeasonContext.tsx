import { createContext, useContext, useState } from "react"

export const SEASONS = [2022, 2023, 2024] as const
export type Season = (typeof SEASONS)[number]

const SeasonContext = createContext<{
  season: Season
  setSeason: (s: Season) => void
}>({ season: 2024, setSeason: () => {} })

export function SeasonProvider({ children }: { readonly children: React.ReactNode }) {
  const [season, setSeason] = useState<Season>(2024)
  return <SeasonContext.Provider value={{ season, setSeason }}>{children}</SeasonContext.Provider>
}

export function useSeason() {
  return useContext(SeasonContext)
}
