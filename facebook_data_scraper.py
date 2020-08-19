import time

from selenium import webdriver
from bs4 import BeautifulSoup

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-notifications")

browser = webdriver.Chrome(executable_path='./chromedriver', chrome_options=chrome_options)


def login(username, password):
    browser.get("https://www.facebook.com")
    browser.maximize_window()

    browser.find_element_by_name('email').send_keys(username)
    browser.find_element_by_name('pass').send_keys(password)
    browser.find_element_by_name('login').click()
    print('Logged in successfully. Please wait...')
    time.sleep(5)


def _scroll_page(numOfScroll):
    for scroll in range(numOfScroll + 1):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print('scrolling...{}'.format(scroll))
        time.sleep(5)


def _find_page_name(data):
    name_a = data.find_all('a', class_='_64-f')
    name_ = name_a[0].find_all('span')[0].text
    print('Extracted page name')
    return name_


def _find_post_text(content):
    post_div = content.find_all(attrs={'data-testid': 'post_message'})
    post_text = ''
    if len(post_div) > 0:
        post_div = post_div[0]
        p = post_div.find_all('p')
        for index in range(0, len(p)):
            post_text += p[index].text
    print('Extracted post text')
    return post_text


def _find_post_id(content):
    postIds = content.find_all(class_="_5pcq")
    post_id = ''
    if len(postIds) > 0:
        postId = postIds[0]
        Id = postId.get('href')
        post_id = 'https://www.facebook.com{}'.format(Id)
    print('Extracted post Id')
    return post_id


def _find_post_comments(content):
    commentList = content.find('ul', {'class': '_7791'})
    postComments = []
    if commentList:
        comment = commentList.find_all('li')
        if comment:
            for li in comment:
                comment_div = li.find(attrs={"aria-label": "Comment"})
                if comment_div:
                    print(comment_div)
                    comment_author = comment_div.find(class_="_6qw4").text
                    comment_text_span = comment_div.find("span", class_="_3l3x")
                    comment_text = ''
                    if comment_text_span:
                        comment_text = comment_text_span.text

                    replies = []
                    repliesList = li.find(class_="_2h2j")
                    if repliesList:
                        reply = repliesList.find_all('li')

                        if reply:
                            for li in reply:
                                reply_comment_div = li.find(attrs={"aria-label": "Comment reply"})
                                if reply_comment_div:
                                    print('->>> {}'.format(li))
                                    reply_author = reply_comment_div.find(class_="_6qw4").text

                                    reply_text_span = reply_comment_div.find("span", class_="_3l3x")
                                    reply_text = ''
                                    if reply_text_span:
                                        reply_text = reply_text_span.text

                                    a_reply = {
                                        'reply_author': reply_author,
                                        'reply_text': reply_text,
                                    }
                                    replies.append(a_reply)
                    a_Comment = {
                        'comment_author': comment_author,
                        'comment_text': comment_text,
                        'replies': replies,
                    }
                    postComments.append(a_Comment)

    return postComments


def _extract_post(data, grab_comment):
    user_contents = data.find_all(class_="_5pcr userContentWrapper")
    extracted_posts = []
    for content in user_contents:
        post_text = _find_post_text(content)
        post_id = _find_post_id(content)
        if grab_comment:
            post_comments = _find_post_comments(content)
        else:
            post_comments = []
        post = {
            'post_id': post_id,
            'post_text': post_text,
            'post_comments': post_comments,
        }
        extracted_posts.append(post)
        print('<<------------extracted post data------------->>')

    return extracted_posts


def extract_data(pages, numOfScroll=3, grab_comment=False):
    pages_info = []
    for page in pages:
        browser.get(page)
        print('Visited page: {}'.format(browser.title))
        _scroll_page(numOfScroll)

        if grab_comment:
            unCollapseCommentsButtonsXPath = '//a[contains(@class,"_666h")]'
            unCollapseCommentsButtons = browser.find_elements_by_xpath(unCollapseCommentsButtonsXPath)
            print('click on comment')
            for unCollapseComment in unCollapseCommentsButtons:
                action = webdriver.common.action_chains.ActionChains(browser)
                try:
                    # move to where the un collapse on is
                    action.move_to_element_with_offset(unCollapseComment, 5, 5)
                    action.perform()
                    unCollapseComment.click()
                except:
                    pass
            rankDropdowns = browser.find_elements_by_class_name('_2pln')  # select boxes who have rank dropdowns
            rankXPath = '//div[contains(concat(" ", @class, " "), "uiContextualLayerPositioner") and not(contains(concat(" ", @class, " "), "hidden_elem"))]//div/ul/li/a[@class="_54nc"]/span/span/div[@data-ordering="RANKED_UNFILTERED"]'

            print('UnCollapse all comments')
            for rankDropdown in rankDropdowns:
                # click to open the filter modal
                action = webdriver.common.action_chains.ActionChains(browser)
                try:
                    action.move_to_element_with_offset(rankDropdown, 5, 5)
                    action.perform()
                    rankDropdown.click()
                except:
                    pass

                # if modal is opened filter comments
                ranked_unfiltered = browser.find_elements_by_xpath(rankXPath)  # RANKED_UNFILTERED => (All Comments)
                if len(ranked_unfiltered) > 0:
                    try:
                        ranked_unfiltered[0].click()
                    except:
                        pass

            moreComments = browser.find_elements_by_xpath('//a[@class="_4sxc _42ft"]')
            print("Scrolling through to click on more comments..")
            print("It may takes time please wait...")
            i = 0
            while len(moreComments) != 0:
                if i % 5 == 0:
                    print("It may takes time please wait...")
                i += 1
                for moreComment in moreComments:
                    action = webdriver.common.action_chains.ActionChains(browser)
                    try:
                        # move to where the comment button is
                        action.move_to_element_with_offset(moreComment, 5, 5)
                        action.perform()
                        moreComment.click()
                    except:
                        # do nothing right here
                        pass

                moreComments = browser.find_elements_by_xpath('//a[@class="_4sxc _42ft"]')
            print("Scrolling through to click on more comments -->> Finished")

        page_source = browser.page_source
        BS_data = BeautifulSoup(page_source, 'html.parser')
        page_name = _find_page_name(BS_data)

        posts = _extract_post(BS_data, grab_comment)
        page = {
            'page_name': page_name,
            'posts': posts,
        }
        pages_info.append(page)
    return pages_info
