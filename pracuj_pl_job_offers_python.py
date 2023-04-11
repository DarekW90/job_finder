import requests
from bs4 import BeautifulSoup

search_job = input("Podaj zawód do wyszukania ofert pracy: ")
number = 1
exp_data = "\n1.praktykant/stażysta\n2.mid/regular\n3.senior\n".ljust(10)
print(exp_data)
exp_level = input("Podaj stopień zaawansowania: ")
if "1" in exp_level:
    et = "1"
elif "2" in exp_level:
    et = "4"
elif "3" in exp_level:
    et = "18"
localization = input("\nPodaj lokalizacje:").lower()
range = input("Podaj promień wyszukania w kilometrach:")

while number <= 10:
    print("Page nr:", number)
    url = (f"https://www.pracuj.pl/praca/{search_job};kw/{localization};wp?rd={range}&et={et}&pn={number}")
    #print(url)


    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=header)

    soup = BeautifulSoup(response.content, "html.parser")  # ''lxml
    # print(soup.prettify()

    elements = soup.find_all("div", class_="b19e46yp p1cye3we")
    print("Znaleziono:", len(soup.find_all("div", class_="b19e46yp p1cye3we")),"ofert\n")

    for element in elements:
        #date = element.find("p", class_="b1qc7djs t1c1o3wg")
        job = element.find("h2", class_="b1iadbg8")
        company = element.find("h4", class_="e1ml1ys4 t1c1o3wg")
        city = element.find("h5", class_="r1vmcu7a t1c1o3wg")
        salary = element.find("span", class_="su9xzpe")
        salary_text = salary.text if salary is not None else "Brak Danych"
        link = element.find("a", class_="o1o6obw3 bwcfwrp njg3w7p")['href']

        # print(link)

        # pub_date = "Data publikacji:".ljust(9)
        job_name = "Nazwa:".ljust(9)
        company_name = "Firma:".ljust(9)
        salary_range = "Widełki:".ljust(9)
        city_name = "Miasto:".ljust(9)
        page_link = "Link:".ljust(9)

        # {pub_date}{date.text}

        print(f"{job_name}{job.text}\n{company_name}{company.text}\n{salary_range}{salary_text}\n{city_name}{city.text}\n{page_link}{link}\n")

    number += 1







