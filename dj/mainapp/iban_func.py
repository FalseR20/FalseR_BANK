# https://www.nbrb.by/legislation/documents/p_440.pdf - IBAN Беларуси
# https://bank.codes/iban/validate/ - проверка

# FALSER BANK IBAN:
# BY-- FLSR ____ ____ ____ ____
#           |    account type
#            ||| currecny.code

def make_iban(type_and_curr: str, number: str) -> str:
    acc = type_and_curr + number
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


if __name__ == '__main__':
    main()
