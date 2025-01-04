import re

def normalize_string(value):
  value = value.strip().strip("_")

  if len(value) == 0:
    return None

  value = value[0].upper() + value[1:]
  value = re.sub(r"\s+", "_", value)
  value = re.sub(r"_+", "_", value)

  return value
