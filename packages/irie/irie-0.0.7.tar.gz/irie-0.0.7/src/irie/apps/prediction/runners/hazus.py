"""
From [1] Section 7.1.3 and [2] Section 9.1:
Bridges are classified based on the following structural characteristics: 
- Seismic Design 
- Number of spans: single vs. multiple span bridges 
- Structure type: concrete, steel, and others 
- Pier type: multiple column bents, single column bents, and pier walls 
- Abutment type and bearing type: monolithic vs. non-monolithic, high rocker bearings, low 
steel bearings, and neoprene rubber bearings 
- Span continuity: continuous, discontinuous (in-span hinges), and simply supported 

The seismic design of a bridge is taken into account in terms of the 
(i) spectrum modification factor, 
(ii) strength reduction factor due to cyclic motion, 
(iii) drift limits, and 
(iv) the longitudinal reinforcement ratio. 

[1] Hazus earthquake technical manual
    https://www.fema.gov/sites/default/files/2020-10/fema_hazus_earthquake_technical_manual_4-2.pdf

[2] Hazus inventory technical manual
    https://www.fema.gov/sites/default/files/documents/fema_hazus-6-inventory-technical-manual.pdf

[3] Mander and Basoz
    https://www.researchgate.net/profile/Jb-Mander/publication/292691534_Seismic_fragility_curve_theory_for_highway_bridges/links/5a7346d7aca2720bc0dbb653/Seismic-fragility-curve-theory-for-highway-bridges.pdf

-------------------------------------------

Table 9-6 in [2] (also 7-1 in [1])

HWB1    All    Non-CA <  1990 N/A > 150 N/A EQ1 0 Conventional Major Bridge - Length >  150 meters 
        All    CA     <  1975 N/A > 150 N/A EQ1 0 Conventional Major Bridge - Length >  150 meters 
HWB2    All    Non-CA >= 1990 N/A > 150 N/A EQ1 0 Seismic      Major Bridge - Length >  150 meters 
        All    CA     >= 1975 N/A > 150 N/A EQ1 0 Seismic      Major Bridge - Length >  150 meters 
HWB3    All    Non-CA <  1990   1   N/A N/A EQ1 1 Conventional Single Span 
        All    CA     <  1975   1   N/A N/A EQ1 1 Conventional Single Span 
HWB4    All    Non-CA >= 1990   1   N/A N/A EQ1 1 Seismic      Single Span 
        All    CA     >= 1975   1   N/A N/A EQ1 1 Seismic      Single Span 
HWB5  101 106  Non-CA <  1990 N/A   N/A N/A EQ1 0 Conventional Multi-Col. Bent, Simple  Support - Concrete 
HWB6  101 106  CA     <  1975 N/A   N/A N/A EQ1 0 Conventional Multi-Col. Bent, Simple  Support - Concrete 
HWB7  101 106  Non-CA >= 1990 N/A   N/A N/A EQ1 0 Seismic      Multi-Col. Bent, Simple  Support - Concrete 
      101 106  CA     >= 1975 N/A   N/A N/A EQ1 0 Seismic      Multi-Col. Bent, Simple  Support - Concrete
HWB8  205 206  CA     <  1975 N/A   N/A N/A EQ2 0 Conventional Single Col., Box Girder -  Continuous Concrete 
HWB9  205 206  CA     >= 1975 N/A   N/A N/A EQ3 0 Seismic      Single Col., Box Girder -  Continuous Concrete 
HWB10 201 206  Non-CA <  1990 N/A   N/A N/A EQ2 1 Conventional Continuous Concrete 
      201 206  CA     <  1975 N/A   N/A N/A EQ2 1 Conventional Continuous Concrete 
HWB11 201 206  Non-CA >= 1990 N/A   N/A N/A EQ3 1 Seismic      Continuous Concrete 
      201 206  CA     >= 1975 N/A   N/A N/A EQ3 1 Seismic      Continuous Concrete 
HWB12 301 306  Non-CA <  1990 N/A   N/A No  EQ4 0 Conventional Multi-Col. Bent, Simple  Support - Steel 
HWB13 301 306  CA     <  1975 N/A   N/A No  EQ4 0 Conventional Multi-Col. Bent, Simple  Support - Steel 
HWB14 301 306  Non-CA >= 1990 N/A   N/A N/A EQ1 0 Seismic      Multi-Col. Bent, Simple  Support - Steel 
      301 306  CA     >= 1975 N/A   N/A N/A EQ1 0 Seismic      Multi-Col. Bent, Simple  Support - Steel 
HWB15 402 410  Non-CA <  1990 N/A   N/A No  EQ5 1 Conventional Continuous Steel 
      402 410  CA     <  1975 N/A   N/A No  EQ5 1 Conventional Continuous Steel 
HWB16 402 410  Non-CA >= 1990 N/A   N/A N/A EQ3 1 Seismic      Continuous Steel 
      402 410  CA     >= 1975 N/A   N/A N/A EQ3 1 Seismic      Continuous Steel 
HWB17 501 506  Non-CA <  1990 N/A   N/A N/A EQ1 0 Conventional Multi-Col. Bent, Simple  Support - Prestressed  Concrete 
HWB18 501 506  CA     <  1975 N/A   N/A N/A EQ1 0 Conventional Multi-Col. Bent, Simple  Support - Prestressed  Concrete 
HWB19 501 506  Non-CA >= 1990 N/A   N/A N/A EQ1 0 Seismic      Multi-Col. Bent, Simple  Support - Prestressed  Concrete
      501 506  CA     >= 1975 N/A   N/A N/A EQ1 0 Seismic      Multi-Col. Bent, Simple  Support - Prestressed  Concrete 
HWB20 605 606  CA     <  1975 N/A   N/A N/A EQ2 0 Conventional Single Col., Box Girder -  Prestressed Continuous  Concrete 
HWB21 605 606  CA     >= 1975 N/A   N/A N/A EQ3 0 Seismic      Single Col., Box Girder -  Prestressed Continuous  Concrete 
HWB22 601 607  Non-CA <  1990 N/A   N/A N/A EQ2 1 Conventional Continuous Concrete
      601 607  CA     <  1975 N/A   N/A N/A EQ2 1 Conventional Continuous Concrete
HWB23 601 607  Non-CA >= 1990 N/A   N/A N/A EQ3 1 Seismic      Continuous Concrete
      601 607  CA     >= 1975 N/A   N/A N/A EQ3 1 Seismic      Continuous Concrete 
HWB24 301 306  Non-CA <  1990 N/A   N/A Yes EQ6 0 Conventional Multi-Col. Bent, Simple  Support - Steel 
HWB25 301 306  CA     <  1975 N/A   N/A Yes EQ6 0 Conventional Multi-Col. Bent, Simple  Support - Steel 
HWB26 402 410  Non-CA <  1990 N/A   N/A Yes EQ7 1 Conventional Continuous Steel 
HWB27 402 410  CA     <  1975 N/A   N/A Yes EQ7 1 Conventional Continuous Steel 
HWB28 N/A N/A All other bridges that are not classified 


--------------------------

Table 9-7: Hazus Highway System Classification

HWB1  Major Bridge - Length > 150 meters (Conventional Design) 
HWB2  Major Bridge - Length > 150 meters (Seismic Design) 
HWB3  Single Span - (Not HWB1 or HWB2) (Conventional Design) 
HWB4  Single Span - (Not HWB1 or HWB2) (Seismic Design) 
HWB5  Concrete, Multi-Column Bent, Simple Support (Conventional Design), Non-California (Non CA) 
HWB6  Concrete, Multi-Column Bent, Simple Support (Conventional Design), California (CA) 
HWB7  Concrete, Multi-Column Bent, Simple Support (Seismic Design) 
HWB8  Continuous Concrete, Single Column, Box Girder (Conventional Design) 
HWB9  Continuous Concrete, Single Column, Box Girder (Seismic Design) 
HWB10 Continuous Concrete, (Not HWB8 or HWB9) (Conventional Design) 
HWB11 Continuous Concrete, (Not HWB8 or HWB9) (Seismic Design) 
HWB12 Steel, Multi-Column Bent, Simple Support (Conventional Design), Non-California (Non-CA) 
HWB13 Steel, Multi-Column Bent, Simple Support (Conventional Design), California (CA) 
HWB14 Steel, Multi-Column Bent, Simple Support (Seismic Design) 
HWB15 Continuous Steel (Conventional Design) 
HWB16 Continuous Steel (Seismic Design) 
HWB17 PS Concrete Multi-Column Bent, Simple Support (Conventional Design), Non-California  
HWB18 PS Concrete, Multi-Column Bent, Simple Support (Conventional Design), California (CA) 
HWB19 PS Concrete, Multi-Column Bent, Simple Support (Seismic Design) 
HWB20 PS Concrete, Single Column, Box Girder (Conventional Design) 
HWB21 PS Concrete, Single Column, Box Girder (Seismic Design)
HWB22 Continuous Concrete, (Not HWB20/HWB21) (Conventional Design) 
HWB23 Continuous Concrete, (Not HWB20/HWB21) (Seismic Design) 
HWB24 Same definition as HWB12 except the bridge length is less than 20 meters 
HWB25 Same definition as HWB13 except the bridge length is less than 20 meters 
HWB26 Same definition as HWB15 except the bridge length is less than 20 meters and Non-CA 
HWB27 Same definition as HWB15 except the bridge length is less than 20 meters and in CA 
HWB28 All other bridges that are not classified (including wooden bridges)


-----------------------------

Table 7-6 Fragility Function Median Values for Highway Bridges 

HWB1  0.40 0.50 0.70 0.90 3.9 3.9 3.9 13.8 
HWB2  0.60 0.90 1.10 1.70 3.9 3.9 3.9 13.8 
HWB3  0.80 1.00 1.20 1.70 3.9 3.9 3.9 13.8 
HWB4  0.80 1.00 1.20 1.70 3.9 3.9 3.9 13.8 
HWB5  0.25 0.35 0.45 0.70 3.9 3.9 3.9 13.8 
HWB6  0.30 0.50 0.60 0.90 3.9 3.9 3.9 13.8 
HWB7  0.50 0.80 1.10 1.70 3.9 3.9 3.9 13.8 
HWB8  0.35 0.45 0.55 0.80 3.9 3.9 3.9 13.8 
HWB9  0.60 0.90 1.30 1.60 3.9 3.9 3.9 13.8 
HWB10 0.60 0.90 1.10 1.50 3.9 3.9 3.9 13.8 
HWB11 0.90 0.90 1.10 1.50 3.9 3.9 3.9 13.8 
HWB12 0.25 0.35 0.45 0.70 3.9 3.9 3.9 13.8 
HWB13 0.30 0.50 0.60 0.90 3.9 3.9 3.9 13.8 
HWB14 0.50 0.80 1.10 1.70 3.9 3.9 3.9 13.8 
HWB15 0.75 0.75 0.75 1.10 3.9 3.9 3.9 13.8 
HWB16 0.90 0.90 1.10 1.50 3.9 3.9 3.9 13.8 
HWB17 0.25 0.35 0.45 0.70 3.9 3.9 3.9 13.8 
HWB18 0.30 0.50 0.60 0.90 3.9 3.9 3.9 13.8 
HWB19 0.50 0.80 1.10 1.70 3.9 3.9 3.9 13.8 
HWB20 0.35 0.45 0.55 0.80 3.9 3.9 3.9 13.8 
HWB21 0.60 0.90 1.30 1.60 3.9 3.9 3.9 13.8 
HWB22 0.60 0.90 1.10 1.50 3.9 3.9 3.9 13.8 
HWB23 0.90 0.90 1.10 1.50 3.9 3.9 3.9 13.8 
HWB24 0.25 0.35 0.45 0.70 3.9 3.9 3.9 13.8 
HWB25 0.30 0.50 0.60 0.90 3.9 3.9 3.9 13.8 
HWB26 0.75 0.75 0.75 1.10 3.9 3.9 3.9 13.8 
HWB27 0.75 0.75 0.75 1.10 3.9 3.9 3.9 13.8 
HWB28 0.80 1.00 1.20 1.70 3.9 3.9 3.9 13.8 
"""
import math
from scipy.stats import norm

