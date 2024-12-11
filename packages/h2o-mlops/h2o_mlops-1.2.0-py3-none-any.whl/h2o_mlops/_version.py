import importlib.resources


version = "0.0.0"

if importlib.resources.is_resource("h2o_mlops", "VERSION"):
    version = importlib.resources.read_text("h2o_mlops", "VERSION").strip()
