---
name: canvas
description: Open the visual canvas
---

# /canvas Command

Opens the infinite canvas for visual workflow design.

## Usage

```
/canvas [action]
```

### Actions

- `/canvas` or `/canvas open` - Start the canvas server
- `/canvas stop` - Stop the canvas server

## Starting the Canvas

```bash
cd tldraw-canvas && npm install && npm run dev
```

Then open: **http://localhost:3000/**

## What You Can Do

1. **Draw & Write** - Pen, highlighter, eraser, text
2. **Add Shapes** - Rectangle, ellipse, arrow, line, and more
3. **Add Media** - Drag and drop images or videos onto canvas
4. **Pan & Zoom** - Mouse drag to pan, scroll wheel to zoom
5. **Select & Transform** - Click to select, drag handles to resize
6. **Export** - Menu > Export as PNG, SVG, or JSON
7. **Auto-Save** - Automatic persistence to localStorage

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Delete | Remove selected |
| Ctrl+A | Select all |
| Ctrl+Z | Undo |
| Ctrl+Shift+Z | Redo |
| Ctrl+C / Ctrl+V | Copy / Paste |
| Scroll | Zoom in/out |

## Canvas Resources

- Documentation: See tldraw-canvas/README.md
- Canvas directory: tldraw-canvas/
