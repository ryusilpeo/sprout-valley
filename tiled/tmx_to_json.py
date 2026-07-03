#!/usr/bin/env python3
"""
Convert a Tiled .tmx map into the JSON format Phaser's tilemap loader expects,
writing it to public/assets/maps/ so the game can load it at runtime.

Phaser reads Tiled's JSON, not .tmx. You *can* also just use Tiled's own
"Export As -> JSON" — this script exists so the pipeline works headless and
stays reproducible (CI, or when you'd rather not click through Tiled's export).

It embeds each tileset's tile/column counts and rewrites the image `source`
to a web path under assets/, so Phaser can find the sheets. Wang/terrain data
is editor-only and dropped (Phaser doesn't need it). Object layers (collision,
spawns) are preserved.

Run:  python3 tiled/tmx_to_json.py tiled/maps/farm.tmx
"""
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
# Maps a tileset image's on-disk location to the web path Phaser will request.
# .tsx images are "../../public/assets/..." relative to tiled/tilesets/.
def web_image_path(tsx_image_source: str, tsx_path: Path) -> str:
    abs_img = (tsx_path.parent / tsx_image_source).resolve()
    # strip everything up to and including "public/"
    parts = abs_img.parts
    i = parts.index("public")
    return "/".join(parts[i + 1 :])  # e.g. assets/world/terrain/grass.png


def parse_tsx(tsx_path: Path) -> dict:
    root = ET.parse(tsx_path).getroot()
    img = root.find("image")
    tiles = {}
    for tile in root.findall("tile"):
        tid = int(tile.get("id"))
        entry = {}
        props = tile.find("properties")
        if props is not None:
            entry["properties"] = [
                {"name": p.get("name"), "type": p.get("type", "string"), "value": p.get("value")}
                for p in props.findall("property")
            ]
        anim = tile.find("animation")
        if anim is not None:
            entry["animation"] = [
                {"tileid": int(f.get("tileid")), "duration": int(f.get("duration"))}
                for f in anim.findall("frame")
            ]
        if entry:
            entry["id"] = tid
            tiles[tid] = entry
    return {
        "name": root.get("name"),
        "tilewidth": int(root.get("tilewidth")),
        "tileheight": int(root.get("tileheight")),
        "tilecount": int(root.get("tilecount")),
        "columns": int(root.get("columns")),
        "image": web_image_path(img.get("source"), tsx_path),
        "imagewidth": int(img.get("width")),
        "imageheight": int(img.get("height")),
        "tiles": tiles,
    }


def convert(tmx_path: Path) -> dict:
    root = ET.parse(tmx_path).getroot()
    out = {
        "compressionlevel": -1,
        "infinite": False,
        "orientation": root.get("orientation"),
        "renderorder": root.get("renderorder"),
        "width": int(root.get("width")),
        "height": int(root.get("height")),
        "tilewidth": int(root.get("tilewidth")),
        "tileheight": int(root.get("tileheight")),
        "nextlayerid": int(root.get("nextlayerid", "1")),
        "nextobjectid": int(root.get("nextobjectid", "1")),
        "type": "map",
        "version": "1.10",
        "tiledversion": "1.11.0",
        "tilesets": [],
        "layers": [],
    }

    for ts in root.findall("tileset"):
        firstgid = int(ts.get("firstgid"))
        source = ts.get("source")
        tsx_path = (tmx_path.parent / source).resolve()
        info = parse_tsx(tsx_path)
        ts_json = {
            "firstgid": firstgid,
            "name": info["name"],
            "tilewidth": info["tilewidth"],
            "tileheight": info["tileheight"],
            "tilecount": info["tilecount"],
            "columns": info["columns"],
            "image": info["image"],
            "imagewidth": info["imagewidth"],
            "imageheight": info["imageheight"],
            "margin": 0,
            "spacing": 0,
        }
        if info["tiles"]:
            ts_json["tiles"] = list(info["tiles"].values())
        out["tilesets"].append(ts_json)

    lid = 1
    for layer in root:
        if layer.tag == "layer":
            data_el = layer.find("data")
            csv_txt = data_el.text.strip()
            data = [int(v) for v in csv_txt.replace("\n", ",").split(",") if v.strip() != ""]
            out["layers"].append({
                "id": int(layer.get("id", lid)),
                "name": layer.get("name"),
                "type": "tilelayer",
                "width": int(layer.get("width")),
                "height": int(layer.get("height")),
                "x": 0, "y": 0,
                "opacity": 1,
                "visible": True,
                "data": data,
            })
            lid += 1
        elif layer.tag == "objectgroup":
            objs = []
            for o in layer.findall("object"):
                obj = {
                    "id": int(o.get("id")),
                    "x": float(o.get("x", 0)),
                    "y": float(o.get("y", 0)),
                    "width": float(o.get("width", 0)),
                    "height": float(o.get("height", 0)),
                    "visible": True,
                    "rotation": 0,
                }
                if o.get("name"):
                    obj["name"] = o.get("name")
                objs.append(obj)
            out["layers"].append({
                "id": int(layer.get("id", lid)),
                "name": layer.get("name"),
                "type": "objectgroup",
                "opacity": 1,
                "visible": True,
                "x": 0, "y": 0,
                "objects": objs,
                "draworder": "topdown",
            })
            lid += 1

    return out


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 1
    tmx = Path(sys.argv[1]).resolve()
    data = convert(tmx)
    out = REPO / "public" / "assets" / "maps" / (tmx.stem + ".json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=1))
    print(f"wrote {out.relative_to(REPO)}  "
          f"({data['width']}x{data['height']}, {len(data['layers'])} layers, "
          f"{len(data['tilesets'])} tilesets)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
