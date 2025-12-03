# AI Co-Pilot Development Methodology

rpRunner was built using - and now includes - a structured workflow for AI-assisted development using Claude (strategy) and Cursor (implementation). This methodology is available for extending rpRunner with your own features.

---

## The Two-Agent Pattern

rpRunner uses a dual-agent approach that separates strategic planning from tactical implementation:

| Agent | Role | Strengths | Artifacts |
|-------|------|-----------|-----------|
| **Claude** | Architecture & Planning | Long-term context, creative direction, system design | `CURSOR_TASK_*.md` specs |
| **Cursor** | Implementation & Testing | Code generation, debugging, rapid iteration | Code changes, `*_COMPLETE.md` reports |

This separation of concerns enables:
- **Better planning**: Claude's extended context for big-picture thinking
- **Faster coding**: Cursor's IDE integration for immediate implementation
- **Documentation continuity**: All decisions captured in markdown
- **Reproducibility**: Clear handoff points enable async collaboration

---

## Task Specification Format

Create `CURSOR_TASK_<feature>.md` in the repo root with this structure:

```markdown
# CURSOR TASK: Feature Name

**Priority**: HIGH/MEDIUM/LOW  
**Estimated Time**: X minutes  
**Created**: Date

## Problem
What needs to be built/fixed and why

## Current State
What exists now (if applicable)

## Target State
What it should look like after implementation

## Files to Modify
- path/to/file.py - What changes
- path/to/another.py - What changes

## Implementation
Step-by-step guidance:
1. First do X
2. Then do Y
3. Finally do Z

## Success Criteria
- [ ] Testable outcome 1
- [ ] Testable outcome 2
- [ ] No linter errors

## Testing
How to verify it works
```

---

## Workflow

### 1. Plan (Claude)

- Define the feature or fix needed
- Research technical requirements
- Design the architecture
- Create detailed `CURSOR_TASK_*.md` specification
- Include examples, edge cases, and success criteria

### 2. Build (Cursor)

- Implement per spec
- Run tests and verify success criteria
- Create `*_COMPLETE.md` completion report with:
  - What was built
  - Files modified
  - Testing results
  - Any deviations from spec

### 3. Archive

- Move completed specs to `_archive/<month>/`
- Keep completion reports in repo root or docs
- Update relevant documentation

### 4. Iterate

- Next task from Claude
- Or user provides new requirements
- Repeat cycle

---

## File Organization

```
rpRunner/
├── CURSOR_TASK_*.md           # Active tasks (repo root)
├── *_COMPLETE.md              # Completion reports
├── _archive/                  # Completed work history
│   ├── dec2025/               # Month-based organization
│   │   ├── CURSOR_TASK_*.md   # Archived specs
│   │   └── *_COMPLETE.md      # Archived reports
│   └── nov2025/
├── docs/                      # Product documentation
│   ├── CO_PILOT_METHODOLOGY.md  # This file
│   ├── GETTING_STARTED.md
│   └── CUSTOMIZATION.md
└── README.md                  # Project overview
```

---

## Benefits of This Methodology

### Context Preservation
- Every decision documented
- Full reasoning captured in specs
- Easy to resume after interruptions
- New contributors can understand "why"

### Quality Control
- Specs force upfront thinking
- Success criteria ensure completeness
- Completion reports verify outcomes
- Archive provides searchable history

### Async Collaboration
- Clear handoff points
- Specs work across time zones
- Multiple implementers can work from same spec
- Progress tracked in completion reports

### Rapid Iteration
- Claude focuses on hard problems (architecture)
- Cursor focuses on fast execution (code)
- No context-switching overhead
- Each agent optimized for its role

---

## Example: Real rpRunner Feature

### Claude Creates Spec

`CURSOR_TASK_ELEVENLABS.md`:
```markdown
# CURSOR TASK: ElevenLabs Emotion Control

**Priority**: HIGH
**Estimated Time**: 2 hours

## Problem
Users need to control voice emotion and expression for documentary narration

## Implementation
1. Enhance providers/elevenlabs_provider.py with emotion tags
2. Create cli/voice_commands.py with 8 commands
3. Add voice IDs to SYSTEM_INVENTORY.json
...
```

### Cursor Implements

