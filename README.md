# PdfCompressor

Ghostscript로 PDF 내부 이미지의 DPI와 JPEG 압축 품질을 조정해 용량을 줄입니다.

```
python3 pdf_compressor.py input.pdf output.pdf --dpi 150 --quality 50
```

Ghostscript(`gs`)가 설치되어 있어야 합니다. 테스트: `python3 -m unittest`
