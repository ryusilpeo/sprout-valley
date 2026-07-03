# Sprout Valley

A Stardew Valley–inspired farming game built with Phaser 3 + TypeScript + Vite,
using the Sprout Lands asset pack by Cup Nooble.

> Assets — From: Sprout Lands — By: Cup Nooble
> (non-commercial license; see `public/assets/license/read_me.txt`)

## Commands

```bash
npm install       # once
npm run dev       # localhost:5173
npm run typecheck
npm run build
```

## Layout

```
public/assets/    runtime assets, organized by game system (see manifest.json
                  for a map of every file back to its original pack path)
_reference/       bitmask autotile keys, UI mockups, palette — docs for humans
_source/          .aseprite originals
_archive/         superseded pack files, kept for the record
src/              game code (rebuilt phase by phase)
docs/plan.md      the full fresh-start plan and file mapping
```

## Phase tracker

- [x] **0 — Foundation**: scaffold, reorganized assets, pipeline proven
- [ ] **1 — Tiled pipeline**: tilesets defined, first hand-built farm map loads
- [ ] **2 — Player**: 4-dir walk, actions, collision, camera
- [ ] **3 — HUD**: nine-slice panels, hearts, coins, mission, hotbar
- [ ] **4 — Farming**: hoe / water / plant / grow / harvest
- [ ] **5 — Inventory & items**
- [ ] **6 — Day cycle & save**
- [ ] **7 — Animals & missions**
- [ ] **8+ — Economy, interiors, mining/fishing, seasons**

Every phase ends with: typecheck clean → zero console errors → commit.
