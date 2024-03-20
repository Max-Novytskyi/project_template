from app.entities.agent_data import AgentData
from app.entities.processed_agent_data import ProcessedAgentData



def process_agent_data(
    agent_data: AgentData,
) -> ProcessedAgentData:
    """
    Process agent data and classify the state of the road surface.
    Parameters:
        agent_data (AgentData): Agent data that containing accelerometer, GPS, and timestamp.
    Returns:
        processed_data_batch (ProcessedAgentData): Processed data containing the classified state of the road surface and agent data.
    """
    # Implement it
    processed_data = ProcessedAgentData()
    x_coord = agent_data.x_coord
    y_coord = agent_data.y_coord
    z_coord = agent_data.z_coord
    if z_coord < 16550 and x_coord < -500 and y_coord < -500 :
        state = "pit"
    elif 16550 < z_coord < 17550 and -500 < x_coord < 500 and -500 < y_coord < 500:
        state = "road"
    elif z_coord > 17550 and x_coord > 500 and y_coord > 500 :
        state = "pothole"
        
    processed_data.agent_data = agent_data
    processed_data.road_state = state
    return processed_data
