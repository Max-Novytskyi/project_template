from app.entities.agent_data import AgentData, AgentDataIn
from app.entities.processed_agent_data import ProcessedAgentData


def process_agent_data(
    agent_data: AgentDataIn,
) -> ProcessedAgentData:
    """
    Process agent data and classify the state of the road surface.
    Parameters:
        agent_data (AgentData): Agent data that containing accelerometer, GPS, and timestamp.
    Returns:
        processed_data_batch (ProcessedAgentData): Processed data containing the classified state of the road surface and agent data.
    """
    y_coord = agent_data.accelerometer.y

    if y_coord < -500:
        state = "pit"
    elif -500 < y_coord < 500:
        state = "road"
    else:
        state = "pothole"

    return ProcessedAgentData(road_state=state, agent_data=agent_data)