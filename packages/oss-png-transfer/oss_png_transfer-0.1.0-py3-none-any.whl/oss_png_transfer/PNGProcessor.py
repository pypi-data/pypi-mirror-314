import zlib
import numpy as np
class PNGProcessor:
    def open_png(self, path):
        path = path

        try:
            with open(path, "rb") as file:
                raw_data = file.read()
        except FileNotFoundError:
            print(f"'{path}' was not found.")
            return
        except Exception as e:
            print(f"other error : {e}")
            return
            
        signature = raw_data[:8]
        #print("signature: ",signature)
        raw_data = raw_data[8:]
        if signature!=b'\x89PNG\r\n\x1a\n':
            print("not a valid PNG file.")
            return

        def decode_4(raw_data): 
            byte1 = raw_data[0] << 24
            byte2 = raw_data[1] << 16  
            byte3 = raw_data[2] << 8
            byte4 = raw_data[3]
            return int(byte1|byte2|byte3|byte4)

        chunks = []
        while raw_data:
            data_length = decode_4(raw_data[:4])
            chunk_type = raw_data[4:8] .decode("ascii")
            chunk_data = raw_data[8:8+data_length]
            crc = raw_data[8+data_length:12+data_length]

            chunks.append((chunk_type,chunk_data))

            raw_data = raw_data[12+data_length:]

        #for type, data in chunks:
        #    print("data_type  : ",type,"/ data_length: ",len(data))

        image_data = b""
        for type, data in chunks:
            if type=='IHDR':
                width = decode_4(data[0:4])
                height = decode_4(data[4:8])
                color_type = data[9]
                #print(f"Width: {width}, Height: {height}, Color Type: {color_type}")
            elif type == "IDAT":
                image_data += data

        if color_type !=0:
            print(f"PNG '{path}' 파일에서 문제가 발생했습니다.")
            print("그레이스케일(0)번 이외의 png 형식은 아직 구현되지 않았습니다.")
            print("버전 업데이트를 기다려주세요!")
            return
        if image_data==b"":
            print(f"PNG '{path}'IDAT 청크를 발견하지 못했습니다.")
            return

        try:
            decompressed_data = zlib.decompress(image_data)
        except:
            print("<zlib> Failed decompressed IDAT data.")
            return

        #print("LENGTH of decoded PNG:",len(decompressed_data))

        row_size = width+1

        pixels = []
        for y in range(height):
            row = []
            for x in range(width): 
                location = y*row_size + x + 1
                row.append(decompressed_data[location])
            pixels.append(row)

        return pixels
    
    def invert_image_colors(self, pixels):
        pixels = np.array(pixels)
        min_val = pixels.min()
        max_val = pixels.max()
        
        inverted_pixels = max_val - (pixels - min_val)
        return inverted_pixels.tolist()
