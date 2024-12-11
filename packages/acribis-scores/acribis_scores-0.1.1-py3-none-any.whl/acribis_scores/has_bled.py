from typing import TypedDict

# See: https://doi.org/10.1378/chest.10-0134


Parameters = TypedDict('Parameters', {
    'Uncontrolled hypertension': bool,
    'Abnormal Renal Function': bool,
    'Abnormal Liver Function': bool,
    'Stroke': bool,
    'Bleeding history or predisposition': bool,
    'Labile international normalized ratio (INR)': bool,
    'Elderly': bool,
    'Drugs': bool,
    'Alcohol': bool,
})


def calc_has_bled_score(parameters: Parameters) -> int:
    return sum(parameters.values())
