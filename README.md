<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]




<!-- PROJECT LOGO -->
<br />
<h3 align="center">Dave3625 - Lab3</h3>
<p align="center">
  <a href="https://github.com/buzzCraft/RobTek-prosjekt/">
    <img src="img/header.jpeg" alt="Robot CHess" width="auto" height="auto">
  </a>

  

  <p align="center">
    ABB Robot playing chess<br \>Using openCV, Python and RobotStudio
    <br />
    ·
    <a href="https://github.com/buzzCraft/RobTek-prosjekt/issues">Report Bug</a>
    ·
    <a href="https://github.com/buzzCraft/RobTek-prosjekt/issues">Request Feature</a>
  </p>



<!-- ABOUT THE PROJECT -->
## About The project

Done as a part of ELVE3610-1 21H course at OsloMet
A camera is mounted above the chess board and capture moves done by the user. 
The information is then sent to the chess client that calculate a response and send it to the robot.

## The chess client
The chess client is a modified version of [Python-Easy-Chess-GUI][Chess]

## Installation
Fork [Python-Easy-Chess-GUI][Chess]
Replace python_easy_chess_gui.py with the python_easy_chess_gui.py in this repo
Upload SJAKKROBOT.rspag to the ABB Robot
Run calib.py to check that the camera is working

Run python_easy_chess_gui.py and connect to the robot

## Further work
Implement a way to use real life pices. [This looks promising][real]

Make a tool for the robot to pick up real pices.

Choose if the robot play as White / Black

## Demo


[![Everything Is AWESOME](https://yt-embed.herokuapp.com/embed?v=svgM8sdBHIU)](https://www.youtube.com/watch?v=svgM8sdBHIU "RoboChess")

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.






<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[issues-shield]: https://img.shields.io/github/issues/buzzCraft/RobTek-prosjekt.svg?style=for-the-badge
[issues-url]: https://github.com/buzzCraft/RobTek-prosjekt/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/buzzCraft/Dave3625-21-Lab/blob/main/Lab1/LICENSE

[chess]: https://github.com/fsmosca/Python-Easy-Chess-GUI
[real]: https://github.com/davidmallasen/LiveChess2FEN


