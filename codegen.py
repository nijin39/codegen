import sys
import application
import json
from jinja2 import Template, Environment, FileSystemLoader
import os

PROJECT_NAME = ""

def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    return Environment(
        loader=FileSystemLoader(path or './')
    ).get_template(filename).render(context)

def create_files(base_directory, entity_name):
    current_directory = os.getcwd()
    base_directory = base_directory
    entity_name = entity_name

    scaffold_file = []
    scaffold_file.append("{}/{}/{}src/main/java/{}/application/{}Service.java"
                         .format(current_directory,PROJECT_NAME,base_directory,entity_name,entity_name.title()))
    scaffold_file.append("{}/{}/{}src/main/java/{}/application/DTO/{}.java"
                         .format(current_directory,PROJECT_NAME,base_directory,entity_name,entity_name.title()+"DTO"))
    scaffold_file.append("{}/{}/{}src/main/java/{}/domain/{}.java"
                         .format(current_directory,PROJECT_NAME,base_directory,entity_name,entity_name.title()))
    scaffold_file.append("{}/{}/{}src/main/java/{}/domain/{}Repository.java"
                         .format(current_directory,PROJECT_NAME,base_directory,entity_name,entity_name.title()))
    scaffold_file.append("{}/{}/{}src/main/java/{}/ui/{}Resource.java"
                         .format(current_directory,PROJECT_NAME,base_directory,entity_name,entity_name.title()))


    for filename in scaffold_file:
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise


    #with open("foo.txt", "w") as f:
    #    f.write(result)

def readConfig():
    with open('filesystem.json', 'r') as f:
        config = json.load(f)

    base_directory = config['codegen']['packageFolder']
    global PROJECT_NAME
    PROJECT_NAME = config['projectName']
    return base_directory


if __name__ == '__main__':
    env = sys.argv[1] if len(sys.argv) > 2 else 'dev'
    
    if env == 'dev':
        config = application.DevelopmentConfig
    elif env == 'test':
        config = application.TestConfig
    elif env == 'prod':
        config = application.ProductionConfig
    else:
        raise ValueError('Invalid environment name')
   
    ci = application.CIConfig
   
    context = {
    'firstname': 'John',
    'lastname': 'Doe'
    }
    result = render('/home/tandem/DEV/codegen/codegen/test.tpl', context)

    base_directory = readConfig()

    create_files(base_directory,"user")
