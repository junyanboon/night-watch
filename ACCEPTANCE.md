# Exception-console acceptance contract

This is the regression fixture for the 2026-07-26 run that motivated the Concierge-first Night Watch.

## Required classification

| Finding | Morning owner | Expected result before publish |
|---|---|---|
| A sensor bypass was removed | Concierge | Re-read the panel; if the sensor is no longer bypassed, close the gate and record the proof |
| A billing-reference message was accepted; final courtesy remains | Concierge, then message policy | Re-read correspondence; queue/reconcile the courtesy. Surface only if its live send mode still requires human review |
| A moved 509A booking is already paid | Concierge | Re-read the exact studio/date booking; close the stale Action/ticket state |
| A 901 booking is already paid | Concierge | Re-read the exact studio/date booking; close the stale Action/ticket state |
| A cooling setpoint is correct | Concierge | Re-read the live setting; close if compliant |
| An artist follow-up is due tomorrow | Concierge/time | Set `Gate: Time`/`Revisit After`; do not show today |
| Coverage item is policy-excluded | Concierge | Cancel/ignore under the canonical rule; do not show |
| A staff-name calendar block represents two documented hours | Concierge | Record the calendar-named time under the standing rule; do not ask the Ops Lead to restate it |
| Alarm credential conflicts are policy-excluded | Concierge | Apply the ignore rule; do not show |
| Correspondence arrived as a screenshot/drop | Concierge | Capture it in the correspondence/ticket system and verify the write |
| A 509B booking was already processed | Concierge | Re-read Skedda/calendar; close if verified |
| Temporary access was already processed | Concierge | Re-read the access window; close if verified |
| A heat complaint is ready to close | Concierge/Custodian | Walk the close steps and move to `Position = Review`; the Custodian terminally closes |

## Expected Ops Lead result

The thirteen findings above must not produce thirteen worksheet decisions.

- Twelve are Concierge-owned or time/policy-handled.
- The courtesy appears only when the live message send mode still requires human review.
- If the courtesy is already Sent and reconciled, the expected result is **All clear**.
- Any failed live read becomes one **system exception**, not an assumption and not a duplicated list of raw findings.

## Invariants

- The page contains no worksheet controls or chat handoff.
- `Checked overnight` is marker `checked`; `Handled automatically` is `completed + parked`; `Needs you` is the freshly verified residual count and must equal marker `needs_ops`.
- Missing handoff cannot render All clear.
- `For = Junyan` defects never appear as Ops Lead actions.
- No automation change relaxes the money, physical/access/configuration, or required-message-review hard stops.
