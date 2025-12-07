from collections import Counter
import heapq
import math



# ============================================================================
# Run-Length Encoding (RLE)
# ============================================================================

class RunLengthEncoding:
    """
    Run Length Encoding (RLE) - Lossless data compression technique.
    
    How it Works:
    Instead of storing every single element, we store:
    - The count (number of times a character repeats)
    - The character itself
    
    Example: AAAABBBCCDAA -> 4A3B2C1D2A
    """
    
    def encode(self, data: str) -> str:
        """
        Encode text using Run-Length Encoding
        Format: count + character pairs (e.g., "4A3B2C1D2A")
        
        Args:
            data (str): Input text to encode
            
        Returns:
            str: Encoded string as count-character pairs
        """
        if not data:  # handle empty input
            return ""
        
        encoded = ""
        count = 1
        
        # Process each character
        for i in range(1, len(data)):
            if data[i] == data[i - 1]:
                # Same character, increment count
                count += 1
            else:
                # Different character, store previous run
                encoded += str(count) + data[i - 1]
                count = 1
        
        # Add the last run
        encoded += str(count) + data[-1]
        
        return encoded
    
    def decode(self, encoded: str) -> str:
        """
        Decode RLE encoded text back to original
        
        Args:
            encoded (str): Encoded text (count-character pairs)
            
        Returns:
            str: Decoded original text
        """
        decoded = ""
        count = ""
        
        # Process each character in encoded string
        for char in encoded:
            if char.isdigit():
                # Accumulate digits (for multi-digit counts)
                count += char
            else:
                # Found a character, repeat it count times
                decoded += char * int(count)
                count = ""
        
        return decoded
    
    def compress(self, text: str):
        """
        Compress text and return statistics
        
        Args:
            text (str): Input text
            
        Returns:
            tuple: (encoded_text, decoded_text, original_size, encoded_size)
        """
        encoded = self.encode(text)
        decoded = self.decode(encoded)
        return encoded, decoded, len(text), len(encoded)
    



# ============================================================================
# Huffman Coding
# ============================================================================

class HuffmanCoding:
    """
    Huffman Coding implementation for lossless compression.
    
    This class provides methods to compress text using Huffman coding algorithm,
    which creates variable-length codes for different characters based on their
    frequency in the input text.
    """
    
    def __init__(self):
        """Initialize Huffman Coding with empty codes dictionary"""
        self.codes = {}
        
    def build_frequency(self, text):
        """
        Build frequency counter for characters in text
        Args:
            text (str): Input text to analyze
        Returns:
            Counter: Dictionary-like object with character frequencies
        """
        return Counter(text)
    
    def build_heap(self, freq):
        """
        Build min heap from frequency dictionary
        Args:
            freq (Counter): Character frequency counter
        Returns:
            list: Min heap structure
        """
        heap = [[weight, [char, ""]] for char, weight in freq.items()]
        # Rearranges the list in ascending order
        heapq.heapify(heap)
        return heap
    
    def build_codes(self, heap):
        """
        Build Huffman codes from heap
        Args:
            heap (list): Min heap structure            
        Returns:
            dict: Dictionary mapping characters to their Huffman codes
        """
        while len(heap) > 1:
            smallest = heapq.heappop(heap)  # smallest
            secsmallest = heapq.heappop(heap)  # second smallest
            
            for pair in smallest[1:]:
                pair[1] = "0" + pair[1]  # left branch → add 0
            
            for pair in secsmallest[1:]:
                pair[1] = "1" + pair[1]  # right branch → add 1
            
            # The combined frequency.
            # Combine the list of character–code pairs
            heapq.heappush(heap, [smallest[0] + secsmallest[0]] + smallest[1:] + secsmallest[1:])
        
        # End of building Huffman codes, the heap contains only one element
        return dict(heap[0][1:])
    
    def huffman_encode(self, text, codes):
        """
        Encode text using Huffman codes
        
        Args:
            text (str): Text to encode
            codes (dict): Dictionary mapping characters to their Huffman codes
            
        Returns:
            str: Encoded binary string
        """
        # Join code for each character of text to produce code
        return "".join(codes[ch] for ch in text)
    
    def compress(self, text):
        """
        Compress text using Huffman coding
        
        Args:
            text (str): Input text to compress
            
        Returns:
            tuple: (encoded_binary, codes_dict, frequency_counter)
        """
        # Step 1: Build frequency
        freq = self.build_frequency(text)
        
        # Step 2: Build heap
        heap = self.build_heap(freq)
        
        # Step 3: Build codes
        self.codes = self.build_codes(heap)
        
        # Step 4: Encode
        encoded = self.huffman_encode(text, self.codes)
        
        return encoded, self.codes, freq
    
    def decode(self, encoded_binary, codes):
        """
        Decode Huffman encoded binary string back to original text
        
        Args:
            encoded_binary (str): Binary string to decode
            codes (dict): Dictionary mapping characters to their Huffman codes
            
        Returns:
            str: Decoded original text
        """
        # Reverse the codes dictionary: code -> character
        reverse_codes = {code: char for char, code in codes.items()}
        
        decoded_text = ""
        current_code = ""
        
        # Process each bit in the encoded binary
        for bit in encoded_binary:
            current_code += bit
            # Check if current code matches any Huffman code
            if current_code in reverse_codes:
                decoded_text += reverse_codes[current_code]
                current_code = ""  # Reset for next character
        
        return decoded_text
    



