from setux.distros.debian import Debian_11


class MX(Debian_11):
    Service = 'SystemV'

    @classmethod
    def release_name(cls, infos):
        did = infos['DISTRIB_ID']
        ver, _, _ = infos['DISTRIB_RELEASE'].partition('.')
        return f'{did}_{ver}'


class MX_21(MX): pass


class MX_23(MX): pass
