# Phase 1 — Tiled pipeline

## What's here

```
tiled/
  tilesets/          .tsx tileset definitions (open these in Tiled)
    grass.tsx        + Wang "grass" terrain for autotiling (Terrain Brush = T)
    tilled_dirt.tsx  + Wang "soil" terrain
    water.tsx        4-frame animation + collide=true
    grass_biome_props.tsx, trees_stumps_bushes.tsx, bridge_wood.tsx,
    paths.tsx, house_wooden.tsx, fences.tsx   (plain, for hand-placing)
  maps/
    farm.tmx         the editable map — OPEN THIS IN TILED
  generate_farm_map.py   regenerates a blocky starter farm.tmx from scratch
  tmx_to_json.py         converts farm.tmx -> public/assets/maps/farm.json

public/assets/maps/farm.json   runtime map Phaser loads (generated; don't hand-edit)
```

## The loop you'll use

1. Open `tiled/maps/farm.tmx` in Tiled.
2. Edit: use the Terrain Brush (T) on the `ground` layer to paint grass with
   auto-correct borders; paint soil on `farm`; draw collision rectangles on the
   `collision` object layer; move `player_spawn` on `spawns`.
3. Export for the game — either:
   - Tiled: File -> Export As -> `public/assets/maps/farm.json`, OR
   - Terminal: `python3 tiled/tmx_to_json.py tiled/maps/farm.tmx`
4. `npm run dev` and look.

## Layers

- **ground** (tilelayer): grass/water base. Water tiles animate in-engine.
- **farm** (tilelayer): tilled soil where crops go (Phase 4 hooks in here).
- **collision** (objectgroup): rectangles become static bodies. Right now it's
  a ring around the island; add rects over trees/house/etc. as you place them.
- **spawns** (objectgroup): named points. `player_spawn` is where the player
  spawns (since Phase 2).

## How autotiling works here

`grass.tsx` defines a Wang *corner* terrain. Each border tile is tagged with
which of its 4 corners are "grass" vs "empty" (the `wangid`). When you paint
with the Terrain Brush, Tiled looks at neighbours and drops in the matching
corner/edge tile automatically — no manual tile-picking. The tile ids come from
the verified 3x3 blob layout (fill = local id 12) plus the 4 inner-corner tiles.

## Adding a new tileset to the map

1. Drop the tileset in Tiled (it appends with a new firstgid).
2. Re-export/convert. `tmx_to_json.py` reads whatever tilesets the .tmx
   references, so no code change is needed for new *tile* sheets.
3. If it's a brand-new image key, add a matching `this.load.image(...)` in
   `MapScene.preload()` using the tileset's name.
