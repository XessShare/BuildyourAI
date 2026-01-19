# Skill: CodeRabbit Reviewer

## Name
**CodeRabbit Reviewer** - Automated Code Review Request & Integration

## Description
This skill automates the triggering and management of CodeRabbit AI code reviews using the configuration from `/home/fitna/homelab/.coderabbit.yaml`. It initiates focused reviews on pull requests, applies homelab-specific review rules (3-system deployment, agent prompts, infrastructure configs), validates deployment scripts for security, and tracks review findings for Sprint 26 tasks.

## When to Use This Skill

### Trigger Conditions
Use this skill when the user requests ANY of the following:
- "Run CodeRabbit review on [PR/file]"
- "Request code review"
- "Check this code with CodeRabbit"
- "Validate [code/config] for deployment"
- "Review agent prompt for Sprint 26"
- "Run security check on [file]"

### Context Indicators
- User mentions pull requests or code review
- User wants automated security/quality checks
- User discusses CodeRabbit or AI code review
- User needs validation before merging PR
- User references `.coderabbit.yaml` configuration

## Process Steps

### Phase 1: Review Configuration Verification (2 minutes)

1. **Check CodeRabbit Configuration**
   Reference: `/home/fitna/homelab/.coderabbit.yaml`

   **Key Settings:**
   ```yaml
   reviews:
     auto_review:
       enabled: true
       drafts: false  # Don't review draft PRs

     focus_areas:
       - architecture
       - security
       - performance
       - best_practices
       - maintainability

     path_instructions:
       - path: "infrastructure/**"
         instructions: |
           Review for:
           - Multi-system deployment compatibility (VPS, ThinkPad, RTX1080)
           - Docker Compose syntax and best practices
           - Secret management (no hardcoded credentials)
           - Health check implementations
           - Rollback strategy documentation

       - path: "agents/**"
         instructions: |
           Review for:
           - Agent prompt structure (80-120 lines)
           - Shared context references
           - Measurable success criteria
           - Output path specifications

       - path: "sprints/sprint-26/**"
         instructions: |
           Review for Sprint 26 specific requirements:
           - Task allocation across 6 agents
           - Deliverable file paths in prompts
           - Brand guidelines compliance
   ```

2. **Verify GitHub CLI Authentication**
   ```bash
   gh auth status

   # If not authenticated
   gh auth login
   ```

3. **Check Repository Connection**
   ```bash
   gh repo view fitna/homelab --web
   ```

### Phase 2: Trigger Review (3-5 minutes)

4. **Review Pull Request**

   **Automatic Review (on PR creation):**
   - CodeRabbit automatically reviews when PR created (if not draft)
   - Check PR for CodeRabbit comment

   **Manual Review Trigger:**
   ```bash
   # Using coderabbit CLI
   coderabbit review --pr PR_NUMBER

   # Or via gh CLI (trigger re-review)
   gh pr comment PR_NUMBER --body "@coderabbitai review"
   ```

5. **Review Specific Files**
   ```bash
   # Review single file
   coderabbit review --file path/to/file.py

   # Review directory
   coderabbit review --path infrastructure/docker/stacks/

   # Review with focus area
   coderabbit review --pr PR_NUMBER --focus security
   ```

6. **Apply Homelab-Specific Checklist**

   **Infrastructure Files:**
   - [ ] No secrets in Docker Compose files
   - [ ] All services have health checks
   - [ ] Environment variables use `.env` references
   - [ ] Traefik labels configured correctly
   - [ ] Volume mounts use named volumes (not bind mounts)
   - [ ] Network mode appropriate for service
   - [ ] Restart policy set (unless-stopped)

   **Deployment Scripts:**
   - [ ] SSH commands use key authentication (no passwords)
   - [ ] Error handling implemented (set -e)
   - [ ] Idempotent (safe to run multiple times)
   - [ ] Logging to deployment log directory
   - [ ] Health checks before proceeding
   - [ ] Rollback strategy documented
   - [ ] No hardcoded IP addresses (use variables)

   **Agent Prompts (Sprint 26):**
   - [ ] Metadata section complete (agent, model, priority, deadline, output_path)
   - [ ] Shared context references present (@project-context.md, etc.)
   - [ ] Objective is 1-2 sentences and measurable
   - [ ] 5-10 requirements listed
   - [ ] Exact deliverable file paths specified
   - [ ] 3-5 success criteria (checkboxes)
   - [ ] Copy-pasteable execution block included
   - [ ] Prompt length 80-120 lines

   **Python Code (AI Agents Platform):**
   - [ ] Type hints on all functions
   - [ ] FastAPI endpoint decorators correct
   - [ ] Pydantic models for validation
   - [ ] Async/await used correctly
   - [ ] Error handling with try/except
   - [ ] Logging statements for debugging
   - [ ] No SQL injection vulnerabilities
   - [ ] Authentication/authorization checks

