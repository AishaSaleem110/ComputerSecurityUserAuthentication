user = [0.27, 0.079, 0.27, 0.36, 0.25, 0.3, 0.27, 0.17, 0.23, 0.12, 0.29, 0.085, 0.093, 0.12, 0, 0.34, 0.23, 0.12,
        0.34, 0.029, 0.19, 0.18, 0.23, 0.23, 0.11, 0.2, 0.18, 0.26, 0.31, 0.31, 0.11, 0.21, 0.079, 0.089, 0.2,
        0.35, 0.12, 0.24, 0.18, 0.31, 0.091, 0.2, 0.26, 0.31, 0.35, 0.21, 0.051, 0.13, 0.094, 0.44, 0.14, 0.27,
        0.18, 0.29, 0.12, 0.06, 0.058, 0.25, 0.18, 0.18, 0.34, 0.23, 0.22, 0.36, 0.12, 0.27, 0.28, 0.18, 0.22,
        0.083, 0.085, 0.21, 0.27, 0.46, 0.13, 0.22, 0.19, 0.0067, 0.16, 0.021, 0.28, 0.11, 0.21, 0.15, 0.23, 0.14,
        0.25, 0.27, 0.37, 0.18, 0, 0.12, 0.34, 0.093, 0.3, 0.21, 0.34, 0.0039, 0.18, 0.079]

intruder = [1.2, 0.77, 0.88, 0.39, 0.51, 0.55, 0.82, 0.54, 0.74, 0.19, 0.53, 0.44, 0.28, 0.7, 0.66, 0.61, 0.33, 0.83,
            0.67, 0.54, 0.6, 0.55, 0.25, 0.54, 0.43, 0.4, 0.37, 0.49, 0.2, 0.79, 0.7, 0.6, 0.59, 0.44, 0.8, 0.57, 0.46,
            0.87, 0.56, 0.48, 0.54, 0.43, 0.38, 1.1, 0.93, 0.66, 0.35, 0.43, 0.56, 0.76, 0.33, 0.13, 0.31, 0.67, 0.68,
            0.69, 0.57, 0.64, 0.5, 0.77, 0.33, 0.69, 0.43, 0.53, 0.71, 0.81, 0.38, 0.85, 0.73, 0.59, 0.56, 0.56, 0.54,
            0.6, 0.61, 0.77, 0.91, 0.69, 0.56, 0.73, 0.64, 0.39, 0.79, 0.66, 0.63, 0.7, 0.65, 0.41, 0.57, 0.57, 0.49,
            0.94, 0.42, 0.5, 0.46, 0.37, 0.56, 0.55, 0.91, 0.55]


# Gives the number of results that are under the threshold in a given list
def how_many_under(value: float, elements: list[float]) -> int:
    count = 0
    for k in elements:
        if k < value:
            count += 1
    return count


# Gives the % of how many results are under the threshold in a given list
def how_much_under(value: float, elements: list[float]) -> float:
    return how_many_under(value, elements) / len(elements)


# Gives you FAR for a given Threshold
def far(value: float, display=False) -> float:
    result = how_much_under(value, intruder)
    if display:
        print(f"FAR is equal to {result * 100:.2f}%")
    return result


# Gives you FFR for a given Threshold
def frr(value: float, display=False) -> float:
    result = (len(user) - how_many_under(value, user)) / len(user)
    if display:
        print(f"FRR is equal to {result * 100:.2f}%")
    return result


# Calculates the score of a threshold
def score(value: float) -> float:
    return frr(value) + far(value)


# Calculates the ideal threshold for the dataset given
def threshold(display: bool = False) -> float:
    low = sum(user) / len(user)
    high = sum(intruder) / len(intruder)
    medium = (low + high) / 2

    # Works until the score of medium is equal to either low or high
    while not (score(medium) == score(high) or score(medium) == score(low)):
        if display:
            print(f"low: {score(low)}, middle: {score(medium)}, high: {score(high)}")
        if score(medium) < score(low):
            low = medium
        elif score(medium) < score(high):
            high = medium
        medium = (low + high) / 2
    return medium


def main():
    # Sort those value in case we need medians
    user.sort()
    intruder.sort()
    # Calculates and display important info
    t = threshold()
    print(f"The threshold should be at : {t}")
    far(t, True)
    frr(t, True)
    return 0


if __name__ == "__main__":
    exit(main())
