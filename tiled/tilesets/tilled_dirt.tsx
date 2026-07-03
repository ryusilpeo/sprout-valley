<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.10" tiledversion="1.11.0" name="tilled_dirt" tilewidth="16" tileheight="16" tilecount="77" columns="11">
 <image source="../../public/assets/world/terrain/tilled_dirt.png" width="176" height="112"/>
 <!-- Same 11x7 blob layout as grass. Used for the farm plot; Phase 4 swaps
      individual tiles to the watered variant at runtime, so no animation here.
      Tilled dirt is walkable (no collide property). -->
 <wangsets>
  <wangset name="soil" type="corner" tile="12">
   <wangcolor name="soil" color="#a9713e" tile="12" probability="1"/>
   <wangtile tileid="0"  wangid="0,0,0,1,0,0,0,0"/>
   <wangtile tileid="1"  wangid="0,0,0,1,0,1,0,0"/>
   <wangtile tileid="2"  wangid="0,0,0,0,0,1,0,0"/>
   <wangtile tileid="11" wangid="0,1,0,1,0,0,0,0"/>
   <wangtile tileid="12" wangid="0,1,0,1,0,1,0,1"/>
   <wangtile tileid="13" wangid="0,0,0,0,0,1,0,1"/>
   <wangtile tileid="22" wangid="0,1,0,0,0,0,0,0"/>
   <wangtile tileid="23" wangid="0,1,0,0,0,0,0,1"/>
   <wangtile tileid="24" wangid="0,0,0,0,0,0,0,1"/>
   <wangtile tileid="8"  wangid="0,1,0,1,0,1,0,0"/>
   <wangtile tileid="9"  wangid="0,1,0,1,0,0,0,1"/>
   <wangtile tileid="19" wangid="0,1,0,0,0,1,0,1"/>
   <wangtile tileid="20" wangid="0,0,0,1,0,1,0,1"/>
  </wangset>
 </wangsets>
</tileset>
