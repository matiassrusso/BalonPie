# Prototipo — Football FAB (Tarea 11)

**Pregunta:** ¿qué patrón de menú usa el FAB de navegación — fan radial (A) o stack vertical (B)?

**Cómo probarlo:** `npm run dev` en `balonpie-frontend/`, abrir cualquier ruta real (ej. `/`), hover
(desktop) o tap (mobile) sobre la pelota en la esquina inferior derecha. Alternar variante con la
barra flotante negra abajo-centro (flechas, o `←`/`→` de teclado), o manualmente con `?fab=A` / `?fab=B`
en la URL.

**Veredicto:** _(completar después de decidir)_

**Al cerrar:** borrar este folder completo (`football-fab-prototype/`) y el mount condicional en
`App.tsx` (`import.meta.env.DEV && <FootballFabPrototype />`). Reimplementar la variante ganadora
como componente real (`FootballFAB.tsx`) siguiendo el plan de ESTADO.md — este código es de prueba,
sin manejo de teclado/foco ni `prefers-reduced-motion`.
