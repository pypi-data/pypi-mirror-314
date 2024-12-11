# Project Title

QR generator tool that returns either a PNG, postscript file, or a postscript object of an input string

## Description

I created this QR generator tool with the express purpose of generating custom QR codes for PDFs without the need for an adobe subscription. The returned postscript data can be used to place into a prewritten postscript file and then converted into a PDF using ghostscript. 

## Getting Started

### Dependencies

* In order to generate a QR image you will require both cv2 and numpy
  ```sh
  pip install opencv-contrib-python
  pip install numpy
  ```

### Installing

* Clone the repo
  ```sh
  git clone https://github.com/PimpDiCaprio/PiQR.git
  ```
* Installing with pip
  ```sh
  pip install PiQR
  ```

### Executing program

* How to run the program
* Step-by-step bullets
```
from PiQR import PiQR

# define the input string for the qr code
qr_string = 'Test Input'

# generate qr binary for the input string
qr_output = PiQR.generate_qr(qr_string, correction_level='Medium')

# the following options are available for displaying or saving the qr code

# display the qr code
PiQR.show_png(qr_output)

# save the qr as a png
PiQR.make_png(qr_output, 'test.png')

# write a postscript file containing the qr
PiQR.write_ps(qr_output, 'test.ps')

# return a postscript object in string form for placement into a ps file
ps_string = PiQR.return_ps(qr_output)

```

## Author

  PimpDiCaprio
  info@aperturesoftware.us

## Version History

* 0.1.1
    * Import Name Fixes
* 0.1.0
    * Initial Release

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* [Thonky's QR Code Tutorial](https://www.thonky.com/qr-code-tutorial/introduction)
* [General Resource QR Wiki](https://en.wikipedia.org/wiki/QR_code)
* [QR Creation Tool with Steps](https://www.nayuki.io/page/creating-a-qr-code-step-by-step)
