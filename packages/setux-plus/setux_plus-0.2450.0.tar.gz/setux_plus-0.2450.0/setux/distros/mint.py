from setux.distros.debian import Debian


class Mint(Debian):
    @classmethod
    def release_name(cls, infos):
        did = infos['DISTRIB_ID']
        if did=='LinuxMint':
            did='Mint'
        release = infos['DISTRIB_RELEASE']
        if '.' in release:
            ver, _, _ = release.partition('.')
        else:
            ver = release
        return f'{did}_{ver}'


class Mint_20(Mint):
    '''Uma'''


class Mint_21(Mint):
    '''Vanessa'''


class Mint_22(Mint):
    '''Wilma'''
