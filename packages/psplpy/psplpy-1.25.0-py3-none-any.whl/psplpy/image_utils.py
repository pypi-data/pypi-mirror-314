import io
from pathlib import Path
from typing import Any, Union
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageOps, ImageFont, ImageChops
from psplpy.other_utils import recursive_convert, is_sys


class Rect:
    RECT = 'rect'                   # the Rect object
    LTWH = 'ltwh'                   # (left, top, width, height)
    LT_RB = 'lt_rb'                 # ((left, top), (right, bottom))
    LTRB = 'ltrb'                   # (left, top, right, bottom)
    LT_RT_RB_LB = 'lt_rt_rb_lb'     # ((left, top), (right, top), (right, bottom), (left, bottom))
    CENTER = 'center'               # (x, y)
    CENTER_RECT = 'center_rect'     # (center_x, center_y, half_width, half_height)
    _LEFT_X, _RIGHT_X, _TOP_Y, _BOTTOM_Y = 'left_x', 'right_x', 'top_y', 'bottom_y'

    def __init__(self, rect: Union['Rect', tuple, list], rect_format: str = None):
        rect_format = rect_format or self._det_rect_format(rect)
        self.rect = self._to_lt_rb(rect, rect_format)

    @staticmethod
    def _det_rect_format(rect: Any) -> str:
        if isinstance(rect, Rect):
            return Rect.RECT
        else:
            if len(rect) == 4:
                if isinstance(rect[0], (int, float)):
                    return Rect.LTWH
                elif len(rect[0]) == 2:
                    return Rect.LT_RT_RB_LB
            elif len(rect) == 2:
                return Rect.LT_RB
            raise ValueError(f'Unknown rectangle type for {rect}.')

    def _to_lt_rb(self, rect: Any, rect_format: str) -> list[list[float]]:
        if rect_format == Rect.RECT:
            result = rect.to_lt_rb()
        elif rect_format == Rect.LT_RB:
            self.rect = rect
            result = self.to_lt_rb()
        elif rect_format == Rect.LTWH:
            left, top, width, height = rect
            result = [[left, top], [left + width, top + height]]
        elif rect_format == Rect.LTRB:
            left, top, right, bottom = rect
            result = [[left, top], [right, bottom]]
        elif rect_format == Rect.LT_RT_RB_LB:
            left, top, right, bottom = rect[0][0], rect[0][1], rect[2][0], rect[2][1]
            result = [[left, top], [right, bottom]]
        elif rect_format == Rect.CENTER_RECT:
            center_x, center_y, half_width, half_height = rect
            left = center_x - half_width
            top = center_y - half_height
            right = center_x + half_width
            bottom = center_y + half_height
            result = [[left, top], [right, bottom]]
        else:
            raise ValueError(f"Unsupported rectangle format {rect_format}")
        return result

    def __iter__(self):
        for item in self.rect:
            yield item

    def __getitem__(self, index) -> list[float]:
        return self.rect[index]

    def __setitem__(self, index, value: list[float] | tuple[float, float]) -> 'Rect':
        self.rect[index] = list(value)
        return self

    def __str__(self):
        return str(f'Rect({self.to_lt_rb()})')

    __repr__ = __str__

    def __eq__(self, other: 'Rect'):
        if isinstance(other, Rect):
            return self.rect == other.rect
        return False

    def _to_other(self, rect_format: str) -> list | float:
        (left, top), (right, bottom) = self.rect
        if rect_format == Rect.LTWH:
            width = right - left
            height = bottom - top
            return [left, top, width, height]
        elif rect_format == Rect.LTRB:
            return [left, top, right, bottom]
        elif rect_format == Rect.LT_RT_RB_LB:
            return [[left, top], [right, top], [right, bottom], [left, bottom]]
        elif rect_format == Rect.CENTER:
            center_x = (left + right) / 2
            center_y = (top + bottom) / 2
            return [center_x, center_y]
        elif rect_format == Rect.CENTER_RECT:
            center_x = (left + right) / 2
            center_y = (top + bottom) / 2
            half_width = (right - left) / 2
            half_height = (bottom - top) / 2
            return [center_x, center_y, half_width, half_height]
        elif rect_format in (Rect._LEFT_X, Rect._RIGHT_X, Rect._TOP_Y, Rect._BOTTOM_Y):
            return locals()[rect_format[:-2]]
        else:
            raise ValueError(f"Unsupported rectangle format {rect_format}")

    def to_lt_rb(self) -> list[list[float]]:
        return [[self.rect[0][0], self.rect[0][1]], [self.rect[1][0], self.rect[1][1]]]

    def to_ltwh(self) -> list[float]:
        return self._to_other(Rect.LTWH)

    def to_ltrb(self) -> list[float]:
        return self._to_other(Rect.LTRB)

    def to_lt_rt_rb_lt(self) -> list[list[float]]:
        return self._to_other(Rect.LT_RT_RB_LB)

    def to_center_rect(self) -> list[float]:
        return self._to_other(Rect.CENTER_RECT)

    @property
    def center(self) -> list[float]:
        return self._to_other(Rect.CENTER)

    @property
    def left_x(self) -> float:
        return self._to_other(Rect._LEFT_X)

    @property
    def right_x(self) -> float:
        return self._to_other(Rect._RIGHT_X)

    @property
    def top_y(self) -> float:
        return self._to_other(Rect._TOP_Y)

    @property
    def bottom_y(self) -> float:
        return self._to_other(Rect._BOTTOM_Y)

    def resize(self, scale: float) -> 'Rect':
        (left, top), (right, bottom) = self.rect

        width = right - left
        height = bottom - top

        new_width = width * scale
        new_height = height * scale

        new_left = left + (width - new_width) / 2
        new_top = top + (height - new_height) / 2
        new_right = new_left + new_width
        new_bottom = new_top + new_height

        self.rect = [[new_left, new_top], [new_right, new_bottom]]
        return self

    def area(self) -> float:
        (left, top), (right, bottom) = self.rect
        width = right - left
        height = bottom - top
        area = width * height
        return area

    def is_inside(self, internal_rect: 'Rect') -> bool:
        """whether a rect is inside the self_rect"""
        self_rect, other_rect = self.to_lt_rb(), internal_rect.to_lt_rb()
        (ax1, ay1), (ax2, ay2) = self_rect
        (bx1, by1), (bx2, by2) = other_rect
        return bx1 >= ax1 and bx2 <= ax2 and by1 >= ay1 and by2 <= ay2

    def overlap_pct(self, rect: 'Rect') -> tuple[float, float]:
        """calculate the ratio of the overlapping of two rectangles to the area of each rectangle"""
        self_rect, other_rect = self.to_lt_rb(), rect.to_lt_rb()

        (x1, y1), (r1, b1) = self_rect
        (x2, y2), (r2, b2) = other_rect
        x_overlap = max(0, min(r1, r2) - max(x1, x2))
        y_overlap = max(0, min(b1, b2) - max(y1, y2))

        area_overlap = x_overlap * y_overlap
        percent1 = area_overlap / self.area()
        percent2 = area_overlap / rect.area()
        return percent1, percent2


