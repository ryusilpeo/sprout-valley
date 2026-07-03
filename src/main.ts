import Phaser from 'phaser';
import BootScene from './scenes/BootScene';
import { VIEW } from './core/constants';

new Phaser.Game({
  type: Phaser.AUTO,
  parent: 'game',
  width: VIEW.width,
  height: VIEW.height,
  backgroundColor: '#a6d9c8',
  pixelArt: true, // crisp 16px art: nearest-neighbour scaling, no antialiasing
  scene: [BootScene],
});
