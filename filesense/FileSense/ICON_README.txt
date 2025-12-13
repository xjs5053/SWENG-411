# Icon File Placeholder

The build scripts reference `icon.ico` for the application icon.

## Options:

### Option 1: Use Default Icon
If icon.ico is not present, PyInstaller will use the default Python icon.

### Option 2: Create Your Own Icon

1. Create or download a 256x256 PNG image
2. Convert to .ico format using:
   - Online: https://convertico.com/
   - Desktop: GIMP, Photoshop
   - Command line: ImageMagick

3. Save as `icon.ico` in the FileSense folder

4. Rebuild with BUILD_ALL.bat

### Option 3: Download Free Icons

**Recommended sources:**
- https://icon-icons.com/ (search "folder" or "search")
- https://icons8.com/icons/set/file-search
- https://www.flaticon.com/search?word=file%20manager

**Suggested keywords:**
- "file search"
- "folder magnifying glass"
- "document search"
- "file manager"

### Icon Specifications

For best results:
- Format: .ico
- Size: 256x256 pixels (supports multiple sizes)
- Color depth: 32-bit (with transparency)
- Included sizes: 16x16, 32x32, 48x48, 256x256

### Quick Icon Creation

**Using GIMP (Free)**:
1. Create 256x256 image
2. Design your icon
3. File → Export As → filename.ico
4. Check "Compressed (PNG)" option
5. Save with multiple sizes

**Using Online Tool**:
1. Visit https://convertico.com/
2. Upload your PNG/JPG
3. Select "256x256" size
4. Download .ico file
5. Rename to icon.ico

## Current Status

The FileSense folder does not include icon.ico by default.

**To add icon before building:**
1. Create or download icon.ico
2. Place in FileSense folder (same directory as app.py)
3. Run BUILD_ALL.bat

**If you build without icon:**
- EXE will use default Python icon
- Everything will still work normally
- You can rebuild later with custom icon
