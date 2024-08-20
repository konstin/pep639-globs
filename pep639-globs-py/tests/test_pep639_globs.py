from pep639_globs.pep639_globs import Pep639Glob, Pep639GlobError


def test_error():
    cases = [
        (
            "..",
            "Glob contains pattern directory indicator (`..`) at position 0, which is not allowed.",
        ),
        (
            "licenses/..",
            "Glob contains pattern directory indicator (`..`) at position 9, which is not allowed.",
        ),
        (
            "licenses/LICEN!E.txt",
            "Glob contains invalid character at position 14: `!`",
        ),
        (
            "licenses/LICEN[!C]E.txt",
            "Glob contains invalid character in range at position 15: `!`",
        ),
        (
            "licenses/LICEN[C?]E.txt",
            "Glob contains invalid character in range at position 16: `?`",
        ),
        (
            "******",
            "Pattern syntax error near position 2: wildcards are either regular `*` or recursive `**`"
        ),
        (
            r"licenses\eula.txt",
            r"Glob contains invalid character at position 8: `\`"
        ),
    ]
    for (glob, expected) in cases:
        try:
            Pep639Glob(glob)
        except Pep639GlobError as exception:
            assert expected == str(exception)


def test_passing():
    cases = [
        "licenses/*.txt",
        "licenses/**/*.txt",
        "LICEN[CS]E.txt",
        "LICEN?E.txt",
        "[a-z].txt",
        "[a-z._-].txt",
        "*/**",
        "LICENSE..txt",
        "LICENSE_file-1.txt",
        # (google translate)
        "licenses/라이센스*.txt",
        "licenses/ライセンス*.txt",
        "licenses/执照*.txt",
    ]
    for case in cases:
        Pep639Glob(case)
