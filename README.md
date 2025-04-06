# YourFuture
FBLA website for students to connect with employers. 

## Included functionality:
- ### Registration for both employers and students.
- ### Profile Creation for both employers and students
- ### Administrators can publish updates
- ### Submission of job postings for employers.
- ### Review and approve/delete postings by Administrators.
- ### Students can search for and apply for jobs
- ### Employers can review the students application
- ### Administrators can remove the submitted applications to give opportunity for students revise and submit.



## Database Design

```
CREATE TABLE "profile" (
  "name" TEXT NOT NULL,
  "email" TEXT NOT NULL,
  "id" INTEGER,
  "bio" TEXT,
  "info" TEXT,
  "skills" TEXT
)

CREATE TABLE "posts" (
  "id" INTEGER NOT NULL UNIQUE,
  "added_by" INTEGER NOT NULL,
  "content" TEXT NOT NULL,
  PRIMARY KEY ("id" AUTOINCREMENT)
)

CREATE TABLE "students" (
  "id" INTEGER,
  "name" TEXT NOT NULL,
  "email" TEXT NOT NULL UNIQUE,
  "password" text NOT NULL,
  "Role" TEXT NOT NULL,
  "status" TEXT,
  PRIMARY KEY ("id" AUTOINCREMENT)
)

CREATE TABLE "jobs" (
  "id" INTEGER NOT NULL UNIQUE,
  "company" TEXT NOT NULL,
  "company_role" TEXT NOT NULL,
  "pay" NUMERIC NOT NULL,
  "status" TEXT,
  "added_by" INTEGER NOT NULL,
  "Description" TEXT NOT NULL,
  PRIMARY KEY ("id" AUTOINCREMENT)
)

CREATE TABLE "intrested_jobs" (
  "company" TEXT NOT NULL,
  "role" TEXT NOT NULL,
  "name" TEXT NOT NULL,
  "email" TEXT NOT NULL,
  "user_id" INTEGER NOT NULL,
  "job_id" INTEGER NOT NULL,
  "reason" TEXT NOT NULL,
  "resume" TEXT NOT NULL,
  "filepath" TEXT NOT NULL,
  "id" INTEGER NOT NULL,
  PRIMARY KEY ("id" AUTOINCREMENT)
)
```