### Phase 3: Review Analysis (5 minutes)

7. **Read CodeRabbit Findings**
   ```bash
   # View PR comments
   gh pr view PR_NUMBER --comments

   # Or via web
   gh pr view PR_NUMBER --web
   ```

8. **Categorize Findings**

   **Critical (Must Fix):**
   - Security vulnerabilities (SQL injection, XSS, hardcoded secrets)
   - Breaking changes without migration path
   - Missing error handling for critical operations
   - Deployment scripts without rollback

   **High (Should Fix):**
   - Performance issues (N+1 queries, missing indices)
   - Missing health checks
   - Incorrect Docker Compose syntax
   - Missing environment variable validation

   **Medium (Consider Fixing):**
   - Code duplication (DRY violations)
   - Missing type hints
   - Suboptimal algorithms
   - Missing logging statements

   **Low (Nice to Have):**
   - Minor style issues
   - Documentation improvements
   - Refactoring opportunities

9. **Generate Summary Report**
   ```markdown
   ## CodeRabbit Review Summary - PR #XX

   **Files Reviewed:** X
   **Findings:** X critical, X high, X medium, X low

   ### Critical Issues
   - [File:Line] Security: Hardcoded API key in config
   - [File:Line] Security: Missing input validation (SQL injection risk)

   ### High Priority
   - [File:Line] Missing health check in docker-compose.yml
   - [File:Line] No error handling in deployment script

   ### Recommendations
   1. Fix critical security issues before merging
   2. Add health checks to all services
   3. Implement error handling in scripts
   4. Consider refactoring duplicated code in [files]

   **Merge Recommendation:** ❌ Do not merge until critical issues resolved
   ```

### Phase 4: Address Findings (Variable)

10. **Fix Critical Issues**
    - Address all critical and high findings
    - Update code based on recommendations
    - Commit fixes to PR branch

11. **Request Re-Review**
    ```bash
    # After fixes, request re-review
    gh pr comment PR_NUMBER --body "@coderabbitai review"

    # Or push commits (auto-triggers review)
    git push origin feature-branch
    ```

12. **Track Review Resolution**
    - [ ] All critical issues resolved
    - [ ] High priority issues addressed or documented as tech debt
    - [ ] CodeRabbit approves changes
    - [ ] Tests passing (if applicable)

### Phase 5: Sprint 26 Integration (Continuous)

13. **Apply Sprint 26 Validation Rules**
    Reference: `.coderabbit.yaml` Sprint 26 section

    **Agent Prompt Validation:**
    - Verify 80-120 line structure
    - Check shared context references
    - Validate deliverable paths exist
    - Confirm success criteria are measurable

    **Infrastructure Config Validation:**
    - Verify 3-system compatibility (VPS, ThinkPad, RTX1080)
    - Check Docker Compose version compatibility
    - Validate secret references (no hardcoded values)
    - Confirm health checks implemented

14. **Update Sprint Board with Review Status**
    Update `/home/fitna/homelab/sprints/sprint-26/SPRINT_BOARD.md`:
    ```markdown
    - [x] [Agent] Task description (X SP) | Priority: Y | Owner: Z | Review: ✅ Approved
    ```

## Rules and Constraints

### Hard Rules (Must Follow)
1. **NEVER merge PR with critical security findings**
2. **ALWAYS review infrastructure changes** (deployment risk)
3. **Agent prompts MUST pass 80-120 line validation**
4. **Deployment scripts MUST have rollback strategy**
5. **Secrets MUST NEVER be hardcoded** in any file
6. **ALL critical and high findings MUST be addressed** before merge

