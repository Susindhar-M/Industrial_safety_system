######################################################################################################
# Authors : Susindhar Manivasagan, Raksha Nagendra, Mansi Sharad Dongare
######################################################################################################
# Do not modify
# planner/problem_generator.py

def generate_problem_file(state):
    with open("planning/problem.pddl", "w") as f:
        f.write("(define (problem industrial-safety)\n")
        f.write("  (:domain industrial-safety)\n")
        f.write("  (:init\n")

        # Hazard predicates
        if state.get("temperature_high"):
            f.write("    (temperature-high)\n")
        if state.get("humidity_high"):
            f.write("    (humidity-high)\n")
        if state.get("fire_detected"):
            f.write("    (fire-detected)\n")
        if state.get("motion_detected"):
            f.write("    (motion-detected)\n")
        if state.get("overcapacity_zone1"):
            f.write("    (overcapacity-zone1)\n")
        if state.get("overcapacity_zone2"):
            f.write("    (overcapacity-zone2)\n")
        if state.get("emergency_active"):
            f.write("    (emergency-stop)\n")

        f.write("  )\n")

        # Motor and fan goals together
        if (
            state.get("emergency_active") or
            state.get("motion_detected") or
            state.get("fire_detected") or
            state.get("overcapacity_zone1") or
            state.get("overcapacity_zone2")
        ):
            f.write("  (:goal (and (motor-off)")
        else:
            f.write("  (:goal (and (motor-on)")

        # Fan should be on during any of these
        if state.get("fire_detected") or state.get("temperature_high") or state.get("humidity_high"):
            f.write(" (fan-on)))\n")
        else:
            f.write(" (fan-off)))\n")

        f.write(")\n")
