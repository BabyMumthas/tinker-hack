"""Start the app with configurable port (avoids 8000 conflict)."""
import uvicorn
from app.config import config

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=config.PORT,
        reload=False,
    )
