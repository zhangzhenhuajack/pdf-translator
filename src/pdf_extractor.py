import os
from PyPDF2 import PdfReader
from pdfminer.high_level import extract_text as pdfminer_extract_text

class PDFExtractor:
    """
    提取PDF文件中的文本内容
    """
    
    @staticmethod
    def extract_with_pypdf(pdf_path):
        """使用PyPDF2提取PDF文本"""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")
            
        text = ""
        try:
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        except Exception as e:
            print(f"PyPDF2提取失败: {e}")
            return None
            
        return text
    
    @staticmethod
    def extract_with_pdfminer(pdf_path):
        """使用pdfminer.six提取PDF文本"""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")
            
        try:
            text = pdfminer_extract_text(pdf_path)
            return text
        except Exception as e:
            print(f"PDFMiner提取失败: {e}")
            return None
    
    @staticmethod
    def extract_text(pdf_path):
        """
        尝试使用多种方法提取PDF文本，确保最佳结果
        """
        # 首先尝试使用PyPDF2
        text = PDFExtractor.extract_with_pypdf(pdf_path)
        
        # 如果PyPDF2提取的内容太少，尝试使用pdfminer
        if text is None or len(text.strip()) < 100:
            text = PDFExtractor.extract_with_pdfminer(pdf_path)
            
        return text
