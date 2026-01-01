#!/bin/bash
set -e

# Pre-flight Check & Local Test Script for GitHub Actions Workflow
# Purpose: Validate all components before triggering GitHub Actions

echo "🔍 GitHub Actions Workflow Pre-Flight Check"
echo "==========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counter for checks
PASSED=0
FAILED=0

# Function to print status
check_pass() {
    echo -e "${GREEN}✅ PASS:${NC} $1"
    ((PASSED++))
}

check_fail() {
    echo -e "${RED}❌ FAIL:${NC} $1"
    ((FAILED++))
}

check_warn() {
    echo -e "${YELLOW}⚠️  WARN:${NC} $1"
}

echo "Step 1: Checking Required Files"
echo "--------------------------------"

# Check workflow file
if [ -f ".github/workflows/design-spec-update.yml" ]; then
    check_pass "Workflow file exists"
else
    check_fail "Workflow file not found"
fi

# Check prompt files (all 5 v2 prompts)
PROMPTS=(
    "sprints/sprint-26/prompt-library/landing-page-prompt-v2.md"
    "sprints/sprint-26/prompt-library/webapp-dashboard-prompt-v2.md"
    "sprints/sprint-26/prompt-library/ios-app-prompt-v2.md"
    "sprints/sprint-26/prompt-library/android-app-prompt-v2.md"
    "sprints/sprint-26/prompt-library/design-system-prompt-v2.md"
)

for prompt in "${PROMPTS[@]}"; do
    if [ -f "$prompt" ]; then
        check_pass "$(basename $prompt) exists"
    else
        check_fail "$(basename $prompt) missing"
    fi
done

# Check design context
if [ -f "sprints/sprint-26/design-research/DESIGN_CONTEXT.md" ]; then
    check_pass "DESIGN_CONTEXT.md exists"
else
    check_fail "DESIGN_CONTEXT.md missing"
fi

echo ""
echo "Step 2: Validating Workflow YAML"
echo "--------------------------------"

# Validate YAML syntax
if python3 -c "import yaml; yaml.safe_load(open('.github/workflows/design-spec-update.yml'))" 2>/dev/null; then
    check_pass "Workflow YAML syntax is valid"
else
    # Try installing PyYAML if not available
    if pip3 install --quiet pyyaml 2>/dev/null; then
        if python3 -c "import yaml; yaml.safe_load(open('.github/workflows/design-spec-update.yml'))" 2>/dev/null; then
            check_pass "Workflow YAML syntax is valid (installed PyYAML)"
        else
            check_fail "Workflow YAML syntax invalid"
        fi
    else
        check_warn "Could not validate YAML (PyYAML not installed)"
    fi
fi

echo ""
echo "Step 3: Checking Python Dependencies"
echo "------------------------------------"

# Check if required Python packages are available
PACKAGES=("anthropic" "google-generativeai" "pydantic")

for pkg in "${PACKAGES[@]}"; do
    if python3 -c "import $pkg" 2>/dev/null; then
        check_pass "$pkg installed"
    else
        check_warn "$pkg not installed (GitHub Actions will install it)"
    fi
done

echo ""
echo "Step 4: Checking API Keys"
echo "------------------------"

# Check local environment variables
if [ -n "$ANTHROPIC_API_KEY" ]; then
    check_pass "ANTHROPIC_API_KEY set locally (${#ANTHROPIC_API_KEY} chars)"
    LOCAL_ANTHROPIC=1
else
    check_warn "ANTHROPIC_API_KEY not set locally (needed for local test)"
    LOCAL_ANTHROPIC=0
fi

if [ -n "$GOOGLE_API_KEY" ]; then
    check_pass "GOOGLE_API_KEY set locally (${#GOOGLE_API_KEY} chars)"
    LOCAL_GOOGLE=1
else
    check_warn "GOOGLE_API_KEY not set locally (needed for local test)"
    LOCAL_GOOGLE=0
fi

