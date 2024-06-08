from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from InquirerPy.base.control import Choice
import undetected_chromedriver as uc
from InquirerPy import inquirer
from selenium import webdriver
import pandas as pd
import openpyxl,os


class Hoax:
    def __init__(self):
        option = uc.ChromeOptions() 
        # option.add_argument('--disable-gpu')
        # option.add_argument('--headless')
        self.driver = uc.Chrome(options=option, use_subprocess=True)
        self.driver.set_page_load_timeout(30)
        self.outWorkbook = openpyxl.load_workbook("HoaxData.xlsx")
        self.outSheet = self.outWorkbook.active
        self.outSheet["A1"] = "Title"
        self.outSheet["B1"] = "Category"
        self.outSheet["C1"] = "Url"
        self.outSheet["D1"] = "Image"
        self.outSheet["E1"] = "Author"
        self.outSheet["F1"] = "Dekripsi"
        self.outSheet["G1"] = "Counter Link"
        self.outSheet["H1"] = "Date"
        self.outSheet["I1"] = "Page"

    def GetCurrentData(self):
        try:
            df = pd.read_excel("HoaxData.xlsx", engine='openpyxl')
            lastRow = df.index[-1] + 2
            lastPage = int(df['Page'].dropna().tolist()[-1])
            return lastRow, lastPage
        except Exception as e:
            print(e)
            return 1, 1

    def Setup(self, page):
        try:
            self.driver.get(f"https://www.kominfo.go.id/content/all/laporan_isu_hoaks?page={page}")
            if "You are now in line" in self.driver.page_source:
                while True:
                    if "You are now in line" not in self.driver.page_source:
                        break
                    print("waiting")
        except Exception as e:
            print(e)

    def GetArticle(self):
        try:
            elements = WebDriverWait(self.driver, 40).until(EC.presence_of_all_elements_located((By.XPATH, "//a[@class='title']")))
            return [x.text for x in elements], [x.get_attribute('href') for x in elements]
        except Exception as e:
            print(e)
            print("error while get article")
            return ["None"],["None"]

    def GetDate(self):
        try:
            elements = WebDriverWait(self.driver, 40).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='date']")))
            return [x.text for x in elements]
        except Exception as e:
            print(e)
            print("error while get data data")
            return ["None"]

    def GetAuthor(self, url):
        try:
            self.driver.get(url)
            Adetail = WebDriverWait(self.driver, 40).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='author']")))
            Lcounter = WebDriverWait(self.driver, 40).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='youtube-container']//ul//a")))
            deskirpsi = WebDriverWait(self.driver, 40).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='youtube-container']//p")))
            details = [details for details in Adetail]
            lCounters = [lCounter.get_attribute('href') for lCounter in Lcounter]
            desc = [desc.text for desc in deskirpsi][1:-1][:-1]
            return details, lCounters,desc
        except Exception as e:
            print("error while get author data",e)
            return None, None

    def GetImage(self):
        try:
            img = WebDriverWait(self.driver, 40).until(EC.presence_of_all_elements_located((By.XPATH, "//img[@class='thumbnail-img artikel--bg-size-cover']")))
            imgu = [x.get_attribute('src') for x in img]
            return imgu
        except Exception as e:
            print(e)
            print("error while get image data")
            return ["None"]

    def Main(self,pages):
        lastRow, lastPage = self.GetCurrentData()
        for x in range(lastPage+1, lastPage + pages+1):
            self.Setup(x)
            title, url = self.GetArticle()
            print("page: ",x)
            for index, page in enumerate(url):
                print("url: ", url[index])
                self.outSheet.cell(row=lastRow + 1, column=1, value=title[index])
                self.outSheet.cell(row=lastRow + 1, column=3, value=page)
                self.outSheet.cell(row=lastRow + 1, column=9, value=x)
                details, lCounters,desc = self.GetAuthor(page)
                img = self.GetImage()   
                date = self.GetDate()
                self.outSheet.cell(row=lastRow + 1, column=4, value=img[0])
                self.outSheet.cell(row=lastRow + 1, column=8, value=date[0])
                self.outSheet.cell(row=lastRow + 1, column=6, value=str(desc))
                if details != None:
                    for detail in details:
                        try:
                            category = detail.text.split("Kategori ")[1]
                            author = category.split("| ")[1]
                            self.outSheet.cell(row=lastRow + 1, column=2, value=category.split(" |")[0])
                            self.outSheet.cell(row=lastRow + 1, column=5, value=author)
                            lastRow = lastRow + 1
                        except Exception as e:
                            print(e)
                            pass
                    for index, linkC in enumerate(lCounters):
                        self.outSheet.cell(row=lastRow + 1, column=7, value=linkC)
                        lastRow = lastRow + 1
                    lastRow = lastRow + 1
                else:
                    self.outSheet.cell(row=lastRow + 1, column=2, value="None")
                    self.outSheet.cell(row=lastRow + 1, column=5, value="None")
                    lastRow = lastRow + 1
                lastRow = lastRow + 1
            print("\n")
        self.outWorkbook.save("HoaxData.xlsx")
        print("done!")
        self.driver.quit()

