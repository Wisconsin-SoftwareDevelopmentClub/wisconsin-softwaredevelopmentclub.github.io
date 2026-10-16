# SDC-Site

Hey there future maintainer! I have done my best to setup the framework for our website going forward.
Maybe it gets scrapped, but if it does not hopefully you can refer to this in order to continue to
improve it, or at the very least keep it updated with the latest info!

In addition to this README page, I have also added comments depicting what will be 
in a given spot after script injections throughout the html in order to clarify 
where some of the elements are coming from.

# Configuration

The site is configurable without touching any of the html! Luckily for you I put
in a little bit of extra effort to make a configuration file, 'config.json'. This 
file has some clear self-explanatory configurations, but since JSON 
does not have comments I will list them here.

* The Board array is made up of 'Board Member' objects that can have
the following data:
    * name
    * title (position on the board)
    * email
    * imgURL (uses absolute path)
    * isContact (whether to list this member in our contacts section in the footer)
* discordLink
* projectLink (project GitHub or whatever platform you use). Changing from
GitHub will require some decent reworks UI wise if that is wanted
* LinkedInLink (note the capital 'I')
* isShowCriticalInfo allows toggling of the critical section underneath the header
* criticalInfo is the text that is displayed by the critical section when enabled

You can add your own configurations to the config file if you feel like it is
warranted. Access to the vars / states is easy using the fetch() API (see
header-footer.js for an example of that). Please note that functions can 
override if they are named the same thing and multiple scripts are active in
the same file, i.e. rename the function that is called by the last then() 
function to something unique.

# Technologies

Everything is done using plain ol' HTML, CSS, and JS. No special libraries etc.
That may be a downside to some, but if you are not familiar with the tech
then it is a plus.

# Layout

index.html is our homepage (and is purposefully named as such according to HTML standards). The homepage has some 'og' meta tags that are for SEO, primarily with
LinkedIn. At the bottom of index.html is where all the articles are, which are
mostly announcements on various parts of the club.

Also on the homepage are a number of scripts that you should be aware of:

* highlight-script.js
* header-footer.js
* date-checker.js
* old-news.js

The 'highlight-script.js' script is specific to the homepage - it plays the carousel with
opacity transitions.

The 'header-footer.js' script is on **all** pages, and should be added to all
new pages since it injects the respective header and footer into the document 
so we do not have to copy paste those pieces on every page (yay).

The 'date-checker.js' script is for time sensitive articles (see #Articles). It
reads all HTML elements on the page with the 'due' attribute, parsing the string
contained by the attribute and comparing that with the current time to see if
it is outdated or not. If it is outdated, some special formatting is applied
(lower opacity, redness and a CLOSED banner appears as of this writing).
The due format is '**yyyy-mm-dd**'. This and the article format is described in
comments where they are used as well.

The 'old-news.js' script deals with overflown news - a bar appears when there is more
news to take in than space on the screen. Clicking the button shows the rest of the
off-screen articles.