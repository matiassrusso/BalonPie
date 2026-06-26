# ESTADO DE BALONPIE

**Fecha de actualización:** 2026-06-26

## 1. Estado general del proyecto

BalonPie es un proyecto full-stack funcional con:

- `balonpie-api/`: backend FastAPI que consume API-Football, normaliza datos y expone endpoints propios.
- `balonpie-frontend/`: app React + TypeScript + Vite con navegación completa entre todas las pantallas.
- `output/`: capturas de QA visual de las tareas de rediseño.

Lo que hoy **funciona** end-to-end:

- ticker superior full-width con última fecha en tiempo real
- sidebar fijo en desktop (220px) / dock top en mobile
- página de Inicio con navegación histórica por jornadas, selector de temporada (2022/2023/2024)
- tabla de posiciones de Liga Profesional con chips de forma
- listado de equipos con buscador en tiempo real (filtro sin llamadas a la API)
- perfil de equipo con stats y resultados recientes
- detalle de partido: header con score, alineaciones en campo táctico, timeline de eventos, estadísticas comparativas con barras
- selector de temporada global via SeasonContext (2022/2023/2024)
- build del frontend limpio: 46 módulos
- 47 tests del backend pasando

Contexto de datos importante:

- el plan Free de API-Football **solo da acceso a seasons 2022, 2023 y 2024**
- la temporada actualmente en curso es 2026 (bloqueada en Free)
- `/proximos-partidos` navega jornadas históricas de 2024, no partidos próximos reales
- `/fixtures/lineups` está disponible en Free: devuelve formación, 11 titulares con posición y grilla táctica, DT, suplentes
- el caché es **en memoria** — reiniciar el backend lo destruye y quema requests del día (límite: 100/día en Free)

Documentos útiles:

- `PLAN_MEJORAS.md`: investigación de producto/datos y backlog de expansión
- `CAMBIOS_Y_PENDIENTES.md`: resumen del ciclo anterior

---

## 2. Tareas de rediseño visual

### Tabla completa de tareas

| Tarea | Estado | Detalle |
|---|---|---|
| Tarea 1 — Layout global y navegación | ✅ Aprobada | Sidebar fijo izquierdo desde `960px`, ticker full-width, dock mobile. |
| Tarea 2 — `PartidoCard` compacta | ✅ Aprobada | Fila densa tipo Promiedos/ElNine, marcador central en Archivo Black, headers por competición. |
| Tarea 3 — Página de Equipos | ✅ Aprobada | Lista compacta estilo Sofascore con agrupación por competición, sin cards grandes. |
| Tarea 4 — Tabla de posiciones | ✅ Aprobada | Tabla compacta, header editorial, escudo inline, chips de forma, fila activa desde `/equipo/:slug`. |
| Tarea 5 — Perfil de equipo (`/equipo/:nombre`) | ✅ Implementada | Header compacto, escudo grande, stats densas, resultados recientes con `PartidoCard`, empty state. |
| Tarea 6 — Detalle de partido (`/partido/:id`) | ✅ Implementada | Header con escudos grandes y score en Archivo Black, timeline de eventos 3 columnas, barras comparativas. |
| Tarea 7 — Selector de temporada | ✅ Implementada | SeasonContext global, SeasonSelector en Inicio y Tabla. Backend parametrizado con `?season=N`. |
| Tarea 8 — Alineaciones en `/partido/:id` | ✅ Implementada | Campo táctico visual, jugadores posicionados por grilla `col:row`, suplentes y DT debajo. |
| Tarea 9 — Buscador de equipos | ✅ Implementada | Filtro en tiempo real por nombre, sin llamadas extra a la API. Empty state cuando no hay resultados. |
| **Visual polish** — Diseño anti-flowcode | ✅ Implementada | Cards de partido con fondo/borde/radius, acento verde en live matches, section headers con borde izquierdo verde, stats como cards individuales, SeasonSelector en verde activo, sección "Última fecha" con header propio. |

