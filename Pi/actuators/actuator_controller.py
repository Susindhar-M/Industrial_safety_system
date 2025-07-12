def control_actuators(plan, relay, lcd):
    motor_on = False
    fan_on = False

    for action in plan:
        if "turn-on-motor" in action:
            motor_on = True
        if "turn-off-motor" in action:
            motor_on = False
        if "turn-on-fan" in action:
            fan_on = True
        if "turn-off-fan" in action:
            fan_on = False

    if motor_on:
        relay.on(1)
    else:
        relay.off(1)

    if fan_on:
        relay.on(2)
    else:
        relay.off(2)

    lcd.display(f"Motor: {'ON' if motor_on else 'OFF'}", f"Fan: {'ON' if fan_on else 'OFF'}")
