class Util:

    @staticmethod
    def little_endian(value):
        """
        littleEndian(value)
        receives: a parsed, hex data piece
        outputs:  the decimal value of that data
        function: swaps byte by byte to convert little endian to big endian
        function: calls 2's compliment to convert to decimal
        returns:  The integer value

        :param value:
        :return:
        """
        length = len(value)  # gets the length of the data piece
        actual = ""
        for x in range(0, length / 2):  # go till you've reach the halway point
            actual += value[length - 2 - (2 * x):length - (2 * x)]  # flips all of the bytes (the last shall be first)
            x += 1
        intVal = Util.twosComp(actual)  # sends the data to be converted from 2's compliment to int
        return intVal  # returns the integer value

    @staticmethod
    def twos_comp(hex_value):
        """
        twosComp(hexValue)
        receives: the big endian hex value (correct format)
        outputs:  the decimal value of that data
        function: if the value is negative, swaps all bits
        up to but not including the rightmost 1.
        Else, just converts straight to decimal.
        (Flip all the bits left of the rightmost 1)
        returns:  the integer value
        """
        firstVal = int(hex_value[:1], 16)
        if firstVal >= 8:  # if first bit is 1
            bValue = bin(int(hex_value, 16))
            bValue = bValue[2:]  # removes 0b header
            newBinary = []
            length = len(bValue)
            index = bValue.rfind('1')  # find the rightmost 1
            for x in range(0, index + 1):  # swap bits up to rightmost 1
                if x == index:  # if at rightmost one, just append remaining bits
                    newBinary.append(bValue[index:])
                elif bValue[x:x + 1] == '1':
                    newBinary.append('0')
                elif bValue[x:x + 1] == '0':
                    newBinary.append('1')
                x += 1
            newBinary = ''.join(newBinary)  # converts char array to string
            finalVal = -int(newBinary, 2)  # converts to decimal
            return finalVal

        else:  # if not a negative number, simply convert to decimal
            return int(hex_value, 16)