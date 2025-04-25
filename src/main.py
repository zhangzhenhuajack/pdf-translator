import os
import argparse
from pdf_extractor import PDFExtractor
from translator import BedrockTranslator
from pdf_generator import PDFGenerator

def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='PDF翻译工具 - 使用AWS Bedrock Nova Pro模型')
    parser.add_argument('input_pdf', help='输入PDF文件路径')
    parser.add_argument('--output', '-o', help='输出PDF文件路径')
    parser.add_argument('--config', '-c', default='config/config.yaml', help='配置文件路径')
    parser.add_argument('--target-lang', '-t', default='中文', help='目标语言')
    
    args = parser.parse_args()
    
    # 设置输出路径
    if not args.output:
        base_name = os.path.splitext(os.path.basename(args.input_pdf))[0]
        args.output = f"{base_name}_translated_CN.pdf"
    
    # 1. 提取PDF文本
    print(f"正在从 {args.input_pdf} 提取文本...")
    extractor = PDFExtractor()
    text = extractor.extract_text(args.input_pdf)
    
    if not text:
        print("无法提取PDF文本，请检查文件是否有效。")
        return
    
    print(f"成功提取 {len(text)} 字符的文本。")
    
    # 2. 翻译文本
    print(f"正在使用AWS Bedrock Nova Pro模型将文本翻译为{args.target_lang}...")
    translator = BedrockTranslator(args.config)
    translated_text = translator.translate_large_text(text, target_language=args.target_lang)
    
    if not translated_text:
        print("翻译失败，请检查AWS凭证和网络连接。")
        return
    
    print("翻译完成！")
    
    # 3. 生成PDF
    print(f"正在生成翻译后的PDF: {args.output}")
    generator = PDFGenerator(args.config)
    result = generator.generate_pdf(translated_text, args.output)
    
    if result:
        print(f"PDF生成成功: {args.output}")
    else:
        print("PDF生成失败。")

if __name__ == "__main__":
    main()
