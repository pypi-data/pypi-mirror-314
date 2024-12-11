from kajihs_utils import batch, get_first
from kajihs_utils.loguru import prompt, setup_logging

# Get first key existing in a dict:
d = {"a": 1, "b": 2, "c": 3}
print(get_first(d, ["x", "a", "b"]))

# Batch a sequence:
seq = list(range(10))
print(list(batch(seq, 3)))

# === Loguru features ===
# Better logged and formatted prompts
prompt("Enter a number")  # snippet: no-exec

# Simply setup well formatted logging in files and console
setup_logging()
