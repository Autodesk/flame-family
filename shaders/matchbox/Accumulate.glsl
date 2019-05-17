//*****************************************************************************/
// 
// Filename: Accumulate.glsl
//
// Copyright (c) 2016 Autodesk, Inc.
// All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license 
// agreement provided at the time of installation or download, or which 
// otherwise accompanies this software in either electronic or hard copy form. 
//*****************************************************************************/

uniform sampler2D input1, matte, adsk_accum_texture;
uniform float adsk_result_w, adsk_result_h;
uniform bool adsk_accum_no_prev_frame;
uniform float weight;
void main()
{
   vec2 coords = gl_FragCoord.xy / vec2( adsk_result_w, adsk_result_h );
   vec4 sourceColor1 = texture2D(input1, coords);
   sourceColor1.a = texture2D(matte, coords).r;

   vec4 sourceColor2 = adsk_accum_no_prev_frame ? sourceColor1 :
                       texture2D(adsk_accum_texture, coords);
   gl_FragColor = mix( sourceColor2, sourceColor1, weight);
}