class ImgConv:
    def __init__(self, image: Union['ImgConv', Image.Image, np.ndarray, bytes, str, Path, io.BytesIO],
                 from_opencv: bool = False):
        if isinstance(image, ImgConv):
            self.image = image.image
        else:
            self.image = image
        if from_opencv:
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

    def __str__(self):
        return f'{self.__class__.__name__}({self.image})'

    __repr__ = __str__

    def _raise_error(self):
        raise ValueError(f"Unsupported input data type {type(self.image)}")

    def to_numpy(self) -> np.ndarray:
        if isinstance(self.image, Image.Image):
            return np.array(self.image)
        elif isinstance(self.image, np.ndarray):
            return self.image
        elif isinstance(self.image, (str, Path, io.BytesIO)):
            return np.array(self.to_pil())
        elif isinstance(self.image, (bytes, bytearray)):
            return ImgConv(self.to_bytesio()).to_numpy()
        else:
            self._raise_error()

    def to_pil(self) -> Image.Image:
        if isinstance(self.image, Image.Image):
            return self.image
        elif isinstance(self.image, np.ndarray):
            return Image.fromarray(self.image)
        elif isinstance(self.image, (str, Path, io.BytesIO)):
            return Image.open(self.image)
        elif isinstance(self.image, (bytes, bytearray)):
            return ImgConv(self.to_bytesio()).to_pil()
        else:
            self._raise_error()

    def to_opencv(self) -> np.ndarray:
        if isinstance(self.image, Image.Image):
            return cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2BGR)
        elif isinstance(self.image, np.ndarray):
            return cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR)
        elif isinstance(self.image, (str, Path)):
            return cv2.imread(str(self.image))
        elif isinstance(self.image, io.BytesIO):
            return cv2.cvtColor(self.to_numpy(), cv2.COLOR_RGB2BGR)
        elif isinstance(self.image, (bytes, bytearray)):
            return ImgConv(self.to_bytesio()).to_opencv()
        else:
            self._raise_error()

    @staticmethod
    def _get_save_params(**kwargs) -> dict:
        return kwargs

    def to_path(self, path: str | Path = None) -> Path:
        if isinstance(self.image, Image.Image):
            self.image.save(**self._get_save_params(fp=path))
            return Path(path)
        elif isinstance(self.image, np.ndarray):
            Image.fromarray(self.image).save(**self._get_save_params(fp=path))
            return Path(path)
        elif isinstance(self.image, (str, Path)):
            if not path:
                return Path(self.image)
            return ImgConv(self.to_pil()).to_path(path)
        elif isinstance(self.image, io.BytesIO):
            Image.open(self.image).save(**self._get_save_params(fp=path))
            return Path(path)
        elif isinstance(self.image, (bytes, bytearray)):
            return ImgConv(self.to_bytesio()).to_path(path)
        else:
            self._raise_error()

    def to_bytesio(self) -> io.BytesIO:
        if isinstance(self.image, Image.Image):
            bytes_io = io.BytesIO()
            self.image.save(bytes_io, **self._get_save_params(format='PNG'))
            return bytes_io
        elif isinstance(self.image, np.ndarray):
            bytes_io = io.BytesIO()
            Image.fromarray(self.image).save(bytes_io, **self._get_save_params(format='PNG'))
            return bytes_io
        elif isinstance(self.image, (str, Path)):
            bytes_io = io.BytesIO()
            Image.open(self.image).save(bytes_io, **self._get_save_params(format='PNG'))
            return bytes_io
        elif isinstance(self.image, io.BytesIO):
            return self.image
        elif isinstance(self.image, (bytes, bytearray)):
            return io.BytesIO(self.image)
        else:
            self._raise_error()

    def to_bytes(self) -> bytes:
        return self.to_bytesio().getvalue()

    def to_bytearray(self) -> bytearray:
        return bytearray(self.to_bytes())


