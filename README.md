# SIMLAB
SIMULATING ELECTRICAL CIRCUITS.. maybe more
Guys this is the readme file


This is the file structure


simlab
├── __init__.py
├── routes.py
├── static
│   ├── assets
│   ├── css
│   │   ├── landing.css
│   │   └── main.css
│   └── js
│       └── landing.js
└── templates
    ├── home.html
    ├── landing.html
    ├── landing_layout.html
    └── layout.html

There are two more folders but those are for when you enable the virtual environment



Now What's where??

__init__.py is the setup file for this module as I call it. Here we add in methods that are related to 
configuration of the app, like the secret key, api key, and more.


As name suggests routes.py has all the routes, you can go ahead and add more routes just to play with it.



The static files have been further branched to assets, css, and js

assets will contain the images ,sounds and that stuff.
css is for css
js is for js files


Now templates ,
this is where we put in the template files for rendering on current route.




There are more stuff to do but this is just an initial setup and we will build on top of this.


Feel free to do any type of modifications (^^)


TroubleShooting

1. I changed the css, js file but it is not updated on the site.
    Solution : This is not flask's fault, Browser has cached the site to reload do Ctrl + Shift + R, this will solve the issue.
2. I got a broken link
    The syntax for mapping to a route is {{url_for('routename')}} , this routename should match the one you have on the routes file,
3. Linking to static files failed??
    syntax for linking to static files is
    {{url_for('static', 'dirname/filename.extension')}}

    dirname is the particular for that type of static file,
    for example if i want to bring in some image 2.png from assets folder
    I will write {{url_for('static', 'assets/2.png')}}


More errors, google or if i can then me )>.<( 
