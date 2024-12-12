import math
from pathlib import Path
from typing import Any
from PIL import Image
from psplpy.image_utils import ImgConv, ImgDraw, Rect
from psplpy import MpKw, MpHttpServer, MpHttpClient


class OcrServer(MpHttpServer):
    def __init__(self, kw: MpKw, use_gpu: bool = False, lang: str = 'ch'):
        super().__init__(kw)
        self.use_gpu, self.lang = use_gpu, lang
        self._import_paddleocr(not self.use_gpu)

    @staticmethod
    def _import_paddleocr(whether_to_import: bool = True):
        if whether_to_import:
            from paddleocr import PaddleOCR
            global PaddleOCR
            PaddleOCR = PaddleOCR

    @staticmethod
    def unify_format(ocr_result: list) -> list:
        """format text info list to: [[[[left top], [right top], [right bottom], [left bottom]], text, confidence], ...]
           for instance:             [[[[49, 5], [89, 5], [89, 19], [49, 19]], 'Text', 0.0004511636577615576], ...]"""
        if ocr_result:  # 防止传入列表本身为空
            ocr_result = ocr_result[0]
            if ocr_result is not None:  # paddleocr如果未检测到，会返回 [None]
                return [[text_info[0], text_info[1][0], text_info[1][1]] for text_info in ocr_result]
        return []

    def init(self) -> None:
        self._import_paddleocr(self.use_gpu)
        self.ocr = PaddleOCR(det_model_dir='/home/a/.paddleocr/whl/det/ch/ch_PP-OCRv4_det_infer',
                             rec_model_dir='/home/a/.paddleocr/whl/rec/ch/ch_PP-OCRv4_rec_infer',
                             cls_model_dir='/home/a/.paddleocr/whl/cls/ch_ppocr_mobile_v2.0_cls_infer',
                             use_gpu=self.use_gpu, use_angle_cls=True, lang=self.lang, show_log=self.show_info)

    def main_loop(self, data: dict) -> Any:
        result = self.ocr.ocr(ImgConv(data['img']).to_numpy(), cls=data.get('cls', False))
        return self.unify_format(result)


class Ocr(MpHttpClient):
    def submit(self, imgs: list | tuple, cls: bool = False) -> int:
        data_list = []
        not_local = self.host not in ['localhost', '127.0.0.1']
        for img in imgs:
            if not_local and isinstance(img, (str, Path)):
                img = ImgConv(img).to_bytesio()
            data_list.append({'img': img, 'cls': cls})
        return super().submit(data_list)

    def fetch(self, task_id: int, timeout: float = 3600) -> list[list]:
        return super().fetch(task_id, timeout)

    def batch(self, imgs: list | tuple, cls: bool = False, timeout: float = 3600) -> list[list]:
        return self.fetch(self.submit(imgs, cls), timeout)

    def get(self, img: Any, cls: bool = False, timeout: float = 3600) -> list:
        return self.batch([img], cls, timeout)[0]


class DrawResult:
    def __init__(self, img: Any, ocr_result: list, save_path: Path | str = None, font_size_ratio: float = 0.7):
        self.img = ImgConv(img).to_pil()
        self.ocr_result, self.save_path, self.font_size_ratio = ocr_result, save_path, font_size_ratio
        self._draw()

    def _draw(self) -> Image.Image | Path:
        if self.ocr_result:
            self.img = ImgDraw(self.img).polygons([i[0] for i in self.ocr_result], outline='red').to_pil()
            self.img = self._draw_text()
        if self.save_path:
            return ImgConv(self.img).to_path(self.save_path)
        return self.img

    def _draw_text(self) -> Image.Image:
        w, h = self.img.size
        draw = ImgDraw(self.img)
        for text_info in self.ocr_result:
            quad = text_info[0]
            edges = (math.sqrt((quad[0][0] - quad[1][0]) ** 2 + (quad[0][1] - quad[1][1]) ** 2),
                     math.sqrt((quad[1][0] - quad[2][0]) ** 2 + (quad[1][1] - quad[2][1]) ** 2),
                     math.sqrt((quad[2][0] - quad[3][0]) ** 2 + (quad[2][1] - quad[3][1]) ** 2),
                     math.sqrt((quad[3][0] - quad[0][0]) ** 2 + (quad[3][1] - quad[0][1]) ** 2))
            min_edge_length = min(edges)
            max_edge_length = max(edges)
            bounding_rect = ImgDraw.bounding_rect(quad).to_lt_rb()

            # make the text rect not overflow the image edge
            right_x = bounding_rect[0][0] + max_edge_length
            bottom_y = bounding_rect[1][1] + min_edge_length
            x_diff = right_x - w if right_x > w else 0
            y = bounding_rect[0][1] - min_edge_length if bottom_y > h else bounding_rect[1][1]
            text_rect = Rect([bounding_rect[0][0] - x_diff, y,
                              max_edge_length, min_edge_length], rect_format=Rect.LTWH)
            draw.text_in_rect(text_info[1], text_rect, 'red')
        return draw.to_pil()
