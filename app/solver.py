"""
Business Logic Module
This module handles marginal cost calculations and the dispatch algorithm execution.
"""
import logging

logger = logging.getLogger(__name__)

def calculate_production_plan(payload):
    load = payload.load # The total load that needs to be met
    fuels = payload.fuels # Fuel prices and wind availability
    
    # capacity and marginal cost based on current fuel prices and environmental taxes of each plant:
    processed_plants = []
    for p in payload.powerplants:
        marginal_cost = 0
        pmax_effective = p.pmax
        
        if p.type == 'windturbine':
            marginal_cost = 0
            pmax_effective = p.pmax * (fuels.wind / 100)
        elif p.type == 'gasfired':
            # Fuel cost plus CO2 emission rights (0.3 ton/MWh)
            marginal_cost = (fuels.gas / p.efficiency) + (0.3 * fuels.co2)
        elif p.type == 'turbojet':
            marginal_cost = fuels.kerosine / p.efficiency
            
        processed_plants.append({
            'name': p.name,
            'pmin': p.pmin,
            'pmax': pmax_effective,
            'cost': marginal_cost,
            'p_assigned': 0.0
        })

    # Economic efficiency: plants are sorted by their marginal cost
    # (Merit Order principle: cheaper units are prioritized.)
    processed_plants.sort(key=lambda x: x['cost'])

    # The Dispatch Algorithm (Greedy approach):
    current_load = 0.0
    for i, plant in enumerate(processed_plants):
        remaining_load = load - current_load
        
        if remaining_load <= 0:
            break
            
        if remaining_load >= plant['pmin']:
            # Assign as much load as possible to the current unit
            take = min(remaining_load, plant['pmax'])
            plant['p_assigned'] = round(take, 1)
            current_load += plant['p_assigned']
        else:
            # CRITICAL CASE: The remaining load is less than the current plant's Pmin,
            # Adjust the previous unit's output to accommodate the new plant.
            if i > 0:
                needed_from_previous = plant['pmin'] - remaining_load
                previous_plant = processed_plants[i-1]
                
                # Verifying if the previous plant can reduce its load without dropping below its Pmin
                if (previous_plant['p_assigned'] - needed_from_previous) >= previous_plant['pmin']:
                    previous_plant['p_assigned'] = round(previous_plant['p_assigned'] - needed_from_previous, 1)
                    plant['p_assigned'] = plant['pmin']
                    current_load = load # The total load is now exactly covered
                else:
                    logger.warning(f"Skipping {plant['name']}: constraints not met by adjusting {previous_plant['name']}")
                    plant['p_assigned'] = 0.0
    
    if round(current_load, 1) < load:
        logger.error(f"Incomplete dispatch: Only covered {current_load}/{load} MW")        
    # Final response formatted to match the required output schema.
    return [{"name": p["name"], "p": p["p_assigned"]} for p in processed_plants]