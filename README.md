<a name="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<br />
<div align="center">
  <a href="https://github.com/lcram33/collatz-cipher">
    <img src="images/logo.png" alt="Logo" width="150" height="150">
  </a>

  <h1 align="center">Collatz cipher</h1>
  
  <h2 align="center">
    A polyalphabetic cipher that derivate a key from Hasse's algorithm.
  </h2>

  <h3 align="center">
    <br />
    <a href="https://github.com/lcram33/collatz-cipher/issues">Report Bug</a>
    ·
    <a href="https://github.com/lcram33/collatz-cipher/issues">Request Feature</a>
  </h3>
</div>

<!-- ABOUT THE PROJECT -->

## About The Project

<p align="left">
  A polyalphabetic cipher that uses Hasse's algorithm with a huge number to substitute characters from a randomly mixed charset.
  See paper for more details on how it works.
</p>

### Warning !

<img src="images/warning.png" width="90" height="90">

<b>
I do not provide any warranty that this cipher is in any way reliable.
<br>
DO NOT USE WITH CRITICAL DATA !
</b>
<br>
No research was made on it so far. Your welcome to contribute in any way !

## Technical part (how it works) & security considerations

<img src="images/semigear.png" width="90" height="90"> <img src="images/shield.png" width="90" height="90">

<i>These parts have been moved to the unofficial paper. See pdf document in the repo.</i>

### Break me !

<img src="images/bulb.png" width="90" height="90">

In <i>challenge/challenge.py</i>, you will find a message encrypted with an unknown key. If you manage to find the original message, it would be a pleasure to know how you did it ! See the contact section.

Please note however that the project changed since. See <i>challenge/params-challenge.py</i> and <i>challenge/collatzcipher-v1.0.py</i> for more details.

### Built With

<a href="https://www.python.org">
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" width=60/>
</a>

<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

python3 (should come with your favorite distro)

```sh
sudo apt update && sudo apt install python3
```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/lcram33/collatz-cipher.git
   ```
2. cd into the created folder

   ```sh
   cd collatz-cipher
   ```

3. Test that everything works as expected (and you meet all depedencies)

   ```sh
   ./test.py && cd test_samples/ && ./test_all.sh && cd ..
   ```

4. See the help of the command line tool
   ```sh
   ./main.py --help
   ```

<!-- USAGE EXAMPLES -->

## Usage

The program is to be runned as follow :

```sh
./main.py <command> <required args> <optional args>
```

Use :

```sh
./main.py <command> --help
```

to get the arguments and a description of what a command does.

Commands:

- list
- gen
- seededkey
- enc
- dec
- encf
- decf
- export
- import
- delete
- check

## Other programs in this repo

- <i>seeded_key.py</i> allows to create keys using a random passphrase, allowing an easier key sharing and key recovery.
- <i>secure_pwd_gen_api.py</i> comes from [one of my other projects](https://github.com/Lcram33/strong_password_generator). It can be used to generate passwords and passphrases for cryptographic use.
- <i>test_randomness.py</i> is to test how "randomly" are the shiftings distributed.
- <i>unicode_list.py</i> was used to produce the latest params.py file.

<!-- ROADMAP -->

## Changelog

### v3

- Encryption of messages through command line
- Data integrity check
- Strong password hashing (using bcrypt for CPU cost)

### v2

- Finally a command line !

### v1.1

- Added null char to the charset, meaning it is now encrypted. To avoid any problem in decryption, it is removed from the initial message before encryption. <br>
- Randomized "confusing threshold" (prevalence of useless chars). <br>
- Randomized noise at the begining and the end of the message. <br>
- First version of paper.

See the [open issues](https://github.com/lcram33/collatz-cipher/issues) for a full list of proposed features (and known issues).

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

<!-- LICENSE -->

## License

Distributed under the GPL-3.0 license. See `LICENSE` for more information.

<!-- CONTACT -->

## Contact

✉️ lcram33@pm.me

Project Link: [https://github.com/lcram33/collatz-cipher](https://github.com/lcram33/collatz-cipher)

## Credits

<a href="https://www.flaticon.com/free-icons/caesar-cipher" title="caesar cipher icons">Caesar cipher icons created by Pixelmeetup - Flaticon</a>
<br>
<a href="https://www.flaticon.com/free-icons/warning" title="warning icons">Warning icons created by Freepik - Flaticon</a>
<br>
<a href="https://www.flaticon.com/free-icons/safe" title="safe icons">Safe icons created by Assia Benkerroum - Flaticon</a>
<br>
<a href="https://www.flaticon.com/free-icons/technology" title="technology icon">Technology icons created by Smashicons - Flaticon</a>
<br>
<a href="https://www.flaticon.com/free-icons/idea" title="technology icon">Idea icons created by Good Ware - Flaticon</a>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/lcram33/collatz-cipher.svg?style=for-the-badge
[contributors-url]: https://github.com/lcram33/collatz-cipher/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/lcram33/collatz-cipher.svg?style=for-the-badge
[forks-url]: https://github.com/lcram33/collatz-cipher/network/members
[stars-shield]: https://img.shields.io/github/stars/lcram33/collatz-cipher.svg?style=for-the-badge
[stars-url]: https://github.com/lcram33/collatz-cipher/stargazers
[issues-shield]: https://img.shields.io/github/issues/lcram33/collatz-cipher.svg?style=for-the-badge
[issues-url]: https://github.com/lcram33/collatz-cipher/issues
[license-shield]: https://img.shields.io/github/license/lcram33/collatz-cipher.svg?style=for-the-badge
[license-url]: https://github.com/lcram33/collatz-cipher/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/marc-lecointre
