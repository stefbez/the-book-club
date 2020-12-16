![](/assets/img/final-website.png)

# The Book Club

## Milestone Project 3

The project can be found here: [The Book Club](https://sb-the-book-club.herokuapp.com/).

As part of the Code Institute Full Stack Development Diploma I have created this website using the technologies learnt throughout the course so far.

This website shows off Python, Flask, Jinja, MongoDB & Materialize knowledge recently learnt along with JQuery, HTML, Bootstrap and CSS previously learnt. These skills are used to make a Book review/sharing site that allows users to view recommended books from other users, and allows them to buy the books. Users can also upload their own books and reviews in the hopes that they will inspire another user to read and enjoy that book.

### Login for testing

The default admin login for the site is:

username: admin
password: Admin123!

## UX

The UX process was vital in creating an appealing site that avid book readers and reviewers would want to visit and use. With a consistent colour scheme throughout, and easy to use features and buttons, this website allows users of any age and technical ability to share books and read reviews.

I used trello to create user stories that are relevant to what each type of user expects and wants from this site. The aim of this site is to create a community of avid book readers who want to share books and recommendations with each other.

### User stories

Writing user stories was an important step in understanding how my website should look and work. Thinking about it from the user's perspective gave me the opportunity to create something that everyone will enjoy and gives the user what they expect.

* As a user I want to see the sites name upon entering
* As a user I want to find books easily on the main page
* As a user I want to see each book's cover photo to find it easily, as if in a library
* As a user and book reader I want to be able to purchase the book recommended with a direct link
* As a user and bookworm I want to see user reviews before choosing which book i want to read next
* As a user who knows what I'm looking for, I want a search function for book title, author name or genre
* As a user and book reader I want to recommend books to others by adding them to the website
* As a user I want to be able to register and login whenever I visit to use all website features
* As a user i want to be able to edit my details after registering
* As a user i want to edit book details that i've submitted after submission
* As a user i want to delete books that i've posted if I don't want it to appear anymore
* As a user I want to be able to delete my profile if I no longer want to use the site
* As an admin user I want to have full access to edit all posts by all users
* As an admin I want to be able to add new genres and delete them in the database from the website
* As an admin user I want to be able to edit users details and delete their profile if needed

### Mockups

Mockups, created on Balsamiq, were the first stage of planning the website can be found [here](/mockups/the-book-club-mockups.pdf)

I created a copy of the database structure that can be viewed [here](/mockups/database-structure.png)

The styling has changed slightly from the mockups, featuring a larger search bar on the library page to encourage users to search for favourite authors or genres or to find a review for a book theyve considered reading. Across the site a few buttons have changed or been positioned differently to shown to enhance UX.

## Features

### Current Features

* The Book Club header shown on navbar throughout site
* Navbar for mobile and larger screens, automatically adjusting dependant on device size. Listed view for larger screens and sidebar/dropdown for smaller screens
* Consistent colour scheme throughout for easy viewing
* Header at the top of every page so the users know what page they're on
* Materialize 'Cards' on multiple pages showing book's information - covers, title, author and/or genre
* Modals used on library page containing extra book information - review, reviewer and a link to buy the book
* Search bar on home page to find book titles, authors and genres
* Profile page displaying all of the current users uploaded books
* Edit profile button allowing the user to change their details that were entered on sign up or delete their profile entirely, including any books uploaded
* Warning modal when selecting to delete any element across the site - Profiles, books or genres
* Edit book option for users to update their submissions
* Delete book option for users to delete their submissions
* Add book form to upload a new book and leave a review
* Sign in, sign up and log out functions with hashed passwords for user security
* Username check on sign up to check tat the username isn't already in use
* Password standards set inline with multiple industry standards, requiring minimum of 8 characters - at least one capital letter, number and special character
* Admin page for admin/super users
* Edit/delete all users from the admin page
* Update user settings to allow them to be an admin/super user
* Edit/delete all books from the admin page
* Add/delete genres from the admin page


### Future Features - to implement

* A book shop linked to the review site
* A chat feature so readers can discuss the books with each other after reading
* Give the user the option to upload a picture of the book cover linked to a cloud source

## Technologies Used

* [Python](https://en.wikipedia.org/wiki/Python_(programming_language)) - Using flask, the python language was used for backend production of the website and allowed many frontend functions to be displayed.
* [Flask](https://en.wikipedia.org/wiki/Flask_(web_framework)) - The web framework written in python was used for all backend functions.
* [Jinja](https://en.wikipedia.org/wiki/Jinja_(template_engine)) - The templating language used in the HTML docs to easily show the data on the frontend.
* [MongoDB](https://en.wikipedia.org/wiki/MongoDB) - The database used to hold the book, user and genre data. It can be written to by the users and admin. The data is read by python functions. The data can be updated and deleted by users and admin. 
* [Materialize](https://materializecss.com/) - The framework that provides basic styling, and interactive items such as the modals. I built upon the basic styling to create a more unique site. Useful for creating a dynamic site that works on all screen sizes.
* [Werkzeug](https://werkzeug.palletsprojects.com/en/1.0.x/) - Used to hash the passwords, to keep logging in and users passwords secure.
* [JQuery](https://jquery.com/) - JQuery library was used to initialise all of the interactive materialize functions.
* [HTML](https://en.wikipedia.org/wiki/HTML) - HTML is used to make up the base of each web page. I created elements that used jinja templating inside to create a more dynamic site
* [CSS](https://en.wikipedia.org/wiki/Cascading_Style_Sheets) - Styling for the whole site, from backgrounds to text fonts, sizes and colors.
* [Font Awesome](https://fontawesome.com/icons?d=gallery) - Used to display icons on the buttons for a good visual aid.
* [Google Fonts](https://fonts.google.com/) - Chose the fonts carefully from Google Fonts and embedded them to the CSS page and used them throughout the site.

## Testing

Testing was carried out on desktop and mobile during the building of each function for the site, making use of the debugger to find any faults in the code quickly.
I work on a mac using OS X and built the site on gitpod using Chrome. When I deployed the final version of the website it worked exactly as expected.
I tested throughout using iPhone X, Samsung Galaxy A40 and MacBook Pro. 

One issue I dealt with and was vital for correct functionality of the website came on the edit profile and admin edit profile pages. The python function used originally had the password updating each time anything was updated, resulting in the hashed password value becoming the actual password. This was remidied by updating the function to update individually. This issue was only discovered through thorough testing.
Tested the HTML pages, CSS, Python & Javascript on the [HTML validator website](https://validator.w3.org/), [CSS validator website](http://www.css-validator.org/), [Python validator website](http://pep8online.com) & [a Javascript validator website](https://jshint.com/).

#### HTML errors:

* Warnings and errors are all centered around the lack of "doctype" and the use of the Jinja template throughout. The html files inherit the DOCTYPE and head tags including links to required sources (JS, CSS and CDNs) from the base.html page. These errors are acceptable as the validator does not recognise Jinja templating.

#### CSS errors:

* No errors found.

#### Python errors:

* No errors

#### JS errors:

* No errors

### Testing across multiple devices and browsers on completion

Developed on a MacBook Pro using GitPod and checked throughout development on Chrome
Tested on the following devices:

* MacBook Pro 13" - Internet Explorer (using Safari developer tools), Safari, Chrome, Edge, Firefox, Opera
* iPhone X - Safari, Chrome, Edge, Firefox, Opera
* Samsung Galaxy A40 - Samsung Browser, Safari, Chrome, Edge, Firefox, Opera

Multiple screen sizes were tested using Chrome developer tools on the MacBook, including Moto G4, Galaxy S5, Pixel 2, iPhone 5/SE, iPhone 6/7/8, iPhone 6/7/8 Plus, iPhone X, iPad, iPad Pro, Desktop and 4K TV screens.

The site appeared and behaved as expected when testing on all different browser sizes

### Testing Process

Testing involved checking each function on the website across all devices and browsers.

* Navbar
    * The hamburger/book icon shows on a smaller screen and the links in the navbar show on larger screens

* Sign Up
    * Validation on the forms work correctly
    * The link to the login page works correctly
    * Signing up takes me to the home page/library page

* Log in
    * Validation on the forms work correctly
    * The link to the sign up page works correctly
    * Log in works correctly and takes me to the home page/library

* Logout
    * Logout works correctly from each page

* Home/Library
    * All books display as expected
    * Extra information on the books in the modals appear correctly

* Profile
    * Edit profile button works as expected
    * All users books display as expected
    * Edit and delete buttons work correctly

* Edit profile/book & Admin edit profile/book
    * Validation on the forms work correctly
    * The cancel and delete buttons work as expected
    * Editing takes me back to the page I came from for continuity

* Edit genre
    * Form working as expected
    * Delete working as expected

### Testing User Stories

* As a user I want to see the sites name upon entering
    * When the user enters the site they can clearly see 'The Book Club' on the top of the page. They will also see it on every subsequent page

* As a user I want to find books easily on the main page
    * The library page has all books listed in alphabetical order according to the title. There is also a seach function built in that the user can search for key words of a book's title, author or genre.
    * During testing I found the need to include other sort functions to the home page to easily find books. I have now included buttons to sort by Title, Author and Genre

* As a user I want to see each book's cover photo to find it easily, as if in a library
    * The library page displays book cover photo's that the user has uploaded. The book cover photos for books that individual user has uploaded are availble to view on the profile page, as well as the ability to edit and delete books from there. And the admin page contains all books with book cover images with the ability to edit and delete

* As a user and book reader I want to be able to purchase the book recommended with a direct link
    * On the library page, once the user clicks on a book for more information, a 'Buy Here' button appears below all of the book information

* As a user and bookworm I want to see user reviews before choosing which book I want to read next
    * User reviews are easily available from the library page, when you click on a book a modal appears with the user review on it

* As a user who knows what I'm looking for, I want a search function for book title, author name or genre
    * A search function is available on the library page, users are able to search by book title, author or genre

* As a user and book reader I want to recommend books to others by adding them to the website
    * The add book function allows users to upload books, with the users own review for others to see

* As a user I want to be able to register and login whenever I visit to use all website features
    * There is a sign up form available for new users and a sign in form with password authentication available for all existing users

* As a user I want to be able to edit my details after registering
    * On the profile page there is a button to edit the users profile. On this you can update your name, username and password

* As a user I want to edit book details that i've submitted after submission
    * On the profile page you can see all books that you've added to the site. From here you can edit book details.

* As a user i want to delete books that i've posted if I don't want it to appear anymore
    * On the profile page you can see all books that you've added to the site. From here you can delete these books.

* As a user I want to be able to delete my profile if I no longer want to use the site
    * On the profile page you can edit your user profile, from there you can delete the profile. Doing so will delete all of your submissions too

* As an admin user I want to have full access to edit all posts by all users
    * Admin users have access to edit all details and are trusted in doing so. They have access to ensure that all books uploaded conform to site standards, e.g correct book covers are used. They can also edit other information if a user requests this from them.

* As an admin I want to be able to add new genres and delete them in the database from the website
    * From the admin page there is a button to edit genres. From there an admin can add a new genre and delete existing genres

* As an admin user I want to be able to edit users details and delete their profile if needed
    * An admin is a trusted person and will only edit or delete a users profile where neccessary or if requested. An admin is able to do this from the admin page.

### Bugs
#### Issues found on devices and browsers

Very few issues found across all devices, browsers and screen sizes. All looked as expected and intended.

Issues:

* Internet explorer displayed the horizontal rule under the header text slightly differently to what was expected, but it still looks good.

* The "X" at the top right of the library modal would sometimes not display on iPhone X safari. Close and open modal and it would display.

## Deployment

I used GitPod to develop the site and Heroku linked to a GitHub repo to host it.

The website can be found on the link at the top of the page and here - [The Book Club](http://sb-the-book-club.herokuapp.com/). I deployed the project using Heroku. At the moment the deployed version uses the master branch, but if future updates are needed these can be done using a separate branch until all updates are tested thoroughly and can be deployed.

### Deployment using Heroku

1. Create a Github repository and open this in Gitpod or your choice of IDE
1. Go to the Heroku Dashboard and create a new app
2. In the settings tab of the app click Reveal Config Vars and enter the values for these keys: 
    * IP
    * MONGO_DBNAME
    * MONGO_URI
    * PORT
    * SECRET_KEY
3. In Gitpod create a .gitignore file
4. Create an env.py file containing all of the variables above and add it to the .gitignore
5. Create a requirements.txt by using the command "pip freeze --local > requirements.txt", in order for Heroku to know which dependancies are required to run the app
6. Create a Procfile by using the command "echo web: python app.py > Procfile"
7. Go to the Deploy tab on Heroku and navigate to the 'Deployment method' section
8. Select 'Connect to GitHub'
9. Make sure your GitHub profile is displayed and enter the repo name from step 1
10. Select search and once it loads click connect to connect to the app
11. Enable automatic deployment clicking the button below
12. Select the branch you want to deploy from in the 'Manual Deploy' section, mine is just the master branch, and select 'Deploy Branch'
13. Wait for a message saying 'Your app was successfully deployed". You can now select the 'View' button to see your deployed site
14. Once the steps above are completed whenever you push to GitHub, Heroku will automatically update

### Clone The Book Club

1. Go to the [repository](https://github.com/stefbez/the-book-club)
2. Click on the green `Code` button that features a download icon
3. Copy the URL - (https://github.com/stefbez/the-book-club.git)
4. Using the terminal in GitPod paste the code `git clone https://github.com/stefbez/the-book-club.git`
5. The whole repository folder, including all files are now available for use
6. The user will be expected to create their own env.py file

## Credits

### Content

* The footer needed to be pushed down to the bottom on some screen sizes, such as iPad pro. I found a way to do this through research online and used [freecodecamp.org/](https://www.freecodecamp.org/news/how-to-keep-your-footer-where-it-belongs-59c6aa05c59c/) to fix this issue. The code used from this website is not my own work, but a solution to a problem I was having

* The code needed to truncate a long book title, on the second line, on the library page came from [here](https://dropshado.ws/post/1015351370/webkit-line-clamp)

* I used [randomkeygen.com](https://randomkeygen.com/) for a randomly generated secret key

* [Coolors](https://coolors.co/) was used to find a colour scheme for the site

* JQuery CDN was used directly from [JQuery](https://code.jquery.com/)

* [Font Awesome](https://fontawesome.com/icons?d=gallery) icons were used for the help, volume and mute buttons

* The CDN's for Materialize were found on [MaterializeCDN](https://cdnjs.com/) and directly from [Materialize](https://materializecss.com/getting-started.html) 

* The CDN for Font Awesome was found [here](https://fontawesome.com/how-to-use/customizing-wordpress/snippets/setup-cdn-webfont)

* Fonts were found and embedded from [Google Fonts](https://fonts.google.com/)

* When stuck, I turned to the Code Institute Slack channels for advice and ideas for how to solve issues, Tutor support from Code Institute and [Stack Overflow](https://stackoverflow.com/)

* Reviews and books on the site are user uploaded and sources of these cannot be referenced.

### Media

* All images are added by the users so cannot be referenced fully

### Acknowledgements

* I took inspiration for this from the Code Institute task manager [mini project](https://github.com/Code-Institute-Solutions/TaskManagerAuth). Expanding on that project, implementing my own ideas and code and learning a lot in the process

* I received support from the tutors at Code Institute with issues and bugs that were occurring, including issues with updating forms without updating passwords each time

* I also received help with testing across numerous devices and different browsers from friends and family