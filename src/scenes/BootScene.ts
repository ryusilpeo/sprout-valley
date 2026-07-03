import Phaser from 'phaser';
import { ASSETS, VIEW } from '../core/constants';

/**
 * Phase 0 boot: proves the reorganized asset pipeline end to end by loading
 * one real sprite from the new paths and drawing it. Nothing else lives here
 * yet — Phase 1 replaces this with the Tiled map loader.
 */
export default class BootScene extends Phaser.Scene {
  constructor() {
    super({ key: 'Boot' });
  }

  preload(): void {
    // 48x48 frames, 4x4 grid: rows = down/up/left/right idle+walk.
    this.load.spritesheet('player', `${ASSETS}/characters/player/player.png`, {
      frameWidth: 48,
      frameHeight: 48,
    });
  }

  create(): void {
    const cx = VIEW.width / 2;
    const cy = VIEW.height / 2;

    this.add
      .text(cx, cy - 60, 'SPROUT VALLEY', {
        fontFamily: 'monospace',
        fontSize: '28px',
        color: '#5d4126',
      })
      .setOrigin(0.5);

    this.add.image(cx, cy + 10, 'player', 0).setScale(3);

    this.add
      .text(cx, cy + 70, 'phase 0: pipeline ok', {
        fontFamily: 'monospace',
        fontSize: '14px',
        color: '#4f8a4a',
      })
      .setOrigin(0.5);
  }
}
