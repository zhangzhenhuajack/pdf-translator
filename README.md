# PDF-Translator

一个使用AWS Bedrock Nova Pro模型将PDF文档翻译成中文（或其他语言）的工具。

## 功能

- 从PDF文件中提取文本
- 使用AWS Bedrock的Nova Pro模型进行高质量翻译
- 生成保留原始格式的翻译PDF文件

## 安装

1. 克隆仓库:
```bash
git clone https://github.com/yourusername/pdf-translator.git
cd pdf-translator
```

2. 安装依赖:
```bash
pip install -r requirements.txt
```

3. 安装必要的系统工具:
```bash
# macOS
brew install pandoc
brew install basictex
export PATH=$PATH:/Library/TeX/texbin
sudo tlmgr update --self
sudo tlmgr install xecjk ctex

# Ubuntu/Debian
sudo apt-get install pandoc texlive-xetex texlive-lang-chinese
```

4. 配置AWS凭证:
```bash
aws configure
```

## 使用方法

基本用法:
```bash
python src/main.py input.pdf -o output_translated.pdf
```

指定目标语言:
```bash
python src/main.py input.pdf -o output_translated.pdf -t "中文"
```

使用自定义配置文件:
```bash
python src/main.py input.pdf -o output_translated.pdf -c my_config.yaml
```

## 配置

在`config/config.yaml`中可以修改以下配置:

- AWS区域和配置文件
- Bedrock模型ID
- PDF输出字体
- 临时文件目录

## 依赖

- Python 3.8+
- AWS账户和Bedrock访问权限
- pandoc
- XeLaTeX (通过basictex或texlive-xetex提供)
