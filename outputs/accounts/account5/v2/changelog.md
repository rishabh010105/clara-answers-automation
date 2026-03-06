# Agent Configuration Changelog
## Overview
Changes implemented from the demo (v1) to the onboarding configuration (v2).

### Updated: `business_hours`
- **Previous**: None
- **New**: Mon-Fri, 9:00 AM - 6:00 PM EST

### Updated: `emergency_routing_rules`
- **Previous**: Connect to on-call tech right away.
- **New**: Try primary at 555-5000. If no answer, try backup at 555-5001.

### Updated: `call_transfer_rules`
- **Previous**: None
- **New**: 20s on primary, 20s on backup. If both fail, apologize and say we are paging the team urgently.

### Updated: `integration_constraints`
- **Previous**: None
- **New**: Do not use or reference ServiceTitan.

### Updated: `questions_or_unknowns`
- **Previous**: Business hours not explicitly defined.
- **New**: None
