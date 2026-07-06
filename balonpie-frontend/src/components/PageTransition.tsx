import { m } from "framer-motion"
import type { ReactNode } from "react"
import { useReducedMotion } from "../hooks/useReducedMotion"

const EASE_OUT: [number, number, number, number] = [0.23, 1, 0.32, 1]

export default function PageTransition({ children }: { readonly children: ReactNode }) {
  const reduced = useReducedMotion()

  if (reduced) {
    return (
      <m.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 0.15, ease: EASE_OUT }}
      >
        {children}
      </m.div>
    )
  }

  return (
    <m.div
      initial={{ opacity: 0, transform: "translateY(8px)" }}
      animate={{ opacity: 1, transform: "translateY(0px)" }}
      exit={{ opacity: 0, transform: "translateY(-8px)" }}
      transition={{ duration: 0.18, ease: EASE_OUT }}
    >
      {children}
    </m.div>
  )
}
