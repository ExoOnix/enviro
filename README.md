<a id="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![AGPL-3.0][license-shield]][license-url]
<!-- [![LinkedIn][linkedin-shield]][linkedin-url] -->



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/ExoOnix/enviro">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Onix Enviro</h3>

  <p align="center">
    Enviro accelerates your workflow with ready-to-use, cloud-based development environments.
    <br />
    <a href="https://docs.onixtech.org/"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://onixtech.org/">View Demo</a>
    &middot;
    <a href="https://github.com/ExoOnix/enviro/issues/new?labels=bug&template=bug_report.md">Report Bug</a>
    &middot;
    <a href="https://github.com/ExoOnix/enviro/issues/new?labels=enhancement&template=feature_request.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

Onix Enviro is a cloud development platform for instant, full-featured dev environments in your browser. Eliminate local setup, run Docker, forward ports, and more.

- No local setup needed
- Run VS Code in browser
- Remote Docker & environment support
- Full stack flexibility

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Django][Django.org]][Django-url]
* [![Tailwind][Tailwindcss.com]][Tailwindcss-url]
* [![Python][Python.org]][Python-url]
* ![Javascript]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This guide will help you install and set up Onix Enviro on your infrastructure.

### Prerequisites

- **Docker** and **Docker Compose** installed on your server or local machine.
- A supported OS (Linux recommended).
- Basic knowledge of Docker and command-line usage.

### Installation

#### 1. Clone the Repository

```sh
git clone https://github.com/ExoOnix/enviro.git
cd enviro
```

#### 2. Configure Environment Variables

Copy the example environment file and edit it to match your configuration:

```sh
cp .env.example .env
# Edit .env with your preferred editor
```

Set values for database, Django secret key, allowed hosts, etc.

#### 3. Set Up Docker Network

Create the required Docker network if it doesn't exist:

```sh
docker network create onixenvnet
```

#### 4. Start the Services

Run the following command to start all services:

```sh
docker compose -f docker-compose.production.yaml up --build -d
```

#### 5. Apply Database Migrations

After the containers are running, apply Django migrations:

```sh
docker compose -f docker-compose.production.yaml exec django-web poetry run python manage.py migrate
```

#### 6. Create a Superuser (Optional)

To access the Django admin, create a superuser:

```sh
docker compose -f docker-compose.production.yaml exec django-web poetry run python manage.py createsuperuser
```

#### 7. Access the Platform

- Visit `http://localhost:8081` (or your server's IP/domain) in your browser. (Port can be changed in the docker compose)
- Log in or sign up to start using Onix Enviro.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

After authenticating, click create project and start programming!


<!-- ROADMAP -->
## Roadmap

- [ ] Kubernetes support


See the [open issues](https://github.com/ExoOnix/enviro/issues) for a full list of proposed features (and known issues).

Feel free to suggest any new features.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/ExoOnix/enviro/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=ExoOnix/enviro" alt="contrib.rocks image" />
</a>



<!-- LICENSE -->
## License

Distributed under the AGPL-3.0. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Mark Shapirovskyy - mshapirovskyy@gmail.com

Project Link: [https://github.com/ExoOnix/enviro](https://github.com/ExoOnix/enviro)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/ExoOnix/enviro.svg?style=for-the-badge
[contributors-url]: https://github.com/ExoOnix/enviro/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ExoOnix/enviro.svg?style=for-the-badge
[forks-url]: https://github.com/ExoOnix/enviro/network/members
[stars-shield]: https://img.shields.io/github/stars/ExoOnix/enviro.svg?style=for-the-badge
[stars-url]: https://github.com/ExoOnix/enviro/stargazers
[issues-shield]: https://img.shields.io/github/issues/ExoOnix/enviro.svg?style=for-the-badge
[issues-url]: https://github.com/ExoOnix/enviro/issues
[license-shield]: https://img.shields.io/github/license/ExoOnix/enviro.svg?style=for-the-badge
[license-url]: https://github.com/ExoOnix/enviro/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: http://linkedin.com/in/mark-shapirovskyy
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
[Django.org]: https://img.shields.io/badge/django-51be95?style=for-the-badge&logo=django&logoColor=white
[Django-url]: https://www.djangoproject.com/
[Tailwindcss.com]: https://img.shields.io/badge/tailwind-00bcff?style=for-the-badge&logo=tailwindcss&logoColor=white
[Tailwindcss-url]: https://tailwindcss.com
[Python.org]: https://img.shields.io/badge/python-28557b?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[Javascript]: https://img.shields.io/badge/javascript-fcdc00?style=for-the-badge&logo=javascript&logoColor=black