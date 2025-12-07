import io
from PIL import Image


class ImageQuantization:
    """
    Image Quantization
    Reduces the number of colors in an image to achieve compression.
    The user can specify the number of colors (2-256).
    
    Best for: Photos and images where quality loss is acceptable
    Trade-off: Fewer colors = smaller file but lower quality
    """

    @staticmethod
    def compress(image, colors=256):
        """
        Compress image through color quantization.
        Args:
            image: PIL Image object
            colors: Number of colors to reduce to (2-256)
            
        Returns:
            Quantized PIL Image object or None on error
        """
        try:
            if image.mode != "RGB":
                image = image.convert("RGB")

            # Quantize to reduce colors
            img_quantized = image.quantize(colors=min(colors, 256))
            return img_quantized
        except Exception as e:
            raise Exception(f"Error processing image: {str(e)}")

    @staticmethod
    def save_compressed_image(img_quantized, format="PNG"):
        """
        Save quantized image and return bytes.
        
        Args:
            img_quantized: Quantized PIL Image object
            format: Image format (PNG, JPEG, BMP, etc.)
            
        Returns:
            Image bytes or None on error
        """
        try:
            buffer = io.BytesIO()
            img_quantized.save(buffer, format=format)
            return buffer.getvalue()
        except Exception as e:
            raise Exception(f"Error saving image: {str(e)}")


