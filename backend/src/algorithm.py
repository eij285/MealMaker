import math

def take_second(elem):
    return (elem[1])

def calculate_similarity(orig_vals, new_vals):
    """Calculates Pearson-correlation similarity for two sets of values
    
    Args:


    Returns:


    """
    # Assert that both are of equal lengths

    # Get mean for both lists (discarding 0's)
    filtered_ov = [x for x in orig_vals if x != 0]
    filtered_nv = [x for x in new_vals if x != 0]

    ov_mean = sum(filtered_ov)/len(filtered_ov)
    nv_mean = sum(filtered_nv)/len(filtered_nv)

    # Compute cosine similarity
    a, b, c = 0, 0, 0

    for orig_val, new_val in zip(orig_vals, new_vals):
        ov_vm = 0
        nv_vm = 0

        # Subtracts mean from orig if rating exists
        if orig_val != 0:
            ov_vm = orig_val - ov_mean
        
        # Subtracts mean from new if rating exists
        if new_val != 0:
            nv_vm = new_val - nv_mean

        # Add results to values a, b and c
        a += ov_vm * nv_vm
        b += ov_vm ** 2
        c += nv_vm ** 2

    # Square root b and c, and comute cosine similarity
    b = math.sqrt(b)
    c = math.sqrt(c)

    # TODO: Identify scenarios where division by 0 occurs and return appropriate
    # value
    if b * c == 0:
        return 0
    else:
        return a / (b * c)
