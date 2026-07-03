# Sprout Valley — Fresh Start Plan
## Part 1: Decision · Part 2: Asset Reorganization (all 224 files) · Part 3: Rebuild Phases

---

# Part 1 — The decision (what "fresh start" means here)

You asked me to decide if there's a better option than scratch. Here it is:

**The look problem was never the code.** Your systems (farm tiles, inventory, missions, saves, autotiling) are correct and well-built. The reference GIF looks better than your game for two reasons: (a) the HUD wasn't using real sprites — already fixed — and (b) **the reference is a hand-composed map**, while your world is assembled procedurally in code. No restart fixes (b); only hand-designing maps does.

So the fresh start we'll do:

| Restart | Keep / port |
|---|---|
| New repo, clean `.gitignore` from day one (no `node_modules`, no videos) | Phaser 3 + TS + Vite stack (it's the right choice; pack's own `assets.json` targets it) |
| **Reorganized asset library** (this document) | Systems code ported milestone-by-milestone: InventorySystem, FarmTileSystem, SaveSystem, EventBus, missions — after review, as each phase needs them |
| **Maps hand-built in Tiled** instead of generated in code — this is the single biggest visual upgrade | The rewritten HudScene + NinePanel from our last two updates |
| World/scene code rebuilt around Tiled map loading | `tiles.ts` frame constants (verified correct against the sheets) |

---

# Part 2 — Asset reorganization

## 2.1 Principles

1. **Organize by game system**, not by pack origin. "Early Access/Plant update 2" tells you when Cup Nooble drew it; `farming/` tells you what it's for.
2. **Runtime vs non-runtime split.** Bitmask references, premade mockups, `.aseprite` sources, and test files never ship — they live outside `assets/`.
3. **Normalized names**: lowercase snake_case, typos fixed (`Herat`→`heart`, `meterials`→`materials`, `Charakter`→`character`, `piknik`→`picnic`, `snomwflakes`→`snowflakes`, `Dialouge`→`dialogue`, `defautlt`→`default`, `probs`→`props`, `cirkels`→`circles`). A `manifest.json` maps every new path → original pack path so nothing is ever untraceable.
4. **Duplicates dropped** (verified byte-identical by checksum): the space-named copies of Basic_Furniture, Basic_Plants, Basic_Grass_Biom_things, Basic_tools_and_meterials, Egg_item, Simple_Milk_and_grass_item, Wood_Bridge. One exception: `Tilesets/Tilled Dirt.png` (128×128) is NOT a duplicate — it's an older layout; archived, not deleted.
5. **Keep the license file** at the asset root, always shipped: credit to Cup Nooble is a license requirement.

## 2.2 Target structure

```
assets/                      ← everything the game loads
  license/read_me.txt
  world/terrain/  world/structures/  world/props/
  farming/
  characters/player/  characters/animals/  characters/enemies/
  fishing/   mining/   seasons/winter/   items/
  ui/panels/  ui/buttons/  ui/icons/  ui/hud/  ui/cursors/  ui/emotes/  ui/fonts/
  audio/
_reference/                  ← docs for humans: bitmask keys, mockups, palette
_source/                     ← .aseprite originals
_archive/                    ← superseded versions, pack tests, original assets.json indexes
```

## 2.3 Complete file mapping (all 224 files)

### assets/world/terrain/ (17)
| New name | Original |
|---|---|
| grass.png | Tilesets/Grass.png |
| hills.png | Tilesets/Hills.png |
| water.png | Tilesets/Water.png |
| tilled_dirt.png | Tilesets/Tilled_Dirt.png |
| tilled_dirt_v2.png | Tilesets/Tilled_Dirt_v2.png |
| tilled_dirt_wide.png | Tilesets/Tilled_Dirt_Wide.png |
| tilled_dirt_wide_v2.png | Tilesets/Tilled_Dirt_Wide_v2.png |
| biome_birch.png | Early Access/Plant update 2/Birch wood Biom.png |
| biome_birch_water_plants.png | …/Birch wood Biom water plants.png |
| biome_cherry.png | …/Cherry Blossom Biom.png |
| biome_cherry_water_plants.png | …/Cherry Blossom Biom water plants.png |
| biome_pine.png | …/Pine Tree Biome.png |
| biome_pine_water_plants.png | …/Pine Tree Biome water plants.png |
| grass_layers_1..4.png (4 files) | …/Ground tilesets/Grass_Tile_Layers.png, layers2, layers3, layers4 |

