# Cambios y Pendientes - BalonPie

**Fecha:** 2026-06-26

---

## 1. Cambios implementados en este ciclo

### 1.1 Tarea 7 — Selector de temporada global

**Archivos:**
- `src/context/SeasonContext.tsx` ← nuevo
- `src/components/SeasonSelector.tsx` ← nuevo
- `src/components/SeasonSelector.css` ← nuevo
- `src/pages/Inicio.tsx`
- `src/pages/Tabla.tsx`
- `balonpie-api/main.py`

**Cambios:**
- `SeasonContext` maneja el estado global de temporada (2022 / 2023 / 2024, default 2024)
- `SeasonSelector` son tres botones segmentados (Archivo Black, activo en verde)
- Inicio y Tabla consumen `useSeason()` y pasan `?season=N` a todos los fetches
- Backend: endpoints `/proximos-partidos`, `/ultima-fecha`, `/tabla` aceptan `?season=N`
- Las claves de caché incluyen la temporada: `"tabla:2024"`, etc.
- Al cambiar temporada en Inicio: `fechaIndex` se resetea a 0 y `proximos` se limpia

### 1.2 Fix — Pantalla negra al cambiar temporada

**Archivos:**
- `src/pages/Inicio.tsx`

**Problema:** el backend devolvía `{"detail": "..."}` cuando fallaba. Ese objeto es truthy, pasaba el guard `{proximos && ...}` y al acceder a `proximos.navegacion.anterior` rompía con `TypeError`.

**Solución:** guard `res.ok` antes de llamar `setProximos`:
```tsx
fetch(url)
  .then((res) => (res.ok ? res.json() : null))
  .then((data) => { if (data) setProximos(data) })
```

### 1.3 Tarea 8 — Alineaciones tácticas en `/partido/:id`

**Archivos:**
- `src/components/AlineacionesCampo.tsx` ← nuevo
- `src/components/AlineacionesCampo.css` ← nuevo
- `src/pages/Partido.tsx`
- `balonpie-api/api_football.py`
- `balonpie-api/main.py`
- `src/api.ts`

**Cambios:**
- Nuevo endpoint backend: `GET /partido/{fixture_id}/lineups`
- `get_lineups(fixture_id)` en `api_football.py`: devuelve `{local, visitante}` con formación, once titular (nombre + pos + grid), suplentes y DT
- `AlineacionesCampo`: campo de fútbol verde con jugadores posicionados según grilla `col:row` de la API
  - Local (verde) en top 6%–47%, visitante (rojo) en top 53%–94%
  - `iniciales(nombre)` para el dot label, `apellido(nombre)` debajo del dot
  - Suplentes y DT en grilla de dos columnas debajo del campo
- Diseño elegido: opción híbrida compacta (campo táctico + suplentes en columnas)
- En `Partido.tsx`: nueva `SeccionAlineaciones` antes de Eventos

### 1.4 Tarea 9 — Buscador en tiempo real en /equipos

**Archivos:**
- `src/pages/Equipos.tsx`
- `src/pages/Pages.css`

**Cambios:**
- Estado `query` local en `Equipos`
- Filtro `Array.filter()` sobre los datos ya cargados, sin llamadas a la API
- `<input type="search">` con clase `equipos-buscador`
- Empty state "Sin resultados para X" cuando `grupos.length === 0` y `query` no está vacío

### 1.5 Visual polish — Diseño anti-"flowcodeado"

**Archivos:**
- `src/components/PartidoCard.css`
- `src/components/PartidoCard.tsx`
- `src/components/SeasonSelector.css`
- `src/pages/Pages.css`
- `src/pages/Partido.css`
- `src/pages/Equipo.css`
- `src/pages/Inicio.tsx`

**Diagnóstico:** la UI usaba `border-bottom: 1px solid #1e2530` para todo — cards de partido, separadores de sección, headers de competencia. Sin jerarquía visual, sin profundidad, sin uso del color de acento.

**Cambios:**

| Elemento | Antes | Después |
|---|---|---|
| `PartidoCard` | fila con `border-bottom` | card con `background / border / border-radius: 12px` + gap entre cards |
| Partido en vivo | texto dorado `EN VIVO` | borde izquierdo verde 3px + fondo verde tintado + badge pill verde |
| Badge "EN VIVO" | texto uppercase dorado en 4ta columna | pill verde (`color: #0D1117; background: var(--color-accent-green)`) |
| Section headers | `border-top + border-bottom`, texto al 45% opacity | `border-left: 3px solid verde` + texto al 70% opacity |
| Stats bar | 3px, sin radius | 4px, `border-radius` + gradiente verde |
| Stats equipo | grilla CSS con `border-right/border-bottom` (efecto spreadsheet) | cards individuales con `background + border + border-radius: 10px` |
| SeasonSelector activo | fondo gris neutro | fondo verde tintado + borde verde + texto verde |
| "Última fecha" en Inicio | `<h1>` suelto sin contexto | `<h2 className="inicio-seccion-titulo">` con `border-top` como separador |
| Competencia label | opacidad 45% | opacidad 60% |
| Grupos de partidos | `gap: 1rem` | `gap: 1.5rem` + `gap: 0.45rem` entre cards del mismo grupo |

