<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/alexpena5635/Covid-Updates">
    <img src="images/Covid-19 Updates.png" alt="Logo" width="80" height="80">
  </a>

<h1 align="center">COVID-19 Updates App</h1>

  <p align="center">
    Application that allows users from Idaho, Oregon, and Washington to view COVID-19 data based on the county their device is located in.
    Backend API built with Python, Flask, PostgreSQL, and Heroki. Android application built with Android Studio and Java. 
    <br />
    <br />
  </p>
</div>


<a href="#images">Images</a>

<br>

<!-- ABOUT THE PROJECT -->
# About The Project
Application consisting of a backend server and an Android App. As a whole, the application allows users from three states (ID, OR, WA) to view COVID-19 data based on which county they are located in.

### **How does everything connect?**

### Server
The backend Python server has two main utilities. 

First, once a day the python server scrapes each states' website for COVID-19 data. This data is mutated into a common form, and then sent to the Postgres database. 
Second, the Python server then has a public facing API. Users can hit the endpoint and query the database for COVID-19 data for a whole state, or state and county. The resulting data is then returned to the user in JSON format. 

State: `myapi/Idaho`
<br>
State and County  - `myapi/Idaho/ada`

The python server is hosted on the cloud provider Heroku, allowing for the public API. 
<br><br>

### Application
The Android application built with Java runs through multiple steps when launched. 

The gps coordinates of a user's phone are retrieved, and sent to the [Nomatim API](https://nominatim.org/release-docs/latest/api/Overview/) to lookup the corresponding state and county. The data is sent back as a JSON response, and is parsed in the app. Once the state and county are extracted, then these are combined with the server URL to hit the API endpoint

`myapi/Idaho/ada`

The JSON response from the server is then parsed through, and the data is displayed on screen, along with the current location. 

## **PICTURE HERE**


<p align="right">(<a href="#top">back to top</a>)</p>


# Built With

### **Server** : Python, Flask, PostgreSQL, Heroku
### **Client** : Java, Android Studio

<p align="right">(<a href="#top">back to top</a>)</p>

# Demo

## Process of Building Rubiks Grid
<img src="RubiksCube.gif" alt="Logo" width="600" height="480">
    

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONTACT -->
# Contact


### Alex Peña - alexpena5635@gmail.com

### Project Link: [https://github.com/alexpena5635/Covid-Updates](https://github.com/alexpena5635/Covid-Updates)

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/alex-peña-944095241 
