import os
import subprocess
import tempfile
import yaml

class PDFGenerator:
    """
    将翻译后的文本生成为PDF文件
    """
    
    def __init__(self, config_path="config/config.yaml"):
        """初始化PDF生成器"""
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        
        self.font = self.config['pdf']['output_font']
        self.temp_dir = self.config['pdf']['temp_dir']
        
        # 确保临时目录存在
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def create_markdown(self, text, output_path):
        """将文本保存为Markdown文件"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        return output_path
    
    def markdown_to_pdf(self, markdown_path, output_pdf_path):
        """使用pandoc将Markdown转换为PDF"""
        try:
            # 检查pandoc是否安装
            subprocess.run(['which', 'pandoc'], check=True, capture_output=True)
            
            # 使用pandoc和xelatex生成PDF
            cmd = [
                'pandoc',
                markdown_path,
                '-o', output_pdf_path,
                '--pdf-engine=xelatex',
                '-V', f'mainfont={self.font}'
            ]
            
            result = subprocess.run(cmd, check=True, capture_output=True)
            
            if os.path.exists(output_pdf_path):
                return output_pdf_path
            else:
                print(f"PDF生成失败: {result.stderr.decode('utf-8')}")
                return None
                
        except subprocess.CalledProcessError as e:
            print(f"执行pandoc命令失败: {e}")
            print(f"错误输出: {e.stderr.decode('utf-8')}")
            return None
        except FileNotFoundError:
            print("未找到pandoc。请确保已安装pandoc和xelatex。")
            print("可以使用以下命令安装:")
            print("  brew install pandoc")
            print("  brew install basictex")
            print("  sudo tlmgr install xecjk ctex")
            return None
    
    def generate_pdf(self, translated_text, output_pdf_path):
        """生成PDF文件的主函数"""
        # 创建临时Markdown文件
        temp_md_path = os.path.join(self.temp_dir, "translated_temp.md")
        self.create_markdown(translated_text, temp_md_path)
        
        # 转换为PDF
        result = self.markdown_to_pdf(temp_md_path, output_pdf_path)
        
        # 清理临时文件
        if os.path.exists(temp_md_path):
            os.remove(temp_md_path)
            
        return result
