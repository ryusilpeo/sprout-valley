<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.10" tiledversion="1.11.0" name="water" tilewidth="16" tileheight="16" tilecount="4" columns="4">
 <image source="../../public/assets/world/terrain/water.png" width="64" height="16"/>
 <!--
   Water is 4 horizontal frames of the same animated tile. Paint tile 0 on a
   "water" layer; the animation below cycles all four so it shimmers in-engine.
   Water is impassable — the collide property is read by the Phaser loader.
 -->
 <tile id="0">
  <properties>
   <property name="collide" type="bool" value="true"/>
  </properties>
  <animation>
   <frame tileid="0" duration="350"/>
   <frame tileid="1" duration="350"/>
   <frame tileid="2" duration="350"/>
   <frame tileid="3" duration="350"/>
  </animation>
 </tile>
</tileset>
