# Agent Configuration Changelog
## Overview
Changes implemented from the demo (v1) to the onboarding configuration (v2).

### Updated: `business_hours`
- **Previous**: None
- **New**: Mon-Fri, 8:00 AM - 5:00 PM EST

### Updated: `emergency_routing_rules`
- **Previous**: Pass directly to dispatch line.
- **New**: Direct to dispatch line at 555-8888.

### Updated: `non_emergency_routing_rules`
- **Previous**: Take a message.
- **New**: Collect details. Mention next business day follow-up.

### Updated: `call_transfer_rules`
- **Previous**: None
- **New**: If transfer to 555-8888 fails, text on-call person.

### Updated: `questions_or_unknowns`
- **Previous**: Business hours not explicitly defined.
- **New**: None
