#!/bin/bash
# Enhanced Daily Work Sheet Generator with Project-Specific Tracking
# Creates comprehensive daily work sheet for agents, J-Jeco, and homelab projects

# Get today's date
TODAY=$(date +%d.%m.%y)
FULL_DATE=$(date +%Y-%m-%d)
DAY_NAME=$(date +%A)
WEEK_NUMBER=$(date +%V)
DIR="/home/fitna/homelab/${TODAY}"

# Create directory
mkdir -p "$DIR"

# Generate enhanced work sheet
cat > "$DIR/DAILY_WORK_SHEET.md" << EOF
# 📅 Daily Work Sheet - ${FULL_DATE} (${DAY_NAME}, Week ${WEEK_NUMBER})

**Status:** 🟡 In Progress  
**Focus:** Multi-Project Development (Agents + J-Jeco + Homelab)  
**Priority Level:** High  

---

## 📊 Overall Progress Dashboard

### Master Progress
\`\`\`
Overall:      [░░░░░░░░░░░░░░░░░░░░] 0%
Agents:       [░░░░░░░░░░░░░░░░░░░░] 0%
J-Jeco:       [░░░░░░░░░░░░░░░░░░░░] 0%
Homelab:      [░░░░░░░░░░░░░░░░░░░░] 0%
\`\`\`

### Daily Statistics
- **Total Tasks:** 0
- **Completed:** 0 ✅
- **In Progress:** 0 🟡
- **Blocked:** 0 🔴
- **Not Started:** 0 ⚪

---

## 🎯 Today's Top 3 Priorities

### Priority 1: 🔥 Critical
- [ ] _Define your most important task_

### Priority 2: ⚡ High
- [ ] _Second most important task_

### Priority 3: ⭐ Medium
- [ ] _Third priority task_

---

## 🤖 AI Agents Project (\`/home/fitna/J-Jeco/\`)

### Progress
\`\`\`
Agents Progress: [░░░░░░░░░░░░░░░░░░░░] 0%
\`\`\`

### Tasks - Agents
- [ ] Update AGENTS.md documentation
- [ ] Test agent functionality
- [ ] Review agent configurations
- [ ] _Add agent-specific tasks..._

### Notes - Agents
- 

---

## 🚀 J-Jeco Platform (\`/home/fitna/homelab/ai-platform/1-first-agent/\`)

### Progress
\`\`\`
J-Jeco Progress: [░░░░░░░░░░░░░░░░░░░░] 0%
\`\`\`

### Tasks - J-Jeco
- [ ] Test LLM integration
- [ ] Update agent workflows
- [ ] Knowledge base management
- [ ] _Add J-Jeco-specific tasks..._

### Notes - J-Jeco
- 

---

## 🏗️ Homelab Infrastructure (\`/home/fitna/homelab/infrastructure/\`)

### Progress
\`\`\`
Homelab Progress: [░░░░░░░░░░░░░░░░░░░░] 0%
\`\`\`

### Tasks - Homelab
- [ ] Check service health
- [ ] Review infrastructure status
- [ ] Update documentation
- [ ] _Add homelab-specific tasks..._

### Notes - Homelab
- 

---

## 📚 Documentation & Cross-Project Tasks

### Documentation
- [ ] Update AGENTS.md across projects
- [ ] Review progress tracking
- [ ] Sync documentation between repos

### Integration & Coordination
- [ ] Sync secrets across systems
- [ ] Check cross-project dependencies
- [ ] Verify deployment consistency

---

## 🚧 Blockers & Issues

### 🔴 Active Blockers
None

### 🟡 Potential Issues
- 

### 🟢 Resolved Today
- 

---

## 📝 Notes & Learnings

### Key Discoveries
- 

### Technical Insights
- 

### Questions to Resolve
- 

### Links & References
- 

---

## ⏱️ Time Tracking

### Morning Session (8:00 - 12:00)
- Started: 
- Tasks: 
- Progress: 

### Afternoon Session (13:00 - 17:00)
- Started: 
- Tasks: 
- Progress: 

### Evening Session (18:00 - 22:00)
- Started: 
- Tasks: 
- Progress: 

---

## 🎉 Completed Tasks

### Agents Project
<!-- Move completed agent tasks here -->

### J-Jeco Platform
<!-- Move completed J-Jeco tasks here -->

### Homelab Infrastructure
<!-- Move completed homelab tasks here -->

### Documentation & Other
<!-- Move other completed tasks here -->

---

## 📈 End of Day Summary

**Achievements:**
- 
- 
- 

**Challenges:**
- 
- 

**Tomorrow's Focus:**
- 
- 
- 

**Metrics:**
- Time spent: ___ hours
- Tasks completed: ___/___
- Blockers resolved: ___
- Documentation updates: ___

---

## 🔗 Quick Links

### Project Directories
- Agents: \`/home/fitna/J-Jeco/\`
- J-Jeco: \`/home/fitna/homelab/ai-platform/1-first-agent/\`
- Homelab: \`/home/fitna/homelab/infrastructure/\`

### Documentation
- [AGENTS.md - J-Jeco](/home/fitna/J-Jeco/AGENTS.md)
- [AGENTS.md - Homelab](/home/fitna/homelab/AGENTS.md)
- [SCHLACHTPLAN_V2.md](/home/fitna/homelab/SCHLACHTPLAN_V2.md)
- [Progress Tracking Guide](/home/fitna/homelab/shared/docs/PROGRESS_TRACKING_GUIDE.md)

### Commands
\`\`\`bash
# Generate evening report
/home/fitna/homelab/shared/scripts/create-evening-report.sh

# Create new daily sheet
/home/fitna/homelab/shared/scripts/create-daily-sheet.sh

# View today's work
cat /home/fitna/homelab/${TODAY}/DAILY_WORK_SHEET.md
\`\`\`

---

**Created:** ${FULL_DATE}  
**Last Updated:** ${FULL_DATE}  
**Template Version:** 2.0 (Enhanced Multi-Project)
EOF

# Create README for the daily directory
cat > "$DIR/README.md" << EOF
# 📅 Daily Work - ${FULL_DATE} (${DAY_NAME})

This directory contains today's work tracking and reporting documents.

## 📄 Files

### DAILY_WORK_SHEET.md
Enhanced daily task tracker with:
- ✅ Multi-project progress tracking (Agents, J-Jeco, Homelab)
- ✅ Project-specific task lists
- ✅ Time tracking per session
- ✅ Comprehensive blocker tracking
- ✅ Cross-project integration tasks
- ✅ End-of-day summary with metrics

### EVENING_REPORT.md (Generated)
Automated evening analysis report including:
- 📊 Task completion statistics
- 📈 Project-specific progress breakdown
- 🎯 Performance analysis
- 🔮 Tomorrow's preparation
- 📎 Historical context

**How to generate:** Run \`/home/fitna/homelab/shared/scripts/create-evening-report.sh\`

## 🔄 Daily Workflow

### Morning Routine
1. Review this DAILY_WORK_SHEET.md
2. Set top 3 priorities
3. Check previous day's EVENING_REPORT.md
4. Update progress baselines

### Throughout Day
1. Check boxes as you complete tasks
2. Update progress bars (each █ = 5%)
3. Document blockers immediately
4. Move completed tasks to appropriate sections
5. Track time per session

### Evening Routine
1. Move all completed tasks to "Completed Tasks" section
2. Fill out "End of Day Summary"
3. Run: \`/home/fitna/homelab/shared/scripts/create-evening-report.sh\`
4. Review generated EVENING_REPORT.md
5. Plan tomorrow's top priorities

## 📊 Progress Bar Guide

\`\`\`
Empty:    [░░░░░░░░░░░░░░░░░░░░] 0%
25%:      [█████░░░░░░░░░░░░░░░] 25%
50%:      [██████████░░░░░░░░░░] 50%
75%:      [███████████████░░░░░] 75%
Complete: [████████████████████] 100%
\`\`\`

## 🎯 Project Focus Areas

### 🤖 Agents (\`/home/fitna/J-Jeco/\`)
- Agent development and testing
- AGENTS.md documentation
- Multi-project coordination

### 🚀 J-Jeco (\`/home/fitna/homelab/ai-platform/1-first-agent/\`)
- AI platform functionality
- Agent workflows
- Knowledge base management

### 🏗️ Homelab (\`/home/fitna/homelab/infrastructure/\`)
- Infrastructure deployment
- Service health monitoring
- System integration

## 🔗 Related Documents

- **Strategic Plan:** \`/home/fitna/homelab/SCHLACHTPLAN_V2.md\`
- **Agent Guides:** 
  - \`/home/fitna/J-Jeco/AGENTS.md\`
  - \`/home/fitna/homelab/AGENTS.md\`
- **Progress Tracking:** \`/home/fitna/homelab/shared/docs/PROGRESS_TRACKING_GUIDE.md\`

---

**Created:** ${FULL_DATE}  
**Day:** ${DAY_NAME}, Week ${WEEK_NUMBER}  
**Template Version:** 2.0
EOF

echo "✅ Enhanced daily work sheet created: $DIR/DAILY_WORK_SHEET.md"
echo "✅ README created: $DIR/README.md"
echo "📂 Directory: $DIR"
echo ""
echo "📖 Usage:"
echo "   Edit work sheet: nano $DIR/DAILY_WORK_SHEET.md"
echo "   Generate evening report: /home/fitna/homelab/shared/scripts/create-evening-report.sh"
