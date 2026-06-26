import { BrowserRouter, Routes, Route } from "react-router-dom"
import Dock from "./components/Dock"
import Ticker from "./components/Ticker"
import Inicio from "./pages/Inicio"
import Tabla from "./pages/Tabla"
import Equipos from "./pages/Equipos"
import Equipo from "./pages/Equipo"
import Partido from "./pages/Partido"
import { SeasonProvider } from "./context/SeasonContext"
import "./App.css"

export default function App() {
  return (
    <BrowserRouter>
      <SeasonProvider>
        <Ticker />
        <div className="app-shell">
          <Dock />
          <main className="app-main">
            <div className="app-content">
              <Routes>
                <Route path="/" element={<Inicio />} />
                <Route path="/tabla" element={<Tabla />} />
                <Route path="/equipos" element={<Equipos />} />
                <Route path="/equipo/:nombre" element={<Equipo />} />
                <Route path="/partido/:id" element={<Partido />} />
              </Routes>
            </div>
          </main>
        </div>
      </SeasonProvider>
    </BrowserRouter>
  )
}
