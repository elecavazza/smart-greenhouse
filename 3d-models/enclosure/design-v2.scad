include <./library/YAPPgenerator_v3.scad>
// ============================================================
//  TWO BREADBOARD ENCLOSURE – YAPP v3 - VERSION 2
//  Internal size for 2× 170×60 boards, sticky-backed
// ============================================================
// ---------- PRINT ----------
printBaseShell      = true;
printLidShell       = false;
// ---------- THICKNESSES ----------
wallThickness       = 1.4;
basePlaneThickness  = 1.8;
lidPlaneThickness   = 1.8;
// ---------- INTERNAL HEIGHT (>= 40 mm REQUIRED) ----------
baseWallHeight      = 30;
lidWallHeight       = 12;
// ---------- INTERNAL FOOTPRINT ----------
pcbLength           = 170;
pcbWidth            = 120;
pcbThickness        = 0;   // irrelevant (no PCB logic used)
// ---------- PADDING ----------
paddingFront        = 1;
paddingBack         = 1;
paddingLeft         = 1;
paddingRight        = 1;
// ---------- LID OVERLAP ----------
ridgeHeight         = 5;
ridgeSlack          = 0.2;
// ---------- COSMETICS ----------
roundRadius         = 3.0;
// ---------- PRINTER ----------
printerLayerHeight  = 0.2;
// ============================================================
//  VIEW / DEBUG
// ============================================================
showSideBySide        = true;
previewQuality        = 6;
renderQuality         = 8;
onLidGap              = 4;
shiftLid              = 6;
colorLid              = "LightGray";
colorBase             = "Gainsboro";
showOrientation       = true;
showPCB               = false;
// ============================================================
//  CUTOUTS – RIGHT WALL 
//  All holes condensed on one side:
//  - 2× RJ45 keystone (14.5×16mm, elevated for clip)
//  - 4× JST 2-pin female (7.6×5.9mm, long side horizontal)
//  - 3× USB PD trigger boards (22×12mm)
// ============================================================
cutoutsRight =
[
    // === RJ45 KEYSTONES (2×) ===
    // Left RJ45 (raised for clip clearance)
    [20,                   // horizontal position
     12,                   // vertical center raised for clip
     14.5, 16,             // width × height
     0,
     yappRectangle,
     yappCenter],
    
    // Right RJ45 (raised for clip clearance)
    [40,                   // horizontal position
     12,                   // vertical center raised for clip
     14.5, 16,             // width × height
     0,
     yappRectangle,
     yappCenter],
    
    // === JST 2-PIN CONNECTORS (4×, 7.6×5.9mm, long side horizontal) ===
    [55,                   // horizontal position
     3,                    // vertical center (flush with floor)
     7.6, 5.9,             // width × height (long side = 7.6mm horizontal)
     0,
     yappRectangle,
     yappCenter],
    
    [64,                   // horizontal position
     3,                    // vertical center
     7.6, 5.9,
     0,
     yappRectangle,
     yappCenter],
    
    [73,                   // horizontal position
     3,                    // vertical center
     7.6, 5.9,
     0,
     yappRectangle,
     yappCenter],
    
    [82,                   // horizontal position
     3,                    // vertical center
     7.6, 5.9,
     0,
     yappRectangle,
     yappCenter],
    
    // === USB PD TRIGGER BOARDS (3×, 22×12mm) ===
    [100,                  // horizontal position
     6,                    // vertical center = 12/2 = 6
     22, 12,               // width × height
     0,
     yappRectangle,
     yappCenter],
    
    [125,                  // horizontal position
     6,                    // vertical center
     22, 12,
     0,
     yappRectangle,
     yappCenter],
    
    [150,                  // horizontal position
     6,                    // vertical center
     22, 12,
     0,
     yappRectangle,
     yappCenter]
];

// ---------- UNUSED FACES ----------
cutoutsBase  = [];
cutoutsLid   = [];
cutoutsFront = [];
cutoutsBack  = [];
cutoutsLeft  = [];
// ============================================================
//  SNAP JOINTS
// ============================================================
// Symmetric snaps, sized for large enclosure
snapJoins =
[
    [12, 6, yappLeft, yappRight, yappSymmetric],
    [(shellWidth/2)-4, 6, yappFront],
    [(shellWidth/2)-4, 6, yappBack]
];
// ============================================================
//  LABELS (NONE)
// ============================================================
labelsPlane = [];
// ============================================================
//  GENERATE
// ============================================================
YAPPgenerate();