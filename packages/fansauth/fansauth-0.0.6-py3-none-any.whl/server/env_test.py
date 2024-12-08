import yaml
from fans.path import Path

from fansauth.server.env import Env, paths


class Test_conf_admin:

    def test_auto_generate(self, tmp_path):
        env = Env()
        env.setup(tmp_path)
        conf = env.paths.conf.load()
        assert conf['initial_admin_username'] == 'admin'
        assert conf['initial_admin_password']

    def test_use_generated(self, tmp_path):
        env = Env()
        env.setup(tmp_path)
        conf = env.paths.conf.load()
        pwd = conf['initial_admin_password']

        env = Env()
        env.setup(tmp_path)
        conf = env.paths.conf.load()
        assert conf['initial_admin_password'] == pwd

    def test_provided_admin(self, tmp_path):
        Path(tmp_path / 'conf.yaml').save({
            'initial_admin_username': 'fans656',
            'initial_admin_password': '<provided>',
        })
        env = Env()
        env.setup(tmp_path)
        conf = env.conf
        assert conf['initial_admin_username'] == 'fans656'
        assert conf['initial_admin_password'] == '<provided>'
