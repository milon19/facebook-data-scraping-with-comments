# Facebook pages post data scraping with comments

### Requirement 
  - <code>pip install selenium</code> <br> 
  - <code>pip install beautifulsoup4 </code>
  
### How it work
- ##### Input your facebook `username/email` and `password` in `password.py` file.
```python
_USERNAME = 'ABCabc'
_PASSWORD = 'XYZxyz'
```
- ##### Input all pages links in `pages.py` file that you want to scrap.
```python
PAGE_LINKS = [
    'https://www.facebook.com/Grameenphone',
    'https://www.facebook.com/RobiFanz',
    'https://www.facebook.com/airtelbuzz/',
    'https://www.facebook.com/10minuteschool/',
]
```

- ##### `setting.py` file:
   
    You can set <b>`number of scroll`</b> in a page that depth you want to scroll default is 3. <br/>
    You can also set <b>`grab_comment`</b> True or False. That decide that are you want to grab comment of a post or not?
    ```python
      numOfScroll = 3
      grab_comment = True
    ```

- ##### Output:
    Output will save in a file name `data.json` in  JSON format.
    
### Run
 - <code>python run.py</code>
