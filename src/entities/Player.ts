import Phaser from 'phaser';
import { PLAYER_SPEED } from '../core/constants';

type Dir = 'down' | 'up' | 'left' | 'right';

/** First frame of each direction's row in the 4x4 player sheet. */
const ROW_START: Record<Dir, number> = { down: 0, up: 4, left: 8, right: 12 };

/**
 * The player: 4-direction walking sprite with arcade physics.
 *
 * player.png is a 4x4 grid of 48x48 frames — rows are down/up/left/right
 * (verified against the sheet's pixels; left and right are real rows, not
 * flips). The physics body covers only the feet so the character can stand
 * in front of obstacles, top-down style.
 */
export default class Player extends Phaser.Physics.Arcade.Sprite {
  private facing: Dir = 'down';
  private keys: {
    up: Phaser.Input.Keyboard.Key;
    down: Phaser.Input.Keyboard.Key;
    left: Phaser.Input.Keyboard.Key;
    right: Phaser.Input.Keyboard.Key;
    w: Phaser.Input.Keyboard.Key;
    a: Phaser.Input.Keyboard.Key;
    s: Phaser.Input.Keyboard.Key;
    d: Phaser.Input.Keyboard.Key;
  };

  constructor(scene: Phaser.Scene, x: number, y: number) {
    super(scene, x, y, 'player', 0);
    scene.add.existing(this);
    scene.physics.add.existing(this);

    // The visible character occupies x17..30 / y16..31 of the 48x48 frame;
    // collide with a band at the feet.
    const body = this.body as Phaser.Physics.Arcade.Body;
    body.setSize(12, 8);
    body.setOffset(18, 24);

    Player.registerAnimations(scene.anims);

    const kb = scene.input.keyboard!;
    const cursors = kb.createCursorKeys();
    const wasd = kb.addKeys('W,A,S,D') as Record<
      'W' | 'A' | 'S' | 'D',
      Phaser.Input.Keyboard.Key
    >;
    this.keys = {
      up: cursors.up,
      down: cursors.down,
      left: cursors.left,
      right: cursors.right,
      w: wasd.W,
      a: wasd.A,
      s: wasd.S,
      d: wasd.D,
    };
  }

  static registerAnimations(anims: Phaser.Animations.AnimationManager): void {
    for (const dir of Object.keys(ROW_START) as Dir[]) {
      const key = `walk_${dir}`;
      if (anims.exists(key)) continue;
      const start = ROW_START[dir];
      anims.create({
        key,
        frames: anims.generateFrameNumbers('player', { start, end: start + 3 }),
        frameRate: 8,
        repeat: -1,
      });
    }
  }

  update(): void {
    const k = this.keys;
    const move = new Phaser.Math.Vector2(
      Number(k.right.isDown || k.d.isDown) - Number(k.left.isDown || k.a.isDown),
      Number(k.down.isDown || k.s.isDown) - Number(k.up.isDown || k.w.isDown)
    );

    if (move.lengthSq() > 0) {
      move.normalize().scale(PLAYER_SPEED);
      // Horizontal wins the facing on diagonals so the animation doesn't flip-flop.
      this.facing = move.x !== 0 ? (move.x > 0 ? 'right' : 'left') : move.y > 0 ? 'down' : 'up';
      this.setVelocity(move.x, move.y);
      this.play(`walk_${this.facing}`, true);
    } else {
      this.setVelocity(0, 0);
      this.stop();
      this.setFrame(ROW_START[this.facing]);
    }
  }
}
