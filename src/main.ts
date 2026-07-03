import Phaser from 'phaser';
import BootScene from './scenes/BootScene';
import MapScene from './scenes/MapScene';
import { VIEW } from './core/constants';

new Phaser.Game({
  type: Phaser.AUTO,
  parent: 'game',
  width: VIEW.width,
  height: VIEW.height,
  backgroundColor: '#a6d9c8',
  pixelArt: true,
  physics: { default: 'arcade', arcade: { debug: false } },
  scene: [BootScene, MapScene],
});
