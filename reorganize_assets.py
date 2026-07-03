#!/usr/bin/env python3
"""
Sprout Valley — asset reorganization script.

Copies the Sprout Lands pack into a game-system-oriented layout:
    assets/       runtime files the game loads (renamed, snake_case, typos fixed)
    _reference/   human docs: bitmask keys, mockups, palette, pack indexes
    _source/      .aseprite originals
    _archive/     superseded versions and pack test files

Every destination is recorded in assets/manifest.json mapping
new path -> original pack path, so nothing is ever untraceable.
Byte-identical duplicates (verified by checksum) are dropped.

Usage:
    python3 reorganize_assets.py <path-to-extracted-pack> <output-dir>
e.g.
    python3 reorganize_assets.py ./sprout ./game
"""

import hashlib
import json
import shutil
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Complete mapping: original pack path -> new path (or DROP for duplicates).
# Paths are relative; forward slashes; must match the pack exactly.
# ---------------------------------------------------------------------------
DROP = "__DROP_DUPLICATE__"

MAPPING: dict[str, str] = {
    # ----- license (always shipped: credit is a license requirement) -----
    "read_me.txt": "assets/license/read_me.txt",
    "UI/read_me.txt": "assets/license/ui_read_me.txt",

    # ----- pack's own Phaser indexes (superseded by our manifest) -----
    "assets.json": "_reference/pack_indexes/root_assets.json",
    "Audio/assets.json": "_reference/pack_indexes/audio_assets.json",
    "Early Access/assets.json": "_reference/pack_indexes/early_access_assets.json",
    "UI/assets.json": "_reference/pack_indexes/ui_assets.json",
    "Tests/assets.json": "_archive/tests/assets.json",

    # ----- audio (renamed by purpose) -----
    "Audio/bing_1.wav": "assets/audio/mission.wav",
    "Audio/bip_1.wav": "assets/audio/ui_blip.wav",
    "Audio/blup_1.wav": "assets/audio/pickup_1.wav",
    "Audio/blup_2.wav": "assets/audio/pickup_2.wav",
    "Audio/boo_1.wav": "assets/audio/animal_1.wav",
    "Audio/boo_2.wav": "assets/audio/animal_2.wav",
    "Audio/flute_1.wav": "assets/audio/jingle_1.wav",
    "Audio/flute_2.wav": "assets/audio/jingle_2.wav",
    "Audio/flute_3.wav": "assets/audio/jingle_3.wav",
    "Audio/flute_4.wav": "assets/audio/jingle_4.wav",
    "Audio/phone_1.wav": "assets/audio/notify_1.wav",
    "Audio/phone_2.wav": "assets/audio/notify_2.wav",
    "Audio/punch_1.wav": "assets/audio/hit_1.wav",
    "Audio/punch_2.wav": "assets/audio/hit_2.wav",
    "Audio/punch_3.wav": "assets/audio/hit_3.wav",
    "Audio/punch_4.wav": "assets/audio/hit_4.wav",
    "Audio/punch_5.wav": "assets/audio/hit_5.wav",
    "Audio/punch_6.wav": "assets/audio/hit_6.wav",
    "Audio/squick_1.wav": "assets/audio/till_1.wav",
    "Audio/squick_2.wav": "assets/audio/till_2.wav",
    "Audio/squick_squick_1.wav": "assets/audio/till_double_1.wav",
    "Audio/squick_squick_2.wav": "assets/audio/till_double_2.wav",

    # ----- characters: player -----
    "Characters/Basic Charakter Spritesheet.png": "assets/characters/player/player.png",
    "Characters/Basic Charakter Actions.png": "assets/characters/player/player_actions.png",
    "Characters/Tools.png": "assets/characters/player/player_tools.png",
    "Early Access/Ocean Pack/swimming.png": "assets/characters/player/swimming.png",

    # ----- characters: animals -----
    "Characters/Free Chicken Sprites.png": "assets/characters/animals/chicken.png",
    "Characters/Free Cow Sprites.png": "assets/characters/animals/cow.png",
    "Characters/Egg_And_Nest.png": "assets/characters/animals/egg_and_nest.png",
    "Early Access/Plant update 2/Bee/bee_spritesheet.png": "assets/characters/animals/bee.png",
    "Early Access/Plant update 2/Bee/small_bee_spritesheet.png": "assets/characters/animals/bee_small.png",
    "Early Access/Plant update 2/frog/frog_spritesheet.png": "assets/characters/animals/frog.png",
    "Early Access/Plant update 2/frog/frog_spritesheet2.png": "assets/characters/animals/frog_2.png",

    # ----- characters: enemies -----
    "Early Access/Dungeon Pack/enemies/bat_animations.png": "assets/characters/enemies/bat.png",
    "Early Access/Dungeon Pack/enemies/small_bat_animations.png": "assets/characters/enemies/bat_small.png",
    "Early Access/Dungeon Pack/enemies/small_green_slime_animations.png": "assets/characters/enemies/slime_green_small.png",
    "Early Access/Dungeon Pack/enemies/bat.gif": "_reference/previews/bat.gif",
    "Early Access/Dungeon Pack/enemies/small bat.gif": "_reference/previews/bat_small.gif",

    # ----- world: terrain -----
    "Tilesets/Grass.png": "assets/world/terrain/grass.png",
    "Tilesets/Hills.png": "assets/world/terrain/hills.png",
    "Tilesets/Water.png": "assets/world/terrain/water.png",
    "Tilesets/Tilled_Dirt.png": "assets/world/terrain/tilled_dirt.png",
    "Tilesets/Tilled_Dirt_v2.png": "assets/world/terrain/tilled_dirt_v2.png",
    "Tilesets/Tilled_Dirt_Wide.png": "assets/world/terrain/tilled_dirt_wide.png",
    "Tilesets/Tilled_Dirt_Wide_v2.png": "assets/world/terrain/tilled_dirt_wide_v2.png",
    "Tilesets/Tilled Dirt.png": "_archive/tilled_dirt_old_128.png",  # older 128x128 layout, NOT a duplicate
    "Early Access/Plant update 2/Birch wood Biom.png": "assets/world/terrain/biome_birch.png",
    "Early Access/Plant update 2/Birch wood Biom water plants.png": "assets/world/terrain/biome_birch_water_plants.png",
    "Early Access/Plant update 2/Cherry Blossom Biom.png": "assets/world/terrain/biome_cherry.png",
    "Early Access/Plant update 2/Cherry Blossom Biom water plants.png": "assets/world/terrain/biome_cherry_water_plants.png",
    "Early Access/Plant update 2/Pine Tree Biome.png": "assets/world/terrain/biome_pine.png",
    "Early Access/Plant update 2/Pine Tree Biome water plants.png": "assets/world/terrain/biome_pine_water_plants.png",
    "Early Access/Plant update 2/Ground tilesets/Grass_Tile_Layers.png": "assets/world/terrain/grass_layers_1.png",
    "Early Access/Plant update 2/Ground tilesets/Grass_Tile_layers2.png": "assets/world/terrain/grass_layers_2.png",
    "Early Access/Plant update 2/Ground tilesets/Grass_Tile_layers3.png": "assets/world/terrain/grass_layers_3.png",
    "Early Access/Plant update 2/Ground tilesets/Grass_Tile_layers4.png": "assets/world/terrain/grass_layers_4.png",

    # ----- world: structures -----
    "Tilesets/Wooden House.png": "assets/world/structures/house_wooden.png",
    "Tilesets/Wooden_House_Walls_Tilset.png": "assets/world/structures/house_wooden_walls.png",
    "Tilesets/Wooden_House_Roof_Tilset.png": "assets/world/structures/house_wooden_roof.png",
    "Tilesets/Doors.png": "assets/world/structures/doors.png",
    "Tilesets/Fences.png": "assets/world/structures/fences.png",
    "Objects/Free_Chicken_House.png": "assets/world/structures/chicken_house.png",
    "Early Access/Village pack/houses/wooden_door_spritesheet.png": "assets/world/structures/door_wooden_anim.png",
    "Early Access/Village pack/houses/Grey brick house/grey_brick_houses.png": "assets/world/structures/village_brick_base.png",
    "Early Access/Village pack/houses/Grey brick house/grey_brick_houses_with_doors.png": "assets/world/structures/village_brick_doors.png",
    "Early Access/Village pack/houses/Grey brick house/grey_brick_houses_with_doors_grass.png": "assets/world/structures/village_brick_doors_grass.png",
    "Early Access/Village pack/houses/Grey brick house/grey_brick_houses_with_grass.png": "assets/world/structures/village_brick_grass.png",
    "Early Access/Village pack/houses/Grey brick house/brick_houses_shadow.png": "assets/world/structures/village_brick_shadow.png",
    "Early Access/Village pack/houses/small house/small_House.png": "assets/world/structures/village_house_base.png",
    "Early Access/Village pack/houses/small house/small_House_light.png": "assets/world/structures/village_house_light.png",
    "Early Access/Village pack/houses/small house/small_House_light_with_door.png": "assets/world/structures/village_house_light_door.png",
    "Early Access/Village pack/houses/small house/small_House_light_with_door_grass.png": "assets/world/structures/village_house_light_door_grass.png",
    "Early Access/Village pack/houses/small house/small_House_light_with_grass.png": "assets/world/structures/village_house_light_grass.png",
    "Early Access/Village pack/houses/small house/small_House_shadow.png": "assets/world/structures/village_house_shadow.png",
    "Early Access/Village pack/houses/small house/small_House_with_door.png": "assets/world/structures/village_house_door.png",
    "Early Access/Village pack/houses/small house/small_House_with_door_grass.png": "assets/world/structures/village_house_door_grass.png",
    "Early Access/Village pack/houses/small house/small_House_with_grass.png": "assets/world/structures/village_house_grass.png",
    "Early Access/Village pack/houses/small hut/small_huts.png": "assets/world/structures/village_hut_base.png",
    "Early Access/Village pack/houses/small hut/small_huts_with_doors.png": "assets/world/structures/village_hut_doors.png",
    "Early Access/Village pack/houses/small hut/small_huts_with_doors_grass.png": "assets/world/structures/village_hut_doors_grass.png",
    "Early Access/Village pack/houses/small hut/small_huts_with_grass.png": "assets/world/structures/village_hut_grass.png",
    "Early Access/Village pack/houses/small hut/small_hut_shadow.png": "assets/world/structures/village_hut_shadow.png",

    # ----- world: props -----
    "Objects/Basic_Furniture.png": "assets/world/props/furniture_basic.png",
    "Early Access/Plant update 2/Furniture/new Wooden Furniture.png": "assets/world/props/furniture_wooden.png",
    "Early Access/Plant update 2/Furniture/new Wooden Furniture items.png": "assets/world/props/furniture_wooden_items.png",
    "Objects/Basic_Grass_Biom_things.png": "assets/world/props/grass_biome_props.png",
    "Early Access/Plant update 2/Trees, stumps and bushes v2.png": "assets/world/props/trees_stumps_bushes.png",
    "Early Access/Plant update 2/wood n shroms.png": "assets/world/props/wood_and_shrooms.png",
    "Objects/Chest.png": "assets/world/props/chest.png",
    "Early Access/Plant update 2/Furniture/Birch_Chest.png": "assets/world/props/chest_birch.png",
    "Early Access/Plant update 2/Furniture/Cherry_Chest.png": "assets/world/props/chest_cherry.png",
    "Early Access/Plant update 2/Furniture/Golden_Chest.png": "assets/world/props/chest_golden.png",
    "Early Access/Plant update 2/Furniture/Oak_Chest.png": "assets/world/props/chest_oak.png",
    "Early Access/Plant update 2/Furniture/Pine_Chest.png": "assets/world/props/chest_pine.png",
    "Early Access/Plant update 2/Furniture/Silver_Chest.png": "assets/world/props/chest_silver.png",
    "Objects/Wood_Bridge.png": "assets/world/props/bridge_wood.png",
    "Objects/Paths.png": "assets/world/props/paths.png",
    "Early Access/Plant update 2/piknik/Piknik basket.png": "assets/world/props/picnic_basket.png",
    "Early Access/Plant update 2/piknik/Piknik blanket.png": "assets/world/props/picnic_blanket.png",
    "Early Access/Plant update 2/Bee/beehive.png": "assets/world/props/beehive.png",
    "Early Access/Plant update 2/Bee/small_beehive.png": "assets/world/props/beehive_small.png",

    # ----- farming -----
    "Objects/Basic_Plants.png": "assets/farming/plants_basic.png",
    "Early Access/Plant update 2/Farming Plants v2.png": "assets/farming/crops.png",
    "Early Access/Plant update 2/Farming Plants v2 watered.png": "assets/farming/crops_watered.png",
    "Early Access/Plant update 2/Farming Plants items v2.png": "assets/farming/crop_items.png",

    # ----- fishing -----
    "Early Access/Ocean Pack/Fish Sprites.png": "assets/fishing/fish_sprites.png",
    "Early Access/Ocean Pack/small fish.png": "assets/fishing/fish_small.png",
    "Early Access/Ocean Pack/mediuml fish.png": "assets/fishing/fish_medium.png",
    "Early Access/Ocean Pack/big fish 2 swimming in cirkels.png": "assets/fishing/fish_big_circles.png",
    "Early Access/Ocean Pack/fishing_rod.png": "assets/fishing/fishing_rod.png",
    "Early Access/Ocean Pack/fishing_rod_2.png": "assets/fishing/fishing_rod_2.png",
    "Early Access/Ocean Pack/fishing animation front.png": "assets/fishing/fishing_anim_front.png",
    "Early Access/Ocean Pack/fishing animation back.png": "assets/fishing/fishing_anim_back.png",
    "Early Access/Ocean Pack/fishing animation side.png": "assets/fishing/fishing_anim_side.png",
    "Early Access/Ocean Pack/fishing water splash frames and rod.png": "assets/fishing/fishing_splash_and_rod.png",

    # ----- mining -----
    "Early Access/Dungeon Pack/tiles/Dungeon_walls.png": "assets/mining/walls.png",
    "Early Access/Dungeon Pack/tiles/dungeon_walls_decor_gates.png": "assets/mining/walls_decor_gates.png",
    "Early Access/Dungeon Pack/tiles/Dungeon_probs.png": "assets/mining/props.png",
    "Early Access/Dungeon Pack/tiles/Rocks.png": "assets/mining/rocks.png",
    "Early Access/Dungeon Pack/tiles/Rails.png": "assets/mining/rails.png",
    "Early Access/Dungeon Pack/tiles/Carts.png": "assets/mining/carts.png",
    "Early Access/Dungeon Pack/tiles/dungeon_items.png": "assets/mining/items.png",
    "Early Access/Dungeon Pack/tiles/switch.png": "assets/mining/switch.png",
    "Early Access/Dungeon Pack/tiles/ground_dirt_orange.png": "assets/mining/ground_orange.png",
    "Early Access/Dungeon Pack/tiles/ground_dirt_orange_dark.png": "assets/mining/ground_orange_dark.png",
    "Early Access/Dungeon Pack/tiles/ground_dirt_orange_hole.png": "assets/mining/ground_orange_hole.png",
    "Early Access/Dungeon Pack/tiles/ground_dirt_orange_darker_hole.png": "assets/mining/ground_orange_darker_hole.png",

    # ----- seasons: winter -----
    "Early Access/Sprout winter/snow tiles 1.png": "assets/seasons/winter/snow_tiles_1.png",
    "Early Access/Sprout winter/snow tiles 2.png": "assets/seasons/winter/snow_tiles_2.png",
    "Early Access/Sprout winter/ice tiles.png": "assets/seasons/winter/ice_tiles.png",
    "Early Access/Sprout winter/snomwflakes.png": "assets/seasons/winter/snowflakes.png",
    "Early Access/Sprout winter/campfire.png": "assets/seasons/winter/campfire.png",
    "Early Access/Sprout winter/fire animation.png": "assets/seasons/winter/fire_anim.png",
    "Early Access/Sprout winter/christmas tree.png": "assets/seasons/winter/christmas_tree.png",
    "Early Access/Sprout winter/present red.png": "assets/seasons/winter/present_red.png",
    "Early Access/Sprout winter/present red 2.png": "assets/seasons/winter/present_red_2.png",
    "Early Access/Sprout winter/present red 3.png": "assets/seasons/winter/present_red_3.png",
    "Early Access/Sprout winter/present green.png": "assets/seasons/winter/present_green.png",
    "Early Access/Sprout winter/present green 2.png": "assets/seasons/winter/present_green_2.png",
    "Early Access/Sprout winter/present animation aseprite file.png": "assets/seasons/winter/present_anim.png",
    "Early Access/Sprout winter/winter items.png": "assets/seasons/winter/winter_items.png",
    "Early Access/Sprout winter/winter sprites.png": "assets/seasons/winter/winter_sprites.png",
    "Early Access/Plant update 2/Ground tilesets/blue_tint_Grass_Tile_Layers.png": "assets/seasons/winter/grass_layers_cold_1.png",
    "Early Access/Plant update 2/Ground tilesets/blue_tint_Grass_Tile_Layers2.png": "assets/seasons/winter/grass_layers_cold_2.png",
    "Early Access/Plant update 2/Ground tilesets/blue_tint_Grass_Tile_Layers3.png": "assets/seasons/winter/grass_layers_cold_3.png",
    "Early Access/Plant update 2/Ground tilesets/blue_tint_Grass_Tile_Layers4.png": "assets/seasons/winter/grass_layers_cold_4.png",

    # ----- items -----
    "Objects/Egg_item.png": "assets/items/egg.png",
    "Objects/Simple_Milk_and_grass_item.png": "assets/items/milk_and_grass.png",
    "Objects/Basic_tools_and_meterials.png": "assets/items/tools_and_materials.png",
    "Early Access/Plant update 2/Bee/bread_jam_honey_items.png": "assets/items/bread_jam_honey.png",
    "Early Access/Plant update 2/piknik/piknik_foods.png": "assets/items/picnic_foods.png",

    # ----- ui: panels -----
    "UI/Sprite sheets/Dialouge UI/dialog box.png": "assets/ui/panels/dialog_9slice.png",
    "UI/Sprite sheets/Dialouge UI/dialog box small.png": "assets/ui/panels/dialog_small.png",
    "UI/Sprite sheets/Dialouge UI/dialog box medium.png": "assets/ui/panels/dialog_medium.png",
    "UI/Sprite sheets/Dialouge UI/dialog box big.png": "assets/ui/panels/dialog_big.png",

    # ----- ui: buttons -----
    "UI/Sprite sheets/buttons/Square Buttons 26x26.png": "assets/ui/buttons/square_26x26.png",
    "UI/Sprite sheets/buttons/Square Buttons 26x19.png": "assets/ui/buttons/square_26x19.png",
    "UI/Sprite sheets/buttons/Square Buttons 19x26.png": "assets/ui/buttons/square_19x26.png",
    "UI/Sprite sheets/buttons/Small Square Buttons.png": "assets/ui/buttons/square_small.png",
    "UI/Sprite sheets/UI Big Play Button.png": "assets/ui/buttons/play_big.png",
    "UI/Sprite sheets/UI Settings Buttons.png": "assets/ui/buttons/settings_buttons.png",
    "UI/Sprite sheets/Setting menu.png": "assets/ui/buttons/settings_menu.png",

    # ----- ui: icons -----
    "UI/Sprite sheets/Icons/All Icons.png": "assets/ui/icons/all_icons.png",
    "UI/Sprite sheets/Icons/white icons.png": "assets/ui/icons/white_icons.png",
    "UI/Sprite sheets/Icons/special icons/Special Icons.png": "assets/ui/icons/special_icons.png",
    "UI/Sprite sheets/Icons/special icons/Small Happines-Sadness icons.png": "assets/ui/icons/happiness_icons.png",

    # ----- ui: hud -----
    "UI/emojis-free/emoji style ui/Inventory_Herat_Spritesheet.png": "assets/ui/hud/hearts.png",
    "UI/emojis-free/emoji style ui/Inventory_Light_Herat_Spritesheet.png": "assets/ui/hud/hearts_light.png",
    "UI/emojis-free/emoji style ui/Inventory_Blocks_Spritesheet.png": "assets/ui/hud/inventory_blocks.png",
    "UI/emojis-free/emoji style ui/Inventory_Spritesheet.png": "assets/ui/hud/inventory_sheet.png",
    "UI/emojis-free/emoji style ui/weather/Weather_Icons_smal_freel.png": "assets/ui/hud/weather_icons.png",
    "UI/emojis-free/emoji style ui/weather/Weather_UI_Free.png": "assets/ui/hud/weather_ui.png",

    # ----- ui: cursors -----
    "UI/Sprite sheets/Mouse sprites/Catpaw Mouse icon.png": "assets/ui/cursors/catpaw.png",
    "UI/Sprite sheets/Mouse sprites/Catpaw holding Mouse icon.png": "assets/ui/cursors/catpaw_holding.png",
    "UI/Sprite sheets/Mouse sprites/Catpaw pointing Mouse icon.png": "assets/ui/cursors/catpaw_pointing.png",
    "UI/Sprite sheets/Mouse sprites/Triangle Mouse icon 1.png": "assets/ui/cursors/triangle_1.png",
    "UI/Sprite sheets/Mouse sprites/Triangle Mouse icon 2.png": "assets/ui/cursors/triangle_2.png",
    "UI/Sprite sheets/Mouse sprites/Triangle Mouse icon 3.png": "assets/ui/cursors/triangle_3.png",

    # ----- ui: emotes -----
    "UI/Sprite sheets/Dialouge UI/Emotes/Teemo Basic emote animations sprite sheet.png": "assets/ui/emotes/player_emotes.png",
    "UI/emojis-free/Emoji_Spritesheet_Free.png": "assets/ui/emotes/emoji.png",
    "UI/emojis-free/speech_bubble_grey.png": "assets/ui/emotes/speech_bubble.png",
    "UI/Sprite sheets/Dialouge UI/dialog box character finished talking click to continue indicator - spritesheet .png": "assets/ui/emotes/dialog_continue_indicator.png",

    # ----- ui: fonts -----
    "UI/fonts/pixelFont-7-8x14-sproutLands.ttf": "assets/ui/fonts/sprout.ttf",

    # ----- _reference: docs for humans -----
    "Tilesets/Bitmask references 1.png": "_reference/bitmask_1.png",
    "Tilesets/Bitmask references 2.png": "_reference/bitmask_2.png",
    "Tilesets/Bitmask references gif.gif": "_reference/bitmask.gif",
    "UI/Sprite sheets/Dialouge UI/Premade dialog box small.png": "_reference/mockups/premade_dialog_small.png",
    "UI/Sprite sheets/Dialouge UI/Premade dialog box medium.png": "_reference/mockups/premade_dialog_medium.png",
    "UI/Sprite sheets/Dialouge UI/Premade dialog box  big.png": "_reference/mockups/premade_dialog_big.png",
    "UI/emojis-free/emoji style ui/inventory_example.png": "_reference/mockups/inventory.png",
    "UI/emojis-free/emoji style ui/inventory_example_2.png": "_reference/mockups/inventory_2.png",
    "UI/emojis-free/emoji style ui/inventory_example_with_slots.png": "_reference/mockups/inventory_slots.png",
    "UI/emojis-free/emoji style ui/inventory_example_with_slots_2.png": "_reference/mockups/inventory_slots_2.png",
    "UI/emojis-free/emoji style ui/inventory_Light_example.png": "_reference/mockups/inventory_light.png",
    "UI/emojis-free/emoji style ui/inventory_Light_example_2.png": "_reference/mockups/inventory_light_2.png",
    "UI/emojis-free/emoji style ui/inventory_Light_example_with_slots.png": "_reference/mockups/inventory_light_slots.png",
    "UI/emojis-free/emoji style ui/Inventory_Light_example_with_slots_2.png": "_reference/mockups/inventory_light_slots_2.png",
    "UI/Sprite sheets/Sprite sheet for Basic Pack.png": "_reference/pack_contact_sheet.png",
    "Sprout Lands color pallet/Sprout Lands defautlt palette.png": "_reference/palette.png",
    "Sprout Lands color pallet/Sprout Lands defautlt palette snip.PNG": "_reference/palette_snip.png",
    "UI/fonts/pixel-letters-7-8x14.png": "_reference/font_letters.png",
    "UI/fonts/pixel-letters-7-8x14-preview.png": "_reference/font_preview.png",

    # ----- _source: aseprite originals -----
    "Sprout Lands color pallet/Sprout Lands defautlt palette.aseprite": "_source/palette.aseprite",
    "Early Access/Sprout winter/christmas tree aseprite file.aseprite": "_source/christmas_tree.aseprite",
    "Early Access/Sprout winter/fire aseprite file.aseprite": "_source/fire.aseprite",
    "Early Access/Sprout winter/present animation aseprite file.aseprite": "_source/present_anim.aseprite",

    # ----- _archive: pack tests + superseded -----
    "Tests/free_character_spritesheet_by-cupnooble.png": "_archive/tests/free_character_spritesheet.png",
    "Tests/teemo 8 directions.png": "_archive/tests/teemo_8_directions.png",
    "Tests/teemo 8 directions test.gif": "_archive/tests/teemo_8_directions.gif",
    "Tests/test character test .gif": "_archive/tests/character_test.gif",

    # ----- dropped byte-identical duplicates (checksums verified) -----
    "Objects/Basic Furniture.png": DROP,
    "Objects/Basic Grass Biom things 1.png": DROP,
    "Objects/Basic Plants.png": DROP,
    "Objects/Basic tools and meterials.png": DROP,
    "Objects/Egg item.png": DROP,
    "Objects/Simple Milk and grass item.png": DROP,
    "Objects/Wood Bridge.png": DROP,
}


