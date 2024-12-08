""" """

import re
import functools


class IntegrityError(ValueError):
    """
    Error in the integrity format

    This type of error is meant to represent an incorrect format of an integrity tag.
    """

    pass


def validate(asil: str) -> bool:
    """
    Validate the format of an ISO26262 integrity level string

    This function takes an integrity level input as a string and returns a boolean indicating if
    the string is a valid representation of an ASIL integrity level. The string is not supposed
    to be in the canonical format to be considered valid.

    This is a simplified wrapper for the underlying Integrity class.

    Arguments
    ---------
    asil : str
        the original string to be validated

    Returns
    -------
    bool:
        True if the ASIL is a valid ASIL tag, false otherwise.
    """
    return Integrity.validate(asil)


def canonicalize(asil: str) -> str:
    """
    Get the canonical form for an ISO26262 integrity level string

    This function takes an integrity level input as a string and returns another string with the
    same level but in the canonical form. It is assumed that asil is a valid asil string, otherwise
    the function raises an exception.

    This is a simplified wrapper for the underlying Integrity class.

    Arguments
    ---------
    asil : str
        the original string to be validated

    Returns
    -------
    str:
        The same level, but in canonical form
    """
    return str(Integrity(asil))


def verify_inheritance(parent: str, child: str) -> bool:
    """
    Check if an Integrity inheritance is valid or not

    Integrity according to ISO2626 should be inherited between requirements. Normally the integrity
    must be inherited as-is from the parent requirement. In case of a decomposition it is also
    necessary that the decomposed integrity, in parentheses, should be equal to the base integrity
    of the parent. It is assumed that the integrity string is a valid integrity.

    This is a simplified wrapper for the underlying Integrity class.

    Arguments
    ---------
    parent : str
        the integrity of the parent requirement
    child: str
        the integrity of the child requirement

    Returns
    -------
    bool:
        True if the inheritance is valid, false otherwise
    """
    return Integrity(child).verify_with_parent(Integrity(parent))