### Archivos frontend tocados (estado actual)

- `src/App.tsx`, `src/App.css`
- `src/context/SeasonContext.tsx` ← nuevo (Tarea 7)
- `src/components/Dock.tsx`, `src/components/Dock.css`
- `src/components/PartidoCard.tsx`, `src/components/PartidoCard.css`
- `src/components/PartidosPorCompetencia.tsx`
- `src/components/SeasonSelector.tsx`, `src/components/SeasonSelector.css` ← nuevo (Tarea 7)
- `src/components/AlineacionesCampo.tsx`, `src/components/AlineacionesCampo.css` ← nuevo (Tarea 8)
- `src/pages/Inicio.tsx`
- `src/pages/Tabla.tsx`
- `src/pages/Equipos.tsx`
- `src/pages/Equipo.tsx`, `src/pages/Equipo.css`
- `src/pages/Partido.tsx`, `src/pages/Partido.css`
- `src/pages/Pages.css`
- `src/api.ts`

---

## 3. Bugs conocidos y deuda técnica

### Bugs conocidos

| Bug | Estado |
|---|---|
| Escudos rotos en `PartidoCard` | ✅ Corregido — fallback por inicial del equipo |
| Build fallaba con error `vite:build-html` | ✅ Corregido |
| Nombre "Central Cordoba..." truncado en header de `/partido/:id` | ✅ Corregido — `width: 100%` sin `max-width` |
| Pantalla negra al cambiar temporada | ✅ Corregido — guard `res.ok` antes de `setProximos` |

### Deuda técnica pendiente

- el frontend **no tiene suite de tests propia**; validación actual: `lint + build + QA visual`
- `/proximos-partidos` tiene semántica histórica, no real-time — sin solución en plan Free
- el seed de equipos necesita expansión y limpieza desde `scripts/fetch_teams.py`
- no hay tratamiento visual para standings de copas con grupos (ej: Libertadores)
- `output/` tiene capturas de QA no curadas ni documentadas formalmente

### Riesgos funcionales

- el backend usa caché en memoria: **reiniciar el servidor destruye el caché y quema requests del día** (100/día en Free)
- si la API externa cambia el shape de los campos, el frontend depende de la normalización del backend
- el primer request en frío a `/equipo/{nombre}` o `/partido/{fixture_id}` puede devolver `503` si la llamada externa falla

---

## 4. Estado del backend

### Endpoints actuales

| Endpoint | Descripción |
|---|---|
| `GET /health` | healthcheck |
| `GET /proximos-partidos?fecha=N&season=S` | jornadas históricas de Liga Profesional |
| `GET /ultima-fecha?season=S` | últimos fixtures de todas las competiciones soportadas |
| `GET /tabla?season=S` | tabla de posiciones Liga Profesional |
| `GET /equipos` | listado de equipos del seed actual |
| `GET /equipo/{nombre}` | estadísticas + resultados recientes |
| `GET /partido/{fixture_id}` | datos + eventos + estadísticas comparativas |
| `GET /partido/{fixture_id}/lineups` | alineaciones tácticas (nuevo en Tarea 8) |

### Tests

```
47 passed in ~0.6s
```

---

## 5. Estado del build

### Frontend

- `npm run lint` → **OK**
- `npm run build` → **OK**

```
vite v8.0.16 building client environment for production...
✓ 46 modules transformed.
dist/assets/index.css   18.86 kB │ gzip: 4.02 kB
dist/assets/index.js   253.32 kB │ gzip: 79.60 kB
✓ built in 143ms
```

### Backend

- `pytest` → **OK** (47 passed)

---

## 6. Próximas tareas — en orden de prioridad

---

### Tarea 10 — Motion System ("tope de gama")

**Objetivo:** que la UI se sienta viva, premium y con carácter propio. No es decoración — cada animación tiene un propósito.

