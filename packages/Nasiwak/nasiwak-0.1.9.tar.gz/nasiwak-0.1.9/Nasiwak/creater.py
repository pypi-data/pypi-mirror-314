import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import os
import zipfile

def create_driver():
        
        """_summary_
        creates a selenium.chrome.WebDriver and returns it

        Returns:
            selenium.chrome.WebDriver : Chrome WebDrivere 
        """
        chrome_options = Options()
        # download_folder = os.path.join(os.getcwd(), f'{id_folder_name}')
        chrome_options.add_experimental_option("prefs", {
        #"download.default_directory": download_folder,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
        })

        # chrome_options.add_argument("--lang=en")

        # Initialize the WebDriver before the loop
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        
        return driver
    

def create_json_config(url,ACCESS_TOKEN) -> dict: 
    """_summary_

    Args:
        url : git file row url
        ACCESS_TOKEN : your access token

    Returns:
        json response: Returns the json-encoded content of a response, if any.
    """
    headers = {"Authorization": f"token {ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)
    
    return response.json()

def extractZip(folder:str):
    """_summary_
    it will take the folder path of the zip file and extract all the zip files in that folder 
    and delete the extracted zip file 

    Args:
        folder : folder path of the zip file where zip file is present
    """
    zip_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith('.zip')]
    for zip_file in zip_files:
        if zip_file.endswith('.zip'):
            with zipfile.ZipFile(zip_file, "r") as zf:
                for info in zf.infolist():
                    try:
                        info.filename = info.orig_filename.encode('cp932').decode('cp932')
                    except:
                        info.filename = info.orig_filename.encode('cp437').decode('cp932')
                    if os.sep != "/" and os.sep in info.filename:
                        info.filename = info.filename.replace(os.sep, "/")
                    zf.extract(info, path=folder)
            
            zip_folder = f'{zip_file}'.split('.zip')[0]
            # logging.info(zip_folder)
            for file in os.listdir(zip_folder):
                try:
                    shutil.move(zip_folder+rf'\{file}',folder)
                except:
                    pass
            shutil.rmtree(zip_folder)
            try:
                os.remove(zip_file)
            except Exception as E:
                print('While deleting zip file i got this error')
                print(f"{E}")
                
def folder_to_zip(folder_path:str, zipfile_path:str):
    """_summary_
        converts the given folder into zip file in the given path
        exaple values for reference\n
        folder_path = 'myfolder'\n
        zipfile_path = 'myfolder.zip'
    Args:
        folder_path (str): path of the folder you want to convert into zip 
        zipfile_path (str): path and name of the zip folder with .zip extenction 
    """

    with zipfile.ZipFile(zipfile_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                # Create the full path of the file
                file_path = os.path.join(root, file)
                # Add file to the ZIP, preserving the folder structure
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)