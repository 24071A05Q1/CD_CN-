print("1. Character Count")
print("2. Character Stuffing")
print("3. Bit Stuffing")

choice = int(input("Enter your choice: "))
data = input("Enter data: ")

if choice == 1:
    words = data.split()

    print("Transmitted Frames:")
    for word in words:
        print(len(word), word)

    print("Received Frames:")
    for word in words:
        print(word)

elif choice == 2:
    flag = 'Flag'
    esc = 'Esc'
    result = flag + " "

    data1 = data.split()

    for ch in data1:
        if ch == flag or ch == esc:
            result += esc + " "
        result += ch + " "

    result += flag + " "

    print("Stuffed Data:", result)
    print("Transmitted Frame:", result)

# Destuffing
    received = result.split()[1:-1]
    original = []
    i = 0

    while i < len(received):
       if received[i] == esc:
           i += 1
       original.append(received[i])
    i += 1

    print("Received Frame:", " ".join(original))

elif choice == 3:
    result = ""
    count = 0

    # Bit Stuffing
    for bit in data:
        result += bit

        if bit == '1':
            count += 1
            if count == 5:
                result += '0'
                count = 0
        else:
            count = 0

    print("Stuffed Data:", result)
    print("Transmitted Frame:", result)

    # Bit Destuffing
    received = ""
    count = 0
    i = 0

    while i < len(result):
        bit = result[i]
        received += bit

        if bit == '1':
            count += 1
            if count == 5:
                i += 1
                count = 0
        else:
            count = 0

        i += 1

    print("Received Frame:", received)

else:
    print("Invalid Choice")