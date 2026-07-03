# Phase 2 — Player

## What's here

```
src/entities/Player.ts     the player: sprite + physics + input + animations
src/scenes/MapScene.ts     spawnPlayer() at player_spawn, collider vs statics,
                           camera startFollow (was static centerOn)
src/scenes/BootScene.ts    placeholder marker code removed; still loads the
                           'player' spritesheet (48x48 frames)
src/core/constants.ts      PLAYER_SPEED = 80 (world px/s)
```

Tool-use animations (`player_actions.png`) were **deferred to Phase 4** — they
land when the hoe/watering can actually do something.

## Sprite sheet facts (pixel-verified — don't re-derive)

- `player.png` is 192x192: a **4x4 grid of 48x48 frames**.
- **Rows: 0=down, 1=up, 2=left, 3=right.** Left and right are real drawn rows,
  not mirror flips. (Verified: row 1 lacks all face-only colors — back of
  head; the mouth color, front-center in row 0, sits left-of-center in row 2
  and right-of-center in row 3.)
- Frame index = `row*4 + col`: down 0–3, up 4–7, left 8–11, right 12–15.
- Within a row, frames 0/2/3 are near-identical; frame 1 is the step pose.
- The visible character occupies x=17..30, y=16..31 of each 48x48 frame
  (14x16 px, feet at y≈31).
- `player_actions.png` is 96x576: a 2x12 grid of 48x48 — 2-frame action pairs
  per row, for Phase 4.

## How the player works

- **Animations**: `walk_down/up/left/right`, 4 frames each at 8 fps, registered
  once in `Player.registerAnimations()` (guarded by `anims.exists`, so multiple
  scenes/instances are safe). Idle = stop and hold frame 0 of the facing row.
  If the walk cycle ever looks like a shuffle, remember frame 1 is the only
  strong step pose — re-cut the cycle there.
- **Input**: arrow keys and WASD both work. Movement builds a vector, then
  `normalize().scale(PLAYER_SPEED)` so diagonals aren't faster. On diagonals
  the horizontal direction wins the facing so the animation doesn't flip-flop.
- **Physics body**: `setSize(12, 8)` + `setOffset(18, 24)` — a small band at
  the feet, top-down style, so the head can overlap obstacles from below.
  Collides against the static bodies MapScene builds from the map's
  `collision` object layer (`buildCollision()` now returns the group instead
  of stashing it in the registry).
- **Camera**: `startFollow(player, true, 0.15, 0.15)` — roundPixels on for
  pixel art, soft lerp; still clamped to map bounds.

## Knobs to tune

| What | Where | Current |
|---|---|---|
| Walk speed | `PLAYER_SPEED` in `src/core/constants.ts` | 80 px/s (5 tiles/s) |
| Anim speed | `frameRate` in `Player.registerAnimations` | 8 fps |
| Body size/placement | `setSize`/`setOffset` in `Player` constructor | 12x8 at (18,24) |
| Camera smoothing | lerp args in `MapScene.setupCamera` | 0.15 |

## Hooks for later phases

- **Phase 4 (tools)**: register action animations alongside the walk anims in
  `Player.registerAnimations()`; the actions sheet rows are 2-frame pairs.
  `facing` is already tracked — tool use will target the tile the player faces.
- Depth-sorting the player against props/trees is not done yet (player is a
  flat `setDepth(100)`); revisit when props become sprites.
