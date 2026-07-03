# Handoff — read this first

Continuing a Stardew Valley–clone project (Phaser 3 + TypeScript + Vite) built
around the Sprout Lands asset pack (Cup Nooble, non-commercial license — see
`public/assets/license/`). Prior work happened in a chat session; this file is
the state transfer into Claude Code.

## Key decisions already made (don't re-litigate these)

- **Fresh rewrite from scratch**, not a port of an earlier messier prototype.
  Reason: earlier version's HUD drew flat rectangles instead of real sprites,
  and the world was assembled in code instead of hand-designed — both fixed
  by rebuilding clean.
- **Assets reorganized** by game system, not by pack origin. Every runtime
  file lives under `public/assets/<system>/...` (world/terrain, world/props,
  world/structures, farming, characters/player, characters/animals,
  characters/enemies, fishing, mining, seasons/winter, items, ui/*, audio).
  `public/assets/manifest.json` maps every renamed file back to its original
  pack path. `_reference/`, `_source/`, `_archive/` hold non-runtime files
  (bitmask keys, mockups, .aseprite originals, superseded versions). Full
  rationale and the complete 224-file mapping: `docs/plan.md`.
- **Maps are hand-built in Tiled**, not generated in code — this was the
  single biggest fix for "doesn't look like the reference GIF." User has
  Tiled 1.12.2 installed.
- **Engine**: Phaser 3 + TypeScript + Vite. Pack's own bundled `assets.json`
  (now archived in `_reference/pack_indexes/`) was written for Phaser, and
  it's the right free choice for 16px pixel art + Tiled maps.

## Phase status

- [x] **Phase 0** — scaffold, reorganized assets, pipeline proven (boot scene
  loads one real sprite).
- [x] **Phase 1** — Tiled pipeline. `.tsx` tilesets in `tiled/tilesets/`
  (grass and tilled_dirt have Wang corner-terrain for autotiling — paint with
  Terrain Brush, key `T`). Hand-built map at `tiled/maps/farm.tmx`, converted
  to `public/assets/maps/farm.json` via `tiled/tmx_to_json.py`. `MapScene.ts`
  loads it: renders layers, animates water (4-frame), turns the `collision`
  object layer into static bodies, centers camera on `spawns/player_spawn`.
  Full write-up: `docs/phase1-tiled.md`.
- [ ] **Phase 2 — Player** (next). Real 4-direction walking from
  `public/assets/characters/player/player.png` (48x48 frames, 4x4 grid: rows
  = down/up/left/right, walk cycle), tool-use animations from
  `player_actions.png`, arcade-physics collision against the Phase 1
  collision bodies, camera follow. Replaces the placeholder `player_marker`
  circle currently drawn in `BootScene.ts`.
- [ ] Phase 3 — HUD (nine-slice panels, hearts, coins, mission tracker,
  hotbar — largely already designed in an earlier iteration; needs porting
  into this fresh codebase's conventions).
- [ ] Phase 4 — Farming (hoe/water/plant/grow/harvest on the `farm` tile
  layer, crop growth stages from `assets/farming/crops.png` /
  `crops_watered.png`).
- [ ] Phase 5 — Inventory & items. Phase 6 — Day cycle & save. Phase 7 —
  Animals & missions. Phase 8+ — economy, interiors, mining/fishing, seasons.

Each phase ends with: `npm run typecheck` clean → zero browser console
errors → git commit.

## Working conventions

- **Tiled edit loop**: edit `tiled/maps/farm.tmx` in Tiled → either Tiled's
  own File > Export As to `public/assets/maps/farm.json`, or run
  `python tiled/tmx_to_json.py tiled/maps/farm.tmx` → `npm run dev`.
- **Naming**: lowercase snake_case for all asset files; typos from the
  original pack fixed (Herat→heart, meterials→materials, etc). Never rename
  files inside `public/assets/` without updating `manifest.json`.
- **Git hygiene**: `.gitignore` already excludes `node_modules/`, `dist/`,
  `*.mp4`. Keep it that way — an earlier prototype accidentally committed
  `node_modules` and a 66MB video; don't repeat that.
- Repo: `https://github.com/ryusilpeo/sprout-valley` (public).

## Known gotchas from this session (save yourself the debugging time)

- **`npm install` required after any fresh clone/unzip** before
  `npm run typecheck` or `npm run dev` will work (vite/client types live in
  node_modules).
- If cloning this repo on a different OS than it was built on, rollup's
  native binary can fail to resolve (`Cannot find module
  @rollup/rollup-<platform>`) — fix is `rm -rf node_modules package-lock.json
  && npm install` fresh on the target machine.
- Browsers rename repeat downloads (`farm.tmx`, `farm (1).tmx`, ...) instead
  of overwriting — if re-downloading any file mid-session, double check
  you're not opening a stale duplicate.
- If Tiled ever rejects a hand-crafted (non-Tiled-authored) `.tmx` with a
  "corrupt layer data" error despite the file being byte-valid CSV, the
  reliable fix is letting Tiled generate the file itself (New Map wizard +
  add external tilesets + hand-paint) rather than debugging the parser
  further — this is what resolved it last time.

## Immediate next step

Start **Phase 2 — Player**. Requirements once you begin:
1. Load `player.png` as a 48x48 spritesheet (already loaded in `BootScene`).
2. Build walk animations from the 4x4 grid (confirm row order against the
   sheet — don't assume; check pixels if unsure).
3. Arcade physics body, collide against the `collision` static group already
   built in `MapScene.buildCollision()` (currently stored in
   `this.registry.set('collision', statics)`).
4. Camera follow instead of the current static `centerOn`.
5. Remove the placeholder marker code once the real player renders.
