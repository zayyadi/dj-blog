from .base import *  # noqa: F403
import os


if os.environ.get("ENV_NAME") == "Prod":
    from .prod import *  # noqa: F403
else:
    from .dev import *  # noqa: F403