(The 4 `blue_tint_Grass_Tile_Layers*.png` → `seasons/winter/` as `grass_layers_cold_1..4.png` — they're the cold-tint variants.)

### assets/world/structures/ (24)
| New name | Original |
|---|---|
| house_wooden.png | Tilesets/Wooden House.png |
| house_wooden_walls.png | Tilesets/Wooden_House_Walls_Tilset.png |
| house_wooden_roof.png | Tilesets/Wooden_House_Roof_Tilset.png |
| doors.png | Tilesets/Doors.png |
| door_wooden_anim.png | Village pack/houses/wooden_door_spritesheet.png |
| fences.png | Tilesets/Fences.png |
| chicken_house.png | Objects/Free_Chicken_House.png |
| village_brick_{base,doors,doors_grass,grass,shadow}.png (5) | Village pack/houses/Grey brick house/* |
| village_house_{base,light,light_door,light_door_grass,light_grass,shadow,door,door_grass,grass}.png (9) | Village pack/houses/small house/* |
| village_hut_{base,doors,doors_grass,grass,shadow}.png (5) | Village pack/houses/small hut/* |

### assets/world/props/ (15)
| New name | Original |
|---|---|
| furniture_basic.png | Objects/Basic_Furniture.png |
| furniture_wooden.png | Plant update 2/Furniture/new Wooden Furniture.png |
| furniture_wooden_items.png | …/new Wooden Furniture items.png |
| grass_biome_props.png | Objects/Basic_Grass_Biom_things.png |
| trees_stumps_bushes.png | Plant update 2/Trees, stumps and bushes v2.png |
| wood_and_shrooms.png | Plant update 2/wood n shroms.png |
| chest.png | Objects/Chest.png |
| chest_{birch,cherry,golden,oak,pine,silver}.png (6) | Plant update 2/Furniture/*_Chest.png |
| bridge_wood.png | Objects/Wood_Bridge.png |
| paths.png | Objects/Paths.png |
| picnic_basket.png, picnic_blanket.png | Plant update 2/piknik/Piknik basket/blanket |
| beehive.png, beehive_small.png | Plant update 2/Bee/beehive.png, small_beehive.png |

### assets/farming/ (4)
| New name | Original |
|---|---|
| plants_basic.png | Objects/Basic_Plants.png |
| crops.png | Plant update 2/Farming Plants v2.png |
| crops_watered.png | Plant update 2/Farming Plants v2 watered.png |
| crop_items.png | Plant update 2/Farming Plants items v2.png |

### assets/characters/player/ (3) · animals/ (8) · enemies/ (3)
| New name | Original |
|---|---|
| player.png | Characters/Basic Charakter Spritesheet.png |
| player_actions.png | Characters/Basic Charakter Actions.png |
| player_tools.png | Characters/Tools.png |
| chicken.png / cow.png | Characters/Free Chicken/Cow Sprites.png |
| egg_and_nest.png | Characters/Egg_And_Nest.png |
| bee.png, bee_small.png | Plant update 2/Bee/{bee,small_bee}_spritesheet.png |
| frog.png, frog_2.png | Plant update 2/frog/frog_spritesheet(.2).png |
| swimming.png | Ocean Pack/swimming.png (player swim anim) |
| bat.png, bat_small.png | Dungeon Pack/enemies/{bat,small_bat}_animations.png |
| slime_green_small.png | …/small_green_slime_animations.png |

(The two enemy preview `.gif`s → `_reference/`.)

### assets/fishing/ (9)
fish_sprites.png, fish_small.png, fish_medium.png ("mediuml" fixed), fish_big_circles.png, fishing_rod.png, fishing_rod_2.png, fishing_anim_{front,back,side}.png, fishing_splash_and_rod.png ← all from Ocean Pack.

### assets/mining/ (12)
walls.png, walls_decor_gates.png, props.png (Dungeon_probs), rocks.png, rails.png, carts.png, items.png (dungeon_items), switch.png, ground_orange.png, ground_orange_dark.png, ground_orange_hole.png, ground_orange_darker_hole.png ← all from Dungeon Pack/tiles + enemies handled above.

### assets/seasons/winter/ (17)
snow_tiles_1.png, snow_tiles_2.png, ice_tiles.png, snowflakes.png, campfire.png, fire_anim.png, christmas_tree.png, present_red{,_2,_3}.png, present_green{,_2}.png, present_anim.png, winter_items.png, winter_sprites.png, plus grass_layers_cold_1..4.png (the blue-tint set from 2.3 §terrain).

### assets/items/ (5)
egg.png (Egg_item), milk_and_grass.png, tools_and_materials.png, bread_jam_honey.png, picnic_foods.png.

### assets/ui/ (34)
- **panels/**: dialog_{small,medium,big}.png, dialog_9slice.png (the 48×48 `dialog box.png` — our nine-slice workhorse)
- **buttons/**: square_26x26.png, square_26x19.png, square_19x26.png, square_small.png, play_big.png, settings_buttons.png, settings_menu.png
- **icons/**: all_icons.png, white_icons.png, special_icons.png, happiness_icons.png
- **hud/**: hearts.png (Inventory_Herat…), hearts_light.png, inventory_blocks.png, inventory_sheet.png, weather_icons.png, weather_ui.png
- **cursors/**: catpaw.png, catpaw_holding.png, catpaw_pointing.png, triangle_1..3.png
- **emotes/**: player_emotes.png (Teemo Basic emote…), emoji.png, speech_bubble.png, dialog_continue_indicator.png
- **fonts/**: sprout.ttf (+ pixel-letters pngs → `_reference/`)

### assets/audio/ (22, renamed by purpose)
ui_blip.wav (bip_1), pickup_1/2.wav (blup), hit_1..6.wav (punch), till_1/2.wav (squick), till_double_1/2.wav (squick_squick), jingle_1..4.wav (flute), notify_1/2.wav (phone), animal_1/2.wav (boo), mission.wav (bing_1).

### _reference/ (≈20)
Bitmask references 1/2 + gif, all 3 Premade dialog boxes, all 8 inventory example/mockup pngs, palette png + snip, font preview pngs, `Sprite sheet for Basic Pack.png` (a promo contact sheet), bat/small-bat preview gifs, all 5 original `assets.json` indexes (they reference old paths — superseded by our manifest, kept for reference).

### _source/ (4)
The `.aseprite` files: palette, christmas tree, fire, present.

### _archive/ (6)
`Tilesets/Tilled Dirt.png` (old 128×128 layout), the whole `Tests/` folder (5 files: teemo tests, free character sheet — Cup Nooble's own experiments, not game assets).

### Dropped entirely (7 byte-identical duplicates)
The space-named twins of: Basic Furniture, Basic Plants, Basic Grass Biom things 1, Basic tools and meterials, Egg item, Simple Milk and grass item, Wood Bridge.

**Count check:** 224 originals = ~160 runtime (renamed) + ~20 reference + 4 source + 6 archive + 7 dropped duplicates + 2 read_me (license kept, UI read_me merged into it) + 5 assets.json (reference). Every file accounted for.

---

# Part 3 — Rebuild phases (slow, one at a time)

**Phase 0 — Foundation.** New repo, `.gitignore` (node_modules, dist, *.mp4), Vite+TS+Phaser scaffold, run the reorganization script, commit the clean asset library + manifest.json. *Deliverable: empty game window, organized assets, first clean commit.*

**Phase 1 — Tiled pipeline.** Define Tiled tilesets (grass/hills/water/tilled dirt/props) with collision properties; hand-build the first farm map modeled on your reference GIF (island shapes, bridges, house, farm plot); load it in Phaser. *Deliverable: the reference map, walkable.* ← this is where the game starts looking like the GIF.

**Phase 2 — Player.** Port player entity: 4-dir walk, action animations, collision, camera. 

**Phase 3 — HUD.** Drop in our already-rewritten HudScene + NinePanel + slot slicing.

**Phase 4 — Farming.** Port FarmTileSystem onto Tiled farm-plot tiles; hoe/water/plant/harvest with `crops.png` / `crops_watered.png` growth stages.

**Phase 5 — Inventory & items.** Port InventorySystem + items.json; pickup, hotbar, stacking.

**Phase 6 — Day cycle.** Clock, sleep, growth tick, save/load (port SaveSystem).

**Phase 7 — Animals & missions.** Chickens, eggs, mission tracker (port MissionSystem).

**Phase 8+ —** shipping/economy → house interior scene → then mining *or* fishing → seasons (winter reskin using `seasons/winter/`).

Each phase ends with: typecheck clean → runs with zero console errors → commit.

---

# What I need from you before executing

1. Confirm this structure (or tell me what to rename/regroup).
2. Confirm the salvage strategy (port systems) vs. literally rewriting everything — I strongly recommend porting.
3. Tiled is a desktop app you'll need installed (free, mapeditor.org) since map-making will be partly your hands on the mouse. OK?

Once confirmed, Phase 0's first concrete artifact is a script that performs this entire reorganization automatically (copies from the pack, renames, writes manifest.json) so it's reproducible and you never hand-move 224 files.
