(define (domain industrial-safety)
  (:requirements :strips :typing)

  (:predicates
    ;; Hazard conditions
    (temperature-high)
    (humidity-high)
    (fire-detected)
    (motion-detected)
    (overcapacity-zone1)
    (overcapacity-zone2)
    (emergency-stop)

    ;; System states
    (safe)
    (motor-on)
    (motor-off)
    (fan-on)
    (fan-off)
  )

  ;; Derive safe condition if no blocking hazards are present
  (:action detect-safe
    :precondition (and
      (not (motion-detected))
      (not (fire-detected))
      (not (overcapacity-zone1))
      (not (overcapacity-zone2))
      (not (emergency-stop))
    )
    :effect (safe)
  )

  ;; Turn motor ON if system is safe
  (:action turn-on-motor
    :precondition (safe)
    :effect (and
      (motor-on)
      (not (motor-off))
    )
  )

  ;; Turn motor OFF if any blocking hazard is present
  (:action turn-off-motor
    :precondition (or
      (motion-detected)
      (fire-detected)
      (overcapacity-zone1)
      (overcapacity-zone2)
      (emergency-stop)
    )
    :effect (and
      (motor-off)
      (not (motor-on))
    )
  )

  ;; Turn fan ON when temperature, humidity, or fire is high
  (:action turn-on-fan
    :precondition (or
      (temperature-high)
      (humidity-high)
      (fire-detected)
    )
    :effect (and
      (fan-on)
      (not (fan-off))
    )
  )

  ;; Turn fan OFF when all fan-related hazards are gone
  (:action turn-off-fan
    :precondition (and
      (not (temperature-high))
      (not (humidity-high))
      (not (fire-detected))
    )
    :effect (and
      (fan-off)
      (not (fan-on))
    )
  )
)
