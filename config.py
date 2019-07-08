#!/usr/bin/python

# Separated unit for configuration, in case we have extra features in the future.
from workflow import Workflow3 as Workflow
from lib.config import Config
from workflow.notify import notify

def main(workflow):
    path=workflow.args[0].strip()
    config=Config(path)
    if config.validate():
        # Behavior: overwrite existing data
        workflow.store_data("configuration", config)
        notify(title="Success!", text="Cheat sheets updated to {}".format(config.getPath()))
    else:
        notify(title="Error:(", text="The path doesn't exist")
    return 0

if __name__=="__main__":
    workflow=Workflow()
    exit(workflow.run(main))
