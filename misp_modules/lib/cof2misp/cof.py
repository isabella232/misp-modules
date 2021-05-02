"""
Common Output Format for passive DNS library.

"""

import ipaddress
import sys
import ndjson


def is_valid_ip(ip: str) -> bool:
    """Check if an IP address given as string would be convertible to
    an ipaddress object (and thus if it is a valid IP).

    Returns
    --------
    True on success, False on validation failure.
    """

    try:
        ipaddress.ip_address(ip)
    except Exception as ex:
        print("is_valid_ip(%s) returned False. Reason: %s" % (ip, str(ex)), file=sys.stderr)
        return False
    return True


def is_cof_valid_simple(d: dict) -> bool:
    """Check MANDATORY fields according to COF - simple check, do not do the full JSON schema validation.

    Returns
    --------
    True on success, False on validation failure.
    """

    if "rrname" not in d:
        print("Missing MANDATORY field 'rrname'", file=sys.stderr)
        return False
    if not isinstance(d['rrname'], str):
        print("Type error: 'rrname' is not a JSON string", file=sys.stderr)
        return False
    if "rrtype" not in d:
        print("Missing MANDATORY field 'rrtype'", file=sys.stderr)
        return False
    if not isinstance(d['rrtype'], str):
        print("Type error: 'rrtype' is not a JSON string", file=sys.stderr)
        return False
    if "rdata" not in d:
        print("Missing MANDATORY field 'rdata'", file=sys.stderr)
        return False
    if "rdata" not in d:
        print("Missing MANDATORY field 'rdata'", file=sys.stderr)
        return False
    if not isinstance(d['rdata'], str) and not isinstance(d['rdata'], list):
        print("'rdata' is not a list and not a string.", file=sys.stderr)
        return False
    if not ("time_first" in d and "time_last" in d) or ("zone_time_first" in d and "zone_time_last" in d):
        print("We are missing EITHER ('first_seen' and 'last_seen') OR ('zone_time_first' and zone_time_last') fields", file=sys.stderr)
        return False
    # currently we don't check the OPTIONAL fields. Sorry... to be done later.
    return True


def validate_cof(d: dict, strict=False) -> bool:
    """Validate an input passive DNS COF (given as dict).
    strict might be set to False in order to loosen the checking.
    With strict==True, a full JSON Schema validation will happen.


    Returns
    --------
    True on success, False on validation failure.
    """
    if not strict:
        return is_cof_valid_simple(d)


if __name__ == "__main__":
    # simple, poor man's unit tests.

    print(80*"=", file=sys.stderr)
    print("Unit Tests:", file=sys.stderr)
    assert not is_valid_ip("a.2.3.4")
    assert is_valid_ip("99.88.77.6")
    assert is_valid_ip("2a0c:88:77:6::1")

    # COF validation
    mock_input = """{"count":1909,"rdata":["cpa.circl.lu"],"rrname":"www.circl.lu","rrtype":"CNAME","time_first":"1315586409","time_last":"1449566799"}
{"count":2560,"rdata":["cpab.circl.lu"],"rrname":"www.circl.lu","rrtype":"CNAME","time_first":"1449584660","time_last":"1617676151"}"""

    i = 0
    for entry in ndjson.loads(mock_input):
        retval = validate_cof(entry, strict=False)
        assert retval
        print("line %d is valid: %s" % (i, retval))
        i += 1

    print(80*"=", file=sys.stderr)
    print("Unit Tests DONE", file=sys.stderr)
