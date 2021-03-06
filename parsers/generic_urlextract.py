#from urlextract import URLExtract
import re
import lib.db
import lib.utils
import urlparse


#TODO: Add this when i move project to python3
# def extract_urls_urlextractor(tool_output):
#     #print(type(tool_output))
#     extractor = URLExtract()
#     urls = extractor.find_urls(tool_output)
#     #print(urls)
#     #for url in extractor.find_urls(tool_output):
#         #print("* " + urls)
#         #print(type(url))
#         #print(urls)
#     return urls



def extract_urls_regex(tool_output):
    intereseting_urls = []
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', tool_output)
    not_interesting_extensions = [".png", ".ico", ".js", ".css", ".woff2", ".ttf", ".jpg", ".jpeg", ".svg", ".eot", ".woff",".gif"]
    for url in urls:
        if not url.endswith(tuple(not_interesting_extensions)):
            intereseting_urls.append(url)
    return intereseting_urls


def extract_urls(tool_output):
    #TODO: Add uncomment these three lines and comment out the forth when i move project to python3
    #a = extract_urls_urlextractor(tool_output)
    #b = extract_urls_regex(tool_output)
    #urls = list(set().union(a, b))
    urls = extract_urls_regex(tool_output)
    return urls


def is_url_in_scope(url):
    workspace = lib.db.get_current_workspace()[0][0]
    try:
        parsed_url = urlparse.urlparse(url)
        scheme = parsed_url[0]
        if ":" in parsed_url[1]:
            vhost, port = parsed_url[1].split(':')
        else:
            vhost = parsed_url[1]
            if scheme == "http":
                port = 80
            elif scheme == "https":
                port = 443
        path = parsed_url[2].replace("//", "/")
    except:
        print("error parsing url")
        if not scheme:
            pass
    in_scope = lib.db.is_vhost_in_db(vhost,workspace)
    if in_scope:
        return str(True),vhost,port,url.rstrip("/"),workspace
    else:
        return str(False)

def insert_url_into_db(vhost,port,url,workspace):
    db_path = (vhost, port, url, 0, "", workspace)
    lib.db.insert_new_path(db_path)
    print("Found Url: " + str(url))

def extract_in_scope_urls_from_task_output(tool_output):
    urls = extract_urls(tool_output)
    for url in urls:
        exists,vhost,port,url,workspace = is_url_in_scope(url)
        if exists == "True":
            insert_url_into_db(vhost,port,url,workspace)





