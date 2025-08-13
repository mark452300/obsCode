"""
颜色转换工具模块

提供 RGB 和 BGR 颜色格式之间的转换功能，主要用于 OBS Studio 的颜色处理。
OBS Studio 内部使用 BGR 格式，而大多数其他应用使用 RGB 格式。
"""


class ColorUtils:
    """颜色转换工具类"""

    @staticmethod
    def rgb_to_bgr(rgb_color: int) -> int:
        """
        将 RGB 颜色转换为 BGR 格式（OBS 使用的格式）

        Args:
            rgb_color: RGB 格式的颜色值 (0xRRGGBB)

        Returns:
            int: BGR 格式的颜色值 (0xBBGGRR)

        Example:
            >>> ColorUtils.rgb_to_bgr(0xFF557F)  # RGB 粉红色
            8345087  # 0x7F55FF (BGR 粉红色)
        """
        r = (rgb_color >> 16) & 0xFF  # 提取红色分量
        g = (rgb_color >> 8) & 0xFF   # 提取绿色分量
        b = rgb_color & 0xFF          # 提取蓝色分量

        # 重新组合为 BGR 格式
        return (b << 16) | (g << 8) | r

    @staticmethod
    def bgr_to_rgb(bgr_color: int) -> int:
        """
        将 BGR 颜色转换为 RGB 格式

        Args:
            bgr_color: BGR 格式的颜色值 (0xBBGGRR)

        Returns:
            int: RGB 格式的颜色值 (0xRRGGBB)

        Example:
            >>> ColorUtils.bgr_to_rgb(0x7F55FF)  # BGR 粉红色
            16733567  # 0xFF557F (RGB 粉红色)
        """
        b = (bgr_color >> 16) & 0xFF  # 提取蓝色分量
        g = (bgr_color >> 8) & 0xFF   # 提取绿色分量
        r = bgr_color & 0xFF          # 提取红色分量

        # 重新组合为 RGB 格式
        return (r << 16) | (g << 8) | b

    @staticmethod
    def rgb_values_to_bgr(r: int, g: int, b: int) -> int:
        """
        将 RGB 分量值转换为 BGR 颜色

        Args:
            r: 红色分量 (0-255)
            g: 绿色分量 (0-255)
            b: 蓝色分量 (0-255)

        Returns:
            int: BGR 格式的颜色值

        Example:
            >>> ColorUtils.rgb_values_to_bgr(255, 85, 127)  # RGB(255, 85, 127)
            8345087  # 0x7F55FF (BGR 格式)
        """
        return (b << 16) | (g << 8) | r

    @staticmethod
    def bgr_values_to_rgb(b: int, g: int, r: int) -> int:
        """
        将 BGR 分量值转换为 RGB 颜色

        Args:
            b: 蓝色分量 (0-255)
            g: 绿色分量 (0-255)
            r: 红色分量 (0-255)

        Returns:
            int: RGB 格式的颜色值

        Example:
            >>> ColorUtils.bgr_values_to_rgb(127, 85, 255)  # BGR(127, 85, 255)
            16733567  # 0xFF557F (RGB 格式)
        """
        return (r << 16) | (g << 8) | b

    @staticmethod
    def extract_rgb_components(rgb_color: int) -> tuple[int, int, int]:
        """
        从 RGB 颜色值中提取各个分量

        Args:
            rgb_color: RGB 格式的颜色值 (0xRRGGBB)

        Returns:
            tuple[int, int, int]: (红色, 绿色, 蓝色) 分量值

        Example:
            >>> ColorUtils.extract_rgb_components(0xFF557F)
            (255, 85, 127)
        """
        r = (rgb_color >> 16) & 0xFF
        g = (rgb_color >> 8) & 0xFF
        b = rgb_color & 0xFF
        return r, g, b

    @staticmethod
    def extract_bgr_components(bgr_color: int) -> tuple[int, int, int]:
        """
        从 BGR 颜色值中提取各个分量

        Args:
            bgr_color: BGR 格式的颜色值 (0xBBGGRR)

        Returns:
            tuple[int, int, int]: (蓝色, 绿色, 红色) 分量值

        Example:
            >>> ColorUtils.extract_bgr_components(0x7F55FF)
            (127, 85, 255)
        """
        b = (bgr_color >> 16) & 0xFF
        g = (bgr_color >> 8) & 0xFF
        r = bgr_color & 0xFF
        return b, g, r

    @staticmethod
    def hex_to_rgb(hex_color: str) -> int:
        """
        将十六进制颜色字符串转换为 RGB 整数

        Args:
            hex_color: 十六进制颜色字符串，支持 "#RRGGBB" 或 "RRGGBB" 格式

        Returns:
            int: RGB 格式的颜色值

        Example:
            >>> ColorUtils.hex_to_rgb("#FF557F")
            16733567  # 0xFF557F
            >>> ColorUtils.hex_to_rgb("FF557F")
            16733567  # 0xFF557F
        """
        # 移除可能的 # 前缀
        hex_color = hex_color.lstrip('#')
        
        # 确保是 6 位十六进制
        if len(hex_color) != 6:
            raise ValueError(f"Invalid hex color format: {hex_color}. Expected 6 characters.")
        
        return int(hex_color, 16)

    @staticmethod
    def rgb_to_hex(rgb_color: int) -> str:
        """
        将 RGB 整数转换为十六进制颜色字符串

        Args:
            rgb_color: RGB 格式的颜色值

        Returns:
            str: 十六进制颜色字符串 (格式: #RRGGBB)

        Example:
            >>> ColorUtils.rgb_to_hex(16733567)
            "#FF557F"
        """
        return f"#{rgb_color:06X}"
