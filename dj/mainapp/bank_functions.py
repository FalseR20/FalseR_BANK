# https://www.nbrb.by/legislation/documents/p_440.pdf - IBAN Беларуси
# https://bank.codes/iban/validate/ - проверка

# FALSER BANK IBAN:
# BY-- FLSR ____ ____ ____ ____
#           |    account type (1 - debit)
#            ||| currency.code

# FALSER BANK CARD
# -238 14-- ---- ---
# |  pay system
#    control digit |

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


def make_card(numbers15: str) -> int:
    sum_ = 0
    for i in range(0, 15):
        z = ord(numbers15[i]) - 48
        if i % 2:
            sum_ += z
        else:
            z *= 2
            sum_ += z % 10 + z // 10
    return int(f"{numbers15}{-sum_ % 10}")


def control_card(number: int):
    return number == make_card(str(number)[:-1])


if __name__ == '__main__':
    # print(make_iban('1BYN', '00000000000'))
    card = make_card('456126121234546')
    print(card)
    print(control_card(card))
