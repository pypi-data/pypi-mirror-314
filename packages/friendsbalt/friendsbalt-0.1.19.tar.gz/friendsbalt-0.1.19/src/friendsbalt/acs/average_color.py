def average_rgb(color1, color2):
    """
    Calculate the average RGB color between two given RGB colors.

    Args:
        color1 (tuple): A tuple representing the first RGB color (r1, g1, b1).
        color2 (tuple): A tuple representing the second RGB color (r2, g2, b2).

    Returns:
        tuple: A tuple representing the average RGB color (r, g, b).
    """
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    return int(round((r1 + r2) / 2)), int(round((g1 + g2) / 2)), int(round((b1 + b2) / 2))

def proportional_average_rgb(color1, size1, color2, size2):
    """
    Calculates the proportional average RGB value between two colors based on their sizes.
    Parameters:
    color1 (tuple): The RGB values of the first color.
    size1 (int): The count of occurences of the first color.
    color2 (tuple): The RGB values of the second color.
    size2 (int): The count of occurences of the second color.
    Returns:
    tuple: The proportional average RGB value calculated based on the sizes of the colors.
    """
    r1, g1, b1 = color1
    r2, g2, b2 = color2

    total_size = size1 + size2

    if total_size == 0:
        return 0, 0, 0
    
    weight1 = size1 / total_size
    weight2 = size2 / total_size

    return (
        int(round(r1 * weight1 + r2 * weight2)),
        int(round(g1 * weight1 + g2 * weight2)),
        int(round(b1 * weight1 + b2 * weight2))
    )