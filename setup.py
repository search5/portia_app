from setuptools import setup
from setuptools.command.install import install as _install
import nodeenv
import tempfile

class install(_install):
    def run(self):
        _install.run(self)

        nodejs_requirements = tempfile.NamedTemporaryFile('w+')
        nodejs_requirements.write('create-vue')

        print("Node.JS Install")
        print("-" * 80)
        parser = nodeenv.make_parser()
        parse_result = parser.parse_args(["-n", "lts", "-p", "-r", ""])

        src_domain = 'nodejs.org'
        nodeenv.src_base_url = 'https://%s/download/release' % src_domain

        parse_result.node = nodeenv.get_last_lts_node_version()

        env_dir = nodeenv.get_env_dir(parse_result)
        nodeenv.create_environment(env_dir, parse_result)
        print("-" * 80)

setup(cmdclass={'install': install})
