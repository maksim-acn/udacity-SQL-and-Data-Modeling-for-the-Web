---
title: "Backend Developer with Python"
source: "https://learn.udacity.com/nd0044?version=5.2.0&partKey=cd0046&lessonKey=e0630afb-6b78-4551-974b-f6854d303dc1&project=rubric"
author:
published:
created: 2026-04-29
description:
tags:
  - "clippings"
---
## Rubric

Use this project rubric to understand and assess the project criteria.

## Data Models

| Criteria | Submission Requirements |
| --- | --- |
| Implement data models in relational, normalized form. | Correct data types are associated with each field.  The `Shows` object has a relationship that connects Artists and Venues, and this relationship is of the correct type. In other words, the project demonstrates the ability to appropriately select from the following types of relationships:  - One-to-one - One-to-many - Many-to-many |
| Connect data models to a database. | The code creates a local postgresql database connection. |
| Demonstrate a good grasp of database normalization. | The `Shows` model has properly set up foreign keys.  The Artists and Venues models are in third normal form. |
| Demonstrate a good grasp of SQLAlchemy. | The code uses SQLAlchemy syntax to completely define the models.  The code has accurate SQL queries wrapped in SQLAlchemy commands per API endpoint, calling to define data models and serving expected responses per API endpoint.  The code only uses raw SQL where SQLAlchemy wrappers do not suffice, otherwise minimizing use of raw SQL. |

## SQL

| Criteria | Submission Requirements |
| --- | --- |
| Use SQL syntax to select records from a database. | The code successfully translates SQLAlchemy code for selecting records from the database into the equivalent PostgresSQL command(s) for selecting records from the database.  The code demonstrates correct use of `SELECT` and `WHERE` query statements to execute search successfully. |
| Use SQL syntax and SQLAlchemy to join relational tables and conduct joined queries. | `JOIN` statements are used to correctly execute joined queries.  The code joins tables from existing models to select Artists by Venues where they previously performed, successfully filling out the Venues page with a “Past Performances” section.  The code joins tables from existing models to successfully fill out the Artists page with a “Venues Performed” section.  The code includes correct equivalents in SQLAlchemy ORM for all corresponding SQL statements. |
| Use SQL to create records with uniqueness constraints. | Code connects the New Artist and New Venue forms to a database by successfully using SQLAlchemy to insert new records into the database upon form submission.  Understands the equivalent SQLAlchemy command in SQL syntax, using INSERT INTO.  Code correctly uses SQL constraints to ensure fields that need to be unique, and fields that are required, are given these constraints on the database level, throwing an error if otherwise. |

## Application Quality & Deployment

| Criteria | Submission Requirements |
| --- | --- |
| Demonstrate the ability to construct a well-organized code base. | Code is decoupled into relevant parts across the files.  The code includes good use of comments where there is lack of clarity. Where comments are not provided, the code is self-documenting.  Encapsulate querying code in proper places across Models and API endpoints. |
| Create a web app that builds successfully and runs without errors | - There are no build or compilation errors in running code and launching the web app. - A user can successfully execute a Search that queries the database. - A user can view a Venue Page with venue and artist information from the database. - A user can view an Artist Page with venue and artist information from the database. - A user can create a new venue listing via the New Venue Page. - A user cannot submit an invalid form submission (e.g., using an invalid State enum or with required fields missing; missing city, missing name, or missing genre is not required). - A user can create new artist listings via the New Artist Page. - A user cannot submit an invalid form submission (e.g., without required fields) - A user should be able to click on the venue for an upcoming show on the Artist's page and, on that Venue's page, see the same show in the Venue Page's upcoming shows section. |

## Suggestions to Make Your Project Stand Out

1. CHALLENGE: Implement time availability, so that an artist is only available to be booked at certain dates/times. Disable the ability to create book an artist for a show outside of their availability.
2. Show Recent Listed Artists and Recently Listed Venues on the homepage, returning results for Artists and Venues sorting by newly created. Limit to the 10 most recently listed items.
3. Showcase what albums and songs an artist has on the Artist’s page.

