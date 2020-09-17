# :mag_right: WebScraping :mag_right:
   API is created to scrap titles of urls. Also, you can search the keywords of the pages and get some statistics about them. 
   
## :mag_right: Requirements

1. python 3
2. pip3 

## :mag_right: How to run the API

1. Open a terminal
2. Go to de API directory.
3. Install with `pip3` all the libraries.
3. Run `python3 app.py` to start the web server
4. Enjoy it :wink:!

## :mag_right: Endpoints 
   Both of the endpoints wait an url that need to be sent through the body of the petition
   in JSON format.
   
### Title
   - **POST /title** Returns the title of the webpage. If an exception occurs, you will be informed.

### Keywords 
   - **POST /keywords** Returns some statistics about the keywords of the webpage. 
   It includes:
      The amount of keywords that the title has.
      Which of the keywords are unique.
      The frequency of the keywords.

### Example with Postman
   - Open the terminal and run the server as explained above.
   - Open postman.
   - Put the url: 'http://localhost:5000/title' .
   - Then choose the 'POST' mode.
   - After that, go to body and select raw and then JSON as format.
   - Push send button!
 
## :mag_right: Bonus
  The API has a function that returns the title of a list of webpages. Those must be stored in a `.csv` file
  which must be in the same place as `app.py`.
  You need to open the terminal and go to the API directory. Then place the `.csv` file and delete the 
  pound key which are in the 3 last lines of the code. And run `python3 app.py`. 
  It's amazing :yum:!