---

## 2. Pendientes

### 2.1 Tarea 10 — Motion System (prioridad alta)

**Qué:** sistema de animaciones premium para que la UI "respire".

**Capas:**

1. **Framer Motion** (`npm install framer-motion`)
   - Transiciones de página: fade + slide al cambiar de ruta (`AnimatePresence`)
   - Scroll reveal: cards entran al viewport con `opacity 0→1` + `y 16px→0`, stagger 40ms entre items del grupo
   - Hover lift: `whileHover={{ y: -3 }}` en cards clickeables
   - Press feedback: `whileTap={{ scale: 0.97 }}` en todos los interactivos
   - Stats bar: se llena animada cuando entra al viewport (Framer `useInView`)

2. **Cursor spotlight** (JS puro)
   - `mousemove` listener en `App.tsx`
   - CSS vars `--mouse-x / --mouse-y` actualizadas en tiempo real
   - `radial-gradient` sutil en el fondo del shell centrado en las vars
   - Opacidad max ~15% — ambience, no distracción
   - Referencia visual: Linear.app, Vercel.com

3. **CSS animations**
   - Badge "EN VIVO": `@keyframes` pulse (escala + opacidad, 2s infinite)
   - Scrollbar webkit custom: thin, oscuro, coherente con la paleta
   - Dock items: micro-slide horizontal al hover

**Timing:**
- Micro-interacciones: 150–300ms
- Transiciones de página: 200ms
- `ease-out` al entrar, `ease-in` al salir
- Wrapper global para `prefers-reduced-motion`

**Archivos a tocar:**
- `src/hooks/useReducedMotion.ts` ← nuevo
- `src/components/PageTransition.tsx` ← nuevo
- `src/App.tsx` — cursor listener + PageTransition
- `src/App.css` — spotlight gradient + scrollbar + keyframes

---

### 2.2 Tarea 11 — Navegación "Pelota" (prioridad alta)

**Qué:** reemplazar el dock actual (sidebar en desktop, dock horizontal en mobile) por un botón flotante en forma de pelota de fútbol. Al hovear/tapear, se despliega el menú de navegación.

**Comportamiento:**
- **Desktop:** hover sobre la pelota → menú se despliega. Salir del área (pelota + menú) → cierra.
- **Mobile:** tap abre, tap fuera o segundo tap cierra.
- La sección activa aparece destacada dentro del menú.

**Diseño de la pelota:**
- SVG inline de pelota de fútbol (hexágonos clásicos) o esfera estilizada con acento verde
- Fixed, bottom-right: `bottom: 1.5rem; right: 1.5rem`
- Tamaño: ~56px desktop / ~52px mobile
- Sombra para elevación: `box-shadow: 0 4px 20px rgba(0,0,0,0.5)`
- Al abrirse: rotación suave `rotate(15deg)` con Framer Motion

**Menú desplegado (Opción B recomendada — speed-dial vertical):**
- Los ítems suben desde la pelota en stagger (40ms entre cada uno)
- Cada ítem: icono SVG + label
- Al cerrarse: se revierten en orden inverso
- Backdrop blur opcional para el fondo

**Alternativa descartada (Opción A — fan radial):** llamativa pero compleja en mobile y difícil de hacer accesible.

**Impacto en el layout:**
- `Dock.tsx` se reemplaza por `FootballFAB.tsx`
- El `app-shell` deja de tener `padding-left: 220px` en desktop → contenido a full ancho
- Agregar `padding-bottom: 5rem` en mobile para que el FAB no tape el final del scroll

**Archivos a crear/modificar:**
- `src/components/FootballFAB.tsx` ← nuevo
- `src/components/FootballFAB.css` ← nuevo
- `src/App.tsx` — reemplazar `<Dock>` por `<FootballFAB>`
- `src/App.css` — eliminar `padding-left` sidebar, ajustar padding-bottom

**Nota:** hacer brainstorming visual (mockup en browser) antes de implementar para definir el look de la pelota y la animación de apertura.

---

### 2.3 Pendientes de dataset

- completar seed de equipos corriendo `scripts/fetch_teams.py` contra las 4 competiciones
- revisar slugs y duplicados antes de dejar fijo

### 2.4 Pendientes de producto

- decidir comportamiento definitivo de `/proximos-partidos` (histórico 2024 vs futuro si se mejora el plan)
- evaluar tratamiento visual para standings de copas con grupos (Libertadores)
- el frontend no tiene suite de tests propia

---

## 3. Reglas importantes para no romper nada

- **No reiniciar el backend sin necesidad** — el caché en memoria se destruye y quema requests (100/día en Free)
- **No tocar nada fuera del alcance de la tarea definida**
- Para tareas visuales: hacer brainstorming/mockup primero, esperar aprobación, luego implementar
- Build check después de cada tarea: `npm run build` debe pasar sin errores
