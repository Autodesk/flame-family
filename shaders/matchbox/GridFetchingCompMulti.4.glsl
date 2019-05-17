//*****************************************************************************/
//
// Filename: GridFetchingCompMulti.4.glsl
//
// Copyright (c) 2016 Autodesk, Inc.
// All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license 
// agreement provided at the time of installation or download, or which 
// otherwise accompanies this software in either electronic or hard copy form.
//*****************************************************************************/

uniform sampler2D front, adsk_results_pass3;

uniform float     adsk_result_w, adsk_result_h;
uniform float     adsk_results_pass3_w, adsk_results_pass3_h;

uniform vec2     tilePositionA, tilePositionB, tilePositionC, tilePositionD;
uniform float    tileRotationA, tileRotationB, tileRotationC, tileRotationD;
uniform float    tileScaleA, tileScaleB, tileScaleC, tileScaleD;

#define HALF_PIXEL 0.5

// These 2 lines define the texture grid resolution and tile resolution 
const vec2     tileSize = vec2(500, 500);  
const vec2     gridSize = vec2(1000, 1000);

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
   // it avoids interpolating on with the adjacent tile
   if ( any(greaterThan(positionInTile,tileSize-vec2(1.0+HALF_PIXEL))) ||
        any(greaterThan(vec2(HALF_PIXEL),positionInTile)) )
   {
      return vec4(0.0);
   }

   // compute the normalized coords of tile pixel to be 
   // fetched within the grid 
   vec2 positionInGrid = (tilePosition+positionInTile)/gridSize;
  
   return texture2D( adsk_results_pass3, positionInGrid );
}

//------------------------------------------------------------------------------
// Function that apply a scale and a rotation to a position within a tile
//
// - tileSize : size of the tiles in pixels
//
// - positionInTile : the position in pixel of the tile pixel to be transformed
//                    (0,0) is the bottom-left corner of the tile
//                    (tileSize.x,tileSize.y) is the upper-rigth corner of the tile
//
// - scale / angle : transform
//------------------------------------------------------------------------------
vec2 scaleRotPositionInTile( vec2 tileSize,
                             vec2 positionInTile,
                             float scale,
                             float angle )
{
   // compute the rotation matrix
   vec2 a_cossin = vec2(cos(-angle),sin(-angle));
   mat2 rotMat = mat2( a_cossin.x, -a_cossin.y, a_cossin.y, a_cossin.x);

   // apply the transform to the position 
   vec2 position = positionInTile - tileSize*vec2(0.5);
   position *= rotMat;
   position *= vec2(1.0/scale);
   position += tileSize*0.5;

   return position;
}

void main()
{
   vec2 outputCoords = vec2(gl_FragCoord.xy / vec2(adsk_result_w, adsk_result_h));
   vec3 inputResult = texture2D (front, outputCoords).rgb;
   
   vec2 tileOffset = vec2(0.5*(adsk_result_w - tileSize.x), 0.5*(adsk_result_h - tileSize.y)); 
   
   vec2 tileCoordsA = scaleRotPositionInTile( tileSize,(gl_FragCoord.xy-tileOffset-tilePositionA),tileScaleA*0.01,tileRotationA);
   vec2 tileCoordsB = scaleRotPositionInTile( tileSize,(gl_FragCoord.xy-tileOffset-tilePositionB),tileScaleB*0.01,tileRotationB);
   vec2 tileCoordsC = scaleRotPositionInTile( tileSize,(gl_FragCoord.xy-tileOffset-tilePositionC),tileScaleC*0.01,tileRotationC);
   vec2 tileCoordsD = scaleRotPositionInTile( tileSize,(gl_FragCoord.xy-tileOffset-tilePositionD),tileScaleD*0.01,tileRotationD);
   
   vec4 tileResultA = fetchInTile(gridSize, tileSize, getTilePosition(gridSize,tileSize,0), tileCoordsA);
   vec4 tileResultB = fetchInTile(gridSize, tileSize, getTilePosition(gridSize,tileSize,1), tileCoordsB);
   vec4 tileResultC = fetchInTile(gridSize, tileSize, getTilePosition(gridSize,tileSize,2), tileCoordsC);
   vec4 tileResultD = fetchInTile(gridSize, tileSize, getTilePosition(gridSize,tileSize,3), tileCoordsD);

		    
   vec3 result=mix(inputResult, tileResultA.rgb/vec3(clamp(tileResultA.a, 0.00001, 1.0)), tileResultA.a);
   result=mix(result, tileResultB.rgb/vec3(clamp(tileResultB.a, 0.00001, 1.0)), tileResultB.a);
   result=mix(result, tileResultC.rgb/vec3(clamp(tileResultC.a, 0.00001, 1.0)), tileResultC.a);
   result=mix(result, tileResultD.rgb/vec3(clamp(tileResultD.a, 0.00001, 1.0)), tileResultD.a);
             
   gl_FragColor = vec4(result, 1.0);
}
