



def _GetListDefault(l, index, default):
    if index < len(l):
        return l[index]
    else:
        return default.Copy()

def _IsBackslashEscapedQuote(string, quote_index):
    """Checks if the quote at the given index is backslash escaped."""
    num_preceding_backslashes = 0
    for char in reversed(string[:quote_index]):
        if char == '\\':
            num_preceding_backslashes += 1
        else:
            break
    return num_preceding_backslashes % 2 == 1

def _FindQuoteEnd(string, quote_type):
    """Recursively finds the ending index of a quote.

    Args:
      string: The string to search inside of.
      quote_type: The quote type we're looking for.

    Returns:
      The index of the end of the first quote.
    """
    trial_index = string.find(quote_type)
    if trial_index == -1:
        return -1
    elif not _IsBackslashEscapedQuote(string, trial_index):
        return trial_index
    else:
        new_start = trial_index + 1
        rest_index = _FindQuoteEnd(string[new_start:], quote_type)
        if rest_index == -1:
            return -1
        else:  # Return the recursive sum
            return new_start + rest_index
