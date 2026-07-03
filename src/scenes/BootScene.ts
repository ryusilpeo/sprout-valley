import Phaser from 'phaser';
import { ASSETS } from '../core/constants';

/**
 * Boot: load the handful of textures needed before the map appears, generate a
 * small placeholder marker for the not-yet-real player, then start MapScene.
 */
export default class BootScene extends Phaser.Scene {
  constructor() {
    super({ key: 'Boot' });
  }

  preload(): void {
    this.load.spritesheet('player', `${ASSETS}/characters/player/player.png`, {
      frameWidth: 48,
      frameHeight: 48,
    });
  }

  create(): void {
    // A simple ring marker as the temporary player stand-in for Phase 1.
    const g = this.add.graphics();
    g.lineStyle(2, 0xffffff, 1).strokeCircle(8, 8, 6);
    g.fillStyle(0x5b8bd0, 1).fillCircle(8, 8, 3);
    g.generateTexture('player_marker', 16, 16);
    g.destroy();

    this.scene.start('Map');
  }
}
