"""C.AI specific constants for the Hermes engine."""

NARRATOR_NAME = "narrator"
DEFAULT_USERNAME = "user"
TIMEOUT_SECONDS = 60
ROUTE_COOKIE_NAME = "route"
MAX_CONTINUATIONS = 5
N_CODE = ord("\n")
TRUNCATION_STEPS_CHOICES = [250, 500, 750, 1000, 1250, 1500]
PRETRUNCATION_TOKENS_PER_MESSAGE = 10
BOD = "<|beginningofdialog|>"
BOM = "<|beginningofmessage|>"
EOM = "<|endofmessage|>"
