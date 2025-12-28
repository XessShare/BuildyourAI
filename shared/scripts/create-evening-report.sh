#!/bin/bash
# Evening Report Generator
# Analyzes today's work and generates comprehensive end-of-day report

set -e

# Configuration
TODAY=$(date +%d.%m.%y)
FULL_DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date +%H:%M:%S)
WORK_DIR="/home/fitna/homelab/${TODAY}"
REPORT_FILE="$WORK_DIR/EVENING_REPORT.md"
WORK_SHEET="$WORK_DIR/DAILY_WORK_SHEET.md"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if work sheet exists
if [ ! -f "$WORK_SHEET" ]; then
    echo -e "${YELLOW}⚠️  No work sheet found for today${NC}"
    echo "Create one first: /home/fitna/homelab/shared/scripts/create-daily-sheet.sh"
    exit 1
fi

echo -e "${BLUE}📊 Generating Evening Report for ${FULL_DATE}${NC}"

# Count task statistics from work sheet
TOTAL_TASKS=$(grep -c "^\- \[" "$WORK_SHEET" || echo 0)
COMPLETED_TASKS=$(grep -c "^\- \[x\]" "$WORK_SHEET" || echo 0)
PENDING_TASKS=$((TOTAL_TASKS - COMPLETED_TASKS))

# Calculate completion percentage
if [ $TOTAL_TASKS -gt 0 ]; then
    COMPLETION_PCT=$(awk "BEGIN {printf \"%.0f\", ($COMPLETED_TASKS / $TOTAL_TASKS) * 100}")
else
    COMPLETION_PCT=0
fi

# Determine status emoji
if [ $COMPLETION_PCT -ge 80 ]; then
    STATUS_EMOJI="🟢"
    STATUS_TEXT="Excellent"
elif [ $COMPLETION_PCT -ge 60 ]; then
    STATUS_EMOJI="🟡"
    STATUS_TEXT="Good"
elif [ $COMPLETION_PCT -ge 40 ]; then
    STATUS_EMOJI="🟠"
    STATUS_TEXT="Moderate"
else
    STATUS_EMOJI="🔴"
    STATUS_TEXT="Needs Improvement"
fi

# Generate report
cat > "$REPORT_FILE" << EOF
# 🌙 Evening Report - ${FULL_DATE}

**Generated:** ${FULL_DATE} ${TIMESTAMP}  
**Status:** ${STATUS_EMOJI} ${STATUS_TEXT}  
**Completion:** ${COMPLETION_PCT}%

---

## 📊 Daily Statistics

### Task Completion
- **Total Tasks:** ${TOTAL_TASKS}
- **Completed:** ${COMPLETED_TASKS} ✅
- **Pending:** ${PENDING_TASKS} ⏳
- **Completion Rate:** ${COMPLETION_PCT}%

