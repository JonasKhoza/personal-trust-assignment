### Project Setup


1. Ensure that you have docker, docker-compose
2. Clone the existing repository
3. Start up the application
```bash
sudo docker-compose up -d
```
4. Run migrations
```bash
sudo docker-compose exec project_web python manage.py migrate
```
5. Create superuser
```bash
sudo docker-compose exec project_web python manage.py createsuperuser
```

### Instruction

This repository includes a basic Django application which can be run using Docker Compose.

Some basic models, views and templates using Bootstrap have been created, and it is now up to you to expand on 
this with some additional functionality. 

Please see below user stories to be used in driving the development of this application. **It will be important to write 
unit and/or functional tests for every user story that you implement.**                                                   

Once complete, commit your code to Github and share your project with us. You have 72 hours to complete as much as you 
are able to, and send your code back to us.

### User Stories

#### Authentication
1. As a non-authenticated user, I should have the ability to login to the application so that I can access the client list.
**Acceptance Criteria:**
    - When a user is not authenticated, the navbar should show that they are not logged in
    - When a user is authenticated, the navbar should show the user logged in, e.g "Logged in as Joe Soap"
    - If the user is not authenticated, there should be a button on the navbar which allows the user to login
    - Login button should only be visible and available for non-authenticated users

2. BONUS: As an authenticated user, I should have the ability to logout out of the application so that I can end my session
**Acceptance Criteria:**
    - Logout button should only be visible and available for authenticated users

#### Clients
1. As a non-authenticated user, I should not be able to access the client list because it may contain confidential information.
**Acceptance Criteria:**
    - Non-authenticated user should not be able to access client list endpoint
    - Non-authenticated user should not be able to see a nav button that directs them to the client list

2. As an authenticated user, I would like to view only 20 clients at a time on the list so that it is manageable without having to scroll down the page
**Acceptance Criteria:**
    - The client list should be paginated to only show 20 clients per page 
    - There should be a pagination form below the list allowing the user to access the following pages
    - The user should have the ability to access the first and last page of results

3. As an authenticated user, I need the ability to search for my clients on name, surname and ID number so that I can easily find clients I am looking for.
**Acceptance Criteria:**
    - Basic search bar above the client list, allowing user to enter either a name, surname or ID number which then filters the list on the server and filters the list accordingly
    - BONUS: Update the list in realtime as the user types in the search bar, even though it is searching on the server side (Welcome to use HTMX or other)

4. As an authenticated user, I need the ability to add new clients along with their addresses, so that there details are stored and accessible via the client list.
**Acceptance Criteria:**
   - The client list view should have a button for the user to create a new client
   - A form should open in a new page which allows the user to input the client details, as well as a Physical and Postal address
   - The client should have both a postal and physical address
   - Once successfully created, the user should be redirected back to the list view
   - Unauthenticated user should not be able to create a client

5. As an authenticated user, when I create a client, I need to validate the ID number to ensure it is a valid RSA ID number and there isn't already a client with that ID number.
**Acceptance Criteria:**
   - As part of the form validation, the below needs to be validated on the server side, and display errors on the form if not valid:
     - Client's ID number is a valid South African ID number and validated against the Luhn algorithm. [Decoding your South African ID number](https://www.westerncape.gov.za/general-publication/decoding-your-south-african-id-number-0)
     - Ensure that a client with the same ID number doesn't already exist in the system
     

#### Client Relationships
1. As an authenticated user, I need the ability to create relationships between clients, so that I am able to identify relatives of my clients.
**Acceptance Criteria:**
   - This will require a new model to store client relationships 
   - On a client row in the client list row, include a button which directs the user to a form allowing them to add a client relationship
   - Allow the user to specify the nature of the relationship (e.g Husband, Wife, Father, Daughter) 
   - When creating a relationship for a client, the inverse should be created simultaneously, i.e When user clicks on Jane Doe to add John Doe as her husband, this should automatically create an 'inverse' record on John Doe stating that Jane Doe is his wife
   - Client cannot have a relationship with themself, it should not be possible for a user to create such
   - Client can only have one relationship with each other client, i.e we cannot add John Doe as a husband and as a son to Jane doe, the validator should prompt the user that this client already has a relationship with John Doe
  



