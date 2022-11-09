# Classic-Captcha-Generator
Generator of classic captchas images, numbers and letters, lines, points, multicolor and deformations.

## Dependencies
- Pillow

## Basic operation
- Save captcha image (We use jpg because captchas generally need to be light and compressible):
```python
  from captcha import Captcha
  name = "my_captcha.jpg"
  Captcha().save(name)
```
- Get captcha image value for verification:
```python
  from captcha import Captcha
  my_captcha = Captcha()
  value_captcha = my_captcha.get_value()
```

## Personalization
The options to customize [with their corresponding parameters and type in parentheses] are:

- Character set to use (chars : str)
- Number of characters in the captcha (amount : int)
- Image mode [RGB, RGBA, etc.] (mode : str)
- Image size in pixels, width and height respectively (size : tuple)
- Background color in RGB format in tuple (bg_color : tuple)
- Font size in pixels (font_size : int)
- Whether there will be lines behind the characters or not (behind_lines : bool)
- Whether there will be lines in front of the characters or not (front_lines : bool)
- If there will be points in the captcha (points : bool)

Example, binary captcha with eight characters:
```python
  from captcha import Captcha
  binary_captcha = Captcha(chars="01"*4, amount=8)
  binary_captcha.save("binary_captcha.jpg")
```

## Captcha for web use
With the script **captcha_img_tag.py** we can get a dictionary with the captcha value and its image in a base64 string  
for direct insertion to the src attribute of any <img> tag.
```python
  from captcha import generate_captcha
  value, b64_data = generate_captcha().values()
```


