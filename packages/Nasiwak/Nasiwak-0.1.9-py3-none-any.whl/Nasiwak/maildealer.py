class Maildealer:
    def __init__(self,maildealer_config):
        
        self.maildealer_config = maildealer_config

    
    def login(self,driver:object) -> None:
        """_summary_
        Used to Login to Maildealer 
        
        Args:
            driver : selenium.chrome.WebDriver
        """
        
        Maildealerurl = self.maildealer_config["MailDealer_url"]
        driver.get(Maildealerurl)
        
        logid = driver.find_element("xpath",self.maildealer_config["login_xpaths"]["ユーザID"])#ログインIDの要素読み込み
        logpassword = driver.find_element("xpath",self.maildealer_config["login_xpaths"]["パスワード"])#パスワードの要素読み込み

        logid.send_keys(self.maildealer_config["username"])
        logpassword.send_keys(self.maildealer_config["password"])

        # driver.find_element("xpath", '/html/body/div/div[1]/div[2]/div/form/div/input[2]')

        #Click on the Login button
        driver.find_element("xpath", self.maildealer_config["login_xpaths"]["ログイン"]).click()

        print("Login successful")
        
