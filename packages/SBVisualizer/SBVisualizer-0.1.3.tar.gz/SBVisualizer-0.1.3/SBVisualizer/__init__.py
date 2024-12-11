# __init__.py

from SBVisualizer.Visualizer import Visualizer

# You can also add other functions or variables if needed
try:
  import tellurium
  import SBMLDiagrams
except ImportError as error:
  print ("The tests rely on tellurium and SBMLDiagrams to construct the models")
  print ("Since tellurium and SBMLDiagrams are not installed the tests can't be run")
  print ("If you want to run the tests, pip install tellurium and SBMLDiagrams first")