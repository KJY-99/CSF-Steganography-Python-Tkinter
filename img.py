import cv2, numpy as np

# Image resize function (Keep aspect ratio)
def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]
    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))
    resized = cv2.resize(image, dim, interpolation = inter)
    return resized

def to_bin(data):
    """Convert `data` to binary format as string"""
    if isinstance(data, str):
        return ''.join([ format(ord(i), "08b") for i in data ])
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [ format(i, "08b") for i in data ]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported.")

def encode(image_name, secret_data, bit_length):
    # Read image
    image = cv2.imread(image_name)
    # Height * Width * RGB (bytes)
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8
    # Stopping criteria
    secret_data += "====="
    # Check image data feasibility
    if len(secret_data) > n_bytes:
        raise ValueError("Need larger image or less data.")
    data_index = 0
    # Converts text data to binary
    binary_secret_data = to_bin(secret_data)
    data_len = len(binary_secret_data)
    for row in image:
        for pixel in row:
            # Convert pixel to binary
            r, g, b = to_bin(pixel)
            # Index last x elements of the pixel, append indexed secret data
            if data_index < data_len:
                pixel[0] = int(r[:-bit_length] + binary_secret_data[data_index:data_index + bit_length], 2)
                data_index += bit_length
            if data_index < data_len:
                pixel[1] = int(g[:-bit_length] + binary_secret_data[data_index:data_index + bit_length], 2)
                data_index += bit_length
            if data_index < data_len:
                pixel[2] = int(b[:-bit_length] + binary_secret_data[data_index:data_index + bit_length], 2)
                data_index += bit_length
            # Exit once all data is encoded
            if data_index >= data_len:
                break
        if data_index >= data_len:
            break
    return image

def decode(image_name, bit_length):
    # Read image
    image = cv2.imread(image_name)
    if image is None:
        raise ValueError("Image not found.")
    binary_data = ""
    for row in image:
        for pixel in row:
            r, g, b = to_bin(pixel)
            # Index last x elements (Bit length)
            binary_data += r[-bit_length:]
            binary_data += g[-bit_length:]
            binary_data += b[-bit_length:]
    # Split by 8 bits
    all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
    # Convert to characters
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        # Stopping criteria
        if decoded_data[-5:] == "=====":
            break
    return decoded_data[:-5]

input_image = "test.png"
output_image = "output.png"
secret_data = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi consectetur aliquet nibh. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Curabitur ultrices porta risus vitae mollis. Donec posuere maximus volutpat. Praesent vestibulum ipsum vel mi interdum, nec semper mauris vulputate. Phasellus efficitur ac est faucibus viverra. Cras id dapibus augue, non accumsan diam. Suspendisse ac orci interdum, porttitor mi a, malesuada nisl. Pellentesque iaculis consectetur elit, eu iaculis lectus efficitur a. Suspendisse finibus, nibh vel varius hendrerit, ex justo fringilla dui, in egestas tortor nulla vitae erat. Aliquam erat volutpat. Quisque bibendum, ante et ultricies viverra, lorem neque aliquet ex, sit amet rhoncus mi massa ac justo. Nulla euismod, magna vel vehicula viverra, urna diam tincidunt sem, at laoreet orci nunc a nisl."
# encode the data into the image
encoded_image = encode(image_name=input_image, secret_data=secret_data, bit_length=2)
# save the output image (encoded image)
cv2.imwrite(output_image, encoded_image)
# decode the secret data from the image
decoded_data = decode(output_image, 2)
print("Decoded data:", decoded_data)