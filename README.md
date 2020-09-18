# code2pdf
A python tool for converting code into print-friendly PDF

<p float="left">
  <img src="https://s1.gifyu.com/images/test_code2pdf__2_.jpg" width="400" />
  <img src="https://s1.gifyu.com/images/test_code2pdf__2__.jpg" width="400" />

</p>

## Notes
1. This is not a project that aims to cover all the demand (there is not much a one file project can do), but just a small tool that caters to my need (alleviating my eye fatigue for reading code on the screen).

2. Technically, it does not generate a pdf file directly. It will generate a Latex project, which can be compiled manually by the user into pdf. I only tested it in the [Overleaf](https://www.overleaf.com/) environment, so uploading the results to [Overleaf](https://www.overleaf.com/) for compiling is highly recommended.

## Usage
The command used to generate the Latex source code is
```
python code2pdf.py [output-path] [code-path] [language]
```
For example, if we want to generate the Latex source for the code repo `./mmdetection` (which is written mainly in python) in `./output_dir`, we can use
```
python code2pdf.py ./output_dir ./mmdetection python
```
Note that the script will make a new directory named `./output_dir`, and will throw an error if it already exists.

For a list of supported languages, please see the table at the end of [link](https://www.overleaf.com/learn/latex/Code_Highlighting_with_minted).
