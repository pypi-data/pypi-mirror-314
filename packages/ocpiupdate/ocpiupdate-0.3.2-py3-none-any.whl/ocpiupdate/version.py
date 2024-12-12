"""Functions for handling comparing a three part version string."""

from typing import Tuple, cast


class Version:
    """Class representation of major.minor.patch version."""

    class ComparisonWithNotAVersionError(TypeError):
        """Error when Version is compared to an invalid type."""

        def __init__(self, operator: str, other: object) -> None:
            """Construct."""
            super().__init__(
                f"`{operator}` operator not defined between "
                f"`{self.__class__.__name__}` and "
                f"`{other.__class__.__name__}`",
            )

    VersionParts = Tuple[int, int, int]
    _version_parts: VersionParts

    def __init__(self, version_str: str) -> None:
        """Construct."""
        version_parts = [int(part) for part in version_str.split(".")]
        if len(version_parts) != 3:
            message = f"Version string has more than 3 components: {version_parts}"
            raise ValueError(message)
        self._version_parts = cast("Version.VersionParts", tuple(version_parts))

    def __repr__(self) -> str:
        """Dunder method: Convert to string evaluating to class constructor."""
        return f"{self.__class__.__name__}({'.'.join(map(str, self._version_parts))!r})"

    def __lt__(self, other: object) -> bool:
        """Dunder method: Less than."""
        if not isinstance(other, self.__class__):
            raise self.ComparisonWithNotAVersionError("<", other)  # noqa: EM101
        return self._version_parts < other._version_parts

    def __le__(self, other: object) -> bool:
        """Dunder method: Less than or equal to."""
        if not isinstance(other, self.__class__):
            raise self.ComparisonWithNotAVersionError("<=", other)  # noqa: EM101
        return self._version_parts <= other._version_parts

    def __eq__(self, other: object) -> bool:
        """Dunder method: Equal to."""
        if not isinstance(other, self.__class__):
            return False
        return self._version_parts == other._version_parts

    def __gt__(self, other: object) -> bool:
        """Dunder method: Greater than."""
        if not isinstance(other, self.__class__):
            raise self.ComparisonWithNotAVersionError(">", other)  # noqa: EM101
        return self._version_parts > other._version_parts

    def __ge__(self, other: object) -> bool:
        """Dunder method: Greater than or equal to."""
        if not isinstance(other, self.__class__):
            raise self.ComparisonWithNotAVersionError(">=", other)  # noqa: EM101
        return self._version_parts >= other._version_parts

    def __ne__(self, other: object) -> bool:
        """Dunder method: Not equal to."""
        if not isinstance(other, self.__class__):
            return True
        return self._version_parts != other._version_parts

    def __hash__(self) -> int:
        """Dunder method: Hash."""
        return hash(self._version_parts)

    def __str__(self) -> str:
        """Dunder method: Convert to string."""
        return ".".join(map(str, self._version_parts))


V2_4_7 = Version("2.4.7")
