import re
import unicodedata
from pathlib import Path
from typing import Any, Callable
import cv2
import numpy as np
from psplpy.image_utils import ImgConv, Rect, ImgDraw


class ImgDet:
    TM_CCOEFF_NORMED = cv2.TM_CCOEFF_NORMED
    TM_CCORR_NORMED = cv2.TM_CCORR_NORMED
    TM_SQDIFF_NORMED = cv2.TM_SQDIFF_NORMED

    @staticmethod
    def _filter_rects(rects: list[Rect], threshold: float) -> list[Rect]:
        """if the two rectangles overlap percentage greater than the threshold, remove the second rectangle"""
        if 0 <= threshold <= 1:
            marked_rects = [[rect, True] for rect in rects]

            for i in range(len(marked_rects)):
                if marked_rects[i][1]:
                    for j in range(i + 1, len(marked_rects)):
                        if marked_rects[j][1]:
                            overlap_ratio = max(marked_rects[i][0].overlap_pct(marked_rects[j][0]))
                            if overlap_ratio >= threshold:
                                marked_rects[j][1] = False

            return [rect[0] for rect in marked_rects if rect[1]]
        return rects

    @staticmethod
    def _get_result(image: Any, template_image: Any, method: int = cv2.TM_CCOEFF_NORMED, save_match: Path | str = None):
        cvt_image = ImgConv(image).to_opencv()
        cvt_template_image = ImgConv(template_image).to_opencv()
        result = cv2.matchTemplate(cvt_image, cvt_template_image, method)  # 使用模板匹配
        if method == ImgDet.TM_SQDIFF_NORMED:
            result = -((result - 0.5) * 2)
        if save_match is not None:
            result_copy = result.copy()
            result_copy = ((result_copy + 1) * (255 / 2)).astype(np.uint8)
            cv2.imwrite(str(save_match), result_copy)
        return result, cvt_image, cvt_template_image

    @staticmethod
    def _draw_result(cvt_image: np.ndarray, rects: list[Rect], path: Path | str) -> None:
        if path is not None:
            copied_image = cvt_image.copy()
            for rect in rects:
                cv2.rectangle(copied_image, rect[0], rect[1], (0, 0, 255), 1)
            cv2.imwrite(str(path), copied_image)

    @staticmethod
    def get_box(image: Any, template_image: Any, confidence: float = 0.9, method: int = cv2.TM_CCOEFF_NORMED,
                draw_result: Path | str = None, save_match: Path | str = None) -> tuple[Rect, float] | None:
        """return: (Rect, confidence) or None"""
        result, cvt_image, cvt_template_image = ImgDet._get_result(image, template_image, method, save_match)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val < confidence:
            return None
        top_left = max_loc
        h, w = cvt_template_image.shape[:2]
        rect = Rect((top_left, (top_left[0] + w, top_left[1] + h)), rect_format=Rect.LT_RB)
        ImgDet._draw_result(cvt_image, [rect], draw_result)
        return rect, float(result[top_left[::-1]])

    @staticmethod
    def get_boxes(image: Any, template_image: Any, confidence: float = 0.9, overlap: float = 0.5,
                  method: int = cv2.TM_CCOEFF_NORMED, draw_result: Path | str = None,
                  save_match: Path | str = None) -> list[tuple[Rect, float]]:
        """return: [(Rect1, confidence1), (Rect2, confidence2), ...] or []"""
        result, cvt_image, cvt_template_image = ImgDet._get_result(image, template_image, method, save_match)
        indices = np.where(result >= confidence)
        positions = np.column_stack(indices)
        sorted_positions = np.argsort(result[indices])[::-1]  # sort in descending order
        sorted_positions = [sorted_position[::-1] for sorted_position in positions[sorted_positions]]

        h, w = cvt_template_image.shape[:2]
        boxes = [Rect([top_left, (top_left[0] + w, top_left[1] + h)], rect_format=Rect.LT_RB)
                 for top_left in sorted_positions]
        boxes = ImgDet._filter_rects(boxes, overlap)
        rects = [(box, float(result[tuple(box[0][::-1])])) for box in boxes]
        ImgDet._draw_result(cvt_image, [rect[0] for rect in rects], draw_result)
        return rects

    @staticmethod
    def det_img(image: Any, template_image: Any, confidence: float = 0.9, method: int = cv2.TM_CCOEFF_NORMED,
                draw_result: Path | str = None, save_match: Path | str = None) -> bool:
        return bool(ImgDet.get_box(image, template_image, confidence, method, draw_result, save_match))


