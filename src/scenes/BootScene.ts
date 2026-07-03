import Phaser from 'phaser';
import { ASSETS } from '../core/constants';

/**
 * Boot: load the handful of textures needed before the map appears, then
 * start MapScene.
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
    this.scene.start('Map');
  }
}
