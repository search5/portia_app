import nodeenv
import os
from subprocess import run, PIPE

def nodejs_setup():
    print("Node.JS Install")
    print("-" * 80)
    parser = nodeenv.make_parser()
    parse_result = parser.parse_args(["-n", "lts", "-p"])

    src_domain = 'nodejs.org'
    nodeenv.src_base_url = 'https://%s/download/release' % src_domain

    parse_result.node = nodeenv.get_last_lts_node_version()

    env_dir = nodeenv.get_env_dir(parse_result)
    nodeenv.create_environment(env_dir, parse_result)
    print("-" * 80)

    os.chdir("portia_web")
    run(["npm", "install"], stdout=PIPE, stderr=PIPE)

    return True
