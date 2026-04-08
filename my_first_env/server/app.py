import uvicorn
from openenv.core.env_server import create_app
from server.my_first_env_environment import NIRFenv
from models import NIRFAction, NIRFObservation

# The Bootcamp version of create_app expects the CLASS name, 
# but it must be the ONLY thing passed as the first argument.
app = create_app(
    NIRFenv,   # ✅ PASS CLASS DIRECTLY
    action_cls=NIRFAction,
    observation_cls=NIRFObservation
)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)