### Soft Rules (Best Practices)
- Request review before marking PR ready
- Address medium priority findings if time permits
- Document technical debt for low priority issues
- Use CodeRabbit suggestions as learning opportunities

### Quality Gates
Before approving PR for merge:
- [ ] CodeRabbit review completed
- [ ] 0 critical findings
- [ ] 0 high priority findings (or documented exceptions)
- [ ] Tests passing (if applicable)
- [ ] Documentation updated
- [ ] Sprint 26 rules validated (if applicable)

## Expected Outputs

### Deliverables
1. **Review Summary Report** - Categorized findings
2. **Issue Tracking** - Critical/high issues logged
3. **Merge Recommendation** - Approve or block
4. **Sprint Board Update** - Review status on tasks

### Success Metrics
- ✅ CodeRabbit review triggered successfully
- ✅ All findings categorized by severity
- ✅ Critical issues resolved before merge
- ✅ Review turnaround time <24 hours

## Error Handling

### Common Issues & Solutions

**Issue: CodeRabbit not reviewing PR**
- **Solution**: Check `.coderabbit.yaml` for drafts: false setting
- **Action**: Mark PR as ready for review (not draft)

**Issue: GitHub CLI not authenticated**
- **Solution**: Run `gh auth login` and follow prompts
- **Check**: `gh auth status`

**Issue: Review findings unclear**
- **Solution**: Ask CodeRabbit for clarification
- **Command**: `gh pr comment PR_NUMBER --body "@coderabbitai explain [finding]"`

**Issue: False positive findings**
- **Solution**: Add suppression comment or update `.coderabbit.yaml`
- **Action**: Document reason for suppression

**Issue: Review takes too long**
- **Solution**: Review specific files/paths instead of full PR
- **Command**: `coderabbit review --path specific/path/`

## Example Usage

### User Request
"Run CodeRabbit review on PR #42 for the new monitoring stack deployment."

### Agent Response
```markdown
I'll trigger CodeRabbit review for PR #42 (monitoring stack deployment).

**Triggering Review...**
```bash
gh pr comment 42 --body "@coderabbitai review"
```

**Review Configuration Applied:**
- Focus areas: architecture, security, performance, best_practices
- Path-specific rules: infrastructure/** (multi-system deployment validation)

**Review Completed! Summary:**

**Files Reviewed:** 3
- infrastructure/docker/stacks/monitoring.yml
- infrastructure/docker/prometheus/prometheus.yml
- infrastructure/docker/grafana/provisioning/datasources/prometheus.yml

**Findings:**
- 0 critical ✅
- 1 high ⚠️
- 2 medium ℹ️
- 3 low 💡

**High Priority Issue:**
⚠️ monitoring.yml:45 - Grafana admin password hardcoded
**Recommendation:** Move to .env file and reference via ${GRAFANA_ADMIN_PASSWORD}

**Medium Priority:**
ℹ️ prometheus.yml:12 - Scrape interval 5s may cause high load
**Recommendation:** Increase to 15s for production

ℹ️ monitoring.yml:78 - Missing health check for Loki service
**Recommendation:** Add healthcheck section

**Merge Recommendation:** ⚠️ Fix high priority issue (hardcoded password) before merging

**Next Steps:**
1. Move Grafana password to .env file
2. Consider increasing scrape interval to 15s
3. Add health check for Loki
4. Request re-review after fixes
```

## Integration Points

### Related Skills
- **Agent 2 - DeploymentOrchestrator**: Validate deployment scripts before execution
- **Agent 3 - AgentTaskGenerator**: Validate generated agent prompts
- **Agent 8 - SOPExecutor**: Review SOP documentation for accuracy

### External Tools
- GitHub CLI (`gh`)
- CodeRabbit CLI (`coderabbit`)
- Configuration: `/home/fitna/homelab/.coderabbit.yaml`

### Data Sources
- CodeRabbit config: `/home/fitna/homelab/.coderabbit.yaml`
- Deployment prompt: `/home/fitna/homelab/CODERABBIT_DEPLOYMENT_PROMPT.md`
- Sprint board: `/home/fitna/homelab/sprints/sprint-26/SPRINT_BOARD.md`

## Version
v1.0 - Initial skill definition based on CodeRabbit integration analysis
