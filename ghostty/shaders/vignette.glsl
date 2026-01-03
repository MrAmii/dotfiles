// Simple vignette shader
// Darkens corners based on distance from center

// ============================================
// VIGNETTE STRENGTH ADJUSTMENT
// ============================================
// Controls how dark the corners/edges become
// 
// LOWER values = STRONGER vignette (darker edges)
// HIGHER values = WEAKER vignette (lighter edges)
//
// Recommended values:
//   0.95 = Very subtle vignette
//   0.85 = Moderate vignette (default)
//   0.75 = Strong vignette
//   0.60 = Very strong vignette
//   0.50 = Extreme vignette (very dark corners)
//
// Valid range: 0.0 to 1.0
//   0.0 = completely black corners
//   1.0 = no vignette at all
// ============================================

#define VIGNETTE_STRENGTH 0.75

void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    // Get texture color
    vec2 uv = fragCoord / iResolution.xy;
    vec4 color = texture(iChannel0, uv);
    
    // Calculate distance from center (normalized to -1 to 1)
    vec2 pos = (fragCoord / iResolution.xy) * 2.0 - 1.0;
    
    // Calculate vignette factor
    float vig = 1.0 - ((1.0 - clamp(pos.x * pos.x, 0.0, 1.0)) * 
                       (1.0 - clamp(pos.y * pos.y, 0.0, 1.0)));
    vig = clamp((-vig) + 1.0, VIGNETTE_STRENGTH, 1.0);
    
    // Apply vignette
    fragColor = vec4(color.rgb * vig, color.a);
}
