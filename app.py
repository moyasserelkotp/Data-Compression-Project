import streamlit as st
import time
from PIL import Image

# Import compression modules
from compression import (
    RunLengthEncoding,
    HuffmanCoding,
    GolombCoding,
    LZWCoding,
    ImageQuantization,
)


# ==================== TECHNIQUES INFO ====================

# Compression technique descriptions
TECHNIQUES_INFO = {
    "RLE": "🔁 **Run-Length Encoding**: Compresses repeated sequences into count-value pairs. Best for: Repetitive data",
    "Huffman": "📊 **Huffman Coding**: Generates optimal prefix-free codes based on symbol frequency. Best for: General purpose",
    "Golomb": "📐 **Golomb Coding**: Parameterized coding optimized for geometric distributions. Best for: Small numbers",
    "LZW": "📚 **LZW Coding**: Dictionary-based algorithm replacing patterns with indices. Best for: Text & mixed data",
    "Quantization": "🎨 **Image Quantization**: Reduces colors in images for compression. Best for: Photos",
}


# ==================== PAGE CONFIGURATION ====================

st.set_page_config(
    page_title="Data Compression Project",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title and description
st.title("📊 Data Compression Project")
st.markdown(
    """
A comprehensive Data Compression Application that provides both **lossless** and **lossy** compression options 
through an intuitive GUI. All techniques are implemented from scratch for deeper algorithmic understanding.
"""
)

# ==================== SESSION STATE INITIALIZATION ====================

if "compressed_data" not in st.session_state:
    st.session_state.compressed_data = None
    st.session_state.huffman_codes = None
    st.session_state.lzw_codes = None
    st.session_state.golomb_m = None
    st.session_state.golomb_codewords = None
    st.session_state.original_size = None
    st.session_state.compress_time = None
    st.session_state.decompress_time = None
    st.session_state.decompressed_data = None
    st.session_state.technique_used = None
    st.session_state.original_image = None
    st.session_state.quantized_image = None


# ==================== SIDEBAR SETTINGS ====================

st.sidebar.header("⚙️ Settings")
st.sidebar.markdown("---")

mode = st.sidebar.radio(
    "📌 Select Compression Mode:",
    ["Lossless Compression", "Lossy Compression (Images)"],
    help="Choose between text/file compression or image compression",
)

if mode == "Lossless Compression":
    technique = st.sidebar.selectbox(
        "🔧 Select Technique:",
        ["RLE", "Huffman", "Golomb", "LZW"],
        help="Select compression algorithm",
    )
else:
    technique = "Quantization"

st.session_state.technique_used = technique

st.sidebar.info(TECHNIQUES_INFO.get(technique, ""))

if mode == "Lossless Compression":
    st.sidebar.markdown("### 💡 Lossless Techniques")
    st.sidebar.write(
        """
    - **RLE**: Count-value pairs
    - **Huffman**: Optimal codes
    - **Golomb**: Geometric dist.
    - **LZW**: Dictionary-based
    """
    )
else:
    st.sidebar.markdown("### 💡 Lossy Techniques")
    st.sidebar.write(
        """
    - **Quantization**: Color reduction
    """
    )

st.sidebar.markdown("---")

# ==================== MAIN CONTENT ====================

st.divider()

# ==================== FILE UPLOAD ====================

st.subheader("📁 Step 1: Upload File")

if mode == "Lossless Compression":
    uploaded_file = st.file_uploader(
        "Choose a text or data file to compress",
        type=["txt", "pdf", "py", "java", "csv", "json", "bin"],
        help="Select a file for lossless compression",
    )
else:
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=["png", "jpg", "jpeg", "bmp", "gif", "webp"],
        help="Select an image for lossy compression",
    )

if uploaded_file:
    st.success(
        f" File selected: **{uploaded_file.name}** | Size: **{uploaded_file.size:,}** bytes"
    )


# ==================== COMPRESSION SETTINGS ====================

if mode == "Lossy Compression (Images)" and uploaded_file:
    st.subheader("🎨 Step 2: Quantization Settings")
    col1, col2 = st.columns([2, 1])

    with col1:
        colors = st.slider(
            "Number of Colors:",
            min_value=2,
            max_value=256,
            value=128,
            step=1,
            help="Fewer colors = smaller file but lower quality",
        )
    with col2:
        st.info(f"📊 Colors: {colors}")


