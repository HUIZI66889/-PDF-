import fitz

def remove_pdf_watermark(input_pdf_path, output_pdf_path):
    # 打开PDF文件
    doc = fitz.open(input_pdf_path)
    
    for page in doc:
        page.clean_contents()  # 清理页面绘图命令
        
        # 获取页面字节流
        xref = page.get_contents()[0]  # 获取页面字节流，以xref的形式返回        
        cont0 = doc.xref_stream(xref).decode()  # 将流解码为字符串

        # 打开文件并写入字节流
        with open("quanshan.txt", "wb") as file:
            file.write(cont0.encode())  # 将字符串编码为字节后写入文件
            
        print("字节流已保存为 quanshan.txt")
        
        # 尝试多次删除水印
        for _ in range(10):  # 最多尝试10次
            start = 0
            while True:
                # 查找水印的起始位置
                start = cont0.find("/Artifact", start)
                if start == -1:
                    break  # 没有找到更多水印，退出循环

                # 查找水印的结束位置
                end = cont0.find("EMC", start)
                if end != -1:
                    # 删除水印部分
                    cont0 = cont0[:start] + cont0[end+3:]  # end+3是因为"EMC"包含3个字符

                    # 更新字节流
                    doc.update_stream(xref, cont0.encode())  # 更新流
                    print("已删除一个水印")
                start = end + 3  # 继续查找下一个水印位置

        # 更新页面的内容
        page.clean_contents()  # 再次清理页面内容
        
    # 保存修改后的PDF文件        
    doc.save(output_pdf_path, garbage=4)
    doc.close()

# 调用函数去除水印
remove_pdf_watermark('jiagebiao.pdf', '000.pdf')
