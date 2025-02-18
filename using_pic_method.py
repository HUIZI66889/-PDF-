import fitz  # PyMuPDF
import os
from PIL import Image
import os

def pdf_to_png(pdf_path, output_folder):
    # 打开 PDF 文件
    pdf_document = fitz.open(pdf_path)
    
    # 创建输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 遍历 PDF 中的每一页
    for page_num in range(pdf_document.page_count):
        # 获取当前页面
        page = pdf_document.load_page(page_num)
        
        # 将页面转换为 pixmap（图像对象）
        pix = page.get_pixmap(dpi=300)  # 可调整dpi参数以控制输出图像的分辨率
        
        # 输出图片的文件路径
        output_path = os.path.join(output_folder, f"page_{page_num + 1}.png")
        
        # 将 pixmap 保存为 PNG 图片
        pix.save(output_path)
        print(f"Page {page_num + 1} saved as {output_path}")
    
    # 关闭 PDF 文件
    pdf_document.close()


def replace_rgb_with_white(image_folder):
    # 遍历文件夹中的所有 PNG 图片
    for filename in os.listdir(image_folder):
        if filename.endswith(".png"):
            image_path = os.path.join(image_folder, filename)
            
            # 打开图片
            img = Image.open(image_path)
            img = img.convert("RGB")  # 转换为 RGB 模式（如果不是的话）
            
            # 获取图片的像素数据
            pixels = img.load()
            
            # 遍历所有像素，检查 RGB 是否在 (216, 216, 216) ± 30 范围内
            for i in range(img.width):
                for j in range(img.height):
                    r, g, b = pixels[i, j]
                    
                    # 判断像素是否在 (216, 216, 216) ± 30 范围内
                    if (186 <= r <= 246) and (186 <= g <= 246) and (186 <= b <= 246):
                        # 将符合条件的像素替换为白色
                        pixels[i, j] = (255, 255, 255)

            # 生成新的文件名，添加 "_modify" 后缀
            new_filename = os.path.splitext(filename)[0] + "_modify.png"
            new_image_path = os.path.join(image_folder, new_filename)
            
            # 保存修改后的图片
            img.save(new_image_path)
            print(f"Processed and saved: {new_image_path}")

# 示例用法  
pdf_path = 'jiagebiao.pdf'  # 替换为你的 PDF 文件路径
output_folder = 'output_images'  # 替换为你希望保存图片的文件夹
pdf_to_png(pdf_path, output_folder)

# 示例用法
replace_rgb_with_white(output_folder)
