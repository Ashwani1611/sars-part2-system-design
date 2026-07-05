# Part 2 - System Design

## Task 2.1

Functional reqs:
1. student can login and see marks + enrolled courses
2. student can enroll in a course
3. admin can add/edit/remove students, courses, faculty

Non functional reqs:
1. app should be fast even with 50k people using it - scalability
2. app should stay up during result day - availability
3. no one should see data they're not allowed to - security

Monolith vs microservices - going with microservices here. more setup work yes but if login breaks it wont take down the whole portal, and student portal needs way more scaling than admin panel since thats where all the traffic will be on result day.

## Task 2.2

Main parts:
- Auth service - login/tokens
- Student Portal - marks + enrollment
- Admin Panel - manage students/courses/faculty
- DB
- Email service - sends notifications
- Audit log - tracks who changed what

Layers for student portal:
1. presentation - handles request, sends response
2. business logic - rules like "only see your own marks", checking course seats etc
3. data access - talks to db, sends data back up

Scaling - horizontal not vertical. one big server can still go down and eventually cant be upgraded more, better to have multiple smaller ones behind a load balancer. for load balancer algo - least connections, not round robin, since some requests are heavier (full marks history vs checking one course).

Elasticity - scale down during semester break since barely anyone uses it, scale up during result day automatically. saves money rest of the year.

Session problem - server A makes ur session, next request goes to server B, B doesnt know u. two ways to fix:
1) sticky session - LB always sends u to same server (but if that server dies u lose session)
2) shared session store like redis - any server can check it (but now thats a new single point of failure if it goes down)