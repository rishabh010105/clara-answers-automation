# Agent Configuration Changelog
## Overview
Changes implemented from the demo (v1) to the onboarding configuration (v2).

### Updated: `business_hours`
- **Previous**: None
- **New**: Mon-Sat, 7:00 AM - 6:00 PM CST

### Updated: `emergency_routing_rules`
- **Previous**: Connect to technician.
- **New**: Call on-call tech at 555-0200.

### Updated: `call_transfer_rules`
- **Previous**: None
- **New**: 45-second timeout. Apologize and assure follow-up.

### Updated: `integration_constraints`
- **Previous**: None
- **New**: Never create AC jobs in ServiceTrade after hours. Heating emergencies are OK.

### Updated: `questions_or_unknowns`
- **Previous**: Business hours not explicitly defined.
- **New**: None
