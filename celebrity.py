import requests, urllib2, logging, os, math, random, time
from bs4 import BeautifulSoup
from PIL import Image

logging.basicConfig(filename='sawfirst.log',level=logging.DEBUG)

def celebrity_page(url, dest_path, dir_name):
    html = urllib2.urlopen(url)
    soup = BeautifulSoup(html)

    celebrityEvents = soup.findAll("div", {"class": "contentbox"})
    for celebrity_event in celebrityEvents:
        celebrityLinks = celebrity_event.findAll("h2")
        for celebrity_link in celebrityLinks:
            event_link = celebrity_link.a["href"]
            event_html = urllib2.urlopen(event_link)
            event_soup = BeautifulSoup(event_html)
            eventGalleryLinks = event_soup.findAll("img", {"class": "attachment-thumbnail size-thumbnail"})
            for event_gallery_link in eventGalleryLinks:
                img_thumb_link = event_gallery_link["src"]
                img_link = img_thumb_link.replace("-130x170", "")
                image_name = str(img_link.split('/')[-1:][0])

                try:
                    print(img_link)
                    imageResponse = requests.get(img_link, stream=True)
                except Exception as e:
                    logging.info(e)
                except OSError as e:
                    logging.info(e)

                if imageResponse.status_code == 200 and 'image' in imageResponse.raw.headers['content-type']:
                    img_path = '%s%s%s.jpg' % (dest_path , dir_name[0] , image_name) # if i<10 else '%s%s' % (dest_path , url.split('/')[-1:][0])
                    imageResponse.raw.decode_content = True # handle spurious Content-Encoding
                    image = Image.open(imageResponse.raw)
                    if image.height >= 600 and image.width >= 600:
                        image.save(img_path)
                        # with open(img_path, 'wb') as f:
                        #     shutil.copyfileobj(imageResponse.raw, f)
                        print('[%d] finished downloading: %s' % (imageResponse.status_code, img_path))
                else:
                    # error_count += 1
                    print('[%d] request link: %s' % (imageResponse.status_code, url))
                    # if 'text/html' in imageResponse.raw.headers['content-type']: # and error_count < 3:
                    print('Bad response [%s]' % (imageResponse.raw.headers['content-type']))
                    pass
                    # else:
                    #     break
                    time.sleep(2)

if __name__ == "__main__":
    url = "http://www.sawfirst.com/abbey-clancy"
    print(url.split('/')[-1:], url)

    dir_name = url.split('/')[-1:] if len(url.split('/')[-1:]) > 1 else [url.replace('/', 'wwlw')]
    dest_path = '/home/savitoj/Pictures/like/%s/' % dir_name[0]
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    celebrity_page(url, dest_path, dir_name)