def sha1(path: Path) -> str:
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 1
    src = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2]).resolve()
    if not src.is_dir():
        print(f"error: source pack not found: {src}")
        return 1

    # Inventory the pack.
    pack_files = sorted(
        p.relative_to(src).as_posix() for p in src.rglob("*") if p.is_file()
    )

    unmapped = [f for f in pack_files if f not in MAPPING]
    missing = [f for f in MAPPING if f not in set(pack_files)]

    if unmapped:
        print("UNMAPPED files in pack (add them to MAPPING):")
        for f in unmapped:
            print("  ", f)
    if missing:
        print("MAPPING entries not found in pack (check names):")
        for f in missing:
            print("  ", f)
    if unmapped or missing:
        print("aborting: mapping must cover the pack exactly.")
        return 2

    # Verify the DROP entries really are duplicates of a kept file.
    kept_by_hash: dict[str, str] = {}
    for rel, dest in MAPPING.items():
        if dest != DROP:
            kept_by_hash.setdefault(sha1(src / rel), rel)
    for rel, dest in MAPPING.items():
        if dest == DROP:
            h = sha1(src / rel)
            if h not in kept_by_hash:
                print(f"refusing to drop {rel}: no kept file shares its checksum")
                return 3

    # Copy. Runtime assets go under public/ (Vite's static dir); the
    # _reference/_source/_archive trees sit at the repo root.
    manifest: dict[str, str] = {}
    copied = dropped = 0
    for rel, dest in sorted(MAPPING.items()):
        if dest == DROP:
            dropped += 1
            continue
        prefixed = f"public/{dest}" if dest.startswith("assets/") else dest
        target = out / prefixed
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src / rel, target)
        manifest[dest] = rel
        copied += 1

    mpath = out / "public" / "assets" / "manifest.json"
    mpath.parent.mkdir(parents=True, exist_ok=True)
    mpath.write_text(json.dumps(manifest, indent=2, sort_keys=True))

    print(f"pack files: {len(pack_files)}  copied: {copied}  dropped duplicates: {dropped}")
    print(f"manifest: {mpath}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
