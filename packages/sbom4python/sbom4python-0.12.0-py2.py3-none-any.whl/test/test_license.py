import pytest

from sbom4python.scanner import SBOMScanner
from lib4sbom.license import LicenseScanner


class TestLicense:
    @pytest.mark.parametrize(
        "expression, result",
        (
            ("bad", "NOASSERTION"),
            ("", "NOASSERTION"),
            ("NONE", "NONE"),
            ("NOASSERTION", "NOASSERTION"),
            ("MIT and Apache-2.0", "MIT and Apache-2.0"),
            ("MIT and Apache", "MIT and Apache-2.0"),
            ("LicenseRef-100", "LicenseRef-100"),
            ("ASL 2.0", "Apache-2.0"),
            ("Apache", "Apache-2.0"),
            ("MIT", "MIT"),
        ),
    )
    def test_license(self, expression, result):
        test_item = SBOMScanner(debug=True)
        license = test_item.process_license_expression(expression)
        assert license == result

    # def test_find_license_id(self, license, result):
    #    test_item = SBOMScanner(debug=True)
    #    license_id = test_item.license_ident(license)
    #    assert license_id == result

    # @pytest.mark.parametrize(
    #    "expression, result",
    #    (
    #        ("bad", "NOASSERTION"),
    #        ("apache", "Apache-2.0"),
    #        ("MIT and Apache-2.0", "MIT and Apache-2.0"),
    #        ("(MIT or BSD) and Apache-2.0", "(MIT or BSD-3-Clause) and Apache-2.0"),
    #    )
    # )

    @pytest.mark.parametrize(
        "license, result",
        (
            ("bad", "UNKNOWN"),
            ("", "UNKNOWN"),
            ("NONE", "NONE"),
            ("NOASSERTION", "NOASSERTION"),
            ("Apache-2.0", "Apache-2.0"),
            ("LicenseRef-100", "LicenseRef-100"),
            ("ASL 2.0", "Apache-2.0"),
            ("Apache", "Apache-2.0"),
            ("MIT", "MIT"),
        ),
    )
    def test_find_license(self, license, result):
        test_item = LicenseScanner()
        x = test_item.get_synonym()
        assert (len(x) > 0)
        licenseid = test_item.find_license(license)
        assert licenseid == result
