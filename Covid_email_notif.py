import smtplib
import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import plotly.graph_objects as go
import plotly.io as pio
from email.mime.image import MIMEImage


emaillist = ['nikhilnagarkar9@gmail.com','nikhilnagarkar97@gmail.com','madhura147@gmail.com','vidyadharnagarkar@yahoo.com','srujanpalkar@gmail.com',
              'vinayanagarkar.v@gmail.com','pranav.jagirdar92@gmail.com','mukund.jagirdar@rediffmail.com','saisjoshi18@gmail.com','pratik.jsh@gmail.com']

#emaillist = ['nikhilnagarkar97@gmail.com']
pio.orca.config.executable = (r'C:\Users\Nikhil\AppData\Local\Programs\orca\orca.exe')
def covid_email(sender,recipients,subject,message):

  msg = MIMEMultipart()
  msg['Subject'] = subject
  msg['From'] = 'ncov.alert@gmail.com'
  msg.attach(message)

  fp = open(r'C:\Users\Nikhil\fig1.png', 'rb')
  msgImage = MIMEImage(fp.read())
  fp.close()

  msgImage.add_header('Content-ID', '<image1>')
  msg.attach(msgImage) 

  
  fp = open(r'C:\Users\Nikhil\fig2.png', 'rb')
  msgImage = MIMEImage(fp.read())
  fp.close()

  msgImage.add_header('Content-ID', '<image2>')
  msg.attach(msgImage) 


  
  fp = open(r'C:\Users\Nikhil\fig3.png', 'rb')
  msgImage = MIMEImage(fp.read())
  fp.close()

  msgImage.add_header('Content-ID', '<image3>')
  msg.attach(msgImage) 
  

  s = smtplib.SMTP('smtp.gmail.com',587)

  s.starttls()

  s.login('ncov.alert@gmail.com','covid-19')

  

  s.sendmail('ncov.alert@gmail.com',recipients,msg.as_string())

  s.quit()    

def create_HTML(date,time,worldwide,india,countries):
  
  html1 = """\
  <html>
    <head></head>
    <body>
    <h2 style="text-align: left;"><strong>Covid-19 Update</strong></h2>
    <p>&nbsp;</p>
    <p style="text-align: left;"><strong>Date: {0}
  """.format(date)

  html2 = """\
    &nbsp; &nbsp;Time: {0}</strong></p>
    <p>&nbsp;</p> 

    </body>
  </html>
  """.format(time)

  html_worldwide = """\
    <h3 style="text-align: left;"><span style="text-decoration: underline;">Worldwide:</h3>
    {0}
    <p><img src= "cid:image1" /></p>
    <p>&nbsp;</p>
    """.format(worldwide.to_html(index=False))

  html_india = """\
    <h3 style="text-align: left;"><span style="text-decoration: underline;">India:</h3>
    {0}
    <p><img src= "cid:image2" /></p>
    """.format(india.to_html(index=False))

  html_country = """\
    <h3 style="text-align: left;"><span style="text-decoration: underline;">Country-wise:</h3>
    {0}
    <p><img src= "cid:image3" /></p>
    <p>&nbsp;</p>
    <h4><em>The data is from Worldometer's&nbsp;real-time updates.</em></<em></h4>
    <p>&nbsp;</p>
    <p>For More Information:</span></p>
    <p><a href="https://www.worldometers.info/coronavirus/">https://www.worldometers.info/coronavirus/</a></p>
    <p><a href="https://www.who.int/emergencies/diseases/novel-coronavirus-2019">https://www.who.int/emergencies/diseases/novel-coronavirus-2019</a></p>
    <p><a href="https://www.mohfw.gov.in/">https://www.mohfw.gov.in/</a></p>
    <p>&nbsp;</p>
    </body>
  </html>
  """.format(countries.to_html(index=False))




  html = html1 + html2 + html_worldwide + html_india + html_country
  
  message = MIMEText(html,'html')
  return message





names = []
data =[]
country_1 = []
country_2 = []
country_3 = []
country_4 = []
country_5 = []
country_china = []
country_list = [country_1,country_2,country_3,country_4,country_5]