# ============================================================================
# Golomb Coding
# ============================================================================

class GolombCoding:
    """
    Golomb Code - Lossless compression.
    
    Parameters in Golomb code:
    - n => integer you want to encode.
    - m => fixed positive integer that controls how numbers are split into quotient and remainder
    
    How to implement Golomb:
    - Quotient -> unary code (ones followed by zero)
    - Remainder -> binary code
    """
    
    def unary_encode(self, q: int) -> str:
        """
        Encode quotient q in unary (q ones followed by a zero).
        
        Args:
            q (int): Quotient value
            
        Returns:
            str: Unary encoded string
        """
        return "1" * q + "0"
    
    def encode(self, n: int, m: int) -> str:
        """
        Encode an integer n using Golomb coding with parameter m.
        
        Args:
            n (int): Number to encode
            m (int): Golomb parameter
            
        Returns:
            str: Codeword as a string of bits
        """
        # Step 1: divide n by m
        q = n // m
        r = n % m
        
        # Step 2: encode quotient in unary
        quotient_code = self.unary_encode(q)
        
        # Step 3: encode remainder
        # m=8=1000 \ m-1=7=0111 \ m&m-1= 1000&0111= 0000
        if (m & (m - 1)) == 0:
            # Case A: m is a power of 2
            k = int(math.log2(m))
            remainder_code = format(r, f'0{k}b')  # fixed-length binary
        else:
            # Case B: m is not a power of 2 → truncated binary
            b = math.ceil(math.log2(m))
            T = 2**b - m
            if r < T:
                remainder_code = format(r, f'0{b-1}b')
            else:
                remainder_code = format(r + T, f'0{b}b')
        
        # Step 4: final codeword
        return quotient_code + remainder_code
    
    def decode(self, codeword: str, m: int) -> int:
        """
        Decode a Golomb codeword back to the original integer
        Args:
            codeword (str): Binary codeword string
            m (int): Golomb parameter (must match encoding parameter)            
        Returns:
            int: Decoded integer value
        """
        # Step 1: Extract quotient from unary code (count ones before the first zero)
        q = 0
        pos = 0
        while pos < len(codeword) and codeword[pos] == '1':
            q += 1
            pos += 1
        
        # Skip the zero separator
        pos += 1
        
        # Step 2: Extract remainder from binary code
        if (m & (m - 1)) == 0:
            # Case A: m is a power of 2
            k = int(math.log2(m))
            remainder_bits = codeword[pos:pos + k]
            r = int(remainder_bits, 2) if remainder_bits else 0
        else:
            # Case B: m is not a power of 2 → truncated binary
            b = math.ceil(math.log2(m))
            T = 2**b - m
            
            # Try reading b-1 bits first
            if pos + b - 1 <= len(codeword):
                remainder_bits = codeword[pos:pos + b - 1]
                r_temp = int(remainder_bits, 2) if remainder_bits else 0
                
                if r_temp < T:
                    r = r_temp
                else:
                    # Need to read b bits instead
                    remainder_bits = codeword[pos:pos + b]
                    r = int(remainder_bits, 2) - T if remainder_bits else 0
            else:
                r = 0
        
        # Step 3: Reconstruct n from quotient and remainder
        n = q * m + r
        return n
    
    def compress(self, numbers: list, m: int):
        """
        Compress a list of numbers using Golomb coding
        Args:
            numbers (list): List of integers to encode
            m (int): Golomb parameter
        Returns:
            list: List of (number, codeword) tuples
        """
        results = []
        for n in numbers:
            codeword = self.encode(n, m)
            results.append((n, codeword))
        return results
    



