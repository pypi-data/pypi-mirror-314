from decimal import Decimal
from random import normalvariate

Variability = Decimal


def normalize_value(value: Decimal, minimum: Decimal, maximum: Decimal) -> Decimal:
    """Scale value position between minimum and maximum to [0:1] bound"""

    # Scale value and maximum relative to zero to enable finding fractional value by straightforward division
    zero_scaled_value: Decimal = value - minimum
    zero_scaled_maximum: Decimal = maximum - minimum

    # Divide scaled values
    normalized_value: Decimal = zero_scaled_value / zero_scaled_maximum

    return normalized_value


def clamp_or_normalize_value(value: Decimal, minimum: Decimal, maximum: Decimal) -> Decimal:
    new_value: Decimal

    if value < minimum:
        new_value = Decimal("0.0")
    elif value > maximum:
        new_value = Decimal("1.0")
    else:
        new_value = normalize_value(value=value, minimum=minimum, maximum=maximum)

    return new_value


def get_variability_amount(variability: Variability,
                           coloring_image_axis_size: Decimal) -> Decimal:
    if variability == Decimal("0.0"):
        variability_amount: Decimal = variability
    else:
        # TODO: get scaled or truncated value rather than retrying until value generated that fits in desired range
        #       search term: Truncated normal distribution
        # https://scipy.github.io/devdocs/reference/generated/scipy.stats.truncnorm.html
        # https://github.com/jessemzhang/tn_test/blob/master/truncated_normal/truncated_normal.py
        # package name: truncnorm
        # package name: pydistributions
        variation_value: Decimal = Decimal('Infinity')
        while variation_value < Decimal("-1.0") or variation_value > Decimal("1.0"):
            variation_value: Decimal = Decimal(normalvariate(mu=0.0, sigma=0.25))

        # Maximum extent of axis considered around point
        variability_radius: Decimal = variability * coloring_image_axis_size
        # Specific extent selected with normal distribution value
        variability_amount: Decimal = variation_value * variability_radius

    return variability_amount