- Reads spec completely
- Asks clarifying questions if needed
- Implements each requirement
- Tests against success criteria
- Creates completion report

### Result

`ELEVENLABS_COMPLETE.md`:
```markdown
# ElevenLabs Integration Complete

## What Was Built
- Enhanced provider with emotion tags
- 8 new CLI commands
- 16+ emotion options
- Complete documentation

## Files Modified
- providers/elevenlabs_provider.py (+30 lines)
- cli/voice_commands.py (644 new lines)
...
```

---

## Best Practices

### For Claude (Spec Writing)

✅ **Do:**
- Include code examples
- Specify exact file paths
- List success criteria
- Estimate time realistically
- Provide context about "why"

❌ **Don't:**
- Write implementation code (leave to Cursor)
- Make vague requirements
- Skip edge cases
- Forget about testing

### For Cursor (Implementation)

✅ **Do:**
- Follow spec exactly (or document deviations)
- Check linters
- Test thoroughly
- Create detailed completion report
- Ask clarifying questions

❌ **Don't:**
- Skip steps in spec
- Make undocumented changes
- Ignore success criteria
- Leave tasks half-finished

### For Both

✅ **Do:**
- Keep specs in repo root (easy to find)
- Archive completed work by month
- Cross-reference related tasks
- Update main README when adding features

❌ **Don't:**
- Let specs pile up (archive regularly)
- Mix planning and implementation
- Skip completion reports
- Forget to update documentation

---

## Extending rpRunner

Want to add your own features? Use this methodology:

### 1. Create Spec (Manual or with Claude)

```markdown
# CURSOR_TASK_MY_FEATURE.md

**Priority**: MEDIUM
**Estimated Time**: 45 min

## Problem
I need rpRunner to do X because Y

## Files to Modify
- cli/my_commands.py (new)
- rprunner.py (add command group)

## Implementation
...
```

### 2. Implement (Manual or with Cursor)

Follow the spec, test thoroughly, document results.

### 3. Share (Optional)

- Archive your spec to `_archive/`
- Submit PR with completion report
- Others benefit from your additions

---

## Real-World Results

**rpRunner development stats using this methodology:**

- **8 major features** in December 2025 alone
- **~3,000 lines of code** written
- **~16,000 lines of documentation**
- **Zero linter errors** on completion
- **95%+ success rate** on first implementation

**Time breakdown:**
- Planning (Claude): ~30%
- Coding (Cursor): ~50%
- Testing/Docs: ~20%

**Key insight**: Upfront planning (Claude specs) reduces implementation time and bugs significantly.

---

## Comparison to Traditional Development

| Aspect | Traditional | AI Co-Pilot |
|--------|-------------|-------------|
| Planning | Mental/notes | Structured specs |
| Implementation | Manual coding | AI-assisted |
| Documentation | Often skipped | Built-in |
| Context switching | High | Minimal |
| Async collaboration | Difficult | Natural |
| Onboarding new devs | Slow | Fast (read specs) |

---

## Tools & Setup

### Required
- **Claude** (via claude.ai or API)
- **Cursor** (IDE with AI integration)
- **Markdown** editor (for specs)

### Optional
- **GitHub** (for PR-based workflow)
- **Linear/Notion** (for higher-level planning)
- **Slack** (for team coordination)

### Workflow in Cursor

1. Create/read spec: `CURSOR_TASK_*.md`
2. Open Cursor Composer (Cmd+I)
3. Paste spec or reference file
4. Let Cursor implement
5. Review changes, test, iterate

---

## Community & Contributions

Want to contribute features to rpRunner?

1. **Discuss** in GitHub Issues
2. **Spec** using this format
3. **Implement** following the spec
4. **Document** with completion report
5. **Submit PR** with both spec and report

Your specs help future contributors understand not just *what* changed, but *why*.

---

## Conclusion

The AI Co-Pilot methodology enables:
- **Faster development** (2-3x speedup in practice)
- **Better documentation** (every decision captured)
- **Lower cognitive load** (agents handle different concerns)
- **Reproducible results** (specs are repeatable)

This isn't just how rpRunner was built - it's now a feature of rpRunner itself, available for your extensions and customizations.

---

**Ready to try it?** Create your first `CURSOR_TASK_*.md` and see how structured AI collaboration transforms development! 🚀