Slight, Moderate, Extensive, Complete = range(4)

# State codes; We'll add more later, right now we assume
# everything is in California
class StateCodes:
    California = 22

def hazus_fragility(
    nbi_data: dict,
    pga: float = 0.5,  # Peak Ground Acceleration (g)
    sa_03s: float = 1.1,  # Spectral Acceleration at 0.3 seconds (g)
    sa_10s: float = 1.4,  # Spectral Acceleration at 1.0 seconds (g)
    soil_type: str = "B",  # Soil classification ("A", "B", "C", "D", "E")
    level: int = None,  # Optional: Specify a damage state (0 = Slight, 1 = Moderate, etc.)
    generate_plot: bool = False,  # Generate fragility curve plot
    return_data: bool = False
) -> dict:
    """
    Compute fragility probabilities for a given bridge using the Hazus methodology.

    Args:
    - nbi_data (dict): NBI data containing bridge-specific properties.
    - pga (float): Peak Ground Acceleration (g).
    - sa_03s (float): Spectral Acceleration at 0.3 seconds (g).
    - sa_10s (float): Spectral Acceleration at 1.0 seconds (g).
    - soil_type (str): Soil classification ("A", "B", "C", "D", "E").
    - level (int): Specify a damage state (0 = Slight, 1 = Moderate, etc.) (optional).
    - generate_plot (bool): Whether to generate and return fragility curve plots.

    Returns:
    - dict: Fragility probabilities for all damage states, optionally with fragility curve plot.
    - float: Probability for the specified damage state (if `level` is provided).
    """
    # Step 0: Extract relevant bridge properties
    properties = _bridge_info(nbi_data)

    # Step 1: Determine Hazus bridge type
    hazus_type: int = _hazus_type(properties)
    if hazus_type == -1:
        raise ValueError("Bridge type not found in Hazus classification")

    # Step 2: Call _hazus_curve to compute fragility probabilities
    fragility_probs = _hazus_curve(hazus_type, properties, pga, sa_03s, sa_10s, soil_type)

    # Step 3: Generate fragility curve plot if requested
    if generate_plot or return_data:
        # Adjust sa_range to start from 0
        sa_range = [0.0] + [0.1 * i for i in range(1, 21)]  # Include 0 explicitly

        curves = {state: [] for state in fragility_probs.keys()}

        # Generate fragility values, handling the case for Sa = 0
        for sa in sa_range:
            for state in fragility_probs.keys():
                median = get_old_medians(hazus_type)[state]
                dispersion = 0.6  # β (dispersion factor)
                curves[state].append(
                    norm.cdf((math.log(sa / median)) / dispersion) if sa > 0 else 0
                )
        
        if return_data:
            fragility_probs["curves"] = curves 
            fragility_probs["sa_range"] = sa_range

    # Step 4: Handle `level` as an integer
    damage_states = ["Slight", "Moderate", "Extensive", "Complete"]
    if level is not None:
        if level not in range(4):
            raise ValueError(f"Invalid level: {level}. Must be an integer in range(4).")
        damage_state = damage_states[level]
        return fragility_probs[damage_state]

    # Step 5: Return all probabilities and optionally the plot
    return fragility_probs


