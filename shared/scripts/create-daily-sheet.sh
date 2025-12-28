#!/bin/bash
# Daily Work Sheet Generator
# Creates a new daily work sheet for today

# Get today's date
TODAY=$(date +%d.%m.%y)
FULL_DATE=$(date +%Y-%m-%d)
DIR="/home/fitna/homelab/${TODAY}"

# Create directory
mkdir -p "$DIR"

# Generate work sheet
cat > "$DIR/DAILY_WORK_SHEET.md" << 'EOF'
# 📅 Daily Work Sheet - ${FULL_DATE}

**Status:** 🟡 In Progress  
**Focus:** Homelab Infrastructure & J-Jeco AI Platform  
**Priority Level:** High  

---

## 📊 Progress Dashboard

### Overall Progress
```
Infrastructure: [░░░░░░░░░░░░░░░░░░░░] 0%
AI Platform:    [░░░░░░░░░░░░░░░░░░░░] 0%
Documentation:  [░░░░░░░░░░░░░░░░░░░░] 0%
Testing:        [░░░░░░░░░░░░░░░░░░░░] 0%
```

### Daily Statistics
- **Tasks Total:** 0
- **Completed:** 0
- **In Progress:** 0
- **Blocked:** 0
- **Not Started:** 0

---

## 🎯 Today's Priorities (Top 3)

### Priority 1: 
- [ ] 

### Priority 2: 
- [ ] 

### Priority 3: 
- [ ] 

---

## 📋 Task List

### Morning Tasks
- [ ] Review yesterday's progress
- [ ] Check system health
- [ ] Plan today's work

### Core Work
- [ ] 
- [ ] 
- [ ] 

### End of Day
- [ ] Update progress dashboard
- [ ] Document learnings
- [ ] Plan tomorrow

---

## 🚧 Blockers & Issues

### Active Blockers
None

### Resolved Today
- 

---

## 📝 Notes & Learnings

### Key Discoveries
- 

### Questions to Resolve
- 

---

## 🎉 Completed Tasks

<!-- Tasks will be moved here as completed -->

---

## 📈 End of Day Summary

**Achievements:**
- 
- 

**Challenges:**
- 
- 

**Tomorrow's Focus:**
- 
- 

**Metrics:**
- Time spent: ___ hours
- Tasks completed: ___
- Blockers resolved: ___

---

**Created:** ${FULL_DATE}  
**Last Updated:** ${FULL_DATE}  
**Template Version:** 1.0
EOF

# Replace placeholders
sed -i "s/\${FULL_DATE}/${FULL_DATE}/g" "$DIR/DAILY_WORK_SHEET.md"
sed -i "s/\${TODAY}/${TODAY}/g" "$DIR/DAILY_WORK_SHEET.md"

echo "✅ Daily work sheet created: $DIR/DAILY_WORK_SHEET.md"
echo "📂 Directory: $DIR"
