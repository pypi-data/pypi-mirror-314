def r2lab_hostname(x):
    """
    Return a valid hostname from a name like either
    1 (int), 1(str), 01, fit1 or fit01 ...
    """
    return "fit{:02d}".format(int(str(x).replace('fit','')))


def parse_slice(slice):
    """
    returns username and hostname from a slice
    can be either username@hostname or just username
    in the latter case the hostname defaults to 
    the r2lab gateway faraday.inria.fr
    """
    if slice.find('@') > 0:
        user, host = slice.split('@')
        return user, host
    else:
        return slice, "faraday.inria.fr"


def find_local_embedded_script(s):
    """
    all the scripts are located in the same place
    find that place among a list of possible locations
    """
    paths = [
        "../../r2lab-embedded/shell/",
        os.path.expanduser("~/git/r2lab-embedded/shell/"), 
        os.path.expanduser("~/r2lab-embedded/shell/"),
    ]
    for path in paths:
        candidate = os.path.join(path, s)
        if os.path.exists(candidate):
            return candidate
    print("WARNING: could not locate local script {}".format(s))
    for path in paths:
        print("W: searched in {}".format(path))