def _bridge_info(nbi: dict) -> dict:
    """
    Safely extract bridge properties, handling undefined skew angles and other placeholders.
    """
    try:
        nbi_bridge = nbi.get("NBI_BRIDGE", {})
        nbi_superstructure = nbi.get("NBI_SUPERSTRUCTURE_DECK", {})

        # Parse "Skew Angle"
        skew_angle_str = nbi_bridge.get("Skew Angle", "0")
        if "99" in skew_angle_str:  # Handle undefined skew
            skew_angle = 0
        else:
            skew_angle = float(skew_angle_str.split(" - ")[0])

        return {
            "state_code":      StateCodes.California,
            "year_built":      int(nbi_bridge.get("Year Built", 0)),
            "skew_angle":      skew_angle,
            "service_type":    int(
                nbi_bridge.get("Type of Service on Bridge Code", "0 - Unknown").split(" - ")[0]
                + nbi_bridge.get("Type Of Service Under Bridge Code", "0 - Unknown").split(" - ")[0]
            ),
            "material_flag":   int(nbi_superstructure.get("Main Span Material", "0 - Unknown").split(" - ")[0]),
            "geometry_flag":   int(nbi_superstructure.get("Main Span Design", "0 - Unknown").split(" - ")[0]),
            "span_count":      int(nbi_superstructure.get("Number of Spans in Main Unit", 0)),
            "approach_spans":  int(nbi_superstructure.get("Number of Approach Spans", 0)),
            "max_span_length": float(nbi_bridge.get("Length of Maximum Span", 0.0)),
            "total_length":    float(nbi_bridge.get("Structure Length", 0.0)),
            "deck_width":      float(nbi_bridge.get("Deck Width - Out to Out", 0.0)),
        }
    except ValueError as e:
        raise ValueError(f"Error processing NBI data: {e}")