url = "https://www.worldometers.info/coronavirus/"
url1 = "https://www.worldometers.info/coronavirus/country/china/"
url2 = "https://www.worldometers.info/coronavirus/country/india/"
key = 1
key_1 = 1
while True:
  date_time = datetime.now()

  time_1 =  int(str(date_time.hour) + str(date_time.minute))
  #print(int(str(date_time.hour) + str(date_time.minute) ))
  if( len(str(date_time.minute)) == 1):
    time_1 = str(date_time.hour) + '0' + str(date_time.minute)
    time_1 = int(time_1)



  #print(time_1)
    
  #if True:
  if ((2059 < time_1 < 2101 and key == 1) ):
    print('OK')
    key = 0
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36'}

    page = requests.get(url,headers=headers)
    soup = BeautifulSoup(page.content,'html.parser')


    #worlwide cases
    global_no_cases  = soup.find_all('div',attrs={'id':'maincounter-wrap'},limit = 3)
    global_no        = [point.find('span').text.strip() for point in global_no_cases]  


    #Countrywise Cases
    country_table   = soup.find('div',attrs={'id':'nav-tabContent'})
    country_1_5     = country_table.find_all('tr',limit = 7)[2:]

    for point in country_1_5:
        names  += [point.find('a',attrs={'class':'mt_a'}).text]
        for i in point.findAll('td'):
            data += [i.text.strip()]
    print(names)
    print(data)    
    for i in (0,1,3,5):
        country_1 += [data[i]]
        country_2 += [data[i+12]]
        country_3 += [data[i+24]]
        country_4 += [data[i+36]]
        country_5 += [data[i+48]]

    """
    #Data of china 
    page = requests.get(url1,headers=headers)
    soup = BeautifulSoup(page.content,'html.parser')
    china  = soup.find_all('div',attrs={'id':'maincounter-wrap'},limit = 3)
    country_china        = [point.find('span').text.strip() for point in china]
    country_china.insert(0,'China')
    #print(country_china)
    #print(country_list) 
    #Sorting country wise data
    
    for i in range(0,5):
          
        if(int(country_list[i][1].replace(',','')) < int(country_china[1].replace(',',''))):
            #print(country_list[i][1],country_china[1])
            country_list.insert(i,country_china)
    """

    print(country_list)

    #Data of India
    page = requests.get(url2,headers=headers)
    soup = BeautifulSoup(page.content,'html.parser')
    india  = soup.find_all('div',attrs={'id':'maincounter-wrap'},limit = 3)
    country_india        = [point.find('span').text.strip() for point in india]


    #Pandas frame formation
    worldwide_frame = {'Total Cases':[global_no[0]],
                      'Total Deaths':[global_no[1]],
                      'Total Recovered':[global_no[2]]}

    india_frame     = {'Total Cases':[country_india[0]],
                      'Total Deaths':[country_india[1]],
                      'Total Recovered':[country_india[2]]}

    country_frame = {'Countries':[country_list[0][0],country_list[1][0],country_list[2][0],country_list[3][0],country_list[4][0]],
              'Total Cases':[country_list[0][1],country_list[1][1],country_list[2][1],country_list[3][1],country_list[4][1]],
              'Total Deaths':[country_list[0][2],country_list[1][2],country_list[2][2],country_list[3][2],country_list[4][2]],
              'Total Recovered':[country_list[0][3],country_list[1][3],country_list[2][3],country_list[3][3],country_list[4][3]]  }

    df_1 = pd.DataFrame(worldwide_frame)
    df_2 = pd.DataFrame(india_frame)
    df_3 = pd.DataFrame(country_frame)   



    date = str(date_time.day) + '/' + str(date_time.month) + '/' + str(date_time.year)
    time = str(date_time.hour) + ':' + str(date_time.minute)
    if( len(str(date_time.minute)) == 1):
      time = str(date_time.hour) + ':0' + str(date_time.minute)
      print(time)
    #print(date,time)
    
    y1_axis = ['Worldwide']
    x1_axis = [global_no[0]]
    x1_axis2 = [global_no[1]]
    x1_axis3 = [global_no[2]]

    y2_axis = ['India']
    x2_axis = [country_india[0]]
    x2_axis2 = [country_india[1]]
    x2_axis3 = [country_india[2]]

    y3_axis = [country_list[4][0],country_list[3][0],country_list[2][0],country_list[1][0],country_list[0][0]]
    x3_axis = [country_list[4][1],country_list[3][1],country_list[2][1],country_list[1][1],country_list[0][1]]
    x3_axis2 = [country_list[4][2],country_list[3][2],country_list[2][2],country_list[1][2],country_list[0][2]]
    x3_axis3 =  [country_list[4][3],country_list[3][3],country_list[2][3],country_list[1][3],country_list[0][3]]
    
    fig1 = go.Figure()
    fig2 = go.Figure()
    fig3 = go.Figure()
    
    
    fig1.add_trace(go.Bar(
      x = x1_axis3,
      y = y1_axis,
      orientation = 'h',
      width = 0.2,
      text = x1_axis3,
      textposition= 'auto',
      name = 'Total Recovered',
      marker_color = 'limegreen'))  

    fig1.add_trace(go.Bar(
        x = x1_axis2,
        y = y1_axis,
        orientation = 'h',
        width = 0.2,
        text = x1_axis2,
        textposition= 'auto',
        name = 'Total Deaths',
        marker_color = 'dimgray'))


    fig1.add_trace(go.Bar(
        x = x1_axis,
        y = y1_axis,
        orientation = 'h',
        width = 0.2,
        text = x1_axis,
        textposition= 'auto',
        name = 'Total Cases',
        marker_color = 'indianred'))

    fig1.update_layout(barmode='group',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',xaxis= dict(showticklabels = False),xaxis_showgrid=False, yaxis_showgrid=False ,font=dict(
          family= 'Arial',
          size=18,
          color="#85CFCB"
      ))





    fig2.add_trace(go.Bar(
      x = x2_axis3,
      y = y2_axis,
      orientation = 'h',
      width = 0.2,
      text = x2_axis3,
      textposition= 'auto',
      name = 'Total Recovered',
      marker_color = 'limegreen'))  

    fig2.add_trace(go.Bar(
        x = x2_axis2,
        y = y2_axis,
        orientation = 'h',
        width = 0.2,
        text = x2_axis2,
        textposition= 'auto',
        name = 'Total Deaths',
        marker_color = 'dimgray'))


    fig2.add_trace(go.Bar(
        x = x2_axis,
        y = y2_axis,
        orientation = 'h',
        width = 0.2,
        text = x2_axis,
        textposition= 'auto',
        name = 'Total Cases',
        marker_color = 'indianred'))

    fig2.update_layout(barmode='group',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',xaxis= dict(showticklabels = False),xaxis_showgrid=False, yaxis_showgrid=False ,font=dict(
          family= 'Arial',
          size=18,
          color="#85CFCB"
      ))



    fig3.add_trace(go.Bar(
      x = x3_axis3,
      y = y3_axis,
      orientation = 'h',
      text = x3_axis3,
      textposition= 'auto',
      name = 'Total Recovered',
      marker_color = 'limegreen'))  

    fig3.add_trace(go.Bar(
        x = x3_axis2,
        y = y3_axis,
        orientation = 'h',
        text = x3_axis2,
        textposition= 'auto',
        name = 'Total Deaths',
        marker_color = 'dimgray'))


    fig3.add_trace(go.Bar(
        x = x3_axis,
        y = y3_axis,
        orientation = 'h',
        text = x3_axis,
        textposition= 'auto',
        name = 'Total Cases',
        marker_color = 'indianred'))

    fig3.update_layout(barmode='group',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',xaxis= dict(showticklabels = False),xaxis_showgrid=False, yaxis_showgrid=False ,font=dict(
          family= 'Arial',
          size=18,
          color="#85CFCB"
      ))
    
    fig1.write_image("fig1.png",width = '950', height = '700')
    fig2.write_image("fig2.png",width = '950', height = '700')
    fig3.write_image("fig3.png",width = '950', height = '700')
    covid_email('ncov.alert@gmail.com',emaillist,'Covid-19 update ' + date,create_HTML(date,time,df_1,df_2,df_3))    
    
    
    print('OK')

    

    if(time_1 < 2059 ):
          key = 1 
          #print(time_1)
