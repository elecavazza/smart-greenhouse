include <./library/YAPPgenerator_v3.scad>
// ============================================================
//  TWO BREADBOARD ENCLOSURE – YAPP v3
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
//  CUTOUTS – RIGHT WALL (22×12 flush, RJ45 elevated for clip)
// ============================================================

cutoutsRight =
[
    // Left 22 × 12 opening (flush with floor)
    [pcbLength/2 - 24,     // horizontal left
     6,                    // vertical center = 12/2 = 6
     22, 12,               // width × height
     0,
     yappRectangle,
     yappCenter],

    // RJ45 keystone (raised for clip clearance)
    [pcbLength/2,          // horizontal center
     12,                   // vertical center raised for clip
     14.5, 16,             // width × height
     0,
     yappRectangle,
     yappCenter],

    // Right 22 × 12 opening (flush with floor)
    [pcbLength/2 + 24,     // horizontal right
     6,                    // vertical center = 12/2 = 6
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
