import argparse
import importlib.util
import os
import importlib
import yaml
import docker_interface
import pkg_resources
from pathlib import Path
import ast


dockerfile_commands = []
dockerfile_commands.append("FROM python:3.10.16-slim-bookworm")
dockerfile_commands.append("WORKDIR /app")
dockerfile_commands.append("RUN apt-get update")
dockerfile_commands.append("RUN apt-get install -y gcc")
dockerfile_commands.append("ENV PYTHONUNBUFFERED=1")
dockerfile_commands.append("COPY requirements.txt .")
dockerfile_commands.append("RUN pip install --no-cache-dir -r requirements.txt")
dockerfile_commands.append("COPY . .")

ast_import_ecida = ast.ImportFrom(module='Ecida',names=[ast.alias(name='EcidaModule', asname=None,lineno=0,col_offset=0)],level=0,lineno=0, col_offset=0,end_lineno=0, end_col_offset=0)

DEFAULTS = {
    "manifests_dir" : "manifests"
}

def add_resource_command(parent_parser, action, res_short, resource_full, func):
    resource_parser = parent_parser.add_parser(
        res_short, 
        help=f"{action} a {resource_full}"
    )
    resource_parser.add_argument(
        "name", 
        metavar="NAME", 
        help=f"Name of the {resource_full} to {action}"
    )
    resource_parser.set_defaults(func=func)
    return resource_parser

def read_from_templates(filename):
    byte_stream = pkg_resources.resource_string(
        __name__, f'ecida-templates/{filename}'
    )
    # content = template_path.read().decode('utf-8')  # Ensure to decode if it's in bytes
    return byte_stream.decode("utf-8")  # Decode bytes to string

def write_content_to_file(content, filename):
    output_path = os.path.join(os.getcwd(), filename)
    with open(output_path, 'w') as output_file:
        output_file.write(content)

def create_module_py(args):
    module_name = args.name.lower()
    content = read_from_templates("module.py")
    content = content.replace('MODULE_NAME', module_name)
    write_content_to_file(content,f"{module_name}.py")
        
def create_environemnet_yaml(args):
    namespace_name = args.name.lower()
    content = read_from_templates("namespace.yaml")
    content = content.replace('NAMESPACE_NAME', namespace_name)
    write_content_to_file(content,f"ecida-env-{namespace_name}.yaml")

def copy_from_templates(filename):
    content = read_from_templates(filename)
    write_content_to_file(content,filename)

def init_codebase(args):
    create_module_py(args)
    copy_from_templates("requirements.txt")
    copy_from_templates(".gitignore")
    

def create_deploy_docker_image(imageTag: str, mainfile:str):
    # Define the base image and working directory
    base_image = "python:3.9-slim-buster"
    workdir = "/app"

    # Define the Dockerfile commands
    dockerfile = []
    dockerfile.append(f"FROM {base_image}")
    dockerfile.append(f"WORKDIR {workdir}")
    dockerfile.append("COPY requirements.txt .")
    dockerfile.append("RUN pip install --no-cache-dir -r requirements.txt")
    dockerfile.append("COPY . .")
    dockerfile.append(f"CMD [\"python\", \"{mainfile}\"]")

    # Write the Dockerfile to disk
    with open("Dockerfile", "w") as f:
        f.write("\n".join(dockerfile))

    # Build the Docker image
    
    os.system(f"docker build -t {imageTag} .")
    os.system(f"docker push {imageTag}")
    os.remove("Dockerfile")
    

def apply_yaml(Module, imageTag:str, secret: str, dir_path: str):
    moduleName = f"{Module.name}-{Module.version}"
    files = {}
    
    for key, git in Module.directories.items():
        files[key] = {
            "localPath": key,
        }
        if "source" in git and git["source"] != "":
            git["secret"] = secret
            files[key]["preload"] = {
                "git" : {
                    "source" : git["source"],
                    "folder" : git["folder"],
                    "secret" : git["secret"]
                }
            }
    kafka = {}
    if len(Module.topics_envVars) > 0:
        kafka = {
                    "server": "KAFKA_BOOTSTRAP_SERVER",
                    "securityProtocol": "KAFKA_SECURITY_PROTOCOL",
                    "saslMechanism": "KAFKA_SASL_MECHANISM",
                    "username": "KAFKA_USERNAME",
                    "password": "KAFKA_PASSWORD",
                    "topics": Module.topics_envVars
                }
    
    
    data = {
        "apiVersion": "ecida.org/v5alpha1",
        "kind" : "Module",
        "metadata": {
            "name": moduleName,
            "namespace": "ecida-repository",
            "labels":{
                "template" : "default"
            },
            "annotations" :{
                "description": getattr(Module, "description", "Not Provided")
            }
        },
        "spec":{
          "definitions": {
              "inputs": Module.inputs,
              "outputs": Module.outputs},
          "implementations":{
              "docker": {
                  "image": imageTag
              },
              "kafka":kafka,
              "file" : files,
              "env": {
                  "ECIDA_DEPLOY": "true"
              }
          }
        }
    }
    yamlFilename = f"auto_generated_{moduleName}.yaml"
    path = Path.joinpath(dir_path, yamlFilename)
    with open(path, "w") as f:
        yaml.dump(data, f)
        print(yamlFilename + " is generated")
    
