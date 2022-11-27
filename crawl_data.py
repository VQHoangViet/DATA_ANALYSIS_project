df = pd.read_csv('/content/drive/MyDrive/LTPTDL/data.csv').drop_duplicates(subset=['SBD', 'Năm thi'])
years = ['2022']
for year in years:
  for idx in range(10000001, 99999999):
      page = requests.get("https://vietnamnet.vn/giao-duc/diem-thi/tra-cuu-diem-thi-tot-nghiep-thpt/{}/{}.html".format(year,idx))
      print("https://vietnamnet.vn/giao-duc/diem-thi/tra-cuu-diem-thi-tot-nghiep-thpt/{}/{}.html, code: {}".format(year,idx, page.status_code))
      if page.status_code is 404:
          print("[INFO] {}/99999999: no data".format(idx))
          df.to_csv('/content/drive/MyDrive/LTPTDL/data.csv', index=False)
          break
      else:
        try:
          print("[GET] {}/99999999".format(idx))
          soup = BeautifulSoup(page.text, "html.parser")
          sub_elements = soup.find_all("td")
          sub_elements = [sub_elements[i:i+2] for i in range(0, len(sub_elements), 2)]
          subjects = {'SBD': soup.find_all("p", {"class": "font-bold"})[0].text,  
                      'Sở GD': soup.find_all("p", {"class": "edu-institution"})[0].text, 
                      'Toán': '',
                      'Văn': '',
                      'Sử': '',
                      'Địa': '',
                      'Lí': '',
                      'Hoá': '',
                      'Sinh': '',
                      'Ngoại ngữ': '',
                      'GDCD': '',
                      'Năm thi': year}
          for element in sub_elements:
              for key, value in subjects.items():
                  if element[0].text == key:
                      subjects[key] = element[1].text
          df = df.append(subjects, ignore_index=True)
          print(subjects)
        except:
          df.to_csv('/content/drive/MyDrive/LTPTDL/data.csv', index=False)
          continue
  df.to_csv('/content/drive/MyDrive/LTPTDL/data.csv', index=False) 