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
    <img src="" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">COVID-19 Updates App</h3>

  <p align="center">
    Application that allows users from three states to view COVID-19 data based on the county their device is located in.
    Backend Python API hosted on Heroku, using Flask and PostgreSQL that scrapes, stores, and retrieves COVID-19 data from each state’s website.
    Android application built using Java with Android Studio to send the device’s location to the Python API and display the COVID-19 data given in response.
    <br />
    <br />
  </p>
</div>


<a href="#generated-images">Generated Images</a>

<br>

<!-- ABOUT THE PROJECT -->
## About The Project

This project was developed for CS324 - Computer Graphics at the University of Idaho Spring 2022.

The graphics system consists of a canvas, on which all drawing takes place. The 2D system implements a viewport and a window, with changeable size and location. Calls to the 2D system involve **`moveTo2D`** and **`drawTo2D`**, which determine where each and every line will be drawn from and to. These functions perform a series of mappings on the x,y points given, to determine where on the pixmap the actual line will be drawn. 

The 3D system expands upon this by implementing a camera, a series of transforms, and **`moveTo3D`**/**`drawTo3D`** functions. The **`moveTo3D`** and **`drawTo3D`** functions apply the active transform (which is the result of premultiplying matricies consisting of the camera, and other transforms) to the x,y,z point. This then becomes a 2D x,y point, and the 2D functions are used to map and draw onto the pixmap. 

The lines drawn on the pixmap are saved as part of a **`.pbm`** file.

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

C++, C

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONTACT -->
## Contact


Alex Peña - alexpena5635@gmail.com

Project Link: [https://github.com/alexpena5635/CS324/tree/main/assign3](https://github.com/alexpena5635/CS324/tree/main/assign3)


<p align="right">(<a href="#top">back to top</a>)</p>

## Generated Images
<p align="right">(<a href="#top">back to top</a>)</p><br>
  <summary>Process of Building Rubiks Grid</summary>
    <img src="RubiksCube.gif" alt="Logo" width="600" height="480">
    
  <summary>Block Letters</summary>
    <img src="output/3D/png/letters_final.png" alt="Logo" width="600" height="480">

  <summary>3D Plot</summary>
    <img src="output/3D/png/plot_final.png" alt="Logo" width="600" height="480">

  <summary>Tron Recognizer</summary>
    <img src="output/3D/png/recognizer_final.png" alt="Logo" width="600" height="480">

  <summary>Simple Rubix Cube</summary>
    <img src="output/3D/png/rubix_final.png" alt="Logo" width="600" height="480">

  <summary>Rubix Cube with Gaps</summary>
    <img src="output/3D/png/rubix_gaps_final.png" alt="Logo" width="600" height="480">

  <summary>Rubix Grid</summary>
    <img src="output/3D/png/rubix_grid_final.png" alt="Logo" width="600" height="480">
    

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/alex-peña-944095241 
