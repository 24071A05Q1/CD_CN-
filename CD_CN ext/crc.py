def crc(data, poly):
    bits = list(data + "0" * (len(poly)-1))

    for i in range(len(data)):
        if bits[i] == '1':
            for j in range(len(poly)):
                bits[i+j] = str(int(bits[i+j]) ^ int(poly[j]))

    return ''.join(bits[-(len(poly)-1):])


def check(data, poly):
    bits = list(data)

    for i in range(len(data)-len(poly)+1):
        if bits[i] == '1':
            for j in range(len(poly)):
                bits[i+j] = str(int(bits[i+j]) ^ int(poly[j]))

    return "Error Detected" if '1' in bits else "No Error"


def hex_to_bin(data):
    return bin(int(data, 16))[2:]


print("1. CRC 12")
print("2. CRC 16")
print("3. CRC CCITT")

choice = int(input("Enter choice: "))

p = {
    1: "0x80F",    # CRC-12
    2: "0x8005",   # CRC-16
    3: "0x1021"    # CRC-CCITT
}

if choice in p:
    data = input("Enter  data: ")
    binary = data

    frame = binary + crc(binary, hex_to_bin(p[choice]))
    print("Transmitted Data:", frame)

    received = input("Enter received data : ")
    received = received

    print("Result:", check(received, hex_to_bin(p[choice])))

else:
    print("Invalid Choice")