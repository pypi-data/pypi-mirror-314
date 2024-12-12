"""
Above Python3.9, the labelImg will collapse
"""

import site
from pathlib import Path

for path in site.getsitepackages():
    canvas_path = Path(path) / 'libs/canvas.py'
    print(canvas_path)
    if canvas_path.exists():
        content = canvas_path.read_text(encoding='utf-8')
        content = content.replace('p.drawRect(left_top.x(), left_top.y(), rect_width, rect_height)',
                                  'p.drawRect(int(left_top.x()), int(left_top.y()), int(rect_width), int(rect_height))')
        content = content.replace('p.drawLine(self.prev_point.x(), 0, self.prev_point.x(), self.pixmap.height())',
                                  'p.drawLine(int(self.prev_point.x()), 0, int(self.prev_point.x()), int(self.pixmap.height()))')
        content = content.replace('p.drawLine(0, self.prev_point.y(), self.pixmap.width(), self.prev_point.y())',
                                  'p.drawLine(0, int(self.prev_point.y()), int(self.pixmap.width()), int(self.prev_point.y()))')
        canvas_path.write_text(content, encoding='utf-8')
        print(f'Fix over')
        break
else:
    raise FileNotFoundError(f"Canvas file not found in site-packages")
