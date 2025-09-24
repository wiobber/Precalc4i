# debug_openai.py
import openai, inspect, sys, pathlib

print(">>> openai.__file__ :", openai.__file__)          # full path to the module
print(">>> openai.__package__ :", openai.__package__)    # should be 'openai'
print(">>> sys.path[0] :", sys.path[0])                  # current working dir
print(">>> cwd :", pathlib.Path.cwd())
print(">>> has Batch? :", hasattr(openai, "Batch"))
