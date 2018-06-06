#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <string>

#include "curl.h"
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
//#include <windows.h>
using namespace std;

size_t write_nothing(void *contents, size_t size, size_t nmemb, void *userp) {
//  printf("size: %d\n", size * nmemb);//test
//  fwrite(contents, size, nmemb, stdout);//test
//  printf("\nsize = %d\n", size);//test
//  printf("\nmemb = %d\n", nmemb);//test
  return size * nmemb;
}
/*useless
size_t write(void *contents, size_t size, size_t nmemb, void *userp) {
//  printf("size: %d\n", size * nmemb);//test
//  fwrite(contents, size, nmemb, stdout);//test
  memcpy(&buffer[buffer_now], contents, size * nmemb);
  buffer_now +=  size * nmemb;
  return size * nmemb;
}
*/





int main(int argc, char *argv[]) {
  chdir("./helper_func");
  static const char *pCACertFile = "cacert.pem";
  CURL *curl;
  char data[255];
  char user[100]; //b07902000
  char pass[100]; //password
  
  strcpy(user, argv[1]);
  strcpy(pass, argv[2]);
  sprintf(data, "user=%s&pass=%s&Submit=µn¤J", user, pass);
  
  
  
  
  
  curl = curl_easy_init();
  CURLcode res;
  //0.
  curl_easy_setopt(curl, CURLOPT_CAINFO, pCACertFile);
  //curl_easy_setopt(curl, CURLOPT_VERBOSE, 1L); //print html header request/responses in console
  curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1); //Follow redirects
  curl_easy_setopt(curl, CURLOPT_COOKIEJAR, "cookie.txt"); //Save cookies here
  curl_easy_setopt(curl, CURLOPT_COOKIEFILE, "cookie.txt"); //Load cookies here
  curl_easy_setopt(curl, CURLOPT_USERAGENT, "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"); //Setting agent. Just do this
  curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_nothing);
  curl_easy_setopt(curl, CURLOPT_ACCEPT_ENCODING, "");
  //----------------------------------------------------------------------------------------------------
  //1.sign in(1)
  curl_easy_setopt(curl, CURLOPT_URL, "https://ceiba.ntu.edu.tw/ChkSessLib.php");//Url
//  curl_easy_setopt(curl, CURLOPT_REFERER, "https://ceiba.ntu.edu.tw/index.php");
  curl_easy_perform(curl);
  /*test
  url = NULL;
  curl_easy_getinfo(curl, CURLINFO_EFFECTIVE_URL, &url);
  if(url)
    printf("A Redirect to: %s\n", url);
  */
  //----------------------------------------------------------------------------------------------------
  //2.sign in(2)
  curl_easy_setopt(curl, CURLOPT_URL, "https://web2.cc.ntu.edu.tw/p/s/login2/p1.php");//Url
  curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data);//Post message
  curl_easy_perform(curl);
  /*test
  url = NULL;
  curl_easy_getinfo(curl, CURLINFO_EFFECTIVE_URL, &url);
  if(url)
    printf("B Redirect to: %s\n", url);
  */
  //----------------------------------------------------------------------------------------------------
  //3.sign in(3)
  curl_easy_setopt(curl, CURLOPT_URL, "https://ceiba.ntu.edu.tw/ChkSessLib.php");//Url
  curl_easy_perform(curl);
  //----------------------------------------------------------------------------------------------------
  
  
  
  
  
  printf("check cookie.txt!!\n");
  curl_easy_cleanup(curl);
  return 0;
}
