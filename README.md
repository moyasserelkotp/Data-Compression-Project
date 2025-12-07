# Data Compression Application

A clean, modular data compression tool with lossless and lossy compression algorithms.

## Features

- **Lossless Compression**: RLE, Huffman, Golomb, LZW
- **Lossy Compression**: Image Quantization
- **Streamlit GUI**: Easy-to-use web interface
- **Performance Metrics**: Real-time compression statistics

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

Open http://localhost:8501 in your browser.

## How to Use

### Text/File Compression (Lossless)
1. Select "Lossless Compression" in sidebar
2. Choose algorithm (RLE, Huffman, Golomb, or LZW)
3. Upload a file
4. Click "Compress" to compress
5. Click "Decompress" to verify
6. Click "Download" to save

### Image Compression (Lossy)
1. Select "Lossy Compression (Images)" in sidebar
2. Upload an image (PNG, JPG, BMP, etc.)
3. Adjust color slider (2-256 colors)
4. Click "Compress"
5. View comparison and download

## Supported Formats

**Lossless**: txt, pdf, doc, docx, py, java, cpp, bin, log, csv, json  
**Lossy**: png, jpg, jpeg, bmp, gif, webp

## Algorithms

| Algorithm | Type | Best For | Complexity |
|-----------|------|----------|-----------|
| RLE | Lossless | Repetitive data | O(n) |
| Huffman | Lossless | General text | O(n log n) |
| Golomb | Lossless | Small numbers | O(n) |
| LZW | Lossless | Patterns | O(n) |
| Quantization | Lossy | Images | O(n) |

## Project Structure

```
compression/          - Compression algorithms package
├── __init__.py      - Package exports
├── lossless.py      - RLE, Huffman, Golomb, LZW
├── lossy.py         - Image Quantization
└── utils.py         - Helper functions

app.py                - Streamlit application
requirements.txt      - Dependencies
sample.txt           - Test file for compression
```

## Testing Sample File

Use `sample.txt` for testing compression. When downloading decompressed files, they will have algorithm name in filename.

## All Algorithms Implemented from Scratch

All compression algorithms are implemented from scratch without external compression libraries, providing a deep understanding of how each technique works.

---
##  deployment 

url: https://data-compression-project-fuxsjqhmyt3jfwgnwdqyka.streamlit.app/

---


**Status**: Production Ready ✓  
**Last Updated**: November 27, 2025