class TxtProc:
    def __init__(self, *flags: str | Callable):
        self.flags = flags

    def process(self, text: str) -> str:
        for flag in self.flags:
            if isinstance(flag, str):
                text = getattr(self, flag)(text)
            elif callable(flag):
                text = flag(text)
            else:
                raise AssertionError
        return text

    @staticmethod
    def casefold(text: str) -> str:
        return text.casefold()

    @staticmethod
    def num(text: str) -> str:
        return re.sub(r'\D', '', text)

    @staticmethod
    def en(text: str) -> str:
        return re.sub(r'[^a-zA-Z]', '', text)

    @staticmethod
    def en_num(text: str) -> str:
        return re.sub(r'[^a-zA-Z0-9]', '', text)

    @staticmethod
    def no_space(text: str) -> str:
        return re.sub(r'\s+', '', text)

    @staticmethod
    def camel_to_snake(camel_case: str) -> str:
        # 将驼峰字符串转换为下划线风格
        return re.sub(r'(?<!^)(?=[A-Z])', '_', camel_case).lower()

    @staticmethod
    def snake_to_camel(snake_case: str) -> str:
        components = snake_case.split('_')
        return ''.join(x.capitalize() for x in components)

    @staticmethod
    def escape(text: str) -> str:
        escape_characters = {'\\': '\\\\', '\'': '\\\'', '\"': '\\\"'}
        for char, escape_sequence in escape_characters.items():
            text = text.replace(char, escape_sequence)
        return text

    @staticmethod
    def valid_var_name(text: str) -> str:
        new_text = ''
        for char in text:
            if char == '_':
                new_text += char
            else:
                category = unicodedata.category(char)
                if category.startswith('L') or category.startswith('Nd'):
                    new_text += char
        return new_text


class TextInfo:
    def __init__(self, region: list | tuple | Rect, text: str, confidence: float):
        self.rect = ImgDraw.bounding_rect(region)
        self.text = text
        self.confidence = confidence

    def __iter__(self):
        for item in [self.rect, self.text, self.confidence]:
            yield item

    @staticmethod
    def _index_mapping(index) -> str:
        index_mapping = {0: 'rect', 1: 'text', 2: 'confidence',
                         -3: 'rect', -2: 'text', -1: 'confidence'}
        if index in index_mapping:
            return index_mapping[index]
        raise IndexError('Index out of range.')

    def __getitem__(self, index):
        if isinstance(index, slice):  # if slice
            return [self[i] for i in range(*index.indices(3))]
        return getattr(self, self._index_mapping(index))

    def __setitem__(self, index, value):
        setattr(self, self._index_mapping(index), value)

    def __str__(self):
        return f'{self.__class__.__name__}({self.rect}, {repr(self.text)}, {self.confidence:.4f})'

    __repr__ = __str__

    def __eq__(self, other):
        if isinstance(other, TextInfo):
            return list(self) == list(other)
        return False


class TextInfoList:
    def __init__(self, text_info_list: list):
        self.text_info_list = self._get_text_info_list(text_info_list)

    @staticmethod
    def _get_text_info_list(text_info_list: list) -> list[TextInfo]:
        self_text_info_list = []
        for info in text_info_list:
            if isinstance(info, TextInfo):
                self_text_info_list.append(info)
            else:
                self_text_info_list.append(TextInfo(*info))
        return self_text_info_list

    def __iter__(self):
        for text_info in self.text_info_list:
            yield text_info

    def __getitem__(self, index):
        if isinstance(index, slice):
            return self.text_info_list[index.start:index.stop:index.step]
        return self.text_info_list[index]

    def __setitem__(self, index, value):
        self.text_info_list[index] = value

    def __str__(self):
        return str(self.text_info_list)

    __repr__ = __str__

    def __eq__(self, other):
        if isinstance(other, TextInfoList):
            return self.text_info_list == other.text_info_list
        return False

    def text_list(self) -> list[str]:
        return [info.text for info in self.text_info_list]

    def merged_text(self) -> str:
        return ''.join(self.text_list())