class Img(ImgConv):
    def __init__(self, image: Union['ImgConv', Image.Image, np.ndarray, bytes, str, Path, io.BytesIO],
                 from_opencv: bool = False):
        super().__init__(image, from_opencv)
        if isinstance(image, (str, Path)):
            self._fp = image
        self.image = self.to_pil()

    def copy(self) -> 'Img':
        return Img(self.image.copy())

    def is_equal(self, other: Union['ImgConv', Image.Image, np.ndarray, bytes, str, Path, io.BytesIO]) -> bool:
        if isinstance(other, (ImgConv, np.ndarray, bytes, str, Path, io.BytesIO)):
            other = ImgConv(other).to_pil()
        if isinstance(other, Image.Image):
            diff = ImageChops.difference(self.image, other)
            return not diff.getbbox()
        return False

    def resize(self, ratio: float = None, x: float = None, y: float = None) -> 'Img':
        if ratio:
            w_h = (int(self.image.width * ratio), int(self.image.height * ratio))
            self.image = self.image.resize(w_h, Image.BICUBIC)
        elif x and y:
            self.image = self.image.resize((int(x), int(y)), Image.BICUBIC)
        return self

    def _enhance(self, enhance_type, *args) -> 'Img':
        enhancer = getattr(ImageEnhance, enhance_type)(self.image)
        self.image = enhancer.enhance(*args)
        return self

    def contrast(self, contrast: float) -> 'Img':
        return self._enhance("Contrast", contrast)

    def brightness(self, brightness: float) -> 'Img':
        return self._enhance("Brightness", brightness)

    def sharpness(self, sharpness: float) -> 'Img':
        return self._enhance("Sharpness", sharpness)

    def grayscale(self) -> 'Img':
        self.image = self.image.convert('L')
        # self.image = ImageOps.grayscale(self.image)   # backup
        return self

    def _is_grayscale(self) -> bool:
        if len(self.image.getbands()) == 1:
            return True

    def binaryzation(self, threshold: int = 255 - 20) -> 'Img':
        """The grayscale greater than the threshold will be set to 255, otherwise set to 0"""
        if not self._is_grayscale():
            self.grayscale()
        self.image = self.image.point(lambda p: p > threshold and 255)
        return self

    def invert(self) -> 'Img':
        self.image = ImageOps.invert(self.image)
        return self

    def rotate(self, angle: float, expand: bool = True) -> 'Img':
        self.image = self.image.rotate(angle, expand=expand)
        return self

    def crop(self, rect: Rect) -> 'Img':
        self.image = self.image.crop(rect.to_ltrb())
        return self

    def dpi(self, dpi: int) -> 'Img':
        self.image.info["dpi"] = (dpi, dpi)
        return self

    def _get_save_params(self, **kwargs) -> dict:
        params = super()._get_save_params(**kwargs)
        if (not params.get('fp')) and hasattr(self, '_fp'):
            params['fp'] = self._fp
        if dpi := self.image.info.get('dpi'):
            params['dpi'] = dpi
        return params


