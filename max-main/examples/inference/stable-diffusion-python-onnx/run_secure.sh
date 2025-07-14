#!/bin/bash
##===----------------------------------------------------------------------===##
# Copyright (c) 2024, Modular Inc. All rights reserved.
#
# Licensed under the Apache License v2.0 with LLVM Exceptions:
# https://llvm.org/LICENSE.txt
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##===----------------------------------------------------------------------===##

# If anything goes wrong, stop running the script.
set -e

MODEL_DIR="../../models/stable-diffusion-onnx"
NPROMPT="bad anatomy, looking away, looking sideways, crooked stick"
NPROMPT="$NPROMPT, stick not going through jaw, orange tongue"
PPROMPT="Cute puppy chewing on a stick"

# Make sure we're running from inside the directory containing this file.
cd "$(dirname "$0")"

echo "🔒 Running Secure Stable Diffusion with Model Validation"
echo "========================================================"
echo ""
echo "This script uses the secure version with comprehensive model security validation."
echo "The model will be validated for potential backdoor threats before execution."
echo ""

# Execute secure model with strict security validation
python3 text_to_image_secure.py \
    --seed 7 \
    --num-steps 20 \
    --prompt "$PPROMPT" \
    --negative-prompt "$NPROMPT" \
    --strict-security

echo ""
echo "✅ Secure execution completed successfully!"