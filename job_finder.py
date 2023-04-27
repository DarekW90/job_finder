import requests, csv, xlsxwriter, os
from bs4 import BeautifulSoup
from datetime import *


print()
print('Wybierz strone internetową do przeszukania:')
print('TIP: można wyszukiwać po cyfrze albo po nazwie\n')
webPages = ['wszystkie','pracuj.pl', 'nofluffjobs.com' ]

enumeratedPages = enumerate(webPages)

for pos, value in enumeratedPages:
    print('{}{}{}'.format(pos,':',value))

page_search = input("Którą stronę mam przeszukać? : ")


if page_search == '0' or page_search == 'wszystkie':
    page_search = "wszystkie"
if page_search == '1' or page_search == 'pracuj.pl':
    page_search = 'pracuj.pl'
if page_search == '2' or page_search == 'nofluffjobs.com':
    page_search = 'nofluffjobs.com'


search_job = input("Podaj zawód do wyszukania ofert pracy: ")

exp_data = "\n1.praktykant/stażysta\n2.junior\n3.mid/regular\n4.senior\n5.expert\n".ljust(10)
print(exp_data)
exp_level = input("Podaj stopień zaawansowania: ")
if "1" in exp_level:
    et = 1
    etId = "praktykant"
    nofluffseniority = "trainee"
elif "2" in exp_level:
    et = 17
    etId="junior"
    nofluffseniority = "junior"
elif "3" in exp_level:
    et = 4
    etId = "mid"
    nofluffseniority = "mid"
elif "4" in exp_level:
    et = 18
    etId = "senior"
    nofluffseniority = "senior"
elif "5" in exp_level:
    et = 19
    etId = "expert"
    nofluffseniority = "expert"
localization = input("\nPodaj lokalizacje:").lower()
range = input("Podaj promień wyszukania w kilometrach:")



excelData = []

if page_search == 'wszystkie':
    print()
    print('Przeglądam strone: pracuj.pl')
    print("*"*30)

    number = 1
    while number <= 100:
        print("Page nr:", number)
        url = (
            f"https://www.pracuj.pl/praca/{search_job};kw/{localization};wp?rd={range}&et={et}&pn={number}")
        print(url)

        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=header)

        soup = BeautifulSoup(response.content, "html.parser")  # ''lxml
        # print(soup.prettify())

        elements = soup.find_all("div", class_="listing_c1dc6in8")

        if len(soup.find_all("div", class_="listing_c1dc6in8")) > 0:
            print("Znaleziono:", len(soup.find_all(
                "div", class_="listing_c1dc6in8")), "ofert\n")
        else:
            print("Nieznaleiono wiecej ofert!")
            break

        for element in elements:

            job = element.find("h2", class_="listing_buap3b6")
            company = element.find("h4", class_="listing_eiims5z size-caption listing_t1rst47b")
            city = element.find("h5", class_="listing_rdl5oe8 size-caption listing_t1rst47b")
            region = city.text if city is not None else "Inna"

            salary = element.find("span", class_="listing_sug0jpb")
            salary_text = salary.text if salary is not None else "Brak Danych"

            link_element = element.find("a", class_="listing_n194fgoq")
            if link_element is not None:
                link = link_element['href']
            else:
                link = "Brak adresu strony"

            job_name = "Tytuł:".ljust(9)
            company_name = "Firma:".ljust(9)
            city_name = "Region:".ljust(9)
            salary_range = "Widełki:".ljust(9)
            page_link = "Link:".ljust(9)

            # print(f'{job_name}{job.text}\n{company_name}{company.text}\n{salary_range}{salary_text}\n{city_name}{region}\n{page_link}{link}\n')
            print(f'{job_name}{job.text}\n{company_name}{company.text}\n{city_name}{region}\n{salary_range}{salary_text}\n{page_link}{link}\n')

            excelData.append({
                'nazwa': job.text,
                'firma': company.text,
                'widełki': salary_text,
                'region': region,
                'link': link
            })

        number += 1

    number = 1
    while number <= 100:
        print("Page nr:", number)
        url = (
            f"https://nofluffjobs.com/pl/{localization}?page={number}&criteria=seniority%3D{nofluffseniority}")
        print(url)

        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=header)

        soup = BeautifulSoup(response.content, "html.parser")  # ''lxml
        # print(soup.prettify())

        elements = soup.find_all("a", class_="posting-list-item")


        if len(soup.find_all("a", class_="posting-list-item")) > 0:
            print("Znaleziono:", len(soup.find_all(
                "a", class_="posting-list-item")), "ofert\n")
        else:
            print("Nieznaleiono wiecej ofert!")
            break

        for element in elements:

            job = element.find("h3", class_="posting-title__position")
            company = element.find("span", class_="d-block")
            city = element.find("span", class_="tw-text-ellipsis")
            region = city.text if city is not None else " "
            salary = element.find(
                "span", class_="text-truncate badgy salary tw-btn tw-btn-secondary-outline tw-btn-xs ng-star-inserted")
            salary_text = salary.text if salary is not None else "Brak Danych"

            shortLink = element['href']
            link = ("https://nofluffjobs.com"+shortLink)
            # print(link)

            job_name = "Tytuł:".ljust(9)
            company_name = "Firma:".ljust(9)
            salary_range = "Widełki:".ljust(9)
            city_name = "Region:".ljust(9)
            page_link = "Link:".ljust(9)

            excelData.append({
                'nazwa': job.text,
                'firma': company.text,
                'widełki': salary_text,
                'region': region,
                'link': link
            })

            print(f'{job_name}{job.text}\n{company_name}{company.text}\n{city_name}{region}\n{salary_range}{salary_text}\n{page_link}{link}\n')

        number += 1

