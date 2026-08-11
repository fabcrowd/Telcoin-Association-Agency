#!/bin/bash
# Pre-tool status hook — shows a human-readable one-liner before each tool runs
# Outputs JSON with systemMessage field, which Claude Code displays in the UI

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name // "unknown"')

case "$TOOL" in
  Read)
    FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""' | xargs basename 2>/dev/null)
    MSG="Reading $FILE"
    ;;
  Write)
    FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""' | xargs basename 2>/dev/null)
    MSG="Writing $FILE"
    ;;
  Edit)
    FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""' | xargs basename 2>/dev/null)
    MSG="Editing $FILE"
    ;;
  MultiEdit)
    FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""' | xargs basename 2>/dev/null)
    MSG="Editing $FILE"
    ;;
  Bash)
    CMD=$(echo "$INPUT" | jq -r '.tool_input.command // ""' | tr '\n' ' ' | cut -c1-80)
    MSG="$ $CMD"
    ;;
  WebSearch)
    QUERY=$(echo "$INPUT" | jq -r '.tool_input.query // ""' | cut -c1-70)
    MSG="Searching: $QUERY"
    ;;
  WebFetch)
    URL=$(echo "$INPUT" | jq -r '.tool_input.url // ""' | sed 's|https://||;s|http://||' | cut -c1-70)
    MSG="Fetching $URL"
    ;;
  Glob)
    PAT=$(echo "$INPUT" | jq -r '.tool_input.pattern // ""')
    MSG="Scanning files: $PAT"
    ;;
  Grep)
    PAT=$(echo "$INPUT" | jq -r '.tool_input.pattern // ""' | cut -c1-50)
    MSG="Searching codebase for: $PAT"
    ;;
  Agent)
    DESC=$(echo "$INPUT" | jq -r '.tool_input.description // "subagent"')
    MSG="Launching agent: $DESC"
    ;;
  TodoWrite)
    MSG="Updating task list"
    ;;
  *)
    MSG="$TOOL"
    ;;
esac

jq -n --arg msg "$MSG" '{"systemMessage": $msg}'
