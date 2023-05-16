import nodeenv
from pathlib import Path
from subprocess import run, PIPE
import shutil

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

def frontend_ready():
    portia_dir = Path("portia")
    portia_assets_dir = portia_dir / "assets"
    portia_templates_dir = portia_dir / "templates"

    portia_templates_dir.mkdir(exist_ok=True)
    if portia_assets_dir.exists():
        shutil.rmtree(portia_assets_dir)
    
    shutil.copy("portia_web/dist/index.html", portia_templates_dir / "index.html")
    shutil.copytree("portia_web/dist/assets", "portia/assets")
