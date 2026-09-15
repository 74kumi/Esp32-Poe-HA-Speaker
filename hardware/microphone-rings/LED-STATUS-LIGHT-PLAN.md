# Microphone-ring status / listening light plan

## Purpose

Future microphone-array rings should reserve support for visible status lighting behind the ceiling-speaker grille. The primary use is a subtle **listening indicator** so a person in the room can tell when the microphone system is active.

The lighting feature belongs to the microphone-ring assembly, not the main PoE speaker PCB. Different ring diameters should use the same control concept wherever practical.

This is a planning document. LED part selection, LED count, driver choice, brightness, diffuser behavior, current budget, and firmware behavior are not yet validated.

## Main-board design-freeze rule

The Rev E / Rev F main PoE speaker board should not be redesigned for optional ring features unless the existing expansion interface cannot safely support a required function.

For microphone-ring lighting, the existing J4 interface is the intended path. J4 already exposes:

- 3.3 V and grounds;
- `I2C_SDA` and `I2C_SCL`;
- `RING_GPIO_SPARE`;
- the PDM microphone clock/data signals required by the microphone ring.

Optional user-interface features should therefore be implemented on the ring using J4 before considering changes to the main board.

A proposed main-board change for a ring feature should identify:

1. the feature that cannot be implemented through the existing interface;
2. the electrical, safety, bandwidth, power, or reliability reason it cannot be implemented there;
3. the minimum main-board change required; and
4. how the change will be verified.

Convenience alone is not sufficient reason to reopen the main-board design.

## Intended visual states

The exact colors and behavior remain firmware/UI decisions, but the ring should be capable of communicating a small set of obvious states.

| State | Example indication | Intent |
| --- | --- | --- |
| Listening / microphones active | soft blue or white | visible privacy/status indication |
| Muted / privacy mode | red | microphones intentionally disabled |
| Boot / setup / provisioning | amber, purple, or slow pulse | temporary service state |
| Fault / attention required | red or amber pattern | diagnostic indication |
| Normal idle | off by default | avoid unnecessary room light |

The final behavior should favor clear status communication over decorative effects.

## Electrical approach

Do not assume that the ESP32 or J4 spare GPIO will directly drive the LEDs.

The preferred architecture is for the microphone ring to contain its own small LED-control stage, using either:

- an I2C LED driver;
- a small ring-local controller; or
- another low-current control method compatible with the existing J4 signals.

The main board should send state information; the ring should handle LED current and sequencing locally.

The exact implementation must be chosen only after the available **3.3 V current budget at J4** is verified. The current design documentation does not yet establish how much additional LED load J4 can safely supply.

Until that budget is known, Ring Rev A should assume modest indicator lighting rather than a high-current decorative RGB ring. Full-brightness addressable RGB operation must not be assumed safe merely because 3.3 V is present on J4.

If the available J4 power budget is insufficient, first evaluate reducing LED count/current or adding appropriate ring-local power handling before reopening the main-board design.

## Mechanical / optical goals

Status LEDs should be placed so that light is visible through the perforated speaker grille while the PCB itself remains hidden.

Design goals:

- distribute light around the ring rather than create one bright point;
- avoid direct glare when viewed from below;
- avoid light leaking into the speaker cavity in a way that is distracting;
- keep LEDs and optics clear of microphone acoustic ports;
- avoid blocking useful grille perforations in front of microphones;
- support different ring diameters without changing the main-board interface;
- allow brightness to be reduced substantially for dark rooms.

The grille itself may provide useful diffusion, but this must be tested on real speakers because grille hole size, paint, backing cloth, and spacing vary.

## Ring Rev A requirements

The first ring for the nominal 8-inch speaker / ~9-inch grille reference installation should reserve for status lighting from the beginning.

Before PCB layout is frozen, Rev A should define:

- candidate LED locations around the ring;
- routing/footprint space for the chosen driver or local controller;
- LED-control connection to J4 through I2C and/or `RING_GPIO_SPARE`;
- estimated worst-case and normal LED current;
- microphone-to-LED spacing so lighting components do not compromise acoustic-port placement;
- a firmware-safe default state where LEDs are off until intentionally enabled.

The first prototype does not need elaborate animations. Proving a uniform, low-brightness listening indication through the installed grille is sufficient.

## Validation

Prototype testing should record:

1. J4 supply voltage and current with LEDs off and at intended maximum brightness;
2. whether LED operation introduces noise into PDM microphone capture;
3. whether PWM or digital LED traffic couples into audio or microphone signals;
4. light uniformity through the installed grille;
5. visibility in normal room lighting and in a dark room;
6. temperature rise of LED/driver components;
7. whether the listening/mute indication remains understandable from typical room viewing positions.

Any LED implementation that materially degrades microphone performance should be revised even if the visual result is good.

## Relationship to the microphone-ring family

Status lighting is a shared capability of the ring family, not a reason to create electrically incompatible ring sizes. Mechanical dimensions may change with speaker/grille size, but compatible rings should retain the same J4 interface and status-control behavior wherever practical.

The long-term goal is that selecting a different ring diameter changes the mechanics, not the main PoE speaker board.