**Capas de implementación:**

#### Capa 1 — Framer Motion (librería)
Instalar: `npm install framer-motion`

- **Transiciones entre páginas:** al cambiar de ruta, fade + slide sutil (100–200ms). Usando `AnimatePresence` + `motion.div` en el layout.
- **Scroll reveal en cards:** cada `PartidoCard` y fila de equipo entra al viewport con `opacity: 0 → 1` + `y: 16px → 0`. Stagger de 40ms entre cards del mismo grupo.
- **Hover en cards clickeables:** `whileHover={{ y: -3, boxShadow: "..." }}` — lift suave.
- **Press feedback:** `whileTap={{ scale: 0.97 }}` en todos los elementos clickeables.
- **Stats bar en Partido:** la barra de estadísticas se anima llenándose cuando el elemento entra en viewport (triggeado por `useInView` de Framer Motion).

#### Capa 2 — Cursor spotlight (JS puro)
Un gradiente radial sutil en el fondo que sigue el cursor del mouse. Referencia: Linear.app, Vercel.

Implementación:
- Event listener `mousemove` en `App.tsx`
- CSS variable `--mouse-x` / `--mouse-y` actualizadas en tiempo real
- Fondo del `app-shell` con `radial-gradient` centrado en esas vars
- Glow muy sutil (max 15–20% opacity) — ambience, no distracción

#### Capa 3 — CSS animations
- **Badge "EN VIVO":** `@keyframes` pulse (opacidad + scale suave, 2s infinite)
- **Scrollbar custom:** webkit thin dark scrollbar coherente con la paleta
- **Dock items:** micro-slide `x: 4px` al hover (si se usa Framer) o CSS `transform: translateX`

**Timing guidelines (de la skill ui-ux-pro-max):**
- Micro-interacciones: 150–300ms
- Transiciones de página: 200ms max
- `ease-out` para entrar, `ease-in` para salir
- Respetar `prefers-reduced-motion` con un wrapper global

**Archivos a crear/modificar:**
- `src/hooks/useReducedMotion.ts` — wrapper de la media query
- `src/components/PageTransition.tsx` — wrapper de AnimatePresence
- `src/components/MotionCard.tsx` — PartidoCard wrapeada con motion
- `src/App.tsx` — cursor spotlight listener + CSS vars
- `src/App.css` — spotlight gradient + scrollbar custom + keyframes pulse

---

### Tarea 11 — Navegación "Pelota" (Football FAB)

**Objetivo:** reemplazar la navegación actual (sidebar en desktop, dock horizontal en mobile) por un botón flotante en forma de pelota de fútbol. Al posarse sobre él, se despliega el menú con todas las secciones.

**Comportamiento:**

- **Desktop (hover):** al pasar el cursor sobre la pelota, el menú se despliega. Al salir del área (pelota + menú), se cierra.
- **Mobile (tap):** primer tap abre, segundo tap o tap fuera cierra.
- **Estado activo:** la sección actual se indica dentro del menú desplegado.

**Diseño de la pelota:**

La pelota es el único elemento de navegación siempre visible:
- SVG de pelota de fútbol (hexágonos blancos y negros) o pelota stylizada con el acento verde del brand
- Tamaño: ~56px en desktop, ~52px en mobile
- Posición: fixed, esquina inferior derecha (bottom: 1.5rem, right: 1.5rem)
- Sombra sutil para elevación

**Diseño del menú desplegado:**

Dos opciones a definir antes de implementar (brainstorming):

- **Opción A — Fan radial:** los ítems del menú se despliegan en arco sobre la pelota, como pétalos. Muy llamativo, difícil en mobile.
- **Opción B — Stack vertical:** el menú sube verticalmente desde la pelota, como un FAB speed-dial de Material. Más limpio y accesible.

**Recomendación:** Opción B (speed-dial) para primera versión. Más predecible, mejor soporte de teclado, funciona igual en mobile y desktop.