### Progress Bar
\`\`\`
EOF

# Generate visual progress bar
FILLED=$((COMPLETION_PCT / 5))
EMPTY=$((20 - FILLED))
PROGRESS_BAR="["
for ((i=0; i<FILLED; i++)); do PROGRESS_BAR+="█"; done
for ((i=0; i<EMPTY; i++)); do PROGRESS_BAR+="░"; done
PROGRESS_BAR+="] ${COMPLETION_PCT}%"

echo "$PROGRESS_BAR" >> "$REPORT_FILE"

cat >> "$REPORT_FILE" << EOF
\`\`\`

---

## 🎯 Project-Specific Progress

### 🤖 J-Jeco AI Platform (agents)
EOF

# Extract J-Jeco related tasks
echo "" >> "$REPORT_FILE"
echo "**Completed:**" >> "$REPORT_FILE"
grep -i "jeco\|agent\|ai" "$WORK_SHEET" | grep "\[x\]" >> "$REPORT_FILE" 2>/dev/null || echo "- None" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "**Pending:**" >> "$REPORT_FILE"
grep -i "jeco\|agent\|ai" "$WORK_SHEET" | grep "\[ \]" >> "$REPORT_FILE" 2>/dev/null || echo "- None" >> "$REPORT_FILE"

cat >> "$REPORT_FILE" << EOF

### 🏗️ Homelab Infrastructure
EOF

echo "" >> "$REPORT_FILE"
echo "**Completed:**" >> "$REPORT_FILE"
grep -i "homelab\|infrastructure\|docker\|deploy" "$WORK_SHEET" | grep "\[x\]" >> "$REPORT_FILE" 2>/dev/null || echo "- None" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "**Pending:**" >> "$REPORT_FILE"
grep -i "homelab\|infrastructure\|docker\|deploy" "$WORK_SHEET" | grep "\[ \]" >> "$REPORT_FILE" 2>/dev/null || echo "- None" >> "$REPORT_FILE"

cat >> "$REPORT_FILE" << EOF

### 📚 Documentation & Planning
EOF

echo "" >> "$REPORT_FILE"
echo "**Completed:**" >> "$REPORT_FILE"
grep -i "doc\|readme\|guide\|plan" "$WORK_SHEET" | grep "\[x\]" >> "$REPORT_FILE" 2>/dev/null || echo "- None" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "**Pending:**" >> "$REPORT_FILE"
grep -i "doc\|readme\|guide\|plan" "$WORK_SHEET" | grep "\[ \]" >> "$REPORT_FILE" 2>/dev/null || echo "- None" >> "$REPORT_FILE"

cat >> "$REPORT_FILE" << EOF

---

## 🎉 Key Achievements Today

EOF

# Extract completed tasks
COMPLETED_SECTION=$(sed -n '/^## 🎉 Completed Tasks/,/^---/p' "$WORK_SHEET" | grep "^\- \[x\]" || echo "")
if [ -n "$COMPLETED_SECTION" ]; then
    echo "$COMPLETED_SECTION" >> "$REPORT_FILE"
else
    echo "- Review the completed tasks in DAILY_WORK_SHEET.md" >> "$REPORT_FILE"
fi

cat >> "$REPORT_FILE" << EOF

---

## 🚧 Blockers & Challenges

EOF

# Extract blockers
BLOCKER_SECTION=$(sed -n '/^## 🚧 Blockers & Issues/,/^---/p' "$WORK_SHEET" | tail -n +3 | head -n -1 || echo "")
if [ -n "$BLOCKER_SECTION" ]; then
    echo "$BLOCKER_SECTION" >> "$REPORT_FILE"
else
    echo "No active blockers reported." >> "$REPORT_FILE"
fi

cat >> "$REPORT_FILE" << EOF

---

## 📝 Learnings & Notes

EOF

# Extract notes
NOTES_SECTION=$(sed -n '/^## 📝 Notes & Learnings/,/^---/p' "$WORK_SHEET" | tail -n +3 | head -n -1 || echo "")
if [ -n "$NOTES_SECTION" ]; then
    echo "$NOTES_SECTION" >> "$REPORT_FILE"
else
    echo "No notes documented today." >> "$REPORT_FILE"
fi

cat >> "$REPORT_FILE" << EOF

---

## 📈 Performance Analysis

### Productivity Score: ${COMPLETION_PCT}/100

**Rating Breakdown:**
- Task Completion: ${COMPLETION_PCT}%
- Blocker Resolution: TBD (manual review)
- Documentation Quality: TBD (manual review)

**Recommendations:**
EOF

if [ $COMPLETION_PCT -lt 50 ]; then
    cat >> "$REPORT_FILE" << EOF
- ⚠️ **Low completion rate** - Review task estimates and time management
- Consider breaking down large tasks into smaller subtasks
- Identify and address blockers earlier in the day
EOF
elif [ $COMPLETION_PCT -lt 80 ]; then
    cat >> "$REPORT_FILE" << EOF
- ✅ Good progress - Keep up the momentum
- Focus on completing high-priority tasks first
- Document learnings to avoid future blockers
EOF
else
    cat >> "$REPORT_FILE" << EOF
- 🎉 **Excellent productivity!** - Maintain current workflow
- Share successful strategies with team/future self
- Consider tackling stretch goals tomorrow
EOF
fi

cat >> "$REPORT_FILE" << EOF

---

## 🔮 Tomorrow's Preparation

### High-Priority Items for Next Day
EOF

# Extract tomorrow's focus if filled out
TOMORROW_SECTION=$(sed -n '/^**Tomorrow.*Focus.*:/,/^$/p' "$WORK_SHEET" | tail -n +2 || echo "")
if [ -n "$TOMORROW_SECTION" ]; then
    echo "$TOMORROW_SECTION" >> "$REPORT_FILE"
else
    cat >> "$REPORT_FILE" << EOF
- Complete pending tasks from today
- Address unresolved blockers
- Continue with current project phase
EOF
fi

cat >> "$REPORT_FILE" << EOF

### Recommended Actions
- [ ] Review this report before starting tomorrow
- [ ] Update project roadmaps if needed
- [ ] Sync with team/stakeholders on blockers
- [ ] Prepare environment for tomorrow's tasks

---

## 📎 Related Documents

- **Work Sheet:** [\`DAILY_WORK_SHEET.md\`](./${TODAY}/DAILY_WORK_SHEET.md)
- **Strategic Plan:** [SCHLACHTPLAN_V2.md](../SCHLACHTPLAN_V2.md)
- **Progress Guide:** [PROGRESS_TRACKING_GUIDE.md](../shared/docs/PROGRESS_TRACKING_GUIDE.md)

---

## 📊 Historical Context

### Week-to-Date Summary
- Daily reports: Check parent directory for previous days
- Trend analysis: Compare completion rates across week

### Month-to-Date Summary
- Overall progress: Review monthly roadmap
- Milestone tracking: Check project status documents

---

**Report Generated:** ${FULL_DATE} ${TIMESTAMP}  
**Next Review:** $(date -d "+1 day" +%Y-%m-%d) Morning  
**Report Version:** 2.0
EOF

echo -e "${GREEN}✅ Evening report created: ${REPORT_FILE}${NC}"
echo ""
echo "📊 Summary:"
echo "   Tasks: ${COMPLETED_TASKS}/${TOTAL_TASKS} completed (${COMPLETION_PCT}%)"
echo "   Status: ${STATUS_TEXT} ${STATUS_EMOJI}"
echo ""
echo "📖 View report:"
echo "   cat ${REPORT_FILE}"
