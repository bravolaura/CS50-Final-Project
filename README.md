# INCOMING
#### Video Demo:  <https://youtu.be/p_YJzxgzPto>
#### Description:
INCOMING is my final project, based on a web app where its principal functionallity is to send and recive emails from friends. In this web app you can manage emails, not only check your email, it will also allow you to delete them or reply. It has the basic funtionalities for a page like this.

#### app.py
##### index
Once you are log in, this page shows the emails by using db.execute (from CS50’s library) to query project.db. Select the username logged-in, and then selects the emails for that username, after that it returns the info for each email.

##### compose
Here also login is required, after that is checked, if is GET method used, it renders the compose.html with the sender autofilled. but if is POST method, that means is sending a message, so the emails table is updated with the info of that message. It also verifys that there's no empty fields. All of this is made by using db.execute (from CS50’s library) to query project.db.

##### login and logout
Read through the implementation of login first. Notice how it uses db.execute (from CS50’s library) to query project.db. And notice how it uses check_password_hash to compare hashes of users’ passwords. Also notice how login “remembers” that a user is logged in by storing his or her user_id, an INTEGER, in session. That way, any of this file’s routes can check which user, if any, is logged in. Finally, notice how once the user has successfully logged in, login will redirect to "/", taking the user to their home page. Meanwhile, notice how logout simply clears session, effectively logging a user out.

Notice how most routes are “decorated” with @login_required (a function defined in helpers.py too). That decorator ensures that, if a user tries to visit any of those routes, he or she will first be redirected to login so as to log in.

##### sent
This is similar as inbox.html, but insted of showing the received messages it shows the sent messages. Also use db.execute (from CS50’s library) to query project.db.

##### email
In here, first make sure it only be accessible using POST method. then using db.execute (from CS50’s library) to query project.db and render the email.html, it passes the values of the query.

##### register
First if is GET method used, it redirects you to the register.html for fill the fields. Then using the POST method, takes the arguments of username, password and confirmation, and stores them as an STRING. That way, is checked if the username already exists by using db.execute to query project.db.
After that, ensures the password is sumitted, and that is 8 characters long, has a number in it.
Then compares password with confirmation password. After everything is completed, the password is hash and username and password are added to the users table.

At the end, is remember which user has looged in and redirect.

##### reply
The reply function, can only be accessed by POST method, and it returns the emails table using db.execute (from CS50’s library) so it can be used to render the reply.html.

##### delete
This can only be accesed by POST method, and basically it updates (deletes) the email in project.db by using  db.execute (from CS50’s library).

#### helpers.py
Next take a look at helpers.py. Ah, there’s the implementation of apology. Next in the file is login_required. Function can return another function.
##### apology
Notice how it ultimately renders a template, apology.html. It also happens to define within itself another function, escape, that it simply uses to replace special characters in apologies. By defining escape inside of apology, we’ve scoped the former to the latter alone; no other functions will be able (or need) to call it.

##### login_required
Here apology and login_required functions are developed.

#### requirements.txt
- cs50
- Flask
- Flask-Session
- requests

#### static/
Inside of static/ is styles.css.

#### templates/
Now look in templates/.

##### apology.html
In apology.html, meanwhile, is a template for an apology. Recall that apology in helpers.py took two arguments: message, which was passed to render_template as the value of bottom, and, optionally, code, which was passed to render_template as the value of top. Notice in apology.html how those values are ultimately used! And here’s why 0:-)

##### compose.html
In compose.html, meanwhile, is a template for an compose. Recall that compose in app.py took one argument: sender, which was passed to render_template as the value of sender.
Notice in compose.html how that value is used! Also recall, that for the POST method, the sender, recipient, subject and body fields must be fill in order to upadte emails table.

##### email.html
In emails.html, is a template for an email. Can only be accessed by POST method, and render the email that was selected which is taken from the request.form.get("emailId") in the email function.

##### index.html
 It displays an HTML table summarizing, for the user currently logged in, which emails the user has recived, with the sender, recipient, subject and date. Also allows the user to view the email and/or delete it.

##### layout.html
Layout.html. It’s a bit bigger than usual, but that’s mostly because it comes with a fancy, mobile-friendly “navbar” (navigation bar), also based on Bootstrap. Notice how it defines a block, main, inside of which templates (including apology.html and login.html) shall go. It also includes support for Flask’s message flashing so that you can relay messages from one route to another for the user to see.

##### login.html
In login.html is, essentially, just an HTML form, stylized with Bootstrap.

##### register.html
Register allows a user to register for an account via a form.

Require that a user input a username, implemented as a text field whose name is username. Render an apology if the user’s input is blank or the username already exists or is not an email address.
Require that a user input a password, implemented as a text field whose name is password, and then that same password again, implemented as a text field whose name is confirmation. Render an apology if either input is blank or the passwords do not match.
Then user’s input is submitted via POST to /register.
INSERT the new user into users, storing a hash of the user’s password, not the password itself. Hash the user’s password with generate_password_hash Odds are you’ll want to create a new template (e.g., register.html) that’s quite similar to login.html.
You are able to see your rows via phpLiteAdmin or sqlite3.

##### reply.html
In reply.html, meanwhile, is a template for an reply. Recall that compose in app.py took one argument: email, which was passed to render_template as the value of email.
Notice in reply.html how that value is used! Also recall, that for the POST method, the sender and recipient are already filled up, and subject and body fields must be fill in order to upadte emails table.

##### sent.html
 It displays an HTML table summarizing, for the user currently logged in, which emails the user has sent, with the sender, recipient, subject and date. Also allows the user to view the email and/or delete it. Pretty much like the inbox.html.
