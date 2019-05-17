//*****************************************************************************/
//
// Filename: GridFetchingComp.1.glsl
//
// Copyright (c) 2016 Autodesk, Inc.
// All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license 
// agreement provided at the time of installation or download, or which 
// otherwise accompanies this software in either electronic or hard copy form.
//*****************************************************************************/

#define HALF_PIXEL 0.5

uniform sampler2D adsk_texture_grid;
uniform float adsk_result_w, adsk_result_h, adsk_results_pass1_w, adsk_results_pass1_h;
uniform int       textureSelector;

  
// These 2 lines define the texture grid resolution and tile resolution 
vec2     tileSize = vec2(adsk_results_pass1_w, adsk_results_pass1_h);  
const vec2     gridSize = vec2(1500, 1500);

//------------------------------------------------------------------------------
// Function that get the position in the grid of the bottom left pixel of a tile.
//
// - gridSize : size of the grid in pixels
//
// - tileSize : size of the tiles in pixels
//
// - tileNum : index of the tile to be fetched (0 is the bottom-left)
//             example of tile index layout  : 6 - 7 - 8
//                                             3 - 4 - 5
//                                             0 - 1 - 2
//------------------------------------------------------------------------------
vec2 getTilePosition( vec2 gridSize, 
                      vec2 tileSize, 
                      int tileNum )
{
   // compute the actual number of tiles per grid row and column
   ivec2 nbTiles = ivec2(gridSize)/ivec2(tileSize);

   // compute the tile position in the grid from its index
   vec2 tile = vec2(mod(float(tileNum), float(nbTiles.x)),float(tileNum/nbTiles.x));

   return tile*tileSize;
}

//------------------------------------------------------------------------------
// Function that fetch a pixel of a tile within the grid texture 
//
// - gridSize : size of the grid in pixels
//
// - tileSize : size of the tiles in pixels
//
// - tilePosition : the position in pixel of the bottom-left corner of the tile
//                  (as returned by getTilePosition)
//
// - positionInTile : the position in pixel of the tile pixel to be fetched
//                    (0,0) is the bottom-left corner of the tile
//                    (tileSize.x,tileSize.y) is the upper-rigth corner of the tile
//
//------------------------------------------------------------------------------
vec4 fetchInTile( vec2 gridSize,
                  vec2 tileSize,
                  vec2 tilePosition, 
                  vec2 positionInTile )
{
   // add a slack of HALF_PIXEL to prevent fetching the border of the tile 
   // it avoids interpolatingon with the adjacent tile
   if ( any(greaterThan(positionInTile,tileSize-vec2(1.0+HALF_PIXEL))) ||
        any(greaterThan(vec2(HALF_PIXEL),positionInTile)) )
   {
      return vec4(0.0);
   }

   // compute the normalized coords of tile pixel to be 
   // fetched within the grid 
   vec2 positionInGrid = (tilePosition+positionInTile)/gridSize;
  
   return texture2D( adsk_texture_grid, positionInGrid );
}


//------------------------------------------------------------------------------
// MAIN
//------------------------------------------------------------------------------
void main()
{
   // fetch the transform position
   vec4 tileResult = fetchInTile(gridSize, tileSize, 
      getTilePosition(gridSize,tileSize,textureSelector), gl_FragCoord.xy);
             
   gl_FragColor = tileResult;
}
