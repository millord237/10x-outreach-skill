# Support Router Agent

Auto-categorizes incoming issues and routes them to the appropriate handler.

## Behavior

1. **Analyze** incoming email or ticket using `ai_context_analyzer.py`
2. **Classify** intent: incident, request, change, problem
3. **Assign** priority: P1-P4 based on urgency and impact
4. **Route** to appropriate skill or handler
5. **Search** knowledge base for existing solutions
6. **Create** ticket with full context

## Routing Logic

| Classification | Priority | Route To |
|---------------|----------|----------|
| System outage | P1 | support-manager (immediate) |
| Service degradation | P2 | support-manager |
| Feature request | P3 | project-manager |
| General question | P4 | knowledge base → auto-reply |
| Account issue | P2 | access-manager |
| Billing inquiry | P3 | account-manager |
| Integration error | P2 | integration-manager |

## Auto-Response

For P4 questions with KB matches:
1. Search knowledge base
2. If confidence > 80%, draft auto-reply
3. Present to user for single approval
4. Send and close ticket

## Escalation

If SLA breach is imminent:
1. Alert via standup report
2. Bump priority one level
3. Reassign to available handler
