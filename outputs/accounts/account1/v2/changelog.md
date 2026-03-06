# Agent Configuration Changelog
## Overview
Changes implemented from the demo (v1) to the onboarding configuration (v2).

### Updated: `business_hours`
- **Previous**: None
- **New**: Mon-Fri, 8:00 AM - 5:00 PM EST

### Updated: `emergency_routing_rules`
- **Previous**: Route to on-call technician.
- **New**: Sprinkler -> phone tree. Alarms -> 555-0199.

### Updated: `non_emergency_routing_rules`
- **Previous**: Take a message.
- **New**: Collect details. Mention next business day follow-up.

### Updated: `call_transfer_rules`
- **Previous**: None
- **New**: 60-second timeout. If fails, notify dispatch via SMS.

### Updated: `questions_or_unknowns`
- **Previous**: Business hours not explicitly defined.
- **New**: None