# ============================================================================
# LZW Coding (Dictionary-based)
# ============================================================================

class LZWCoding:
    """
    LZW Coding (Dictionary based) - Lossless data compression algorithm.
    
    LZW compresses data by:
    - Building a dictionary of sequences of characters (or bytes).
    - Replacing repeated sequences in the data with shorter codes that
    refer to dictionary entries.
    """
    
    def encode(self, text):
        """
        LZW encoding algorithm
        Args:
            text (str): Input text to encode
        Returns:
            tuple: (list of codes, dictionary used)
        """
        # Step 1: Initialize dictionary with all single characters (ASCII 0–255)
        dictionary = {}
        for i in range(256):
            dictionary[chr(i)] = i  # map character to its ASCII code
        
        next_code = 256  # next available dictionary code
        current_c = ""  # current sequence
        result = []  # list of output codes
        
        # Step 2: Loop through each character in the input text
        for next_n in text:
            combined = current_c + next_n  # combine current sequence with the next char
            
            if combined in dictionary:
                # if the combined sequence exists, make it the new current sequence
                current_c = combined
            else:
                # output the code for the current sequence
                result.append(dictionary[current_c])
                # add the new sequence to the dictionary
                dictionary[combined] = next_code
                next_code += 1
                # reset current sequence to the new character
                current_c = next_n
        
        # Step 3: Output the code for the last sequence
        if current_c != "":
            result.append(dictionary[current_c])
        
        return result, dictionary
    
    def decode(self, codes, initial_dict_size=256):
        """
        LZW decoding algorithm
        This function takes the encoded codes and reconstructs the original text.
        Args:
            codes (list): List of integer codes from encoding
            initial_dict_size (int): Initial dictionary size (default 256 for ASCII)
        Returns:
            str: Reconstructed text string
        """
        # Step 1: Initialize reverse dictionary (code -> string)
        dictionary = {i: chr(i) for i in range(initial_dict_size)}
        
        next_code = initial_dict_size
        
        # Step 2: Get first code
        if not codes:
            return ""
        
        current_code = codes[0]
        decoded_text = dictionary[current_code]
        previous_string = decoded_text
        
        # Step 3: Process remaining codes
        for code in codes[1:]:
            if code in dictionary:
                # Code exists in dictionary
                current_string = dictionary[code]
            elif code == next_code:
                # Special case: code not in dictionary yet
                current_string = previous_string + previous_string[0]
            else:
                raise ValueError(f"Invalid code: {code}")
            
            # Output the string for this code
            decoded_text += current_string
            
            # Add new entry to dictionary
            dictionary[next_code] = previous_string + current_string[0]
            next_code += 1
            
            # Update previous string
            previous_string = current_string
        
        return decoded_text
    
    def compress(self, text):
        """
        Compress text using LZW coding
        
        Args:
            text (str): Input text to compress
            
        Returns:
            tuple: (codes, dictionary, decoded_text)
        """
        codes, dict_used = self.encode(text)
        decoded_text = self.decode(codes)
        return codes, dict_used, decoded_text
    

