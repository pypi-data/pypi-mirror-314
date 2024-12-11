# How to test plots
# have the plot function return data
# ex. histogram function in numpy that returns arrays
# smoke test - does it throw an exception?
# if there is no data to return
# if is_plot is True - shows the plot
# if false - doesn't show the plot


# Write program to change thickness of lines
# Set the flux of one species and the rest of the species follow
# Get the fluxes of all the species
# Set the line thickness of one of the fluxes
  # the other ones scale to that one
import SBMLDiagrams as sb
class Visualizer:
  # Initializer
  # Attributes: r
  def __init__(self, r=None, colors=None):
    # assume that r = teloada already happened
    self.r = r
    self.colors = colors if colors is not None else {}
    self.line_thickness = {}
    self.sb = None

  # Loads into SBML
  def loadIntoSBML(self):
    # loads in to SBML
    sbml = self.r.getSBML()
    self.sb = sb.load(sbml)

  # Get fluxes
  # returns a dict: key-species, value-flux
  def get_fluxes(self)->dict:
    '''
    Get the fluxes of all the species
    Returns: 
      dictionary with the rxn name and flux
    '''
    fluxes = {} # Rxn name:flux
    reaction_ids = self.r.getReactionIds()
    rxn_rates = self.r.getReactionRates()
    fluxes = {rxn: rate for rxn, rate in zip(reaction_ids, rxn_rates)}
    return fluxes
  
  from math import isnan  # Importing the isnan function from the math module

  def get_line_thickness(self, rxn_name: str, thickness: float) -> dict:
    """
    Adjusts the line thickness for all reactions based on the selected reaction's flux
    and scales them between a minimum of 0.1 and a maximum of 50.
    Args:
        rxn_name (str): The name of the reaction for which the thickness is being set.
        thickness (float): The desired thickness for the specified reaction.
    Returns:
        dict: A dictionary mapping reaction names to their corresponding scaled line thicknesses.
    """
    fluxes = self.get_fluxes()
    max_thickness = 50.0
    min_thickness = 0.1

    # Validate the input reaction: ensure the flux is non-zero
    if fluxes[rxn_name] == 0:
        raise ValueError(f"Reaction '{rxn_name}' has zero flux, cannot scale thickness.")
    # Check for edge case: If all fluxes are zero or invalid, raise an error
    if len(fluxes) == 0:
        raise ValueError("All reactions have invalid or zero flux; cannot scale thicknesses.")
    # Calculate the minimum and maximum flux values
    max_flux = max(abs(flux) for flux in fluxes.values())
    min_flux = min(abs(flux) for flux in fluxes.values())
    # Map fluxes to the desired thickness range [min_thickness, max_thickness]
    self.line_thickness = {}
    for rxn, flux in fluxes.items():
        if flux != 0:
            # Normalize flux to the range [0, 1] based on the min and max flux
            normalized_flux = (abs(flux) - min_flux) / (max_flux - min_flux)  # Normalize flux
            # Scale the normalized flux to the desired thickness range
            self.line_thickness[rxn] = min_thickness + normalized_flux * (max_thickness - min_thickness)
        else:
            # Assign the minimum thickness for zero-flux reactions
            self.line_thickness[rxn] = min_thickness
    return self.line_thickness


  
  def set_line_thickness(self, line_thicknesses:dict):
    '''
    Sets the line thickness with SBMLDiagrams. User gets the line thicknesses and 
    saves them to a dict. Then the user loads them to set the thickness

    Args:
        line_thicknesses (dict): A dictionary where keys are reaction names and values 
        are their corresponding line thicknesses.
    '''
    for rxn_name, thickness in line_thicknesses.items():
      if not self.sb:
            raise RuntimeError("SBMLDiagrams object not initialized. Call loadIntoSBML() first.")
      for rxn_name, thickness in line_thicknesses.items():
          self.sb.setReactionLineThickness(rxn_name, thickness)
        
  # Decide on the color scheme for fluxes
  # Positive flux color gradient - Green (low) to red (high)
  # Negative flux color gradient - Green (low) to blue (high)
  # Take the system and find the max flux

  def get_color_gradient(self):
    '''
    Assigns a color to each species 
    Args: 
        None
    Retuns:
        A dictionary with reaction names as keys and RGB value tuples as values.
    '''
    fluxes = self.get_fluxes() # dict
    abs_fluxes = [abs(value) for value in fluxes.values()]
    max_flux = max(abs_fluxes)

    colors_dict = {}

    for rxn_name, flux in fluxes.items():
      # Positive and 0 flux
      if flux >= 0:
        factor = flux / max_flux
        rgb_vector = (255 * factor, 255 * (1 - factor), 0)   

      # Negative flux
      else:
        factor = abs(flux) / max_flux
        rgb_vector = (0, 255 * (1-factor), 255 * factor)
      colors_dict[rxn_name] = tuple(map(int, rgb_vector))
    return colors_dict

  def extract_rgb_values(self, rxn_name:str)->tuple:
    """
    Extracts the RGB values for a single reaction from a color gradient.
    Args:
        rxn_name (str): The name of the reaction to extract RGB values for.
    Returns:
        tuple: A tuple containing the (red, green, blue) values for the specified reaction.
    """
    colors_dict = self.make_color_gradient()  
    if rxn_name not in colors_dict:
        raise ValueError(f"Reaction '{rxn_name}' not found in the color gradient.")   
    return colors_dict[rxn_name]
  
  def rgb_to_hex(self, rgb_tuple)->str:
    """
    Converts RGB values to a hexadecimal color code.
    Args:
        rgb_tuple (tuple): A tuple containing (red, green, blue) values.
    Returns:
        str: The corresponding hexadecimal color code.
    """
    r, g, b = rgb_tuple
    if any(not (0 <= val <= 255) for val in (r, g, b)):
        raise ValueError("RGB values must be in the range 0-255")
    return f'#{r:02X}{g:02X}{b:02X}'
  
  def set_colors(self):
    """
    Sets the fill colors for reactions in the SBML model based on their fluxes.
    Args:
        None
    Returns:
        None
    """
    if not self.sb:
      raise RuntimeError("SBMLDiagrams object not initialized. Call loadIntoSBML() first.")
    colors_dict = self.get_color_gradient()
    for rxn_name, rgb_tuple in colors_dict.items():
      hex_color = self.rgb_to_hex(rgb_tuple) 
      self.sb.setReactionFillColor(rxn_name, hex_color)
      self.sb.setReactionArrowHeadFillColor(rxn_name, hex_color)
  
  def draw(self, output_fileName: str):
    '''
    Draws the full SBML model
    Args: 
      Name of the file it draws the program in 
    '''
    self.sb.draw(output_fileName=output_fileName)