import numpy as np
from PIL import Image
import os
import warnings

class HSLSixColorProcessor:
    def __init__(self, palette=None):
        """
        初始化HSL六色处理器

        :param palette: 可选的自定义调色板，默认为六种标准颜色
        """
        warnings.filterwarnings("ignore", category=RuntimeWarning)

        if palette is None:
            self.palette = np.array([
                [0, 0, 0],        # 黑色
                [255, 255, 255],  # 白色
                [255, 0, 0],      # 红色
                [0, 255, 0],      # 绿色
                [0, 0, 255],      # 蓝色
                [255, 255, 0]     # 黄色
            ])
        else:
            self.palette = palette

    def clamp(self, array, min_val, max_val):
        """
        将数组值限制在指定范围内

        :param array: 输入数组
        :param min_val: 最小值
        :param max_val: 最大值
        :return: 限制后的数组
        """
        return np.clip(array, min_val, max_val)

    def find_closest_palette_color(self, old_pixel, palette):
        """
        找到最接近给定像素的调色板颜色

        :param old_pixel: 原始像素颜色
        :param palette: 调色板
        :return: 最接近的调色板颜色
        """
        distances = np.linalg.norm(palette - old_pixel, axis=1)
        closest_index = np.argmin(distances)
        return palette[closest_index]

    def zigzag_scan(self, width, height):
        """
        生成Z字形扫描顺序

        :param width: 图像宽度
        :param height: 图像高度
        :return: Z字形扫描的坐标列表
        """
        scan = []
        for i in range(width + height - 1):
            if i % 2 == 0:
                for y in range(i + 1):
                    x = i - y
                    if x < width and y < height:
                        scan.append((x, y))
            else:
                for x in range(i + 1):
                    y = i - x
                    if x < width and y < height:
                        scan.append((x, y))
        return scan

    def calculate_local_mean(self, weighted_pixels, x, y):
        """
        计算局部像素平均值

        :param weighted_pixels: 像素权重矩阵
        :param x: x坐标
        :param y: y坐标
        :return: 局部平均值
        """
        kernel = weighted_pixels[max(0, y-1):min(y+2, weighted_pixels.shape[0]),
                                 max(0, x-1):min(x+2, weighted_pixels.shape[1])]
        return np.mean(kernel)

    def rgb_to_hsl_adjust_saturation(self, image_path, saturation_factor=0.8):
        """
        使用HSL方法调整图像饱和度

        :param image_path: 输入图像路径
        :param saturation_factor: 饱和度调整因子，默认为0.8
        :return: 调整后的PIL图像
        """
        image = Image.open(image_path).convert('RGB')
        image_np = np.array(image, dtype=float) / 255.0

        # 计算最大值和最小值
        Imax = np.max(image_np, axis=2)
        Imin = np.min(image_np, axis=2)
        L = (Imax + Imin) / 2

        # 计算饱和度
        S = np.where(Imax == Imin, 0, np.where(L <= 0.5, (Imax - Imin) / (Imax + Imin), (Imax - Imin) / (2.0 - (Imax + Imin))))

        # 计算alpha
        alpha = np.where(saturation_factor + S > 1, (1 - S) / S, saturation_factor / (1 - saturation_factor))

        # 计算新的RGB值
        R, G, B = image_np[:, :, 0], image_np[:, :, 1], image_np[:, :, 2]
        R_new = R + (R - L) * alpha
        G_new = G + (G - L) * alpha
        B_new = B + (B - L) * alpha

        # 确保新的RGB值在0到1之间
        new_image = np.stack([np.clip(R_new, 0, 1), np.clip(G_new, 0, 1), np.clip(B_new, 0, 1)], axis=2)

        # 转换回uint8类型
        new_image_uint8 = (new_image * 255).astype(np.uint8)
        new_image_pil = Image.fromarray(new_image_uint8)
        return new_image_pil

    def adaptive_error_diffusion_dithering(self, input_image):
        """
        使用自适应误差扩散抖动算法处理图像

        :param input_image: 输入PIL图像
        :return: 处理后的PIL图像
        """
        input_image = input_image.convert("RGB")
        width, height = input_image.size
        output_image = Image.new("RGB", (width, height))
        input_pixels = np.array(input_image, dtype=np.float32)

        weighted_pixels = input_pixels
        output_pixels = np.zeros_like(input_pixels)

        scan_order = self.zigzag_scan(width, height)

        for x, y in scan_order:
            old_pixel = weighted_pixels[y, x]

            # 添加噪声以减少伪影
            noise = np.random.uniform(-0.2, 0.2, old_pixel.shape) * 5
            old_pixel = self.clamp(old_pixel + noise, 0, 255)

            new_pixel = self.find_closest_palette_color(old_pixel, self.palette)
            output_pixels[y, x] = new_pixel
            quant_error = old_pixel - new_pixel

            local_mean = self.calculate_local_mean(weighted_pixels, x, y)
            adaptive_factor = 1.2 - (np.mean(np.abs(quant_error)) / 255.0) * (local_mean / 255.0)

            if x < width - 1:
                weighted_pixels[y, x + 1] = self.clamp(
                    weighted_pixels[y, x + 1] + quant_error * (7 / 48 * adaptive_factor), 0, 255)
            if x < width - 2:
                weighted_pixels[y, x + 2] = self.clamp(
                    weighted_pixels[y, x + 2] + quant_error * (5 / 48 * adaptive_factor), 0, 255)
            if y < height - 1:
                if x > 1:
                    weighted_pixels[y + 1, x - 2] = self.clamp(weighted_pixels[y + 1, x - 2] + quant_error * (
                            3 / 48 * adaptive_factor), 0, 255)
                if x > 0:
                    weighted_pixels[y + 1, x - 1] = self.clamp(weighted_pixels[y + 1, x - 1] + quant_error * (
                            5 / 48 * adaptive_factor), 0, 255)
                weighted_pixels[y + 1, x] = self.clamp(
                    weighted_pixels[y + 1, x] + quant_error * (7 / 48 * adaptive_factor), 0, 255)
                if x < width - 1:
                    weighted_pixels[y + 1, x + 1] = self.clamp(weighted_pixels[y + 1, x + 1] + quant_error * (
                            5 / 48 * adaptive_factor), 0, 255)
                if x < width - 2:
                    weighted_pixels[y + 1, x + 2] = self.clamp(weighted_pixels[y + 1, x + 2] + quant_error * (
                            3 / 48 * adaptive_factor), 0, 255)
            if y < height - 2:
                weighted_pixels[y + 2, x] = self.clamp(
                    weighted_pixels[y + 2, x] + quant_error * (5 / 48 * adaptive_factor), 0, 255)
                if x < width - 1:
                    weighted_pixels[y + 2, x + 1] = self.clamp(weighted_pixels[y + 2, x + 1] + quant_error * (
                            3 / 48 * adaptive_factor), 0, 255)
                if x > 0:
                    weighted_pixels[y + 2, x - 1] = self.clamp(weighted_pixels[y + 2, x - 1] + quant_error * (
                            3 / 48 * adaptive_factor), 0, 255)
                if x < width - 2:
                    weighted_pixels[y + 2, x + 2] = self.clamp(weighted_pixels[y + 2, x + 2] + quant_error * (
                            1 / 48 * adaptive_factor), 0, 255)
                if x > 1:
                    weighted_pixels[y + 2, x - 2] = self.clamp(weighted_pixels[y + 2, x - 2] + quant_error * (
                            1 / 48 * adaptive_factor), 0, 255)

        output_image = Image.fromarray(np.clip(output_pixels, 0, 255).astype('uint8'), 'RGB')
        return output_image

    def process_images(self, input_folder, output_folder, saturation_factor=0.8, file_types=None):
        """
        批量处理图像

        :param input_folder: 输入图像文件夹路径
        :param output_folder: 输出图像文件夹路径
        :param saturation_factor: 饱和度调整因子，默认为0.8
        :param file_types: 要处理的文件类型，默认为 ['.jpg', '.png']
        """
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        if file_types is None:
            file_types = ['.jpg', '.png', '.jpeg', '.bmp', '.tiff']

        for filename in os.listdir(input_folder):
            if any(filename.lower().endswith(ext) for ext in file_types):
                input_image_path = os.path.join(input_folder, filename)

                # HSL调整饱和度
                hsl_adjusted_image = self.rgb_to_hsl_adjust_saturation(input_image_path, saturation_factor)

                # 误差扩散抖动
                output_image = self.adaptive_error_diffusion_dithering(hsl_adjusted_image)

                output_image_path = os.path.join(output_folder, filename)
                output_image.save(output_image_path)
                print(f"Processed {filename}")

def process_folder(input_folder, output_folder, saturation_factor=0.8, palette=None, file_types=None):
    """
    快速处理整个文件夹的便捷函数

    :param input_folder: 输入图像文件夹路径
    :param output_folder: 输出图像文件夹路径
    :param saturation_factor: 饱和度调整因子，默认为0.8
    :param palette: 可选的自定义调色板
    :param file_types: 要处理的文件类型列表
    """
    processor = HSLSixColorProcessor(palette)
    processor.process_images(input_folder, output_folder, saturation_factor, file_types)