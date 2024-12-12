from __future__ import annotations

import datetime


def _cmp(x, y):
    return 0 if x == y else 1 if x > y else -1


class date(datetime.date):
    """Date with time zone."""

    # pylint: disable=redefined-slots-in-subclass
    __slots__ = "_year", "_month", "_day", "_hashcode", "_tzinfo"

    def __new__(cls, year, month: int | None = None, day: int | None = None, tzinfo: datetime.tzinfo | None = None):  # pylint: disable=signature-differs
        """Constructor.

        Arguments:

        year, month, day, tzinfo (required, base 1)
        """
        if isinstance(year, bytes) and len(year) == 4 and 1 <= ord(year[2:3]) <= 12:
            self = datetime.date.__new__(cls, year)  # type: ignore
            self._setstate(year, month)
            self._hashcode = -1
            return self

        self = datetime.date.__new__(cls, year=year, month=month, day=day)  # type: ignore
        self._year = year
        self._month = month
        self._day = day
        self._hashcode = -1
        _check_tzinfo_arg(tzinfo)
        self._tzinfo = tzinfo
        return self

    # Read-only field accessors

    @property
    def tzinfo(self) -> datetime.tzinfo | None:
        """timezone info object"""
        return self._tzinfo

    # Comparisons of date objects with other.

    def __eq__(self, other):
        if isinstance(other, date):
            return self._cmp(other) == 0
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, date):
            return self._cmp(other) != 0
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, date):
            return self._cmp(other) <= 0
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, date):
            return self._cmp(other) < 0
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, date):
            return self._cmp(other) >= 0
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, date):
            return self._cmp(other) > 0
        return NotImplemented

    def _cmp(self, other):
        assert isinstance(other, date)
        y, m, d, tz = self.year, self.month, self.day, self.tzinfo
        y2, m2, d2, tz2 = other.year, other.month, other.day, other.tzinfo

        offset1 = (tz or datetime.timezone.utc).utcoffset(None) or datetime.timedelta(0)
        offset2 = (tz2 or datetime.timezone.utc).utcoffset(None) or datetime.timedelta(0)

        return _cmp((y, m, d, -offset1), (y2, m2, d2, -offset2))

    # Pickle support.

    def _getstate(self):
        yhi, ylo = divmod(self._year, 256)
        basestate = bytes([yhi, ylo, self._month, self._day])
        if self._tzinfo is None:
            return (basestate,)
        else:
            return (basestate, self._tzinfo)

    def _setstate(self, string, tzinfo):
        if tzinfo is not None and not isinstance(tzinfo, datetime.tzinfo):
            raise TypeError("bad tzinfo state arg")

        yhi, ylo, self._month, self._day = string
        self._year = yhi * 256 + ylo
        # pylint: disable=attribute-defined-outside-init
        self._tzinfo = tzinfo

    def __reduce__(self):
        return (self.__class__, self._getstate())


def _check_tzinfo_arg(tz):
    if tz is not None and not isinstance(tz, datetime.tzinfo):
        raise TypeError("tzinfo argument must be None or of a tzinfo subclass")
