 1. Hierarchy & Permissions
  - Yes to --dangerously-skip-permissions by default - it's much more efficient
  - But with strict boundaries: Each worker gets a narrow, specific task with clear success criteria
  - Information hiding: Workers don't know about CCC or other sessions - they just know their task
  - One-way reporting: Workers report to me, but can't make requests or ask questions

  2. Error Recovery Strategy
  Tier 1 (Auto-retry): Syntax errors, missing imports, file not found
  Tier 2 (Retry with guidance): Logic errors, wrong approach
  Tier 3 (Fail gracefully): Non-critical features, nice-to-haves
  Tier 4 (Alert & halt): Critical path failures, data corruption risks

  3. Communication Architecture
  - Star topology: All communication flows through me (no peer-to-peer)
  - State files: Workers write progress to JSON files I monitor
  - Clear contracts: Each session gets input spec → produces output spec

  4. My Optimal Approach
  - Start with 2-3 sessions max (not 5-10) until pattern is proven
  - Use "Build a Local Todo App" as proof - frontend (React), backend (FastAPI), tests
  - Each session gets ~20-30 min focused work, then I coordinate/merge