//*****************************************************************************/
//
// Filename: BleachBypass.glsl
//
// Copyright (c) 2014 Autodesk, Inc.
// All rights reserved.
//
// This computer source code and related instructions and comments are the
// unpublished confidential and proprietary information of Autodesk, Inc.
// and are protected under applicable copyright and trade secret law.
// They may not be disclosed to, copied or used by any third party without
// the prior written consent of Autodesk, Inc.
//*****************************************************************************/

//Forward Declaration
float adsk_getLuminance( in vec3 color );
vec3 adsk_log2scene( in vec3 src );
vec3 adsk_scene2log( in vec3 src );
bool adsk_isSceneLinear();
vec4 adsk_getBlendedValue( int blendType, vec4 srcColor, vec4 dstColor );

uniform float adskUID_effect;
uniform float adskUID_exposure;
uniform bool adskUID_clampNegative;

uniform int adskUID_blendModes;

vec4 adskUID_lightbox( vec4 source )
{
   // we need to perform the conversion conditionally
   vec3 logSrc = adsk_isSceneLinear()?adsk_scene2log( source.rgb ):source.rgb;
   
   // rec 709 luma weights
   float lum = clamp( adsk_getLuminance( logSrc ), 0.0, 1.0 );
   float L = clamp(min(1.0, max(0.0,10.0*(lum - 0.45))), 0.0, 1.0 );
   vec3 blend = vec3(lum, lum, lum) ;
   vec3 result1 = 2.0 * logSrc * blend ;
   vec4 greyscale = vec4(result1, L);

   vec3 result2 = vec3(1.0) - (2.0*(vec3(1.0)-blend)*(vec3(1.0)-logSrc));
   vec3 newColor = mix(greyscale.rgb,result2,greyscale.a);

   vec3 mixRGB = adskUID_effect * newColor;
   mixRGB += (vec3(1.0 - adskUID_effect) * logSrc );
   
   const float filmGamma = 0.6;
   float expos_scale = filmGamma * log( 2.0 ) / ( log( 10.0 ) * 0.002 * 1023.0 );
   vec3 exposure = ( vec3(adskUID_exposure) * expos_scale - vec3(0.18) + mixRGB ) + vec3(0.18);

   // we need to perform the conversion conditionally
   vec3 result = adsk_isSceneLinear()?adsk_log2scene( exposure ):exposure;
   
   // Blending Modes
   result = adsk_getBlendedValue( adskUID_blendModes, vec4(source.rgb, 1.0), vec4(result, 1.0)).rgb;

   return vec4( adskUID_clampNegative ? max( result, vec3( 0.0 ) ) : result, source.a );
}
