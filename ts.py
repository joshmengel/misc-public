import json, os, time, datetime, random, threading, requests, string, sys, colorama
from bs4 import BeautifulSoup as soup
from discord_webhook import DiscordEmbed, DiscordWebhook
from time import sleep
from datetime import datetime
from classes.logger import logger
log = logger().log

h = True

def main():
    def purchase(x):
        def atc(ticket_number):

            while True:
                        data = {all_tickets[ticket_number] : quantity, 'submit_ticket_request' : 'Get Tickets ››'}
                        log('[TASK '+str(x)+'] Attempting to add to cart '+name_options[ticket_number])
                        f = requests.post(url, data = data)
                        if f.status_code == 302 or 200:
                            if 'https://tickets.ticketspace.co.nz/reservation' in f.url:
                                log('[TASK '+str(x)+'] Successfully reserved cart for {}: {}'.format(name_options[ticket_number], f.url))
                                try: 
                                    #insert you own webhook where it says url = ''
                                    webhook = DiscordWebhook(url='')
                                    embed = DiscordEmbed(title='Reserved Cart - Ticketspace', color=3407684)
                                    embed.set_thumbnail(url=image)
                                    embed.add_embed_field(name = 'Event', value = title, inline = True)
                                    embed.add_embed_field(name = 'Venue', value = venue, inline = True)
                                    embed.add_embed_field(name = 'Tickets', value = name_options[ticket_number] + ' x '+str(quantity) , inline = False)
                                    embed.add_embed_field(name = 'Complete Checkout', value = '[Click here!]('+f.url+')', inline = True) 
                                    try:
                                        time=(str(datetime.now())[10:19])
                                        minute = int(time[4:6])+15
                                        if minute > 60:
                                            hour = int(time[1:3])+1
                                        else:
                                            hour = int(time[1:3])
                                        expires = '{}:{}'.format(hour, minute)
                                    except:
                                        expires = 'N/A'
                                    
                                    embed.add_embed_field(name = 'Expires at', value = str(expires), inline = True)   
                                    embed.set_footer(text='@FootlockerNZ')
                                    embed.set_timestamp()
                                    webhook.add_embed(embed)
                                    response = webhook.execute()
                                    log('[TASK '+str(x)+'] Sent webhook for reservation '+f.url)#,sys.exit()
                                except Exception as e:
                                    log('[TASK '+str(x)+'] Failed to send webhook')
                                    log('[TASK '+str(x)+'] EXCEPTION OCCURED: '+str(e))
                            else:
                                log('[TASK '+str(x)+'] Status Code in 302/200 but no redirect. Product is likely sold out. Attempting to reserve next option')
                                ticket_number = ticket_number+1
                        else:
                            log('[TASK '+str(x)+'] Failed to grab reservation redirect. Restarting [Status Code:{}]'.format(str(f.status_code)))
        
        ticket_number = 0
        while True:
            title = 'Not found'
            venue = 'Not found'
            image = 'https://cdn.dribbble.com/users/1796234/screenshots/6419082/grispres.png'
            ticket_names = 'Not found'
            r = requests.get(url)
            if r.status_code == 200:
                log('[TASK '+str(x)+'] Request landed [Status Code: 200]')
                page = soup(r.text, 'html.parser')
                if h:
                    try:
                        ticket_options = page.findAll('select')
                        all_tickets = []
                        for i in ticket_options:
                            all_tickets.append(i['name']) 
                        if not all_tickets:
                            log('[TASK '+str(x)+'] Tickets are currently unavailable. Retrying in {}s'.format(str(delay))), sleep(int(delay))
                            purchase(x)
                        else:    
                            log('[TASK '+str(x)+'] Scraped ticket options - {}'.format(all_tickets))
                    except:
                        log('[TASK '+str(x)+'] Failed to scrape ticket ids. Retrying in {}s'.format(str(delay))), sleep(int(delay))
                        purchase(x)

                    try:
                        title = page.find('h1', {'class':'showtitle'}).text.strip()
                    except:
                        log('[TASK '+str(x)+'] Failed to scrape title')

                    try:
                        name_options = []
                        ticket_names = page.findAll('span', {'class':'product_name'})
                        for i in ticket_names:
                            name_options.append(i.text.strip())
                    except:
                        log('[TASK '+str(x)+'] Failed to scrape ticket names')

                    try:
                        venue = page.find('span', {'class':'venuename'}).text.strip()
                    except:
                        log('[TASK '+str(x)+'] Failed to scrape venue')
            
                    try:
                        image = 'https:'+page.find('img')['src']
                    except:
                        log('[TASK '+str(x)+'] Failed to scrape image')

                    try:
                        log('[TASK '+str(x)+'] Scraped ticket details: {} - {} - {} - {} '.format(title, name_options[ticket_number], all_tickets[ticket_number], venue))
                        atc(ticket_number)
                    except:
                        atc(ticket_number)
                else:
                    log('[TASK '+str(x)+'] Something went wrong. Restarting')
            else:
                log('[TASK '+str(x)+'] Request  failed to land [Status Code: {}]'.format(str(r.status_code)))

    for x in range(tasks):
            try:
                x = x + 1
                log('[TASK '+str(x)+'] Starting task')
                (threading.Thread(target=purchase, args=(x, ))).start()
            except Exception as e:
                log('[TASK '+str(x)+'] EXCEPTION OCCURED: '+str(e))


print('-----------------------------------------')
print('-----------------------------------------')
print('-----------------------------------------')
print('- Ticketspace Script - By @FootlockerNZ -')
print('-----------------------------------------')
print('-----------------------------------------')
print('-----------------------------------------')

url = input('Enter event url: ')
print('-----------------------------------------')
quantity = int(input('Enter the quantity of tickets you want: '))
print('-----------------------------------------')
tasks = int(input('How many tasks do you want to run?: '))
print('-----------------------------------------')
delay = int(input('Enter your delay (s): '))
print('-----------------------------------------')

def select():
    start = int(input('Enter 1 to start or 0 to exit: '))
    print('-----------------------------------------')
    if start == 0:
        sys.exit()
    elif start == 1:
        main()
    else:
        print('Invalid input'), sleep(3)
        print('-----------------------------------------')
        select()

select()