class TxtDet:
    IN = 'in'
    IS = 'is'

    def __init__(self, txt_processor: TxtProc = None, process_text: bool = True):
        self.txt_processor = txt_processor or TxtProc()
        self.process_text = process_text    # whether process the 'text' argument

    @staticmethod
    def get_txt(text_info_list: list | TextInfoList, rect: Any, overlap: float = 0.75) -> TextInfo:
        rect = Rect(rect)
        for text_info in TextInfoList(text_info_list):
            percentage = min(rect.overlap_pct(text_info.rect))
            if percentage >= overlap:
                return text_info

    def _get_condition(self, text: str | re.Pattern, mode: str) -> Callable:
        if self.process_text:
            text = self.txt_processor.process(text)
        if isinstance(text, str):
            if mode == self.IN:
                return lambda text_info: text in text_info.text
            elif mode == self.IS:
                return lambda text_info: text == text_info.text
        elif isinstance(text, re.Pattern):
            return lambda text_info: text.search(text_info.text)
        raise AssertionError

    def _txt_process(self, text_info_list: list | TextInfoList) -> TextInfoList:
        if not isinstance(text_info_list, TextInfoList):
            text_info_list = TextInfoList(text_info_list)
        for info in text_info_list:
            info.text = self.txt_processor.process(info.text)
        return text_info_list

    def _get_boxes(self, text_info_list: list | TextInfoList, text: str | re.Pattern, get_one: bool = False,
                   mode: str = IN) -> TextInfoList | TextInfo:
        condition = self._get_condition(text, mode)
        result_list = TextInfoList([])
        print(self._txt_process(text_info_list))
        for original_info, processed_info in zip(TextInfoList(text_info_list), self._txt_process(text_info_list)):
            if condition(processed_info):
                if get_one:
                    return original_info
                result_list.text_info_list.append(original_info)
        return result_list

    def get_boxes(self, text_info_list: list | TextInfoList, text: str | re.Pattern,
                  mode: str = IN) -> TextInfoList:
        return self._get_boxes(text_info_list, text, mode=mode)

    def get_box(self, text_info_list: list | TextInfoList, text: str | re.Pattern, mode: str = IN) -> TextInfo | None:
        return self._get_boxes(text_info_list, text, get_one=True, mode=mode)

    class MatchObj:
        def __init__(self, text_info_list: list | TextInfoList, matched_text_info_list: list | TextInfoList):
            self.text_info_list = text_info_list
            self.matched_text_info_list = matched_text_info_list
            self.result_list = []

        @property
        def match_list(self) -> list[TextInfo]:
            return [self.matched_text_info_list[i] for i in range(len(self.result_list)) if self.result_list[i]]

        @property
        def mismatch_list(self) -> list[TextInfo]:
            return [self.matched_text_info_list[i] for i in range(len(self.result_list)) if not self.result_list[i]]

        def _update_bool_and_confidence(self, expected_confidence: float) -> None:
            self.confidence = self.result_list.count(True) / len(self.result_list)
            self.bool = self.confidence >= expected_confidence

    def match(self, text_info_list: list | TextInfoList, matched_text_info_list: list | TextInfoList,
              overlap: float = 0.75, confidence: float = 1, mode: str = IN) -> MatchObj:
        match_obj = self.MatchObj(text_info_list, matched_text_info_list)
        text_info_list, processed_text_info_list = TextInfoList(text_info_list), self._txt_process(text_info_list)

        for matched_text_info in TextInfoList(matched_text_info_list):
            flag = False
            condition = self._get_condition(matched_text_info.text, mode)
            for original_info, processed_info in zip(text_info_list, processed_text_info_list):
                if condition(processed_info):
                    if min(matched_text_info.rect.overlap_pct(original_info.rect)) >= overlap:
                        flag = True
                        break
            match_obj.result_list.append(flag)
        match_obj._update_bool_and_confidence(confidence)
        return match_obj
