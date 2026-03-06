# Agent Configuration Changelog
## Overview
Changes implemented from the demo (v1) to the onboarding configuration (v2).

### Updated: `business_hours`
- **Previous**: None
- **New**: Mon-Fri, 7:00 AM - 4:00 PM PST

### Updated: `emergency_routing_rules`
- **Previous**: Try routing to cell phone.
- **New**: Call dispatcher at 555-9001.

### Updated: `call_transfer_rules`
- **Previous**: None
- **New**: 30-second timeout. Apologize and let them know we are paging the on-call team.

### Updated: `integration_constraints`
- **Previous**: None
- **New**: No service outside 90210 zip code.

### Updated: `questions_or_unknowns`
- **Previous**: Business hours not explicitly defined.
- **New**: None