def create_image_tag(username: str, M) -> str:
    imageName = username + "/" + M.name.lower()
    latest_tag, error = docker_interface.fetch_latest_tag(imageName)
    if error == None:
        imageTag, error = docker_interface.increment_tag(latest_tag)
        if error != None:
            imageTag = latest_tag + ".1"
    else:
        imageTag = M.version.lower()
    return imageName + ":" + imageTag

def main():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(prog="ecidacli")
    parser.add_argument("-f", "--main-file", help="main file to process (example: main.py)")
    
    subparsers = parser.add_subparsers(required= True, metavar="COMMAND", title=None, dest="command")
    parser_manifests = subparsers.add_parser('manifests', help='generate the kubernetes manifests')
    parser_build = subparsers.add_parser('build', help='build the container and push it to container registry')
    subparsers.add_parser('version', help='print ecidacli version')
    
    # Add arguments to the parser
    parser_build.add_argument("-u", "--username", help="username for container registry authentication")
    parser_manifests.add_argument("-u", "--username", help="username for container registry authentication")
    parser_manifests.add_argument("-s", "--secret", help="name of secret in the kubernetes-cluster")
    parser_manifests.add_argument("-d", "--dir", help="directory to put yaml files [default: manifests]")

    # Create commands
    create_parser = subparsers.add_parser("create", help="create resources e.g. module and environment")
    create_subparsers = create_parser.add_subparsers(metavar="RESOURCE", title=None, dest="resource")
    add_resource_command(create_subparsers, "create", "module", "module", create_module_py)
    add_resource_command(create_subparsers, "create", "env", "environment", create_environemnet_yaml)

    
    # Init Command
    parser_init = subparsers.add_parser('init', help='Initialize the codebase')
    parser_init.add_argument("name", metavar="NAME", help=f"Name of the first module") 
    parser_init.set_defaults(func=init_codebase)
    
    # Parse the command line arguments
    
    args = parser.parse_args()
    
    # Import the module dynamically
    try:
        if args.command == "manifests":      
            manifests(args)
        elif args.command == "build":
            build(args)
        elif args.command == "version":
            print("ecidacli version: v0.1.11")
        else:
            args.func(args)
            
    except Exception as e:
        print(e)
        # print(f"{mainfile} does not contain an EcidaModule")

def load_function(file_path, func_name):
    with open(file_path, 'r') as f:
        code = f.read()

    tree = ast.parse(code)
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]

    globals_in_module = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    # Check if the value assigned is a plain string (not f-strings or expressions)
                    if isinstance(node.value, ast.Constant):
                        globals_in_module[target.id] = node.value.s  # `s` gives the string value

    
    for func in functions:
        if func.name == func_name:
            # Create a new module with the function definition
            new_code = ast.Module([ast_import_ecida, func], type_ignores=[])
            new_module = compile(new_code, file_path, 'exec')

            # Create a new module object
            spec = importlib.util.spec_from_loader(func_name, loader=None)
            module = importlib.util.module_from_spec(spec)

            # Execute the new module
            exec(new_module, globals_in_module)
            module.__dict__.update(globals_in_module)
            # Return the function
            return getattr(module, func_name)

    raise ValueError(f"Function '{func_name}' not found in file '{file_path}'")

    
def common(main_file: str, username: str):
    func = load_function(main_file, "create_module")
    M = func()
    imageTag = create_image_tag(username, M)
    return M, imageTag
    
def manifests(args):
    # Parsing arguments
    main_file = args.main_file    
    username = args.username
    secret = args.secret
    manifests_dir = args.dir
    if manifests_dir == None:
        manifests_dir = DEFAULTS["manifests_dir"]      
        
    # Creating Module
    M, imageTag = common(main_file, username)
    
    # Creating Path
    dir_path = Path(main_file).parent.absolute()
    dir_path = Path.joinpath(dir_path, manifests_dir)
    dir_path.mkdir(exist_ok=True, parents=True)
    
    # Create and dump yaml
    apply_yaml(M, imageTag, secret,dir_path)
    
    
def build(args):
    # Parsing Arguments
    main_file = args.main_file    
    username = args.username
    
    M, imageTag = common(main_file, username)
    dirname = os.path.dirname(main_file)
    os.chdir(dirname)
    basefile = os.path.basename(main_file)
    create_deploy_docker_image(imageTag, basefile)
    print(f"{main_file} built successfully")
    

if __name__ == "__main__":
    main()