def _hazus_curve(type: int, properties: dict, pga: float, sa_03s: float, sa_10s: float, soil_type: str) -> dict:
    """
    Compute fragility probabilities for the four damage states and optionally generate fragility curves.

    Args:
    - type (int): Bridge classification (integer from 1 to 28).
    - properties (dict): Dictionary containing bridge-specific properties.
    - pga (float): Peak Ground Acceleration (g).
    - sa_03s (float): Spectral Acceleration at 0.3 seconds (g).
    - sa_10s (float): Spectral Acceleration at 1.0 seconds (g).
    - soil_type (str): Soil classification ("A", "B", "C", "D", "E").
    - generate_curve (bool): If True, generate and display fragility curves.

    Returns:
    - dict: Fragility probabilities for Slight, Moderate, Extensive, and Complete damage states.
    """
    # Validate inputs
    required_keys = {"span_count", "skew_angle"}
    missing_keys = required_keys - properties.keys()
    if missing_keys:
        raise ValueError(f"Missing required properties: {missing_keys}")

    valid_soil_types = {"A", "B", "C", "D", "E"}
    if soil_type not in valid_soil_types:
        raise ValueError(f"Invalid soil type: {soil_type}. Must be one of {valid_soil_types}.")

    span_count = properties["span_count"]
    skew_angle = properties["skew_angle"]

    # Call modify_ground_motion to get the modified values
    modified_values = modify_ground_motion(pga, sa_03s, sa_10s, soil_type)
    modified_pga = modified_values['modified_pga']
    modified_sa_03s = modified_values['modified_sa_03s']
    modified_sa_10s = modified_values['modified_sa_10s']

    # Compute K_skew, K_shape, K3D
    K_skew = math.sqrt(math.sin(math.radians(90 - skew_angle)))
    if modified_sa_03s == 0:
        raise ValueError("Modified Sa(0.3 sec) cannot be zero.")
    K_shape = (2.5 * modified_sa_10s) / modified_sa_03s
    A, B = get_a_b(type)
    if span_count - B == 0:
        raise ValueError("Invalid span count resulting in division by zero.")
    K3D = 1 + A / (span_count - B)

    # Retrieve old medians and compute new medians
    old_medians = get_old_medians(type)
    I_shape = get_i_shape(type)
    factor_slight = 1 if I_shape == 0 else min(1, K_shape)

    new_medians = {"Slight": old_medians["Slight"] * factor_slight}
    damage_states = ["Moderate", "Extensive", "Complete"]
    new_medians.update(
        {state: old_medians[state] * K_skew * K3D for state in damage_states}
    )

    # Compute fragility probabilities
    def compute_probability(sa: float, median: float, beta: float = 0.6) -> float:
        return norm.cdf((math.log(sa / median)) / beta)

    if modified_sa_10s <= 0:
        raise ValueError("Modified Sa(1.0 sec) must be positive.")
    fragility_probs = {
        state: compute_probability(modified_sa_10s, median)
        for state, median in new_medians.items()
    }

    return fragility_probs


