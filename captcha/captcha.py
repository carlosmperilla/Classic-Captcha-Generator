import random
import string
from PIL import Image, ImageDraw, ImageFont, ImageFilter


class Captcha:
    """Generate a JPEG image with a classic captcha. Applying lines, points, random colors and filters."""
    
    CHARS : str = string.digits + string.ascii_letters
    AMOUNT : int = 6
    MODE : str = "RGB"
    SIZE : tuple = (480, 120)
    BG_COLOR : tuple = (255, 255, 255)
    FONT_SIZE : int = 96

    
    def __init__(
                self, 
                chars:str = CHARS,
                amount:int = AMOUNT, 
                mode:str = MODE, 
                size:tuple = SIZE, 
                bg_color:tuple = BG_COLOR, 
                font_size:int = FONT_SIZE, 
                behind_lines:bool = True, 
                front_lines:bool = True, 
                points:bool = True) -> None:

        self.chars = chars
        self.amount = amount
        self.mode = mode
        self.size = size
        self.bg_color = bg_color
        self.font_size = font_size
        self.behind_lines = behind_lines
        self.front_lines = front_lines
        self.points = points
        
        self.generate_random_chars()
        self.generate_base_img()

        self.build_captcha()
        self.apply_filters()

    def generate_base_img(self) -> None:
        """We generate the canvas of the base image."""
        self.base_img = Image.new(self.mode, self.size, self.bg_color)
        self.base_draw = ImageDraw.Draw(self.base_img)

    def build_captcha(self) -> None:
        """Build the captcha by adding lines, dots and putting the text."""
        
        self.draw_thick_lines()
        if self.points:
            self.draw_points()
        if self.behind_lines:
            self.draw_lines
        
        self.put_chars()

        if self.front_lines:
            self.draw_lines()

    def generate_random_chars(self) -> None:
        """Generates a random set of characters."""

        self.random_chars = "".join(random.sample(self.chars, self.amount))

    def draw_thick_lines(self) -> None:
        """Draw thick lines to generate a multi-color background."""
        self.draw_lines(min_width=min(self.size), max_width=max(self.size))

    def draw_lines(self, min_width=2, max_width=5) -> None:
        """Draw random lines across the base canvas."""

        for i in range(random.randint(5, 10)):
            start = random.randint(0, self.size[0]), random.randint(0, self.size[1])
            end = random.randint(0, self.size[0]), random.randint(0, self.size[1])
            random_color  = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            random_width = random.randint(min_width, max_width)
            self.base_draw.line([start, end], fill=random_color, width=random_width)

    def draw_points(self) -> None:
        """Draw random points across the base canvas."""
        
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                if random.randint(0,3) == random.randint(0, 3):
                    random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    self.base_draw.point([x, y], fill=random_color)
    
    def draw_text(self, draw, char, font_size) -> None:
        """Draw a character on a canvas with a random color."""

        font = ImageFont.truetype('../fonts/arial.ttf', font_size)
        font_width, font_height = font.getsize(char)
        random_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        draw.text([(self.size[0]//self.amount-font_width)/2, (self.size[1]-font_height)/2], char, font=font, fill=random_color)
        
        return font_width, font_height

    def put_chars(self) -> None:
        """Rotates and resizes the characters and places them on the base canvas."""

        w_section = self.size[0]//self.amount
        for index, char in enumerate(self.random_chars, 0):
            char_img = Image.new('RGBA', (w_section, self.size[1]), (255, 0, 0, 0))
            char_draw = ImageDraw.Draw(char_img)
            font_width, font_height = self.draw_text(char_draw, char, self.font_size)
            char_img = char_img.rotate(random.randint(-45, 45), expand=1)
            
            pos_x = 0+w_section*index
            if index == self.amount-1:
                pos_x -= font_width//2
                
            w_deformation = random.randint(8,10)/10
            h_deformation = random.randint(8,10)/10
            newsize = (w_section*w_deformation, self.size[1]*h_deformation)
            char_img = char_img.resize((int(newsize[0]), int(newsize[1])))
            
            Image.Image.paste(self.base_img, char_img, [pos_x, 0], char_img)

    def apply_filters(self) -> None:
        """Apply filters to the captcha."""

        self.base_img = self.base_img.filter(ImageFilter.EDGE_ENHANCE_MORE)
        self.base_img = self.base_img.filter(ImageFilter.BoxBlur(.2))

    def get_value(self) -> str:
        """Returns the value string of the captcha instance"""

        return self.random_chars

    def save(self, fp) -> None:
        """Save the image to a jpg file."""

        self.base_img.convert("RGB").save(fp, "JPEG", optimize = True, quality = 100)