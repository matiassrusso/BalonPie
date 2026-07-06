import { AnimatePresence, LazyMotion, domAnimation, useMotionValue, useSpring } from "framer-motion"
import { useEffect } from "react"
import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom"
import Dock from "./components/Dock"
import PageTransition from "./components/PageTransition"
import Ticker from "./components/Ticker"
import Inicio from "./pages/Inicio"
import Tabla from "./pages/Tabla"
import Equipos from "./pages/Equipos"
import Equipo from "./pages/Equipo"
import Partido from "./pages/Partido"
import { SeasonProvider } from "./context/SeasonContext"
import { useReducedMotion } from "./hooks/useReducedMotion"
// PROTOTYPE — Tarea 11: comparar variantes del Football FAB. Ver football-fab-prototype/NOTES.md.
import FootballFabPrototype from "./components/football-fab-prototype/FootballFabPrototype"
import "./App.css"

function useCursorSpotlight() {
  const reducedMotion = useReducedMotion()
  const mouseX = useMotionValue(0)
  const mouseY = useMotionValue(0)
  const springX = useSpring(mouseX, { duration: 0.4, bounce: 0 })
  const springY = useSpring(mouseY, { duration: 0.4, bounce: 0 })

  useEffect(() => {
    if (reducedMotion) return

    const onMouseMove = (e: MouseEvent) => {
      mouseX.set(e.clientX)
      mouseY.set(e.clientY)
    }

    window.addEventListener("mousemove", onMouseMove)
    return () => window.removeEventListener("mousemove", onMouseMove)
  }, [reducedMotion, mouseX, mouseY])

  useEffect(() => {
    if (reducedMotion) return

    const unsubX = springX.on("change", (latest) => {
      document.documentElement.style.setProperty("--mouse-x", `${latest}px`)
    })
    const unsubY = springY.on("change", (latest) => {
      document.documentElement.style.setProperty("--mouse-y", `${latest}px`)
    })
    return () => {
      unsubX()
      unsubY()
    }
  }, [reducedMotion, springX, springY])
}

function AnimatedRoutes() {
  const location = useLocation()

  return (
    <AnimatePresence mode="wait">
      <PageTransition key={location.pathname}>
        <Routes location={location}>
          <Route path="/" element={<Inicio />} />
          <Route path="/tabla" element={<Tabla />} />
          <Route path="/equipos" element={<Equipos />} />
          <Route path="/equipo/:nombre" element={<Equipo />} />
          <Route path="/partido/:id" element={<Partido />} />
        </Routes>
      </PageTransition>
    </AnimatePresence>
  )
}

export default function App() {
  useCursorSpotlight()

  return (
    <BrowserRouter>
      <SeasonProvider>
        <Ticker />
        <LazyMotion features={domAnimation}>
          <div className="app-shell">
            <Dock />
            <main className="app-main">
              <div className="app-content">
                <AnimatedRoutes />
              </div>
            </main>
          </div>
        </LazyMotion>
        {import.meta.env.DEV && <FootballFabPrototype />}
      </SeasonProvider>
    </BrowserRouter>
  )
}