# Check GitHub secrets (will fail if not set up)
echo ""
echo "Checking GitHub repository secrets..."
if gh secret list &>/dev/null; then
    if gh secret list | grep -q "ANTHROPIC_API_KEY"; then
        check_pass "ANTHROPIC_API_KEY set in GitHub"
    else
        check_fail "ANTHROPIC_API_KEY not set in GitHub"
    fi

    if gh secret list | grep -q "GOOGLE_API_KEY"; then
        check_pass "GOOGLE_API_KEY set in GitHub"
    else
        check_fail "GOOGLE_API_KEY not set in GitHub"
    fi
else
    check_warn "Cannot access GitHub secrets (gh CLI not authenticated or insufficient permissions)"
    echo "         You need to manually verify secrets at: https://github.com/fitna/homelab/settings/secrets/actions"
fi

echo ""
echo "Step 5: Checking Git Status"
echo "---------------------------"

# Check current branch
CURRENT_BRANCH=$(git branch --show-current)
check_pass "Current branch: $CURRENT_BRANCH"

# Check if there are uncommitted changes
if git diff --quiet && git diff --cached --quiet; then
    check_pass "Working directory is clean"
else
    check_warn "Working directory has uncommitted changes"
    echo "         Run 'git status' to see changes"
fi

# Check if we're in a git repo
if git rev-parse --git-dir > /dev/null 2>&1; then
    check_pass "Repository is a valid git repo"
else
    check_fail "Not in a git repository"
fi

echo ""
echo "=========================================="
echo "Summary: $PASSED passed, $FAILED failed"
echo "=========================================="
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All critical checks passed!${NC}"
    echo ""
    echo "Next Steps:"
    echo "1. If API keys are set in GitHub, trigger workflow at:"
    echo "   https://github.com/fitna/homelab/actions/workflows/design-spec-update.yml"
    echo ""
    echo "2. Or run local test with: ./sprints/sprint-26/test-workflow-locally.sh --test"
    echo ""
else
    echo -e "${RED}❌ Some checks failed. Fix issues before proceeding.${NC}"
    echo ""
    echo "Common fixes:"
    echo "- Add API keys to GitHub: https://github.com/fitna/homelab/settings/secrets/actions"
    echo "- Install missing files from sprints/sprint-26/"
    echo ""
fi

# Optional: Run local test if --test flag provided and keys are available
if [ "$1" == "--test" ] && [ $LOCAL_ANTHROPIC -eq 1 ] && [ $LOCAL_GOOGLE -eq 1 ]; then
    echo ""
    echo "🧪 Running Local Test (Single Spec Generation)"
    echo "=============================================="
    echo ""

    echo "Testing Landing Page generation with Claude..."
    python3 - <<'EOF'
import os
from anthropic import Anthropic

try:
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    # Read prompt
    with open("sprints/sprint-26/prompt-library/landing-page-prompt-v2.md") as f:
        prompt_content = f.read()
        prompt = prompt_content.split("```")[1].strip()

    # Read context
    with open("sprints/sprint-26/design-research/DESIGN_CONTEXT.md") as f:
        context = f.read()

    print("📤 Sending request to Claude...")

    # Generate spec (small max_tokens for test)
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,  # Small test
        messages=[{
            "role": "user",
            "content": f"{prompt}\n\n**Additional Context:**\n{context[:2000]}"
        }]
    )

    output = message.content[0].text
    print("✅ Claude API call successful!")
    print(f"📝 Generated {len(output)} characters")
    print("\nFirst 200 chars of output:")
    print("-" * 50)
    print(output[:200])
    print("-" * 50)

except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)
EOF

    if [ $? -eq 0 ]; then
        echo ""
        echo -e "${GREEN}✅ Local test successful! Workflow should work in GitHub Actions.${NC}"
    else
        echo ""
        echo -e "${RED}❌ Local test failed. Check API key or network connection.${NC}"
    fi
elif [ "$1" == "--test" ]; then
    echo ""
    echo -e "${YELLOW}⚠️  Cannot run local test: API keys not set in environment${NC}"
    echo "To test locally, export API keys:"
    echo "  export ANTHROPIC_API_KEY='sk-ant-...'"
    echo "  export GOOGLE_API_KEY='AIza...'"
    echo "  ./sprints/sprint-26/test-workflow-locally.sh --test"
fi

echo ""
