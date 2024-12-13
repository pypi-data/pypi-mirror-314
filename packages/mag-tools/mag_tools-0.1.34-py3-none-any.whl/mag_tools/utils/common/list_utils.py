import re
from typing import List, Optional, Dict, Tuple


class ListUtils:
    @staticmethod
    def split_by_keyword(lines:List[str], keyword:Optional[str]=None) -> List[List[str]]:
        """
        根据关键字或空行将字符串数组切分成若干块。

        参数：
        :param lines: 字符串数组
        :param keyword: 关键字,为None或空时表示按空行分隔
        :return: 切分后的块列表，每个块是一个字符串数组
        """
        if keyword is None or keyword == "":
            return ListUtils.__split_by_empty_line(lines)

        blocks = [[]]
        current_block = []

        for line in lines:
            if keyword in line:
                if current_block:
                    blocks.append(current_block)
                    current_block = []
            current_block.append(line)

        if current_block:
            blocks.append(current_block)

        return blocks

    @staticmethod
    def split_by_keywords(lines: List[str], keywords: List[str]) -> Dict[str, List[str]]:
        segments = {keyword: [] for keyword in keywords}
        current_keyword = None

        for line in lines:
            if line in keywords:
                current_keyword = line
            segments[current_keyword].append(line)

        return segments

    @staticmethod
    def split_by_boundary(lines: List[str], keyword_map: Dict[str, Tuple[Optional[str], Optional[str]]]) -> Dict[
        str, List[str]]:
        text = "\n".join(lines)
        segments = {segment_name: [] for segment_name in keyword_map}

        # 构建正则表达式模式
        keyword_patterns = {segment_name: re.escape(segment_name) for segment_name in keyword_map}
        for segment_name, (begin_keyword, end_keyword) in keyword_map.items():
            if begin_keyword is None and end_keyword is None:
                # 处理没有分界线的情况
                keywords = [keyword for keyword in keyword_map.keys()]
                return ListUtils.split_by_keywords(lines, keywords)
            else:
                # 处理有分界线的情况
                pattern = rf"{keyword_patterns[segment_name]}\n{re.escape(begin_keyword)}.*?\n{re.escape(end_keyword)}"
                matches = re.finditer(pattern, text, re.DOTALL)

                for match in matches:
                    block_lines = match.group().split("\n")
                    segments[segment_name].extend(block_lines)

        # 处理 BASE 段
        base_pattern = re.escape("BASE")
        base_matches = list(re.finditer(base_pattern, text))
        if base_matches:
            base_start = base_matches[0].start()
            next_keyword_start = min(
                (match.start() for match in re.finditer("|".join(keyword_patterns.values()), text) if
                 match.start() > base_start), default=len(text))
            segments["BASE"] = text[base_start:next_keyword_start].strip().split("\n")

        return segments

    @staticmethod
    def trim(lines: List[str]) -> List[str]:
        """
        去掉字符串数组的起始和结尾的空行
        :param lines: 字符串数组
        :return: 去掉空行后的字符串数组
        """
        # 去掉起始的空行
        while lines and lines[0].strip() == '':
            lines.pop(0)

        # 去掉结尾的空行
        while lines and lines[-1].strip() == '':
            lines.pop()

        return lines

    @staticmethod
    def __split_by_empty_line(lines:List[str]) -> List[List[str]]:
        """
        根据空行将字符串数组切分成若干块，并删除空行。

        参数：
        :param lines: 字符串数组
        :return: 切分后的块列表，每个块是一个字符串数组
        """
        blocks = []
        current_block = []

        for line in lines:
            if line.strip() == "":
                if current_block:
                    blocks.append(current_block)
                    current_block = []
                current_block.append(line)  # 将空行作为块的第一行
            else:
                current_block.append(line)

        if current_block:
            blocks.append(current_block)

        return blocks
