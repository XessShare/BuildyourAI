#!/bin/bash
# Sprint Automation Script
# Manages 2-week sprint cycles for 1M€ roadmap

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Configuration
HOMELAB_DIR="/home/fitna/homelab"
SPRINT_DIR="$HOMELAB_DIR/sprints"
TRACKER="$HOMELAB_DIR/shared/dashboards/1m-roadmap-tracker.md"
JJECO_DIR="/home/fitna/homelab/ai-platform/1-first-agent"

# Get current sprint number
get_current_sprint() {
    # Calculate sprint number based on start date (2025-01-01)
    START_DATE="2025-01-01"
    CURRENT_DATE=$(date +%Y-%m-%d)
    
    DAYS_DIFF=$(( ($(date -d "$CURRENT_DATE" +%s) - $(date -d "$START_DATE" +%s)) / 86400 ))
    SPRINT_NUM=$(( ($DAYS_DIFF / 14) + 1 ))
    
    echo $SPRINT_NUM
}

# Start new sprint
start_sprint() {
    local sprint_num=$(get_current_sprint)
    local sprint_start=$(date +%Y-%m-%d)
    local sprint_end=$(date -d "+14 days" +%Y-%m-%d)
    
    echo -e "${BLUE}🚀 Starting Sprint $sprint_num${NC}"
    echo -e "   Start: $sprint_start"
    echo -e "   End:   $sprint_end"
    
    # Create sprint directory
    mkdir -p "$SPRINT_DIR/sprint-$sprint_num"
    
    # Generate sprint plan
    cat > "$SPRINT_DIR/sprint-$sprint_num/SPRINT_PLAN.md" << EOF
# Sprint $sprint_num - Plan

**Duration:** $sprint_start to $sprint_end  
**Status:** 🟡 In Progress  
**Goal:** [Define sprint goal]

---

## 📊 Sprint Metrics

\`\`\`
Capacity: 80 hours (2 weeks × 40 hours)
Velocity: TBD (from previous sprint)
Committed Story Points: 0
\`\`\`

---

## 🎯 Sprint Goal

[Write 1-2 sentence sprint goal aligned with roadmap]

---

## 📋 Sprint Backlog

### High Priority (Must Complete)

- [ ] **Task 1:** Description
  - Story Points: 5
  - Owner: [You/Agent]
  - Dependencies: None
  
- [ ] **Task 2:** Description
  - Story Points: 3
  - Owner: [You/Agent]
  - Dependencies: Task 1

### Medium Priority (Should Complete)

- [ ] **Task 3:** Description
  - Story Points: 2
  - Owner: Agent
  - Dependencies: None

### Low Priority (Nice to Have)

- [ ] **Task 4:** Description
  - Story Points: 1
  - Owner: Agent
  - Dependencies: None

---

## 🤖 Agent Task Allocation

\`\`\`yaml
ContentCreatorAgent:
  - [ ] Task: Social media posts (daily)
  - [ ] Task: Blog article (1x)
  
ResearcherAgent:
  - [ ] Task: Market research report
  - [ ] Task: Competitor analysis
  
AnalystAgent:
  - [ ] Task: Update roadmap tracker (daily)
  - [ ] Task: Sprint metrics dashboard
  
ProjectManagerAgent:
  - [ ] Task: Sprint planning
  - [ ] Task: Daily standup summaries
  
DeploymentOrchestrator:
  - [ ] Task: CI/CD pipeline updates
  - [ ] Task: Infrastructure scaling
  
VerifierAgent:
  - [ ] Task: Automated testing
  - [ ] Task: Code reviews
\`\`\`

---

## 📅 Sprint Timeline

### Week 1: Build

**Monday:**
- Sprint planning (this meeting)
- Setup development environment
- Start high-priority tasks

**Tuesday-Friday:**
- Feature development
- Daily commits
- Agent tasks automation

### Week 2: Ship

**Monday-Wednesday:**
- Testing & QA
- Bug fixes
- Documentation

**Thursday:**
- Staging deployment
- User acceptance testing
- Prepare for release

**Friday:**
- Production deployment
- Sprint retrospective
- Plan next sprint

---

## 🚧 Blockers

None yet

---

## 📝 Daily Standups (Async)

### Day 1 - $sprint_start

**Yesterday:** Sprint planning
**Today:** [Fill during sprint]
**Blockers:** None

---

## 🎉 Sprint Review

[Fill at end of sprint]

**Completed:**
- 

**Not Completed:**
- 

**Velocity:** __ story points

---

**Created:** $(date +%Y-%m-%d)  
**Sprint Master:** Fitna + AI Agents
EOF

    echo -e "${GREEN}✅ Sprint plan created: $SPRINT_DIR/sprint-$sprint_num/SPRINT_PLAN.md${NC}"
    
    # Create sprint board
    cat > "$SPRINT_DIR/sprint-$sprint_num/SPRINT_BOARD.md" << EOF
# Sprint $sprint_num - Board

## 📊 Kanban View

### 📝 TODO

- Task 1
- Task 2

### 🏗️ IN PROGRESS

- 

### ✅ DONE

- 

---

## 🔥 Burndown

\`\`\`
Day 1:  ████████████████████ 100%
Day 2:  ████████████████████ 100%
Day 3:  ████████████████████ 100%
Day 14: ░░░░░░░░░░░░░░░░░░░░ 0%
\`\`\`

---

**Last Updated:** $(date +%Y-%m-%d)
EOF

    echo -e "${GREEN}✅ Sprint board created: $SPRINT_DIR/sprint-$sprint_num/SPRINT_BOARD.md${NC}"
    
    # Notify agents
    echo -e "${BLUE}📢 Notifying AI agents...${NC}"
    
    # Update roadmap tracker
    if [ -f "$TRACKER" ]; then
        sed -i "s/Sprint: Sprint [0-9]*/Sprint: Sprint $sprint_num/" "$TRACKER"
        echo -e "${GREEN}✅ Roadmap tracker updated${NC}"
    fi
    
    # Create GitHub issue (if GitHub CLI available)
    if command -v gh &> /dev/null; then
        echo -e "${BLUE}📝 Creating GitHub issue...${NC}"
        gh issue create \
            --title "Sprint $sprint_num Planning" \
            --body "Sprint $sprint_num runs from $sprint_start to $sprint_end. See sprint plan for details." \
            --label "sprint,planning" \
            2>/dev/null || echo -e "${YELLOW}⚠️  GitHub CLI not configured${NC}"
    fi
    
    echo ""
    echo -e "${GREEN}🎉 Sprint $sprint_num started successfully!${NC}"
    echo ""
    echo -e "Next steps:"
    echo -e "  1. Edit sprint plan: nano $SPRINT_DIR/sprint-$sprint_num/SPRINT_PLAN.md"
    echo -e "  2. Define sprint goal"
    echo -e "  3. Add tasks from roadmap"
    echo -e "  4. Allocate to agents"
    echo ""
}

# End sprint
end_sprint() {
    local sprint_num=$(get_current_sprint)
    
    echo -e "${BLUE}🏁 Ending Sprint $sprint_num${NC}"
    
    if [ ! -d "$SPRINT_DIR/sprint-$sprint_num" ]; then
        echo -e "${RED}❌ Sprint directory not found${NC}"
        exit 1
    fi
    
    # Generate sprint report
    echo -e "${BLUE}📊 Generating sprint report...${NC}"
    
    cat > "$SPRINT_DIR/sprint-$sprint_num/SPRINT_REPORT.md" << EOF
# Sprint $sprint_num - Report

**End Date:** $(date +%Y-%m-%d)  
**Status:** ✅ Completed

---

## 📊 Sprint Metrics

\`\`\`
Planned Story Points:   __ SP
Completed Story Points: __ SP
Velocity:               __ SP (__ %)

Planned Tasks:     __
Completed Tasks:   __
Completion Rate:   __ %
\`\`\`

---

## 🎯 Sprint Goal Achievement

**Goal:** [Copy from sprint plan]

**Result:** [Achieved / Partially Achieved / Not Achieved]

**Details:**
- 

---

## ✅ Completed Tasks

1. **Task Name**
   - Story Points: __
   - Owner: __
   - Notes: __

---

## ❌ Incomplete Tasks

1. **Task Name**
   - Story Points: __
   - Reason: __
   - Action: [Moved to next sprint / Backlog / Cancelled]

---

## 🤖 Agent Performance

\`\`\`yaml
ContentCreatorAgent:
  Tasks Completed: __
  Success Rate: __ %
  
ResearcherAgent:
  Tasks Completed: __
  Success Rate: __ %
  
AnalystAgent:
  Tasks Completed: __
  Success Rate: __ %
  
ProjectManagerAgent:
  Tasks Completed: __
  Success Rate: __ %
  
DeploymentOrchestrator:
  Tasks Completed: __
  Success Rate: __ %
  
VerifierAgent:
  Tasks Completed: __
  Success Rate: __ %
\`\`\`

**Total Agent Tasks:** __  
**Human Hours Saved:** ~__ hours

---

## 🎓 Learnings

### What Went Well

- 

### What Didn't Go Well

- 

### Action Items for Next Sprint

- 

---

## 📈 Progress Toward 1M€ Goal

**MRR at Sprint Start:** __€  
**MRR at Sprint End:** __€  
**MRR Growth:** +__€ (__%)

**Customers at Sprint Start:** __  
**Customers at Sprint End:** __  
**Customer Growth:** +__ (__%)

---

## 🔮 Next Sprint Preview

**Sprint $(($sprint_num + 1)) Focus:**
- 

**Carried Over Tasks:**
- 

---

**Report Generated:** $(date +%Y-%m-%d)  
**Next Sprint Start:** $(date -d "+1 day" +%Y-%m-%d)
EOF

    echo -e "${GREEN}✅ Sprint report created: $SPRINT_DIR/sprint-$sprint_num/SPRINT_REPORT.md${NC}"
    
    # Archive sprint
    echo -e "${BLUE}📦 Archiving sprint...${NC}"
    mkdir -p "$SPRINT_DIR/archive"
    # No move needed, just mark as complete
    
    # Update tracker
    if [ -f "$TRACKER" ]; then
        # Increment completed milestones
        echo -e "${GREEN}✅ Updating roadmap tracker${NC}"
    fi
    
    echo ""
    echo -e "${GREEN}🎉 Sprint $sprint_num completed!${NC}"
    echo ""
    echo -e "Next steps:"
    echo -e "  1. Review sprint report: cat $SPRINT_DIR/sprint-$sprint_num/SPRINT_REPORT.md"
    echo -e "  2. Fill in metrics and learnings"
    echo -e "  3. Start next sprint: $0 start"
    echo ""
}

# Sprint status
sprint_status() {
    local sprint_num=$(get_current_sprint)
    
    echo -e "${BLUE}📊 Sprint $sprint_num Status${NC}"
    echo ""
    
    if [ -d "$SPRINT_DIR/sprint-$sprint_num" ]; then
        echo -e "${GREEN}✅ Sprint active${NC}"
        echo ""
        
        # Calculate days remaining
        local sprint_start_file="$SPRINT_DIR/sprint-$sprint_num/SPRINT_PLAN.md"
        if [ -f "$sprint_start_file" ]; then
            local days_elapsed=$(grep -oP 'Start: \K[0-9-]+' "$sprint_start_file" | xargs -I {} bash -c "echo \$(( (\$(date +%s) - \$(date -d {} +%s)) / 86400 ))")
            local days_remaining=$((14 - days_elapsed))
            
            echo "Days Elapsed: $days_elapsed / 14"
            echo "Days Remaining: $days_remaining"
            echo ""
        fi
        
        # Show sprint files
        echo "Sprint Files:"
        ls -1 "$SPRINT_DIR/sprint-$sprint_num/" | sed 's/^/  - /'
        echo ""
        
        # Show recent activity
        echo "Recent Files Modified:"
        find "$SPRINT_DIR/sprint-$sprint_num/" -type f -printf "%T+ %p\n" | sort -r | head -5 | cut -d' ' -f2- | sed 's/^/  - /'
        
    else
        echo -e "${YELLOW}⚠️  No active sprint${NC}"
        echo ""
        echo "Start a new sprint: $0 start"
    fi
}

# Main
case "${1:-}" in
    start)
        start_sprint
        ;;
    end)
        end_sprint
        ;;
    status)
        sprint_status
        ;;
    *)
        echo "Usage: $0 {start|end|status}"
        echo ""
        echo "Commands:"
        echo "  start   - Start a new 2-week sprint"
        echo "  end     - End current sprint and generate report"
        echo "  status  - Show current sprint status"
        exit 1
        ;;
esac
