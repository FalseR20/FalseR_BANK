def delete_nulls(iban: str) -> str:
    while iban[0] == "0":
        iban = iban[1:]
    return iban

def iban_control_int(iban: str) -> int:
    # https://expert.chistov.pro/public/1105804/ - описание формулы
    # https://www.ibancalculator.com/iban_validieren.html - проверка
    iban = iban[4:] + iban[:2] + "00"
    new_iban = ""
    for char in iban:
        num = ord(char) - 55
        if num >= 10:
            new_iban += str(num)
        else:
            new_iban += char

    print("IBAN:", new_iban)

    num, new_iban = int(new_iban[:9]), new_iban[9:]
    n = num % 97
    print(n, num, new_iban)
    while new_iban:
        if len(new_iban) <= 7:
            num = int(str(n) + delete_nulls(new_iban))
            new_iban = ""
        else:
            num = int(str(n) + delete_nulls(new_iban[:7]))
            new_iban = new_iban[7:]
        n = num % 97
        print(n, num, new_iban)
    return n


print(iban_control_int("BY20OLMP31350000001000000933"))
