#!/usr/bin/env python3
"""
Generate the Phase 1 starter farm map (tiled/maps/farm.tmx).

This lays down a playable first map modelled on the reference GIF: a grass
island surrounded by water, with a tilled farm plot. It's deliberately simple
and blocky — the point is to give you a correct, valid .tmx to OPEN IN TILED
and refine by hand (rounder coastlines, trees, the house, bridges, paths).

Tile GIDs: Tiled assigns each tileset a "firstgid". We keep the order fixed:
    water        firstgid 1   (tiles 1..4)
    grass        firstgid 5   (tiles 5..81)
    tilled_dirt  firstgid 82  (tiles 82..158)
So a grass tile with local id N is GID 5+N; grass FILL (local 12) = GID 17.

Run:  python3 tiled/generate_farm_map.py
"""
from pathlib import Path

W, H = 40, 40  # map size in tiles

# firstgids (must match the <tileset> order in the TMX below)
WATER_FIRST = 1
GRASS_FIRST = 5
SOIL_FIRST = 82

# handy grass GIDs from the blob set (local id + GRASS_FIRST)
G = lambda local: GRASS_FIRST + local
GRASS = {
    "fill": G(12),
    "tl": G(0), "t": G(1), "tr": G(2),
    "l": G(11), "r": G(13),
    "bl": G(22), "b": G(23), "br": G(24),
}
WATER = WATER_FIRST + 0        # animated water tile
SOIL_FILL = SOIL_FIRST + 12

# The grass island: a rectangle inset from the water border. Coordinates are
# (col, row). Kept rectangular on purpose — you'll carve the organic shape in
# Tiled with the terrain brush.
ISLAND = {"x0": 3, "y0": 3, "x1": W - 4, "y1": H - 4}

# Farm plot: a tilled-dirt rectangle inside the island (like the GIF's plot).
PLOT = {"x0": 22, "y0": 20, "x1": 31, "y1": 27}


def build_ground() -> list[int]:
    """Ground layer: water everywhere, grass island on top."""
    data = [WATER] * (W * H)
    ix0, iy0, ix1, iy1 = ISLAND.values()
    for y in range(iy0, iy1 + 1):
        for x in range(ix0, ix1 + 1):
            if x == ix0 and y == iy0:
                gid = GRASS["tl"]
            elif x == ix1 and y == iy0:
                gid = GRASS["tr"]
            elif x == ix0 and y == iy1:
                gid = GRASS["bl"]
            elif x == ix1 and y == iy1:
                gid = GRASS["br"]
            elif y == iy0:
                gid = GRASS["t"]
            elif y == iy1:
                gid = GRASS["b"]
            elif x == ix0:
                gid = GRASS["l"]
            elif x == ix1:
                gid = GRASS["r"]
            else:
                gid = GRASS["fill"]
            data[y * W + x] = gid
    return data


def build_farm() -> list[int]:
    """Farm layer: tilled soil rectangle, empty (0) elsewhere."""
    data = [0] * (W * H)
    for y in range(PLOT["y0"], PLOT["y1"] + 1):
        for x in range(PLOT["x0"], PLOT["x1"] + 1):
            data[y * W + x] = SOIL_FILL
    return data


def csv(data: list[int]) -> str:
    rows = []
    for y in range(H):
        rows.append(",".join(str(data[y * W + x]) for x in range(W)))
    return "\n".join(rows)


def main() -> None:
    ground = csv(build_ground())
    farm = csv(build_farm())

    # A water-border collision object ringing the island keeps the player on
    # land in Phase 1 before per-tile collision exists. You'll replace/extend
    # these rectangles in Tiled as the coastline changes.
    ix0, iy0, ix1, iy1 = ISLAND.values()
    px = lambda t: t * 16
    border_objs = f"""
  <object id="1" x="0" y="0" width="{W*16}" height="{px(iy0)}"/>
  <object id="2" x="0" y="{px(iy1+1)}" width="{W*16}" height="{px(H-iy1-1)}"/>
  <object id="3" x="0" y="0" width="{px(ix0)}" height="{H*16}"/>
  <object id="4" x="{px(ix1+1)}" y="0" width="{px(W-ix1-1)}" height="{H*16}"/>"""

    tmx = f"""<?xml version="1.0" encoding="UTF-8"?>
<map version="1.10" tiledversion="1.11.0" orientation="orthogonal" renderorder="right-down" width="{W}" height="{H}" tilewidth="16" tileheight="16" infinite="0" nextlayerid="6" nextobjectid="5">
 <tileset firstgid="{WATER_FIRST}" source="../tilesets/water.tsx"/>
 <tileset firstgid="{GRASS_FIRST}" source="../tilesets/grass.tsx"/>
 <tileset firstgid="{SOIL_FIRST}" source="../tilesets/tilled_dirt.tsx"/>
 <layer id="1" name="ground" width="{W}" height="{H}">
  <data encoding="csv">
{ground}
</data>
 </layer>
 <layer id="2" name="farm" width="{W}" height="{H}">
  <data encoding="csv">
{farm}
</data>
 </layer>
 <objectgroup id="3" name="collision">{border_objs}
 </objectgroup>
 <objectgroup id="4" name="spawns">
  <object id="10" name="player_spawn" x="{px(12)}" y="{px(20)}" width="16" height="16"/>
 </objectgroup>
</map>
"""
    out = Path(__file__).parent / "maps" / "farm.tmx"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(tmx)
    print(f"wrote {out}  ({W}x{H} tiles)")


if __name__ == "__main__":
    main()