def modify_ground_motion(pga: float, sa_03s: float, sa_10s: float, soil_type: str) -> dict:
    """
    Modify PGA, Sa(0.3 sec), and Sa(1.0 sec) based on soil amplification factors (Table 4.7).

    Inputs:
    - pga (float): Peak Ground Acceleration (g).
    - sa_03s (float): Spectral Acceleration at 0.3 seconds (g).
    - sa_10s (float): Spectral Acceleration at 1.0 seconds (g).
    - soil_type (str): Soil classification ("A", "B", "C", "D", "E").

    Returns:
    - dict: Modified PGA, Sa(0.3 sec), and Sa(1.0 sec).
    """

    # Amplification factors for each parameter
    amplification_factors = {
        "FPGA": [
            (0.1, {"A": 0.8, "B": 0.9, "C": 1.3, "D": 1.6, "E": 2.4}),
            (0.2, {"A": 0.8, "B": 0.9, "C": 1.2, "D": 1.4, "E": 1.9}),
            (0.3, {"A": 0.8, "B": 0.9, "C": 1.2, "D": 1.3, "E": 1.6}),
            (0.4, {"A": 0.8, "B": 0.9, "C": 1.2, "D": 1.2, "E": 1.4}),
            (0.5, {"A": 0.8, "B": 0.9, "C": 1.2, "D": 1.1, "E": 1.2}),
            (0.6, {"A": 0.8, "B": 0.9, "C": 1.2, "D": 1.1, "E": 1.1}),
        ],
        "FA": [
            (0.25, {"A": 0.8, "B": 0.9, "C": 1.3, "D": 1.6, "E": 2.4}),
            (0.5, {"A": 0.8, "B": 0.9, "C": 1.3, "D": 1.4, "E": 1.7}),
            (0.75, {"A": 0.8, "B": 0.9, "C": 1.2, "D": 1.2, "E": 1.3}),
            (1.0, {"A": 0.8, "B": 0.9, "C": 1.2, "D": 1.1, "E": 1.1}),
            (1.25, {"A": 0.8, "B": 0.9, "C": 1.2, "D": 1.0, "E": 0.9}),
            (1.5, {"A": 0.8, "B": 0.9, "C": 1.2, "D": 1.0, "E": 0.8}),
        ],
        "FV": [
            (0.1, {"A": 0.8, "B": 0.8, "C": 1.5, "D": 2.4, "E": 4.2}),
            (0.2, {"A": 0.8, "B": 0.8, "C": 1.5, "D": 2.2, "E": 3.3}),
            (0.3, {"A": 0.8, "B": 0.8, "C": 1.5, "D": 2.0, "E": 2.8}),
            (0.4, {"A": 0.8, "B": 0.8, "C": 1.5, "D": 1.9, "E": 2.4}),
            (0.5, {"A": 0.8, "B": 0.8, "C": 1.5, "D": 1.8, "E": 2.2}),
            (0.6, {"A": 0.8, "B": 0.8, "C": 1.4, "D": 1.7, "E": 2.0}),
        ],
    }

    def get_factor(value, factor_type):
        rows = amplification_factors[factor_type]
        # Below minimum threshold
        if value <= rows[0][0]:
            return rows[0][1][soil_type]
        # Above maximum threshold
        if value > rows[-1][0]:
            return rows[-1][1][soil_type]
        # Linear interpolation for intermediate values
        for i in range(len(rows) - 1):
            lower_bound, lower_factors = rows[i]
            upper_bound, upper_factors = rows[i + 1]
            if lower_bound < value <= upper_bound:
                lower_factor = lower_factors[soil_type]
                upper_factor = upper_factors[soil_type]
                # Interpolate
                return lower_factor + (upper_factor - lower_factor) * (value - lower_bound) / (upper_bound - lower_bound)
        raise ValueError("Interpolation failed unexpectedly.")

    # Calculate modified values
    modified_pga = pga * get_factor(pga, "FPGA")
    modified_sa_03s = sa_03s * get_factor(sa_03s, "FA")
    modified_sa_10s = sa_10s * get_factor(sa_10s, "FV")

    return {"modified_pga": modified_pga,
        "modified_sa_03s": modified_sa_03s,
        "modified_sa_10s": modified_sa_10s,
    }

