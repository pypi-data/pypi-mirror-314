import nox
import pathlib

# Tested versions. Python → list of mercurials. Usually sync-ed with extension_utils
TESTED = {
    '2.7': [
        '3.4', '3.8', '4.1', '4.9', '5.0', '5.5', '5.9',
    ],
    '3.8': [
        '5.0', '5.9',
    ],
    '3.9': [
        '5.9', '6.1',
    ],
    '3.10': [
        '5.5', '5.9', '6.1', '6.2', '6.4', '6.7', '6.8',
    ],
    '3.12': [
        '6.5', '6.7', '6.8',
    ]
}

###########################################################################

nox.options.envdir = pathlib.Path.home() / ".nox_venvs" / "mercurial_exts"
nox.options.reuse_venv = True


###########################################################################

def _hgver_to_clause(ver):
    ver_items = ver.split('.')
    result = "Mercurial>={0}.{1},<{0}.{2}".format(
        ver_items[0], ver_items[1], int(ver_items[1]) + 1)
    return result


@nox.session
@nox.parametrize('python,hgver', [
    (pyver, hgver)
    for pyver in TESTED
    for hgver in TESTED[pyver]
])
def tests(session, hgver):
    if not session.python.startswith('2.') and hgver.startswith('5.'):
        session.env['HGPYTHON3'] = '1'

    session.install('mercurial_extension_utils >= 1.5.0', 'cram >= 0.6', _hgver_to_clause(hgver))
    session.install('.')
    session.run('cram', '-v', 'tests')