# ==================== COMPRESSION & DECOMPRESSION ====================

st.subheader("🔄 Step 3: Compress & Decompress")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    compress_btn = st.button(
        "🔴 Compress", key="compress_btn", width='stretch'
    )

with col2:
    decompress_btn = st.button(
        "🔵 Decompress", key="decompress_btn", width='stretch'
    )

with col3:
    download_btn = st.button(
        "💾 Download", key="download_btn", width='stretch'
    )


# ==================== COMPRESSION LOGIC ====================

if compress_btn:
    if uploaded_file is None:
        st.error(" Please select a file first!")
    else:
        with st.spinner("⏳ Compressing..."):
            try:
                start_time = time.time()

                if mode == "Lossless Compression":
                    data = uploaded_file.read()
                    st.session_state.original_data = data
                    st.session_state.original_size = len(data)

                    if technique == "RLE":
                        # RLE compression using RunLengthEncoding class
                        text = data.decode('utf-8', errors='ignore').strip()
                        rle = RunLengthEncoding()
                        encoded = rle.encode(text)
                        st.session_state.compressed_data = encoded.encode('utf-8')

                    elif technique == "Huffman":
                        # Huffman works with strings
                        text = data.decode('utf-8', errors='ignore')
                        huffman = HuffmanCoding()
                        encoded, codes, freq = huffman.compress(text)
                        st.session_state.compressed_data = encoded.encode('utf-8')
                        st.session_state.huffman_codes = codes

                    elif technique == "Golomb":
                        # Golomb works with numbers (byte values)
                        golomb = GolombCoding()
                        
                        # Convert data to list of byte values
                        numbers = list(data)
                        
                        # Calculate optimal m parameter based on data statistics
                        # m should be around the average value for best compression
                        avg_value = sum(numbers) / len(numbers) if numbers else 1
                        m_param = max(2, int(avg_value))  # m must be >= 2, use average as estimate
                        
                        # Compress using Golomb coding
                        results = golomb.compress(numbers, m=m_param)
                        
                        # Store codewords and parameters for decompression
                        codewords = [codeword for _, codeword in results]
                        st.session_state.compressed_data = " ".join(codewords).encode('utf-8')
                        st.session_state.golomb_m = m_param
                        st.session_state.golomb_codewords = codewords

                    elif technique == "LZW":
                        # LZW works with strings
                        text = data.decode('utf-8', errors='ignore')
                        lzw = LZWCoding()
                        codes, dictionary, decoded = lzw.compress(text)
                        # Store codes as space-separated string
                        st.session_state.compressed_data = " ".join(str(c) for c in codes).encode('utf-8')
                        st.session_state.lzw_codes = codes  # Store original codes for decompression

                else:  # Lossy Compression
                    try:
                        image = Image.open(uploaded_file)
                        st.session_state.original_image = image.copy()
                        st.session_state.original_size = len(uploaded_file.getvalue())

                        img_quantized = ImageQuantization.compress(image, colors)
                        if img_quantized:
                            st.session_state.quantized_image = img_quantized
                            st.session_state.compressed_data = (
                                ImageQuantization.save_compressed_image(img_quantized)
                            )
                        else:
                            st.error("Failed to compress image")
                    except Exception as e:
                        st.error(f"Error opening image: {str(e)}")

                st.session_state.compress_time = time.time() - start_time
                st.success(
                    f"Compression completed in **{st.session_state.compress_time:.4f}** seconds!"
                )
                
                # Show algorithm explanation
                st.markdown("---")

            except Exception as e:
                st.error(f"Compression Error: {str(e)}")

# ==================== DECOMPRESSION LOGIC ====================