def get_a_b(bridge_type: int) -> tuple:
    """
    Retrieve coefficients A and B for K3D calculation based on bridge type.

    Args:
    - bridge_type (int): The bridge type (integer between 1 and 28).

    Returns:
    - tuple: Coefficients (A, B) corresponding to the bridge type's equation.
    """
    # Mapping of equations to A and B values from Table 7-2
    equation_to_ab = {
        "EQ1": (0.25, 1),
        "EQ2": (0.33, 0),
        "EQ3": (0.33, 1),
        "EQ4": (0.09, 1),
        "EQ5": (0.05, 0),
        "EQ6": (0.20, 1),
        "EQ7": (0.10, 0),
    }

    # Map bridge type to equations from Table 7-1
    bridge_to_equation = {
        1: "EQ1", 2: "EQ1", 3: "EQ1", 4: "EQ1", 5: "EQ1", 6: "EQ1", 7: "EQ1", 8: "EQ2", 9: "EQ3", 10: "EQ2",
        11: "EQ3", 12: "EQ4", 13: "EQ4", 14: "EQ1", 15: "EQ5", 16: "EQ3", 17: "EQ1", 18: "EQ1", 19: "EQ1",
        20: "EQ2", 21: "EQ3", 22: "EQ2", 23: "EQ3", 24: "EQ6", 25: "EQ6", 26: "EQ7", 27: "EQ7",
    }

    # Get the equation for the bridge type
    equation = bridge_to_equation.get(bridge_type)
    if not equation:
        raise ValueError(f"Unknown bridge type: {bridge_type}")

    # Retrieve and return A and B values
    return equation_to_ab[equation]

