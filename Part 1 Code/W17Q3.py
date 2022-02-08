from datetime import datetime
from hashlib import sha1, sha256
from itertools import permutations

hash_wanted = "fc2298f491eac4cff95e7568806e088a901c904cda7dd3221f551e5b89b3c3aa"

salt = "5UA@/Mw^%He]SBaU"

information = {
    "username": "laplusbelle",
    "name": "Marie",
    "surname": "Curie",
    "pet": "Woof",
    "bday": datetime(1980, 1, 2),
    "employer": "UKC",
    "mother": "Jean Neoskour",
    "father": "Jvaist Fairecourir",
    "husband": "Eltrofor",
    "husband_bday": datetime(1981, 12, 29),
}

formats = ["%d", "%m", "%y", "%Y", "%d%m", "%m%d", "%m%y", "%y%m", "%m%d%y", "%d%m%y", "%y%m%d", "%m%d%Y", "%d%m%Y",
           "%Y%m%d"]


def check_password(password: str, display=False) -> str:
    '''
    Check if a given string is a possible password

    :param password: The string that needs to be checked
    :param display: Displays the results and the wanted value
    :return: The type of encryption it can be
    '''
    new_password = (password + salt).encode("utf-8")
    sha1_result = sha1(new_password).hexdigest()
    sha256_result = sha256(new_password).hexdigest()

    if display:
        print(sha1_result, sha256_result, hash_wanted)
    if sha1_result == hash_wanted:
        return "SHA1"
    elif sha256_result == hash_wanted:
        return "SHA256"
    else:
        return "NONE"


def make_date_format(date: datetime) -> list[str]:
    '''
    Takes a given date and returns a list of all the formats for the given date

    :param date: The given date
    :return: A list of the date with different format
    '''
    results = []
    for k in formats:
        results.append(date.strftime(k))
    return results


def get_values_dict() -> list[str]:
    '''
    Makes a list of every string value in the information dictionary.
    This also transforms every value in both upppercase and lowercase.
    If a space is present it will be replaced

    :return:
    '''
    values = []
    for k in information:
        value = information[k]
        if isinstance(value, str):
            values.append(value)
            values.append(value.lower())
            values.append(value.upper())
            values.append(value.replace(" ", "_"))
            values.append(value.lower().replace(" ", "_"))
            values.append(value.upper().replace(" ", "_"))
            values.append(value.replace(" ", ""))
            values.append(value.lower().replace(" ", ""))
            values.append(value.upper().replace(" ", ""))
    return list(set(values))


def make_posibility(begin=0, comb_num=1) -> int:
    '''
    Check every possible password depending on the number of combinations

    :param begin: Starts at 0 with only 1 element
    :param comb_num: Goes to the number of element tested
    :return: If the program found something it returns 0 otherwise it's 1
    '''
    all_elements = get_values_dict() + make_date_format(information["husband_bday"]) + make_date_format(
        information["bday"])
    display_percent = 10000

    for i in range(begin, comb_num):
        perm_list = list(permutations(all_elements, 1 + i))
        perm_list_len = len(perm_list)
        #print(f"Step {i + 1} Starts !")
        for k in range(perm_list_len):
            word = "".join(perm_list[k])
            value = check_password(word)
            if value != "NONE":
                print(f"Successfully Found : {value} with password '{word}'")
                return 0
            if k % display_percent == display_percent - 1:
                pass
                #print(f"Step {i + 1}: {int((k * 100) / perm_list_len)}%")
        #print(f"Step {i + 1} Done !")
    print("Nothing Found")
    return 1


def main():
    '''
    Is the main function

    :return: The exit code
    '''
    return make_posibility(int(input("Beginning Combination: ")), int(input("Max Combination: ")))


if __name__ == '__main__':
    exit(main())