**Ítems del menú:** Inicio, Tabla, Equipos (los mismos del dock actual)

**Animación:**
- Los ítems aparecen en stagger (Framer Motion) desde la pelota hacia arriba
- La pelota rota ligeramente al abrirse (transform: rotate 15deg)
- Al cerrarse, se revierten en orden inverso

**Impacto en el layout:**
- Eliminar el sidebar/dock actual (`Dock.tsx` se reemplaza o se convierte en el menú interno)
- El `app-shell` ya no necesita `padding-left: var(--sidebar-width)` en desktop
- El contenido ocupa todo el ancho — el contenido gana espacio en desktop
- Agregar `padding-bottom` en mobile para que el FAB no tape el final del scroll

**Archivos a crear/modificar:**
- `src/components/FootballFAB.tsx` — componente principal (pelota + menú)
- `src/components/FootballFAB.css` — estilos del FAB y menú
- `src/App.tsx` — reemplazar `<Dock>` por `<FootballFAB>`
- `src/App.css` — eliminar `padding-left` del sidebar, ajustar padding-bottom

**SVG de la pelota:**
Usar un SVG inline de pelota de fútbol estilizada. El patrón clásico de hexágonos en blanco/negro se puede simplificar a una esfera oscura con parches verdes (coherente con el brand). Alternativamente: esfera con el logo "BP" adentro que se transforma al abrir.

---

## 7. Comandos para levantar el proyecto

### Backend

```powershell
# Desde balonpie\balonpie-api
.\venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000
```

```powershell
# Tests
.\venv\Scripts\python.exe -m pytest
```

### Frontend

```powershell
# Desde balonpie\balonpie-frontend
npm run dev
```

```powershell
# Checks
npm run lint
npm run build
```

### URLs locales

- Backend: `http://127.0.0.1:8000`
- Frontend: `http://localhost:5173` (dev) / `http://127.0.0.1:4173` (preview)

### Rutas clave para QA visual

- `http://localhost:5173/` — Inicio
- `http://localhost:5173/tabla` — Tabla de posiciones
- `http://localhost:5173/equipos` — Listado de equipos
- `http://localhost:5173/equipo/river-plate` — Perfil de equipo
- `http://localhost:5173/partido/1158660` — River 3-0 Central Córdoba (fixture con datos completos)

---

## 8. Prompt para retomar en la próxima sesión

```
Continuamos con BalonPie. Leé ESTADO.md para contexto completo.

Estado al retomar:
- Tareas 1 a 9 del rediseño visual completadas, más un pase de polish visual
- SeasonContext global (2022/2023/2024), AlineacionesCampo, buscador en tiempo real
- PartidoCard como card real (fondo/borde/radius), section headers con acento verde, stats como cards
- Build limpio: 46 módulos, 18.86 KB CSS, 253.32 KB JS
- Backend: 47 tests pasando, caché en memoria (no reiniciar sin necesidad — 100 req/día Free)
- API-Football plan Free: acceso a seasons 2022-2024 únicamente

Próximas tareas (en orden):
1. Tarea 10 — Motion System: Framer Motion (transiciones de página, scroll reveal, hover/tap), cursor spotlight (gradiente radial que sigue el mouse), CSS animations (badge live pulsante, scrollbar custom)
2. Tarea 11 — Navegación "Pelota": FAB flotante en forma de pelota de fútbol que al hover/tap despliega el menú. Opción B (speed-dial vertical) recomendada para primera versión. Reemplaza el Dock actual.

Para la Tarea 10, arrancar instalando framer-motion y hacer primero las transiciones de página, después scroll reveal, después cursor.
Para la Tarea 11, hacer un brainstorming visual antes de implementar (ver opciones de menú).

No toques nada fuera del alcance de la tarea que definamos.
No reinicies el backend sin necesidad — el caché en memoria se destruye y quema requests.
```