if decompress_btn:
    if st.session_state.compressed_data is None:
        st.error(" Please compress a file first!")
    else:
        if mode == "Lossy Compression (Images)":
            st.error(
                " Cannot decompress lossy compression (lossy data is permanently removed)"
            )
        else:
            with st.spinner("⏳ Decompressing..."):
                try:
                    start_time = time.time()

                    if technique == "RLE":
                        # RLE decompression using RunLengthEncoding class
                        encoded_text = st.session_state.compressed_data.decode('utf-8')
                        rle = RunLengthEncoding()
                        decoded = rle.decode(encoded_text)
                        st.session_state.decompressed_data = decoded.encode('utf-8')

                    elif technique == "Huffman":
                        if st.session_state.huffman_codes is None:
                            st.error(" Huffman codes not available!")
                        else:
                            huffman = HuffmanCoding()
                            encoded_binary = st.session_state.compressed_data.decode('utf-8')
                            decoded_text = huffman.decode(encoded_binary, st.session_state.huffman_codes)
                            st.session_state.decompressed_data = decoded_text.encode('utf-8')

                    elif technique == "Golomb":
                        if st.session_state.golomb_m is None or st.session_state.golomb_codewords is None:
                            st.error(" Golomb parameters not available!")
                        else:
                            golomb = GolombCoding()
                            m = st.session_state.golomb_m
                            codewords = st.session_state.golomb_codewords
                            # Decode each codeword back to number
                            decoded_numbers = [golomb.decode(codeword, m) for codeword in codewords]
                            
                            # Convert numbers back to bytes
                            decoded_bytes = bytes(decoded_numbers)
                            st.session_state.decompressed_data = decoded_bytes

                    elif technique == "LZW":
                        if hasattr(st.session_state, 'lzw_codes') and st.session_state.lzw_codes:
                            lzw = LZWCoding()
                            decoded_text = lzw.decode(st.session_state.lzw_codes)
                            st.session_state.decompressed_data = decoded_text.encode('utf-8')
                        else:
                            st.error(" LZW codes not available for decompression!")

                    st.session_state.decompress_time = time.time() - start_time
                    st.success(
                        f" Decompression completed in **{st.session_state.decompress_time:.4f}** seconds!"
                    )

                except Exception as e:
                    st.error(f" Decompression Error: {str(e)}")


# ==================== DOWNLOAD LOGIC ====================

if download_btn:
    if st.session_state.compressed_data is None:
        st.error(" Please compress a file first!")
    else:
        st.markdown("---")
        st.markdown("## 📥 Download Your Files")
        
        col1, col2 = st.columns(2)
        
        # Download compressed file
        with col1:
            st.markdown("### 🔴 Compressed File")
            st.markdown("""
            **Readable text format** - Shows compression output as numbers or text!
            """)
            
            # Convert compressed data to readable format for download
            if technique == "RLE":
                readable_compressed = st.session_state.compressed_data
            
            elif technique == "Huffman":
                # Huffman compressed data is a binary string 
                readable_compressed = st.session_state.compressed_data
            
            elif technique == "LZW":
                # LZW is already stored as space-separated codes 
                readable_compressed = st.session_state.compressed_data
            
            else:
                # Format other algorithms as space-separated numbers
                if technique == "Golomb":
                    readable_compressed = st.session_state.compressed_data
                else:
                    compressed_bytes = list(st.session_state.compressed_data)
                    readable_compressed = " ".join(str(b) for b in compressed_bytes).encode('utf-8')
            
            compressed_filename = f"compressed_{technique}_{int(time.time())}.txt"
            st.download_button(
                label="📦 Download Compressed",
                data=readable_compressed,
                file_name=compressed_filename,
                mime="text/plain",
                width='stretch',
            )
            st.caption(f"Size: {len(readable_compressed):,} bytes (readable format)")
            

        
        # Download decompressed file (if available)
        with col2:
            st.markdown("### 🟢 Decompressed File")
            if st.session_state.decompressed_data is not None:
                st.markdown("""
                **Text/Original data** - This is the decompressed version.
                It should match your original file exactly!
                """)
                decompressed_filename = f"sample_{technique}_{int(time.time())}.txt"
                st.download_button(
                    label="📄 Download Decompressed",
                    data=st.session_state.decompressed_data,
                    file_name=decompressed_filename,
                    mime="text/plain",
                    width='stretch',
                )
                st.caption(f"Size: {len(st.session_state.decompressed_data):,} bytes")
            else:
                st.info("💡 Click 'Decompress' button to generate decompressed file")
        
        st.markdown("---")
        st.success(" Both files available for download!")


# ==================== RESULTS SECTION ====================

