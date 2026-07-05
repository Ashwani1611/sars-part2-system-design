# Part 2 README

## Architecture decision (2.1)

went with microservices not monolith. student portal gets way more
traffic than admin panel on result day so want to scale that alone. also
if email service crashes it shouldnt take down login or marks viewing,
which would happen in a monolith since everything runs in same process
there.

## SOLID used

- single responsibility - student class only has student data, no email
  code in it. if notification stuff changes i dont touch student class.
- open closed - enrollment class can be extended (waitlistedenrollment
  in lld_classes.py) without changing original enrollment code.
- dependency inversion - enrollment talks to enrollmentrepository which
  is just an interface, not tied to one db. can change db later without
  touching enrollment.

## observer pattern (2.3d)

used this so admin panel doesnt need to know about email or audit log
services directly. it just calls notify() and whatever observers are
registered get told about it. admin panel stays separate from
notification stuff - if i want sms notifications later i just add
another observer, no changes needed in admin panel code. also added
deregister so an observer can be removed.

## redundancy (2.4)

for db - primary plus replica. if primary dies a replica takes over.

why microservices dont crash together - each service is its own process
so if email crashes it doesnt affect student portal. in a monolith
everything shares one process so a crash there can take everything down
with it. to stop that, calls from student portal to email service
should be wrapped in try catch so failure there just gets logged and
ignored, or made async so student portal doesnt wait on it at all.

sync vs async replication - sync means every write waits for replica to
confirm before its done, slower than async but no data loss. if primary
crashes right before last write reaches replica - since its sync, that
write cant be confirmed without replica having it too, so replica should
have everything already confirmed. student reading off new primary
(old replica) sees last confirmed state, nothing half done. before
saying its fully fixed, dba needs to check nothing got lost and bring
old primary back as a replica, not let both be primary at same time.