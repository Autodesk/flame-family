//*****************************************************************************/
//
// Filename: GridFetchingComp.4.glsl
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
uniform float     adsk_results_pass1_w, adsk_results_pass1_h;

uniform vec2     tilePosition;
uniform float    tileRotation, tileScale;


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
   
   vec2 tileOffset = vec2(0.5*(adsk_result_w - adsk_results_pass1_w), 0.5*(adsk_result_h - adsk_results_pass1_h));
   vec2 tileSize = vec2(adsk_results_pass1_w, adsk_results_pass1_h); 
   
   vec2 tileCoords = scaleRotPositionInTile( tileSize,(gl_FragCoord.xy-tileOffset-tilePosition),tileScale*0.01,tileRotation)/tileSize;
   
   vec3 inputResult = texture2D (front, outputCoords).rgb;
   vec4 textureGridResult = texture2D (adsk_results_pass3, tileCoords); 
		    
   vec3 result=mix(inputResult, textureGridResult.rgb/vec3(clamp(textureGridResult.a, 0.00001, 1.0)), textureGridResult.a);
             
   gl_FragColor = vec4(result, textureGridResult.a);
}
