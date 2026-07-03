import Phaser from 'phaser';
import { ASSETS, TILE, ZOOM } from '../core/constants';

/**
 * Phase 1 — loads the hand-built Tiled map (exported to JSON), renders its
 * tile layers, animates the water, and turns the "collision" object layer into
 * static physics bodies. A placeholder marker stands in for the player until
 * Phase 2; the camera centres on the map's player_spawn.
 *
 * Pipeline reminder: edit tiled/maps/farm.tmx in Tiled, then run
 *   python3 tiled/tmx_to_json.py tiled/maps/farm.tmx
 * to refresh public/assets/maps/farm.json that this scene loads.
 */
export default class MapScene extends Phaser.Scene {
  constructor() {
    super({ key: 'Map' });
  }

  preload(): void {
    this.load.tilemapTiledJSON('farm', `${ASSETS}/maps/farm.json`);
    // Tileset images — keys must match the tileset "name" in the map JSON.
    this.load.image('water', `${ASSETS}/world/terrain/water.png`);
    this.load.image('grass', `${ASSETS}/world/terrain/grass.png`);
    this.load.image('tilled_dirt', `${ASSETS}/world/terrain/tilled_dirt.png`);
  }

  create(): void {
    const map = this.make.tilemap({ key: 'farm' });

    const water = map.addTilesetImage('water', 'water')!;
    const grass = map.addTilesetImage('grass', 'grass')!;
    const soil = map.addTilesetImage('tilled_dirt', 'tilled_dirt')!;
    const sets = [water, grass, soil];

    const ground = map.createLayer('ground', sets, 0, 0)!;
    map.createLayer('farm', sets, 0, 0)!;

    this.animateWater(map, ground);
    this.buildCollision(map);
    this.setupCamera(map);
    this.placePlayerMarker(map);
  }

  /**
   * The water tile carries a Tiled animation (4 frames). Phaser doesn't play
   * tile animations from static layers automatically, so we swap the tile
   * index on a timer across every water tile in the ground layer.
   */
  private animateWater(map: Phaser.Tilemaps.Tilemap, layer: Phaser.Tilemaps.TilemapLayer): void {
    const waterSet = map.getTileset('water') as Phaser.Tilemaps.Tileset;
    const first = waterSet.firstgid; // GIDs first..first+3
    let frame = 0;
    this.time.addEvent({
      delay: 350,
      loop: true,
      callback: () => {
        frame = (frame + 1) % 4;
        layer.forEachTile((tile) => {
          if (tile.index >= first && tile.index <= first + 3) {
            tile.index = first + frame;
          }
        });
      },
    });
  }

  /** Turn the "collision" object rectangles into static bodies. */
  private buildCollision(map: Phaser.Tilemaps.Tilemap): void {
    const objs = map.getObjectLayer('collision');
    if (!objs) return;
    const statics = this.physics.add.staticGroup();
    for (const o of objs.objects) {
      if (o.width && o.height) {
        const body = this.add.rectangle(
          (o.x ?? 0) + o.width / 2,
          (o.y ?? 0) + o.height / 2,
          o.width,
          o.height
        );
        statics.add(body);
      }
    }
    this.registry.set('collision', statics);
  }

  private setupCamera(map: Phaser.Tilemaps.Tilemap): void {
    const cam = this.cameras.main;
    cam.setZoom(ZOOM);
    cam.setBounds(0, 0, map.widthInPixels, map.heightInPixels);
    const spawn = this.spawnPoint(map);
    cam.centerOn(spawn.x, spawn.y);
  }

  private spawnPoint(map: Phaser.Tilemaps.Tilemap): { x: number; y: number } {
    const spawns = map.getObjectLayer('spawns');
    const p = spawns?.objects.find((o) => o.name === 'player_spawn');
    if (p) return { x: (p.x ?? 0) + TILE / 2, y: (p.y ?? 0) + TILE / 2 };
    return { x: map.widthInPixels / 2, y: map.heightInPixels / 2 };
  }

  /** Temporary stand-in for the player (Phase 2 replaces this). */
  private placePlayerMarker(map: Phaser.Tilemaps.Tilemap): void {
    const s = this.spawnPoint(map);
    this.add.image(s.x, s.y, 'player_marker').setDepth(100);
  }
}
