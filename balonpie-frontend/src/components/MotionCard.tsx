import { m } from "framer-motion"
import type { ReactNode } from "react"
import { useReducedMotion } from "../hooks/useReducedMotion"

const MAX_STAGGER_DELAY = 0.32
const EASE_OUT: [number, number, number, number] = [0.23, 1, 0.32, 1]

export default function MotionCard({
  children,
  index = 0,
}: {
  readonly children: ReactNode
  readonly index?: number
}) {
  const reduced = useReducedMotion()
  const delay = Math.min(index * 0.04, MAX_STAGGER_DELAY)

  if (reduced) {
    return (
      <m.div
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true, margin: "-40px" }}
        transition={{ duration: 0.2, delay, ease: EASE_OUT }}
      >
        {children}
      </m.div>
    )
  }

  return (
    <m.div
      initial={{ opacity: 0, transform: "translateY(16px)" }}
      whileInView={{ opacity: 1, transform: "translateY(0px)" }}
      viewport={{ once: true, margin: "-40px" }}
      // ponytail: whileHover/whileTap keep the y/scale shorthand (not full transform strings)
      // because both can be active at once (mouse held down while hovering) and Framer only
      // composes simultaneous transforms through its own x/y/scale motion values, not raw strings.
      whileHover={{ y: -3 }}
      whileTap={{ scale: 0.97 }}
      transition={{ duration: 0.25, delay, ease: EASE_OUT }}
    >
      {children}
    </m.div>
  )
}