@functools.total_ordering
class Integrity:
    """
    Class representing ISO26262 integrity levels

    This class represents an instance of an ISO26262 integrity level. It can be created starting
    from a string and then it stores internally an encoding of the integrity. Optionally it can also
    store the original string.

    Once created it outputs the canonical ASIL string as mentioned in ISO26262 and allows the
    comparison between different integrities and the validation of inheritance between them.

    Attributes
    ----------
    original : str
        the original string parsed to create this object, if selected at creation time
    """

    @staticmethod
    def __encode(asil: str) -> int:
        """
        Map levels to integers

        The mapping is:

        - QM <=> 0
        - A <=> 1
        - B <=> 2
        - C <=> 3
        - D <=> 4

        Arguments
        ---------
        asil : str
            the asil string

        Returns
        -------
        int:
            Corresponding integer to the level
        """
        if asil == "QM":
            return 0
        return ord(asil) - ord("A") + 1

    @staticmethod
    def __decode(level: int) -> str:
        """
        Map integers to levels

        The mapping is:

        - QM <=> 0
        - A <=> 1
        - B <=> 2
        - C <=> 3
        - D <=> 4

        Arguments
        ---------
        level : int
            the asil level

        Returns
        -------
        str:
            Corresponding string for the level
        """
        if level == 0:
            return "QM"
        return chr(level + ord("A") - 1)

    @staticmethod
    def __parse(asil: str) -> tuple[str, str]:
        """
        Parse the ASIL string

        Parse the string and identify the tokens related to the base and decomposed ASIL. The tokens
        are returned as tuple. When the string does not have a decomposition the second token is
        None. If the asil string is not matched at all, then both tokens are returned as None.

        Arguments
        ---------
        asil : str
            the original string to be parsed

        Returns
        -------
        tuple[str, str]:
            The base and decomposed ASIL level tokens. Each token can be None or one of "A", "B",
            "C" or "D" or "QM".
        """
        mo = re.match(
            r"^(ASIL[-_ ]?([ABCD])|(QM)) ?(\( ?([ABCD]) ?\)|\( ?(QM) ?\))?$",
            asil.strip(),
            re.IGNORECASE,
        )
        if not mo:
            return (None, None)
        base = mo[2]
        if not base:
            base = mo[3]
        if not mo[4]:
            return base.upper(), None

        if mo[5]:
            decomposed = mo[5]
        else:
            decomposed = mo[6]

        return base.upper(), decomposed.upper()

    @staticmethod
    def validate(asil: str) -> bool:
        """
        Validate the format of an ISO26262 integrity level string

        This function takes an integrity level input as a string and returns a boolean indicating if
        the string is a valid representation of an ASIL integrity level. The string is not supposed
        to be in the canonical format to be considered valid.

        Arguments
        ---------
        asil : str
            the original string to be validated

        Returns
        -------
        bool:
            True if the ASIL is a valid ASIL tag, false otherwise.
        """
        return Integrity.__parse(asil) != (None, None)

    def __init__(self, asil: str = "", store_original: bool = False) -> None:
        """
        Initialize an ISO26262 Integrity object

        Initializes an object by validating and encoding the ASIL tag. Optionally, the original
        string can be stored aside the encoded string. This can be useful if the original
        representation is necessary as an Integrity object, once created, will always output the
        asil string in canonical form.

        Arguments
        ---------
        asil : str
            the original string to be validated and stored encoded in the object
        store_original: bool
            keep the original string if needed, can be accessed later
        """
        if store_original:
            self.__original = asil
        else:
            self.__original = None

        base_in, decomposed_in = self.__parse(asil)
        if (base_in, decomposed_in) == (None, None):
            raise IntegrityError("Invalid integrity format '{}'".format(asil))

        self.__base = Integrity.__encode(base_in)

        if not decomposed_in:
            self.__decomposed = None
        else:
            self.__decomposed = Integrity.__encode(decomposed_in)

    def __str__(self) -> str:
        """
        Print out the canonical form of the ASIL

        Print out the internally-encoded ASIL in canonical format.

        Returns
        -------
        str:
            the canonical form of the ASIL string encoded in the object
        """
        base_out = "ASIL {}".format(Integrity.__decode(self.__base))

        if self.__decomposed is not None:
            return "{}({})".format(base_out, Integrity.__decode(self.__decomposed))

        return base_out

    def __repr__(self) -> str:
        """
        Print out the internal representation of the object

        Useful for development purposes.

        Returns
        -------
        str:
            the stringified internal content of the object
        """
        return "Integrity(base='{}', decomposed='{}', original='{}')".format(
            self.__base, self.__decomposed, self.__original
        )

    def __eq__(self, other: "Integrity") -> bool:
        """
        Comparison equality

        Compare equals if the base integrity is the same for both objects, independently from the
        decomposed integrity.

        Arguments
        ---------
        other : Integrity
            the Integrity instance to compare with

        Returns
        -------
        bool:
            True if the comparison is equal, false otherwise
        """
        return self.__base == other.__base

    def __lt__(self, other: "Integrity") -> bool:
        """
        Comparison lower than

        Compare lower than if the base integrity is lower than another object's independently from
        the decomposed integrity.

        Arguments
        ---------
        other : Integrity
            the Integrity instance to compare with

        Returns
        -------
        bool:
            True if the comparison is lower than, false otherwise
        """
        return self.__base < other.__base

    @property
    def original(self) -> str:
        """
        Get the original string if stored in this object

        If the object was created with `store_original=True` then the original string can be
        accessed via this property. Otherwise an `AttributeError` is raised.

        Returns
        -------
        str:
            The original string of the integrity
        """
        if self.__original is None:
            raise AttributeError("The original integrity was not set for this object")

        return self.__original

    def verify_with_parent(self, parent: "Integrity") -> bool:
        """
        Check if an Integrity inheritance of a parent is valid or not

        Integrity according to ISO2626 should be inherited between requirements. Normally the
        integrity must be inherited as-is from the parent requirement. In case of a decomposition it
        is also necessary that the decomposed integrity, in parentheses, should be equal to the base
        integrity of the parent. It is assumed that the integrity string is a valid integrity.

        The comparison must be done with another integrity that is considered the integrity of a
        parent requirement.

        Arguments
        ---------
        parent : str
            the integrity of the parent requirement

        Returns
        -------
        bool:
            True if the inheritance is valid, false otherwise
        """
        return self.__decomposed == parent.__base and self.__base <= self.__decomposed

    def verify_with_child(self, child: "Integrity") -> bool:
        """
        Check if an Integrity inheritance of a child is valid or not

        Integrity according to ISO2626 should be inherited between requirements. Normally the
        integrity must be inherited as-is from the parent requirement. In case of a decomposition it
        is also necessary that the decomposed integrity, in parentheses, should be equal to the base
        integrity of the parent. It is assumed that the integrity string is a valid integrity.

        The comparison must be done with another integrity that is considered the integrity of a
        child requirement.

        Arguments
        ---------
        child : str
            the integrity of the child requirement

        Returns
        -------
        bool:
            True if the inheritance is valid, false otherwise
        """
        return child.verify_with_parent(self)