def get_i_shape(bridge_type: int) -> int:
    """
    Retrieve I_shape (indicator for skew effects) for the given bridge type
    from Table 7-1.

    Args:
    - bridge_type (int): The bridge type (integer from 1 to 28).

    Returns:
    - int: I_shape value (0 or 1) based on Table 7-1.
    """
    # Mapping of bridge types to I_shape values from Table 7-1
    i_shape_mapping = {
        1: 0, 2: 0, 3: 1, 4: 1, 5: 0, 6: 0,
        7: 0, 8: 0, 9: 0, 10: 1, 11: 1, 12: 0,
        13: 0, 14: 0, 15: 1, 16: 1, 17: 0, 18: 0,
        19: 0, 20: 0, 21: 0, 22: 1, 23: 1, 24: 0,
        25: 0, 26: 1, 27: 1,
    }

    if bridge_type not in i_shape_mapping:
        raise ValueError(f"Unknown bridge type: {bridge_type}")

    return i_shape_mapping[bridge_type]

def get_old_medians(bridge_type: int) -> dict:
    """
    Retrieve the old medians for Slight, Moderate, Extensive, and Complete damage states
    from Table 7-6 based on the bridge type.

    Args:
    - bridge_type (int): The bridge type (integer from 1 to 28).

    Returns:
    - dict: Old median values for each damage state.
    """
    old_medians = {
        1: {"Slight": 0.40, "Moderate": 0.50, "Extensive": 0.70, "Complete": 0.90},
        2: {"Slight": 0.60, "Moderate": 0.90, "Extensive": 1.10, "Complete": 1.70},
        3: {"Slight": 0.80, "Moderate": 1.00, "Extensive": 1.20, "Complete": 1.70},
        4: {"Slight": 0.80, "Moderate": 1.00, "Extensive": 1.20, "Complete": 1.70},
        5: {"Slight": 0.25, "Moderate": 0.35, "Extensive": 0.45, "Complete": 0.70},
        6: {"Slight": 0.30, "Moderate": 0.50, "Extensive": 0.60, "Complete": 0.90},
        7: {"Slight": 0.50, "Moderate": 0.80, "Extensive": 1.10, "Complete": 1.70},
        8: {"Slight": 0.35, "Moderate": 0.45, "Extensive": 0.55, "Complete": 0.80},
        9: {"Slight": 0.60, "Moderate": 0.90, "Extensive": 1.30, "Complete": 1.60},
        10: {"Slight": 0.60, "Moderate": 0.90, "Extensive": 1.10, "Complete": 1.50},
        11: {"Slight": 0.90, "Moderate": 0.90, "Extensive": 1.10, "Complete": 1.50},
        12: {"Slight": 0.25, "Moderate": 0.35, "Extensive": 0.45, "Complete": 0.70},
        13: {"Slight": 0.30, "Moderate": 0.50, "Extensive": 0.60, "Complete": 0.90},
        14: {"Slight": 0.50, "Moderate": 0.80, "Extensive": 1.10, "Complete": 1.70},
        15: {"Slight": 0.75, "Moderate": 0.75, "Extensive": 0.75, "Complete": 1.10},
        16: {"Slight": 0.90, "Moderate": 0.90, "Extensive": 1.10, "Complete": 1.50},
        17: {"Slight": 0.25, "Moderate": 0.35, "Extensive": 0.45, "Complete": 0.70},
        18: {"Slight": 0.30, "Moderate": 0.50, "Extensive": 0.60, "Complete": 0.90},
        19: {"Slight": 0.50, "Moderate": 0.80, "Extensive": 1.10, "Complete": 1.70},
        20: {"Slight": 0.35, "Moderate": 0.45, "Extensive": 0.55, "Complete": 0.80},
        21: {"Slight": 0.60, "Moderate": 0.90, "Extensive": 1.30, "Complete": 1.60},
        22: {"Slight": 0.60, "Moderate": 0.90, "Extensive": 1.10, "Complete": 1.50},
        23: {"Slight": 0.90, "Moderate": 0.90, "Extensive": 1.10, "Complete": 1.50},
        24: {"Slight": 0.25, "Moderate": 0.35, "Extensive": 0.45, "Complete": 0.70},
        25: {"Slight": 0.30, "Moderate": 0.50, "Extensive": 0.60, "Complete": 0.90},
        26: {"Slight": 0.75, "Moderate": 0.75, "Extensive": 0.75, "Complete": 1.10},
        27: {"Slight": 0.75, "Moderate": 0.75, "Extensive": 0.75, "Complete": 1.10},
        28: {"Slight": 0.80, "Moderate": 1.00, "Extensive": 1.20, "Complete": 1.70},
    }

    if bridge_type not in old_medians:
        raise ValueError(f"Unknown bridge type: {bridge_type}")

    return old_medians[bridge_type]

