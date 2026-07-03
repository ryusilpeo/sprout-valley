/** One place for the numbers everything else agrees on. */

/** Native tile size of every Sprout Lands tileset. */
export const TILE = 16;

/** Camera zoom: 16px art shown at 3x reads closest to the reference GIF. */
export const ZOOM = 3;

/** Logical viewport in screen pixels (canvas size before CSS scaling). */
export const VIEW = { width: 600, height: 600 } as const;

/** Root of all runtime assets (see public/assets/manifest.json for origins). */
export const ASSETS = 'assets';