if st.session_state.compressed_data is not None and st.session_state.original_size is not None:
    st.divider()
    st.subheader("📊 Step 4: Results & Analysis")

    import math

    # Calculate ACTUAL binary compressed size for metrics (bits → bytes)
    if technique == "RLE":
        # RLE binary format: each run = 1 byte (count) + 1 byte (char) = 2 bytes
        num_runs = len(st.session_state.compressed_data) // 2
        compressed_size = num_runs * 2  # bytes

    elif technique == "LZW":
        # LZW: calculate actual bits needed based on maximum code value
        codes = st.session_state.lzw_codes if hasattr(st.session_state, 'lzw_codes') and st.session_state.lzw_codes else []
        if codes:
            max_code = max(codes)
            bits_per_code = math.ceil(math.log2(max_code + 1))  # bits needed to represent max code
            total_bits = len(codes) * bits_per_code
            compressed_size = math.ceil(total_bits / 8)  # convert bits to bytes (round up)
        else:
            compressed_size = len(st.session_state.compressed_data)

    elif technique == "Huffman":
        # Huffman: binary string length in bits → bytes
        if isinstance(st.session_state.compressed_data, bytes):
            binary_string = st.session_state.compressed_data.decode('utf-8', errors='ignore')
            total_bits = len(binary_string)  # each character is a bit ('0' or '1')
            compressed_size = math.ceil(total_bits / 8)  # convert to bytes
        else:
            compressed_size = len(st.session_state.compressed_data)

    elif technique == "Golomb":
        # Golomb: sum up all codeword bit lengths
        if hasattr(st.session_state, 'golomb_codewords') and st.session_state.golomb_codewords:
            total_bits = sum(len(codeword) for codeword in st.session_state.golomb_codewords)
            compressed_size = math.ceil(total_bits / 8)  # convert to bytes
        else:
            compressed_size = len(st.session_state.compressed_data)

    else:
        # For lossy compression (images), use actual byte size
        compressed_size = len(st.session_state.compressed_data)

    original_size = st.session_state.original_size
    size_reduction = original_size - compressed_size
    compression_ratio = (
        (size_reduction / original_size * 100) if original_size > 0 else 0
    )

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📦 Original Size", f"{original_size:,} B", f"{original_size / 1024:.2f} KB"
        )

    with col2:
        st.metric(
            "🗜️ Compressed Size",
            f"{compressed_size:,} B",
            f"{compressed_size / 1024:.2f} KB",
        )

    with col3:
        st.metric(
            "📉 Compression Ratio",
            f"{compression_ratio:.2f}%",
            f"Saved {size_reduction:,} B",
        )

    with col4:
        st.metric("⏱️ Compression Time", f"{st.session_state.compress_time:.4f}s")

    # Detailed Statistics Table
    st.markdown("### 📋 Detailed Statistics")
    stats_data = {
        "Metric": [
            "Original Size",
            "Compressed Size",
            "Size Reduction",
            "Compression Ratio",
            "Compression Time",
            "Decompression Time",
            "Technique Used",
            "Compression Type",
        ],
        "Value": [
            f"{original_size:,} bytes ({original_size / 1024:.2f} KB)",
            f"{compressed_size:,} bytes ({compressed_size / 1024:.2f} KB)",
            f"{size_reduction:,} bytes",
            f"{compression_ratio:.2f}%",
            f"{st.session_state.compress_time:.4f} seconds",
            (
                f"{st.session_state.decompress_time:.4f} seconds"
                if st.session_state.decompress_time
                else "Pending"
            ),
            technique,
            "Lossless" if mode == "Lossless Compression" else "Lossy",
        ],
    }
    st.table(stats_data)

    # Image Preview for lossy
    if mode == "Lossy Compression (Images)":
        st.markdown("### 🖼️ Image Comparison")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Original Image")
            if st.session_state.original_image:
                st.image(st.session_state.original_image, width='stretch')

        with col2:
            # Use colors from session state or default to 128 if not defined
            display_colors = colors if 'colors' in locals() else 128
            st.subheader(f"Quantized Image ({display_colors} colors)")
            if st.session_state.quantized_image:
                st.image(st.session_state.quantized_image, width='stretch')


# ==================== FOOTER ====================

st.divider()
st.sidebar.markdown("---")
st.sidebar.success(
    """
    ✅ **Application Ready!**
    
    📌 Steps:
    1. Select mode & technique
    2. Upload file/image
    3. Click Compress
    4. View results
    5. Download if needed
    
    **Supported Formats:**
    - Lossless: txt, pdf, doc, py, java, csv, json, bin
    - Lossy: png, jpg, jpeg, bmp, gif, webp
"""
)
