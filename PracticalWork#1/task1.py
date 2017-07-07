#!/usr/bin/env python
"""
 Python. Practical Work #1
 This code allows to send packages from input file to addressant(output file)
"""

END_PACKAGE          = "end"
FILENAME_EXTENSION   = ".txt"

# Addressants
IVASYK               = 'I'
DMYTRO               = 'D'
OSTAP                = 'O'
LESYA                = 'L'

# Messages for result of working
EMPTY_FILE_MESSAGE = "File is empty!!!"
NOT_OPEN_MESSAGE   = "Can not open file"
SUCCESS_MESSAGE    = "Files is created!!!"

def main(path_file='messages'):
    """
        Main function of this program.
        This function shows result of working program

        Parameters
        ----------
            path_file : str
                Name of input file
        """

    try:
        # get all packages
        packages = read(path_file + FILENAME_EXTENSION)

        # get dictionary with addressants as key and list of packages for addressant as value.
        dict = packagesToDictionary(packages)

        for item in dict:
            # create files with packages for each addressant
            generateFile(item +  FILENAME_EXTENSION, dict[item])
        print SUCCESS_MESSAGE

    except IOError:
        print NOT_OPEN_MESSAGE

    except Exception as e:
        print e.message



def read(path_file):
    """
    Read lines from file.
    If file can not opened then will be thrown exception IOError.
    If file is empty then will be thrown my exception.

    Parameters
    ----------
        path_file : str
            Name of input file
    Returns
    -------
        list
            All lines from input file
    """

    # open file for read
    with open(path_file, 'r') as f:
        lines = f.readlines()
        if not lines:
            raise Exception(EMPTY_FILE_MESSAGE)
        return lines


def packagesToDictionary(packages):
    """
    This function formates dictionary with addressants as key,
    and list of packages for addressant as value.

    Parameters
    ----------
        packages : list of str
            All packages from input file
    Returns
    -------
        dict
            Dictionary with addressants as key,
            and list of packages for addressant as value
    """

    dict = {IVASYK: [], DMYTRO: [], OSTAP: [], LESYA: []}

    for package in packages:
        # get all addressants who gets packege
        addressants = getAddressants(package.strip('\n'))

        # add package to items of dictionary
        if addressants:
            for addressant in addressants:
                dict[addressant].append(package)

    return dict


def getAddressants(package):
    """
    This function finds addressants whose has to get package.

    Parameters
    ----------
        package : str
            One package
    Returns
    -------
        list
            List of addressants
        None
            if package is empty
    """
    addressants = []

    if not package:
        return

    # Checking package for Lesya
    if package.split()[-1] == 'end':
        addressants.append('L')

    # Checking package for Ivasyk
    if len(package) % 2 == 0:
        addressants.append('I')
    # Checking package for Dmytro
    elif package[0].isupper():
        addressants.append('D')
    # Checking package for Ostap
    elif not addressants:
        addressants.append('O')

    return addressants


def generateFile(pathFile, packages):
    """
        This function generates file with packages.

        Parameters
        ----------
            pathFile : str
                Name of new file
            packages : list of str
                Packages for one addressant
        """

    # open file for write
    with open(pathFile, 'w') as file:
        file.writelines(packages)

if __name__ == "__main__":
    main()
