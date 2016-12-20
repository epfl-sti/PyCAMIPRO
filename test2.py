def octal_to_decimal(number):
    i = 1
    decimal = 0
    while (number != 0):
        reminder = number % 10
        number /= 10
        decimal += reminder * i
        i *= 8
    return decimal

print octal_to_decimal(11)
