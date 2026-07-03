<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.10" tiledversion="1.11.0" name="grass" tilewidth="16" tileheight="16" tilecount="77" columns="11">
 <image source="../../public/assets/world/terrain/grass.png" width="176" height="112"/>
 <!--
   Autotiling: this tileset defines a Wang "corner" terrain set called "grass".
   Paint with the Terrain Brush (keyboard: T) and Tiled fills in the right
   edge/corner tiles automatically. Two terrains:
     - empty  (transparent / not-grass, colour left as background)
     - grass  (the green)
   Corner colours are read clockwise from top: TopRight, BottomRight,
   BottomLeft, TopLeft. The 3x3 blob at tiles 0,1,2 / 11,12,13 / 22,23,24 is
   the border set; tile 12 is fully-grass; solid texture variants live in
   rows 5-6 for hand-detailing.
 -->
 <wangsets>
  <wangset name="grass" type="corner" tile="12">
   <wangcolor name="grass" color="#7bb34a" tile="12" probability="1"/>
   <!-- corner mask order: TR, BR, BL, TL. 0 = empty, 1 = grass -->
   <wangtile tileid="0"  wangid="0,0,0,1,0,0,0,0"/>  <!-- TL outer corner -->
   <wangtile tileid="1"  wangid="0,0,0,1,0,1,0,0"/>  <!-- top edge -->
   <wangtile tileid="2"  wangid="0,0,0,0,0,1,0,0"/>  <!-- TR outer corner -->
   <wangtile tileid="11" wangid="0,1,0,1,0,0,0,0"/>  <!-- left edge -->
   <wangtile tileid="12" wangid="0,1,0,1,0,1,0,1"/>  <!-- fully grass -->
   <wangtile tileid="13" wangid="0,0,0,0,0,1,0,1"/>  <!-- right edge -->
   <wangtile tileid="22" wangid="0,1,0,0,0,0,0,0"/>  <!-- BL outer corner -->
   <wangtile tileid="23" wangid="0,1,0,0,0,0,0,1"/>  <!-- bottom edge -->
   <wangtile tileid="24" wangid="0,0,0,0,0,0,0,1"/>  <!-- BR outer corner -->
   <!-- inner (concave) corners, from the block to the right in the sheet -->
   <wangtile tileid="8"  wangid="0,1,0,1,0,1,0,0"/>  <!-- inner TL -->
   <wangtile tileid="9"  wangid="0,1,0,1,0,0,0,1"/>  <!-- inner TR -->
   <wangtile tileid="19" wangid="0,1,0,0,0,1,0,1"/>  <!-- inner BL -->
   <wangtile tileid="20" wangid="0,0,0,1,0,1,0,1"/>  <!-- inner BR -->
  </wangset>
 </wangsets>
</tileset>
