import os
import google.auth
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from .mcp_bigquery import query_transactions, log_anomaly

_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

current_dir = os.path.dirname(__file__)
instructions_path = os.path.join(current_dir, "GEMINI.md")
with open(instructions_path, "r") as f:
    system_instructions = f.read()

root_agent = Agent(
    name="fintrac_agent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=system_instructions,
    tools=[query_transactions, log_anomaly],
)

app = App(root_agent=root_agent, name="app")