def _hazus_type(properties: dict) -> int:
    """
    Classify the bridge into one of the Hazus types (1-28) using the properties extracted.
    The mapping logic is based on Table 9.6.
    
    Args:
        properties (dict): A dictionary containing the bridge properties extracted from `_bridge_info()`
        
    Returns:
        int: Hazus type classification (1-28) or -1 if no match is found
    """
    year_built = properties["year_built"]
    span_count = properties["span_count"]
    max_length = properties["max_span_length"]
    total_length = properties["total_length"]
    material_flag = properties["material_flag"]
    geometry_flag = properties["geometry_flag"]

    bridge_class = -1

    # Determine if the bridge is seismic based on year built and state code
    seismic_year = 1975 if properties["state_code"] == StateCodes.California else 1990
    
    # Implement classification rules from Table 9-6
    # Some classes are not relevant and they're not included. 
    if year_built < seismic_year:
        if max_length > 150:
            bridge_class = 1  # Older, long-span bridges
        else:
            if span_count == 1:
                bridge_class = 3  # Older, short, single-span bridges
            else:
                if material_flag == 1 :
                    bridge_class = 6  # Concrete, simple support
                elif material_flag == 2 and geometry_flag == 6:
                    bridge_class = 8  # Single box, continuous concrete
                elif material_flag == 2:
                    bridge_class = 10  # Continuous concrete
                elif material_flag == 3 and total_length >= 20:
                    bridge_class = 13  # Steel, simple support, total length >= 20
                elif material_flag == 3 and total_length < 20:
                    bridge_class = 25  # Steel, simple support, total length < 20
                elif material_flag == 4 and total_length >= 20:
                    bridge_class = 15  # Continuous steel, total length >= 20
                elif material_flag == 4 and total_length < 20:
                    bridge_class = 17  # Continuous steel, total length < 20
                elif material_flag == 5:
                    bridge_class = 18  # Prestressed concrete, simple support
                elif material_flag == 6 and geometry_flag == 6:
                    bridge_class = 20  # Prestressed continuous concrete, single box
    else:
        if max_length > 150:
            bridge_class = 2  # Newer, long-span bridges
        else:
            if span_count == 1:
                bridge_class = 4  # Newer, short, single-span bridges
            else:
                if material_flag == 1:
                    bridge_class = 7  # Concrete, simple support
                elif material_flag == 2 and geometry_flag == 6:
                    bridge_class = 9  # Single box, continuous concrete
                elif material_flag == 2:
                    bridge_class = 11  # Continuous concrete
                elif material_flag == 3:
                    bridge_class = 14  # Steel, simple support
                elif material_flag == 4:
                    bridge_class = 16  # Continuous steel
                elif material_flag == 5:
                    bridge_class = 19  # Prestressed concrete, simple support
                elif material_flag == 6:
                    bridge_class = 21  # Prestressed continuous concrete, single box

    return bridge_class

