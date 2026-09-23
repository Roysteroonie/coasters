# RLO Player Coaster Generator

Windows desktop generator for the locked **V4** player coaster design.

## Locked production design

- 100 × 100 mm rounded-square coaster
- 4 mm total thickness
- 1 mm artwork depth
- White body + black artwork
- Face-down production orientation is handled automatically
- High football-shirt name arch
- Reduced, centralised number size approved on the **JAMES 7** calibration model
- Black fill / white separation / black outer keyline treatment
- Multipart 3MF output plus STL backups and a PNG preview

## Build the Windows app with GitHub Actions

You do **not** need Python or Blender on your own PC.

1. Put all repository files on the `main` branch.
2. Open **Actions** in GitHub.
3. Select **Build Windows Coaster Generator**.
4. Choose **Run workflow**.
5. Wait for the build to finish.
6. Open the completed workflow run and download the artifact named:
   `RLO-Player-Coaster-Generator-Windows`
7. Unzip it anywhere on Windows.
8. Double-click `RLO_Player_Coaster_Generator.exe`.

The GitHub build bundles its own OpenSCAD runtime, so the finished portable package does not require a separate OpenSCAD installation.

## Use the app

### One player

Enter a player name and number, choose an output folder, then click **Generate Player**.

Example:

- Name: `JAMES`
- Number: `7`

Creates files including:

- `JAMES_7_FACE_DOWN.3mf`
- `JAMES_7_WHITE_BODY.stl`
- `JAMES_7_BLACK_ART.stl`
- `JAMES_7_finished_preview.png`

### Entire squad from Excel

Choose an `.xlsx` workbook whose first sheet contains:

| Name | Position | Number |
|---|---|---|
| James | Defender | 7 |
| Aaronson | Midfielder | 11 |
| Farke | Manager | BOSS |

Then click **Generate XLSX**.

The app recognises the header names and creates one V4 coaster for every valid row.

## Creality Print

The production 3MF is deliberately generated **face-down**. The text therefore looks mirrored when viewed from above the build plate. Once the coaster is printed and turned over, the visible face reads correctly.

Assign the two model parts as:

- `WHITE_BODY` → white filament
- `BLACK_ART` → black filament

## Important

`coaster_core.py` contains the locked V4 dimensions. Do not alter the geometry constants unless intentionally creating a new design revision.