elif page_search == 'pracuj.pl':
    print()
    print('Przeglądam strone: pracuj.pl')
    print("*"*30)

    number = 1
    while number <= 100:
        print("Page nr:", number)
        url = (
            f"https://www.pracuj.pl/praca/{search_job};kw/{localization};wp?rd={range}&et={et}&pn={number}")
        print(url)

        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=header)

        soup = BeautifulSoup(response.content, "html.parser")  # ''lxml
        # print(soup.prettify())

        elements = soup.find_all("div", class_="listing_c1dc6in8")

        if len(soup.find_all("div", class_="listing_c1dc6in8")) > 0:
            print("Znaleziono:", len(soup.find_all(
                "div", class_="listing_c1dc6in8")), "ofert\n")
        else:
            print("Nieznaleiono wiecej ofert!")
            break

        for element in elements:

            job = element.find("h2", class_="listing_buap3b6")
            company = element.find("h4", class_="listing_eiims5z size-caption listing_t1rst47b")
            city = element.find("h5", class_="listing_rdl5oe8 size-caption listing_t1rst47b")
            region = city.text if city is not None else "Inna"

            salary = element.find("span", class_="listing_sug0jpb")
            salary_text = salary.text if salary is not None else "Brak Danych"

            link_element = element.find("a", class_="listing_n194fgoq")
            if link_element is not None:
                link = link_element['href']
            else:
                link = "Brak adresu strony"

            job_name = "Tytuł:".ljust(9)
            company_name = "Firma:".ljust(9)
            city_name = "Region:".ljust(9)
            salary_range = "Widełki:".ljust(9)
            page_link = "Link:".ljust(9)

            # print(f'{job_name}{job.text}\n{company_name}{company.text}\n{salary_range}{salary_text}\n{city_name}{region}\n{page_link}{link}\n')
            print(f'{job_name}{job.text}\n{company_name}{company.text}\n{city_name}{region}\n{salary_range}{salary_text}\n{page_link}{link}\n')

            excelData.append({
                'nazwa': job.text,
                'firma': company.text,
                'widełki': salary_text,
                'region': region,
                'link': link
            })

        number += 1

elif page_search == 'nofluffjobs.com':
    print()
    print('Przeglądam strone: nofluffjobs.com')
    print("*"*30)

    number = 1
    while number <= 100:
        print("Page nr:", number)
        url = (
            f"https://nofluffjobs.com/pl/{localization}?page={number}&criteria=seniority%3D{nofluffseniority}")
        print(url)

        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=header)

        soup = BeautifulSoup(response.content, "html.parser")  # ''lxml
        # print(soup.prettify())

        elements = soup.find_all("a", class_="posting-list-item")


        if len(soup.find_all("a", class_="posting-list-item")) > 0:
            print("Znaleziono:", len(soup.find_all(
                "a", class_="posting-list-item")), "ofert\n")
        else:
            print("Nieznaleiono wiecej ofert!")
            break

        for element in elements:

            job = element.find("h3", class_="posting-title__position")
            company = element.find("span", class_="d-block")
            city = element.find("span", class_="tw-text-ellipsis")
            region = city.text if city is not None else " "
            salary = element.find(
                "span", class_="text-truncate badgy salary tw-btn tw-btn-secondary-outline tw-btn-xs ng-star-inserted")
            salary_text = salary.text if salary is not None else "Brak Danych"

            shortLink = element['href']
            link = ("https://nofluffjobs.com"+shortLink)
            # print(link)

            job_name = "Tytuł:".ljust(9)
            company_name = "Firma:".ljust(9)
            salary_range = "Widełki:".ljust(9)
            city_name = "Region:".ljust(9)
            page_link = "Link:".ljust(9)

            excelData.append({
                'nazwa': job.text,
                'firma': company.text,
                'widełki': salary_text,
                'region': region,
                'link': link
            })

            print(f'{job_name}{job.text}\n{company_name}{company.text}\n{city_name}{region}\n{salary_range}{salary_text}\n{page_link}{link}\n')

        number += 1

now = datetime.now()
dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")

if not os.path.exists("files"):
    os.makedirs("files")

workbook = xlsxwriter.Workbook(
    f'files//{page_search}_{localization}_{etId}_{dt_string}.xlsx')
worksheet = workbook.add_worksheet("Praca")

worksheet.write(0, 0, "#")
worksheet.write(0, 1, "Nazwa")
worksheet.write(0, 2, "Firma")
worksheet.write(0, 3, "Widełki")
worksheet.write(0, 4, "Region")
worksheet.write(0, 5, "Link")

for index, entry in enumerate(excelData):
    worksheet.write(index+1, 0, str(index))
    worksheet.write(index+1, 1, entry["nazwa"])
    worksheet.write(index+1, 2, entry["firma"])
    worksheet.write(index+1, 3, entry["widełki"])
    worksheet.write(index+1, 4, entry["region"])
    worksheet.write(index+1, 5, entry["link"])

workbook.close()
 