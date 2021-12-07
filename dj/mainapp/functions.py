# https://www.nbrb.by/legislation/documents/p_440.pdf - IBAN Беларуси
# https://www.ibancalculator.com/iban_validieren.html - проверка

# FALSER BANK IBAN:
# BY-- FLSR ____ ____ ____ ____
#           |||  currecny.code
#              | account type

def make_iban(curr: str, acc_type: str, number: str) -> str:
    acc = curr + acc_type + number
    acc_numbers = ""
    for char in acc:
        num = ord(char)
        acc_numbers += str(num - 55) if num >= 65 else char
    control = 98 - (int("15212827" + acc_numbers + "113400") % 97)  # *FLSR* + acc_numbers + *BY00*
    return "BY" + "%02d" % control + "FLSR" + acc


def control_iban(iban: str) -> int:
    if iban[:2] != "BY":
        return True
    acc = iban[4:]
    acc_numbers = ""
    for char in acc:
        num = ord(char)
        acc_numbers += str(num - 55) if num >= 65 else char
    control = 98 - (int(acc_numbers + "113400") % 97)
    return control == int(iban[2:4])


def str_iban(iban: str) -> str:
    out = iban[:4] + ' ' + iban[4:8] + ' ' + iban[8:12] + ' ' + iban[12:]
    return out


def main():
    iban = make_iban("USD", "1", "000000000000")
    print(iban)
    print(str_iban(iban))
    print(control_iban(iban))


if __name__ == '__main__':
    main()
