//*****************************************************************************/
// 
// Filename: GridFetchingComp.3.glsl
//
// Copyright (c) 2016 Autodesk, Inc.
// All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license 
// agreement provided at the time of installation or download, or which 
// otherwise accompanies this software in either electronic or hard copy form.
//*****************************************************************************/

uniform sampler2D adsk_results_pass2;
uniform float adsk_result_w, adsk_result_h;
uniform float softness;

void main(void)
{
   vec2 coords = gl_FragCoord.xy / vec2( adsk_result_w, adsk_result_h );
   
   float sig = softness;
   vec4 blurry = vec4(0,0,0,0);
   vec4 finalColor = vec4(0.0);
   float sw = 0.0;
 
   float rad = 2.0*clamp(3.0 * sig + 1.0, 1.0, adsk_result_w/2.0);
   const vec2 dir = vec2(0, 1);

   for ( float x = -rad/2.0; x<=rad/2.0; ++x )
        {
           vec2 coords = (gl_FragCoord.xy + x * dir ) / vec2( adsk_result_w, adsk_result_h );
           if ( coords.x < 0.0 || coords.x>adsk_result_w )
              continue;

           float tmpx = x/sig;

           float w = exp( -0.5 * (tmpx* tmpx ));
           sw += w;
        blurry += w*texture2D( adsk_results_pass2, coords );

        }
     
   blurry /= sw;

   finalColor = blurry ;
   
   gl_FragColor = finalColor ;
}
