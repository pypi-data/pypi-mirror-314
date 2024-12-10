# PygameXtras
PygameXtras is a library designed to make programming with pygame easier. It supplies classes that aim at reducing the time and effort that go into everyday tasks like displaying text, creating buttons, managing entry forms, etc.

## Example
```python
import pygame
import PygameXtras as px

pygame.init()
screen = pygame.display.set_mode((500, 600))
clock = pygame.time.Clock()

circle_center = (350, 350)
circle_radius = 50

mouse_radius = 70
color = "blue"

line_y = 260

buttons = [
    px.Button(
        screen,
        c,
        25,
        (15 + i * 140, 15),
        "topleft",
        fd=(125, 40),
        bw=3,
        br=10,
        hl=True,
        bgc=c,
    )
    for i, c in enumerate(("purple", "green", "blue"))
]

label_touching = px.Label(screen, "not touching", 16, (0, 0), tc="red")
label_distance = px.Label(screen, "distance: n/a", 30, (25, 75), "topleft", tc=0)

entry = px.Entry(
    screen,
    "",
    25,
    (15, 135),
    "topleft",
    fd=(200, 40),
    bgc=150,
    bw=3,
    br=10,
    twe="custom color",
    ast=True,
)

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    for button in buttons:
        if button.update(events):
            color = button.backgroundcolor

    entry.update(events)
    if entry.get_state():
        entry.update_colors(bordercolor="blue")
    else:
        entry.update_colors(bordercolor="black")
    if entry.get() != "":
        try:
            color = px.parsers.Color.parse(entry.get())
        except:
            pass

    mouse_pos = pygame.mouse.get_pos()
    mouse_pos = (mouse_pos[0], max(line_y, mouse_pos[1]))
    if px.Collisions.circle_circle(
        mouse_pos, mouse_radius, circle_center, circle_radius
    ):
        label_touching.update_text("touching")
        label_touching.update_colors(textcolor="lime")
    else:
        label_touching.update_text("not touching")
        label_touching.update_colors(textcolor="red")
    label_touching.update_pos(mouse_pos)
    label_distance.update_text(
        f"distance: {max(0, round(px.get_distance(mouse_pos, circle_center) - mouse_radius - circle_radius, 1))} px"
    )

    screen.fill((20, 90, 20))
    pygame.draw.circle(screen, (128, 128, 128), circle_center, circle_radius)
    pygame.draw.circle(screen, color, mouse_pos, mouse_radius)
    pygame.draw.line(
        screen, (0, 0, 0), (0, line_y - mouse_radius), (500, line_y - mouse_radius)
    )
    label_touching.draw()
    label_distance.draw()
    for button in buttons:
        button.draw()
    entry.draw()

    pygame.display.flip()
    clock.tick(120)
```

## Label arguments
Labels (any classes inheriting from Label) can be styled using keyword arguments. The tables given below list all positional and keyword arguments and their specific uses. Please note: The types `Color`, `Coordinate`, `PositiveInt`, `PositiveFloat`, `Size2` and `Size4` refer to any values which are successfully digested by their respective parser (found in `PygameXtras.parsers`).

### Positional arguments for Labels
name | type | info | default
-|-|-|-
surface|pygame.Surface, None|the surface which the Label should be drawn to|-
text|Any|the text displayed on the Label|-
size|PositiveFloat|the size of the displayed text|-
xy|Coordinate|the pixel coordinates of the Label|-
anchor|str|the point within the Label which should be bound to the `xy` coordinate, similar to `pygame.Rect`s positioning system|`"center"`

### Keyword arguments for Labels
The last column, "LBE", shows for which widget (L = Label, B = Button, E = Entry) which keyword is relevant.

long | short | type | info | default | LBE
-|-|-|-|-|-
textcolor|tc|Color|sets the textcolor|`(0,0,0)`|LBE
backgroundcolor|bgc|Color|sets the backgroundcolor, transparent if set to `None`|`None`|LBE
antialias|aa|bool|whether antialiasing should be used|`True`|LBE
font|f|str|font style (to see all built-in fonts, run `PygameXtras.get_fonts()`)|`verdana`|LBE
x_axis_addition|xad|PositiveInt|adds pixels to the background of the label along the x axis|`0`|LBE
y_axis_addition|yad|PositiveInt|adds pixels to the background of the label along the y axis|`0`|LBE
borderwidth|bw|PositiveInt|sets the borderwidth|`0`|LBE
bordercolor|bc|Color|sets the bordercolor|`(0,0,0)`|LBE
force_width|fw|PositiveInt|sets the width of the Label to the given size|`None`|LBE
force_height|fh|PositiveInt|sets the height of the Label to the given size|`None`|LBE
force_dim|fd|Size2|sets the width and the height of the Label to the given size|`None`|LBE
borderradius|br|PositiveInt, Size4|sets the borderradius|`1`|LBE
text_offset|to|Coordinate|offsets the text within the Label by the given amount|`(0,0)`|LBE
image|img|pygame.Surface|sets the background of the Label to be the image given|`None`|LBE
info|info|Any|can be used to attach any information to the Label|`None`|LBE
text_binding|tb|str|binds the text to a location within the Label (similar to `anchor`)|`center`|LBE
highlight|hl|bool, Color|highlights the Button if the cursor touches it|`None`|BE
active_area|aA|Size4|limits the Button functionality to an absolute area (any clicks on the button while it is outside of the given area are not registered)|`None`|BE
bold|bo|bool|sets text styling to bold|`False`|LBE
italic|it|bool|sets text styling to italic|`False`|LBE
underline|ul|bool|sets text styling to underline|`False`|LBE
one_click_manager|ocm|OneClickManager|suppresses clicks if a different Button has already been clicked|`None`|BE
template|t|dict|injects style keywords from the given template|`None`|LBE
margin|m|PositiveInt, Size4|adds a margin that decreases the size of the Label without affecting its position |`None`|LBE
font_file|ff|str|sets the font of the Label to the given font|`None`|LBE
