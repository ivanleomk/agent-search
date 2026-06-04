#!/bin/bash

# Use this file to install test dependencies and run the tests.
# It will be copied to /tests/test.sh and run from the working directory.

apt-get update
apt-get install -y curl

curl -LsSf https://astral.sh/uv/0.9.7/install.sh | sh

source $HOME/.local/bin/env

# Run rewardkit to evaluate task output using LLM-as-a-judge
uvx --from harbor-rewardkit==0.1.4 rewardkit /tests --output /logs/verifier/reward.json

# Parse the score from reward.json and write to reward.txt
if [ -f /logs/verifier/reward.json ]; then
  python3 -c "import json; data = json.load(open('/logs/verifier/reward.json')); print(int(data.get('completeness', 0)))" > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
