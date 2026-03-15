import logging
import uvicorn
from fastapi import FastAPI, HTTPException
from app.schemas import Payload, ProductionResponse
from app.solver import calculate_production_plan

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("powerplant-api")

app = FastAPI(
    title="Powerplant Production Plan API",
    description="International service for Unit Commitment optimization and power dispatch."
)

@app.post("/productionplan", response_model=list[ProductionResponse])
async def production_plan(payload: Payload):
    """
    This endpoint receives the load requirements along with fuel data and power plant specifications. 
    Regarding the internal logic, it delegates the calculation to the merit-order solver; 
    therefore, it returns the optimal production plan tailored to the requested demand.
    """
    try:
        logger.info(f"Received production plan request for a load of {payload.load} MW")
        
        # core business logic:
        result = calculate_production_plan(payload)
        
        return result
        
    except Exception as e:
        logger.error(f"Error encountered while processing the production plan: {str(e)}")
        # Providing a structured 500 error if any failure occurs during the calculation process
        raise HTTPException(status_code=500, detail="Internal Server Error during calculation")

if __name__ == "__main__":
    # Adhering to the required port 8888
    uvicorn.run(app, host="0.0.0.0", port=8888)