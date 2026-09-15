# Modular microphone-ring concept

## Purpose

The PoE speaker project is intended to support a family of microphone-array rings that can be adapted to many existing ceiling speakers without requiring a speaker-specific electronics design.

The concept is simple: remove the ceiling-speaker grille, choose the largest microphone ring that fits cleanly behind or within the grille, mount it around the speaker opening, route a small cable to the rear electronics, connect it to the main PoE speaker board, and reinstall the grille.

The microphone ring should be visually hidden once the grille is installed. The speaker itself remains the acoustic output device; the ring adds distributed microphones around the perimeter for room/voice capture.

This document describes the concept only. Ring PCB layouts, microphone selection, mounting methods, acoustic performance, firmware, and production dimensions are not yet validated.

## Design philosophy

The main PoE speaker board should remain common across installations. Speaker compatibility is handled mechanically by selecting a ring of the appropriate diameter.

Instead of making a different complete electronics system for every ceiling-speaker model, the project should eventually provide several ring diameters using the same electrical interface and microphone topology.

A useful installation should require as little modification to the existing speaker as practical:

1. Remove the speaker grille.
2. Measure the usable clear diameter behind the grille.
3. Select the largest ring variant that fits without interfering with the woofer, tweeter, grille attachment, mounting hardware, or speaker suspension.
4. Mount the ring to the grille/frame or to a small adapter using a reversible method where practical.
5. Route the ring cable toward the rear of the speaker. An existing opening is preferred. A new cable pass-through may be added only when doing so does not damage the driver, wiring, enclosure, fire rating, listing, or structural integrity of the speaker assembly.
6. Mount the PoE speaker electronics in an appropriate protected location behind/near the speaker.
7. Connect the microphone ring to the main board and reinstall the grille.

The result should look like an ordinary ceiling speaker from the room.

## Ring family

Ring sizes should be defined by geometry rather than by a specific speaker brand or model.

Each ring variant should eventually document at least:

| Parameter | Meaning |
| --- | --- |
| PCB outside diameter | Largest physical diameter of the ring PCB |
| Clear inside diameter | Opening available for the speaker cone/tweeter/acoustic path |
| Microphone-circle diameter | Diameter through the microphone acoustic ports |
| Microphone count | Intended number of microphones on the ring |
| Mounting envelope | Space needed for clips, adhesive mounts, screws, or an adapter |
| Maximum component height | Clearance required behind the grille |
| Cable exit | Location and direction of the ring cable/connector |
| Intended grille range | Approximate speaker/grille dimensions that can accept the ring |

Exact standard sizes are intentionally TBD. The first useful set should be chosen after measuring several common ceiling speakers rather than guessing from nominal woofer size alone.

A future naming scheme could use the microphone-circle or PCB outside diameter in millimeters so the name describes geometry rather than a vendor model.

## Electrical interface

The current Rev E main board reserves connector **J4** for the future microphone ring.

J4 exposes:

- 3.3 V power and grounds
- one shared `PDM_CLK`
- four PDM data signals: `PDM_DATA0_CONN` through `PDM_DATA3_CONN`
- `I2C_SDA` and `I2C_SCL`
- one spare ring GPIO

The project target is an eight-microphone ring. A likely implementation is to arrange compatible PDM microphones around the perimeter and use the four PDM data lanes for paired microphones, but the exact microphone parts, pairing method, clock rate, loading, cable constraints, connector implementation, and firmware capture scheme still require engineering validation.

The ring should not require a different main-board connector for each diameter. Electrically compatible ring sizes should be interchangeable.

## Mechanical goals

The microphone ring should:

- fit behind a perforated ceiling-speaker grille and remain visually unobtrusive;
- keep the center substantially open so it does not block the woofer or coaxial tweeter;
- avoid contact with the moving cone, surround, tweeter assembly, grille, or mounting dogs/clamps;
- tolerate speaker vibration without rattling;
- provide strain relief for its cable;
- support simple mounting methods such as clips, small standoffs, removable adhesive fixtures, or model-specific 3D-printed adapters;
- minimize required permanent modification to an existing speaker;
- allow multiple PCB diameters while keeping the same electrical design where practical.

A circular PCB is the default concept, but segmented or multi-piece rings may be considered if full circular PCBs become unnecessarily expensive at larger diameters.

## Acoustic goals and risks

The ring is intentionally close to a loudspeaker, which creates significant acoustic challenges. Mechanical fit alone is not sufficient.

Future prototypes need to evaluate:

- microphone self-noise and sensitivity through the installed grille;
- consistency between microphone positions;
- vibration mechanically coupled from the speaker/frame into the microphones;
- airflow and pressure effects near the woofer;
- acoustic shadowing caused by the speaker frame or grille structure;
- microphone saturation while the local speaker is playing;
- echo cancellation / speaker-reference requirements for simultaneous playback and voice capture;
- beamforming performance at different ring diameters;
- whether microphone spacing creates useful or harmful spatial aliasing over the intended voice band.

Ring diameter should therefore be treated as an acoustic parameter as well as a mechanical one.

## Installation and safety constraints

The goal is broad retrofit compatibility, not permission to modify every speaker indiscriminately.

Do not drill or modify a speaker assembly when doing so would compromise a listed backcan, fire/plenum rating, transformer enclosure, mains/high-voltage wiring, structural mounting, warranty, or other required safety feature. When an existing cable path is available, use it.

The microphone ring and main electronics also need an installation method that cannot fall into the occupied space if a grille or adhesive mount fails.

## Proposed development sequence

1. Measure a small sample of common ceiling speakers and record grille ID, usable ring area, depth, frame obstructions, and cable-routing options.
2. Select two or three prototype ring diameters that cover meaningfully different speaker sizes.
3. Select and electrically validate the PDM microphone topology against J4.
4. Build one ring size first and prove microphone capture before producing every mechanical size.
5. Evaluate mounting approaches behind real grilles.
6. Test microphone response with the local speaker silent and playing.
7. Evaluate beamforming / direction finding / voice capture and echo-cancellation requirements.
8. Once the electrical design is stable, replicate the same circuit topology into additional ring diameters.

## Relationship to the main board

The microphone ring is a separate future PCB from the Rev E PoE speaker main board. Development of the ring should not block first-prototype validation of Ethernet, power, DAC, and amplifier functions on the main board.

The current J4 interface is a design provision, not proof that an eight-microphone capture system is complete or validated.