class ImgDraw(Img):
    @staticmethod
    def _get_font_path() -> Path:
        has_font = True
        if is_sys(is_sys.LINUX):
            path = Path('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc')
        elif is_sys(is_sys.WINDOWS):
            path = Path(r'C:\Windows\Fonts\msyh.ttc')
        else:
            has_font = False
        if not has_font or not path.exists():
            mes = ('Font file not found, please use the class attribute "FONT_PATH" to designate another font path, '
                   'or try to use "sudo apt install -y ttf-wqy-zenhei" to install it on Linux.')
            raise FileNotFoundError(mes)
        return path
    FONT_PATH = _get_font_path()

    def __init__(self, image: Union['ImgConv', Image.Image, np.ndarray, bytes, str, Path, io.BytesIO],
                 from_opencv: bool = False):
        super().__init__(image, from_opencv)
        self.draw = ImageDraw.Draw(self.image)

    @staticmethod
    def rgb_to_l(rgb_color: tuple[int, int, int] | list[int]) -> int:
        red, green, blue = rgb_color
        grayscale = 0.2989 * red + 0.5870 * green + 0.1140 * blue
        return round(grayscale)

    @staticmethod
    def bounding_rect(polygon: list | tuple | Rect) -> Rect:
        """find the smallest rectangle that can cover a polygon"""
        if isinstance(polygon, Rect):
            return polygon
        x_min = min(x for x, y in polygon)
        y_min = min(y for x, y in polygon)
        x_max = max(x for x, y in polygon)
        y_max = max(y for x, y in polygon)
        return Rect((x_min, y_min, x_max, y_max), rect_format=Rect.LTRB)

    def _get_color(self, outline: Any, box: tuple[int, int, int, int] | list[int]) -> Any:
        if not outline:
            region = self.image.crop(box)
            colors = region.getdata()
            avg_red = sum([color[0] for color in colors]) // len(colors)
            avg_green = sum([color[1] for color in colors]) // len(colors)
            avg_blue = sum([color[2] for color in colors]) // len(colors)

            grayscale = self.rgb_to_l((avg_red, avg_green, avg_blue))
            if grayscale < 128:
                return 'white'
            return 'black'
        return outline

    def rectangles(self, rects: list[Rect], outline: Any = None, width: float = 1) -> 'ImgDraw':
        for rect in rects:
            got_outline = self._get_color(outline, rect.to_ltrb())
            self.draw.rectangle(rect.to_ltrb(), outline=got_outline, width=width)
        return self

    def polygons(self, polygons: list, outline: Any = None, width: float = 1) -> 'ImgDraw':
        for polygon in polygons:
            got_outline = self._get_color(outline, self.bounding_rect(polygon).to_ltrb())
            self.draw.polygon(recursive_convert(polygon, to=tuple), outline=got_outline, width=width)
        return self

    def text(self, text: str, left_top_point: tuple[float, float], font_size: int = 10, fill: Any = None) -> 'ImgDraw':
        font = ImageFont.truetype(str(self.FONT_PATH), font_size)
        got_fill = self._get_color(fill, self.draw.textbbox(left_top_point, text, font=font))
        self.draw.text(left_top_point, text, font=font, fill=got_fill)
        return self

    def text_in_rect(self, text: str, rect: Rect, fill: Any = None) -> 'ImgDraw':
        def _get_font() -> ImageFont.FreeTypeFont:
            height, width = bottom - top, right - left
            font = ImageFont.truetype(str(self.FONT_PATH), size=int(height))
            while True:
                bbox = self.draw.textbbox(left_top_point, text, font=font)
                bbox_left, bbox_top, bbox_right, bbox_bottom = bbox
                if bbox_right > right or bbox_bottom > bottom:
                    height -= 1
                    font = ImageFont.truetype(str(self.FONT_PATH), size=int(height))
                else:
                    return font

        left, top, right, bottom = rect.to_ltrb()
        left_top_point = (left, top)
        text_font = _get_font()
        got_fill = self._get_color(fill, self.draw.textbbox(left_top_point, text, font=text_font))
        self.draw.text(left_top_point, text, font=text_font, fill=got_fill)
        return self