class Satker:
    def __init__(self):
        option = uc.ChromeOptions() 
        # option.add_argument('--disable-gpu')
        # option.add_argument('--headless')
        self.driver = uc.Chrome(options=option, use_subprocess=True)
        self.driver.set_page_load_timeout(30)
        self.outWorkbook = openpyxl.load_workbook("SatkerData.xlsx")
        self.outSheet = self.outWorkbook.active
        self.outSheet["A1"] = "Title"
        self.outSheet["B1"] = "Category"
        self.outSheet["C1"] = "Url"
        self.outSheet["D1"] = "Image"
        self.outSheet["E1"] = "Author"
        self.outSheet["F1"] = "Deskripsi"
        self.outSheet["G1"] = "Date"
        self.outSheet["H1"] = "Page"

    def GetCurrentData(self):
        try:
            df = pd.read_excel("SatkerData.xlsx", engine='openpyxl')
            lastRow = df.index[-1] + 2
            lastPage = int(df['Page'].dropna().tolist()[-1])
            return lastRow, lastPage
        except Exception as e:
            print(e)
            return 1, 1

    def Setup(self, page):
        try:
            self.driver.get(f"https://www.kominfo.go.id/content/all/berita_satker?page={page}")
            if "You are now in line" in self.driver.page_source:
                while True:
                    if "You are now in line" not in self.driver.page_source:
                        break
                    print("waiting")
        except Exception as e:
            print(e)

    def GetArticle(self): #get title and news url
        try:
            elements = WebDriverWait(self.driver, 40).until(EC.presence_of_all_elements_located((By.XPATH, "//a[@class='title']")))
            return [x.text for x in elements], [x.get_attribute('href') for x in elements]
        except Exception as e:
            print(e)
            print("error getting articel data")
            

    def GetDate(self): #get news date
        try:
            elements = WebDriverWait(self.driver, 40).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='date']")))
            return [x.text for x in elements]
        except Exception as e:
            print(e)
            print("error getting date data")

    def GetAuthor(self, url): #get news author
        try:
            self.driver.get(url)
            Adetail = WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "/html/body/div[8]/div/div[2]/div/div[1]/div[1]/div[2]/div[1]")))
            deskripsi = WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='youtube-container']//p")))
            desc = [desc.text for desc in deskripsi][0:-1][:-1][:-1]
            details = [details for details in Adetail]
            return details,desc
        except Exception as e:
            print(e)
            print("error getting author data")
            return None

    def GetImage(self): #get news image
        try:
            img = WebDriverWait(self.driver, 40).until(EC.presence_of_all_elements_located((By.XPATH, "//img[@class='thumbnail-img artikel--bg-size-cover']")))
            imgu = [x.get_attribute('src') for x in img]
            return imgu
        except Exception as e:
            print(e)
            print("error getting image data")

    def GetDesc(self):
        try:
            # self.driver.get("https://www.kominfo.go.id/content/all/berita_satker?page=2")
            desc = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='description']")))
            description = [x.text for x in desc]
            return description
        except Exception as e:
            print(e)
            print("this is error deskripsi")


    def Main(self,pages):
        lastRow, lastPage = self.GetCurrentData()
        for x in range(lastPage+1, lastPage + pages+1):
            self.Setup(x)
            desc = self.GetDesc()
            title, url = self.GetArticle()
            print("page: ",x)
            for index, page in enumerate(url):
                print("url: ", url[index])
                self.outSheet.cell(row=lastRow + 1, column=1, value=title[index])
                self.outSheet.cell(row=lastRow + 1, column=3, value=page)
                self.outSheet.cell(row=lastRow + 1, column=8, value=x)
                details,desc = self.GetAuthor(page)
                img = self.GetImage()   
                date = self.GetDate()
                self.outSheet.cell(row=lastRow + 1, column=6, value=str(desc))
                self.outSheet.cell(row=lastRow + 1, column=4, value=img[0])
                self.outSheet.cell(row=lastRow + 1, column=7, value=date[0])
                if details != None:
                    for detail in details:
                        try:
                            category = detail.text.split("Kategori ")[1]
                            author = category.split("| ")[1]
                            self.outSheet.cell(row=lastRow + 1, column=2, value=category.split(" |")[0])
                            self.outSheet.cell(row=lastRow + 1, column=5, value=author)
                            lastRow = lastRow + 1
                        except Exception as e:
                            print(e)
                            pass
                    lastRow = lastRow + 1
                else:
                    self.outSheet.cell(row=lastRow + 1, column=2, value="None")
                    self.outSheet.cell(row=lastRow + 1, column=5, value="None")
                    lastRow = lastRow + 1
                lastRow = lastRow + 1
            print("\n")
        self.outWorkbook.save("SatkerData.xlsx")
        print("done!")
        self.driver.quit()

class UI:
    def __init__(self):
        self.proceed= False

    def main(self):
        action = inquirer.select(
            message="Select an action:",
            choices=[
                "Isu Hoax",
                "Satker",
                Choice(value=None, name="Exit"),
            ],
            default=None,
        ).execute()

        if action == "Isu Hoax":
            hox = Hoax()
            page = inquirer.text(
                message="insert jumlah page yang ingin di scrape: ",
                multicolumn_complete=True,
            ).execute()
            hox.Main(int(page))
        elif action == "Satker":
            satker = Satker()
            page = inquirer.text(
                message="insert jumlah page yang ingin di scrape: ",
                multicolumn_complete=True,
            ).execute()
            satker.Main(int(page))
if __name__ == "__main__":
    os.system('cls')
    myui = UI()
    myui.main()
